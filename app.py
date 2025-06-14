# Import các thư viện cần thiết
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

# Khởi tạo Flask app và cấu hình database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
db = SQLAlchemy(app)

# Model User: Lưu thông tin người dùng
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='user', lazy=True)  # Quan hệ 1-n với Task

# Model Task: Lưu thông tin công việc
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)  # Nội dung công việc
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Thời gian tạo
    status = db.Column(db.String(20), default='pending')  # Trạng thái: pending/completed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Khóa ngoại tới User

    def __repr__(self):
        return f'<Task {self.id}>'

# Decorator kiểm tra đăng nhập - Bảo vệ các route cần xác thực
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để tiếp tục', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route đăng ký: Xử lý form đăng ký và tạo tài khoản mới
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Kiểm tra username và email trùng lặp
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email đã được sử dụng', 'danger')
            return redirect(url_for('register'))

        # Tạo user mới với mật khẩu đã mã hóa
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Đăng ký thành công! Vui lòng đăng nhập', 'success')
            return redirect(url_for('login'))
        except:
            flash('Có lỗi xảy ra, vui lòng thử lại', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

# Route đăng nhập: Xác thực người dùng và tạo session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # Kiểm tra thông tin đăng nhập
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'danger')

    return render_template('login.html')

# Route đăng xuất: Xóa session và đăng xuất người dùng
@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công', 'info')
    return redirect(url_for('login'))

# Route trang chủ: Hiển thị danh sách task và form thêm task mới
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        # Xử lý thêm task mới
        task_content = request.form['content']
        new_task = Task(content=task_content, user_id=session['user_id'])

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Có lỗi xảy ra khi thêm task'

    else:
        # Lấy và hiển thị danh sách task của người dùng
        user_tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.date_created.desc()).all()
        total_tasks = len(user_tasks)
        pending_tasks = len([t for t in user_tasks if t.status == 'pending'])
        completed_tasks = total_tasks - pending_tasks
        return render_template('index.html', 
                             tasks=user_tasks,
                             total_tasks=total_tasks,
                             pending_tasks=pending_tasks,
                             completed_tasks=completed_tasks)

# Route thống kê: Hiển thị các số liệu thống kê về task
@app.route('/stats')
@login_required
def stats():
    # Lấy tất cả task của người dùng
    user_tasks = Task.query.filter_by(user_id=session['user_id']).all()
    total_tasks = len(user_tasks)
    completed_tasks = len([t for t in user_tasks if t.status == 'completed'])
    pending_tasks = total_tasks - completed_tasks
    
    # Tính tỷ lệ hoàn thành công việc
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Thống kê task theo ngày
    tasks_by_date = {}
    for task in user_tasks:
        date = task.date_created.strftime('%Y-%m-%d')
        if date not in tasks_by_date:
            tasks_by_date[date] = {'total': 0, 'completed': 0}
        tasks_by_date[date]['total'] += 1
        if task.status == 'completed':
            tasks_by_date[date]['completed'] += 1

    return render_template('stats.html',
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks,
                         completion_rate=completion_rate,
                         tasks_by_date=tasks_by_date)

# Route trang giới thiệu
@app.route('/about')
def about():
    return render_template('about.html')

# Route trang liên hệ
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route trang hướng dẫn sử dụng
@app.route('/guide')
def guide():
    return render_template('guide.html')

# Route test hiển thị hình ảnh
@app.route('/test-images')
def test_images():
    return render_template('test_images.html')

# Route xóa task: Xóa task theo ID
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    
    # Kiểm tra quyền xóa task
    if task_to_delete.user_id != session['user_id']:
        flash('Bạn không có quyền xóa task này', 'danger')
        return redirect('/')

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Có lỗi xảy ra khi xóa task'

# Route cập nhật task: Sửa nội dung task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task = Task.query.get_or_404(id)
    
    # Kiểm tra quyền cập nhật task
    if task.user_id != session['user_id']:
        flash('Bạn không có quyền cập nhật task này', 'danger')
        return redirect('/')

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Có lỗi xảy ra khi cập nhật task'

    else:
        return render_template('update.html', task=task)

# Route chuyển đổi trạng thái: Đánh dấu task hoàn thành/chưa hoàn thành
@app.route('/toggle/<int:id>')
@login_required
def toggle_status(id):
    task = Task.query.get_or_404(id)
    
    # Kiểm tra quyền thay đổi task
    if task.user_id != session['user_id']:
        flash('Bạn không có quyền thay đổi task này', 'danger')
        return redirect('/')
        
    # Đổi trạng thái task (pending <-> completed)
    task.status = 'completed' if task.status == 'pending' else 'pending'
    
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Có lỗi xảy ra khi cập nhật trạng thái'

# Khởi chạy ứng dụng với chế độ debug
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

with app.app_context():
    db.create_all()
    # Tạo tài khoản admin mặc định nếu chưa tồn tại
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin123'),
            email='admin@example.com'
        )
        db.session.add(admin_user)
        db.session.commit() 