import os
import requests
from urllib.parse import urlparse

def download_image(url, filename):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            os.makedirs('static/images', exist_ok=True)
            with open(f'static/images/{filename}', 'wb') as f:
                f.write(response.content)
            print(f'Downloaded {filename} successfully')
        else:
            print(f'Failed to download {filename}')
    except Exception as e:
        print(f'Error downloading {filename}: {str(e)}')

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Tạo thư mục images nếu chưa tồn tại
images_dir = os.path.join('static', 'images')
ensure_dir(images_dir)

# Danh sách hình ảnh cần tải
images = {
    # Logo công nghệ
    'python.png': 'https://www.python.org/static/community_logos/python-logo.png',
    'flask.png': 'https://cdn.worldvectorlogo.com/logos/flask.svg',
    'sqlite.png': 'https://www.sqlite.org/images/sqlite370_banner.gif',
    'bootstrap.png': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Bootstrap_logo.svg/512px-Bootstrap_logo.svg.png',
    
    # Hình ảnh minh họa
    'team.jpg': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800',
    'contact.jpg': 'https://images.unsplash.com/photo-1423666639041-f56000c27a9a?w=800',
    'register.jpg': 'https://images.unsplash.com/photo-1554415707-6e8cfc93fe23?w=800',
    'login.jpg': 'https://images.unsplash.com/photo-1526040652367-ac003a0475fe?w=800',
    'add-task.jpg': 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800',
    'update-task.jpg': 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800',
    'stats.jpg': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800'
}

# Tải các hình ảnh
for filename, url in images.items():
    download_image(url, filename)

print("\nHoàn thành! Tất cả hình ảnh đã được tải về thư mục static/images") 