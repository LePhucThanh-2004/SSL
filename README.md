# Hệ thống Quản lý Công việc (Task Management System)

## Thông tin đề tài
- **Tên đề tài:** Xây dựng Hệ thống Quản lý Công việc
- **Lớp:** 64CLC - Trường Đại học Nha Trang
- **Công nghệ sử dụng:** Python, Flask, SQLite, Bootstrap

## Tính năng chính
1. **Quản lý người dùng**
   - Đăng ký tài khoản
   - Đăng nhập/Đăng xuất
   - Xác thực và phân quyền

2. **Quản lý công việc**
   - Thêm công việc mới
   - Xem danh sách công việc
   - Cập nhật trạng thái
   - Chỉnh sửa nội dung
   - Xóa công việc

3. **Thống kê và báo cáo**
   - Tổng quan công việc
   - Biểu đồ tiến độ
   - Phân tích theo thời gian

4. **Giao diện**
   - Thiết kế responsive
   - Tương thích đa thiết bị
   - Giao diện người dùng thân thiện

## Yêu cầu hệ thống
- Python 3.7 trở lên
- pip (Python package installer)

## Cài đặt và Chạy

1. Clone repository
```bash
git clone <repository-url>
```

2. Tạo môi trường ảo
```bash
python -m venv venv
```

3. Kích hoạt môi trường ảo
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

5. Chạy ứng dụng
```bash
python app.py
```

Truy cập ứng dụng tại: http://localhost:5000

## Cấu trúc thư mục
```
.
├── app.py              # File chính của ứng dụng
├── requirements.txt    # Danh sách thư viện
├── instance/          # Database
├── static/            # Assets (CSS, JS, Images)
│   ├── css/
│   └── images/
└── templates/         # HTML templates
    ├── base.html     # Template cơ sở
    ├── index.html    # Trang chủ
    ├── login.html    # Đăng nhập
    ├── register.html # Đăng ký
    ├── about.html    # Giới thiệu
    ├── contact.html  # Liên hệ
    ├── guide.html    # Hướng dẫn
    ├── stats.html    # Thống kê
    └── update.html   # Cập nhật task
``` 