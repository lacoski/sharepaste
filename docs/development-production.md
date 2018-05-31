# Triển khai Pasteme - Django + Apache + Mysql (CentOS7)
---
## Phần 1: Chuẩn bị môi trường
> Develop môi trường CentOS 7

### Bước 1: Cài đặt môi trường
```
yum groupinstall "Development Tools" -y

yum -y install https://centos7.iuscommunity.org/ius-release.rpm

yum -y install python36u

pip3.6 install virtualenv
```

> NOTE: disable setenforce
 - lỗi selinux: Block truy cập file django

### Bước 2: Cài đặt Apache httpd
```
yum install httpd -y
yum install python36u-mod_wsgi -y
```
### Bước 3: Cài đặt Mysql

__Tham khảo__
```
https://github.com/lacoski/mysql-1
```
> start, enable service mysql

__Bổ sung package__
```
yum install mariadb-devel -y
```

### Bước 4: Cài python3, pip3
#### Cài python3
```
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install python-devel
yum -y install python36-devel
yum -y install python36
```

__Kiểm tra vesion__
```
python3.6 -V
```

#### Cài đặt pip pip2 pip3
```
yum -y install python-pip
sudo yum -y install python36u-pip
```

### Bước 5: Cài virtualenv Python
```
pip3 install virtualenv
```

## Phần 2: Cấu hình Project

### Bước 1: Cấu hình Mysql
__Tạo mới db tên `pasteme`__

```
mysql> create database pasteme;
Query OK, 1 row affected (0.00 sec)
```

> Năng cao: Nên tạo user riêng với quyền quản trị DB riêng mysql

### Bước 2: Cấu hình Project
#### Chuẩn bị virtualenv Python
```
cd /var/www/
virtualenv env
source env/bin/activate
(env) [..]$ pip3 install -r requirement.txt
```
> File requirement check trong [project]/requirements
#### Cấu hình setting.py
> Path: [project]/pasteme/pasteme/wsgi.py

```
vi [project]/pasteme/pasteme/setting.py
```

__Lưu ý cấu hình__
- Database (sử dụng mysql)

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pasteme',
        'USER': '[user]',
        'PASSWORD': '[password user]',
        'HOST': '[ip host mysql]',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
```

- Domain accept

```
ALLOWED_HOSTS = ['(ip host or domain accept)','(ip host or domain accept)']

VD: ALLOWED_HOSTS = ['thanh.com']
```
#### Cấu hình wsgi.py
> Path: [project]/pasteme/pasteme/wsgi.py

__Chỉnh sửa nội dung file: `wsgi.py`__
```
vi [project]/pasteme/pasteme/wsgi.py
```
Nội dung
```
import os,sys,site

sys.path.append('/path/to/project/')
sys.path.append('/path/to/env/lib/pythonx.x/')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pasteme.settings")

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
```
#### Cấu hình Migrations model tới db mysql
> PATH: [project]/pasteme

```
cd [project]/pasteme

python3 manage.py makemigrations
python3 manage.py migrate
```

### Phần 3: Cấu hình httpd
#### Bước 1: Chuyển project tới thư mục /var/www/
```
cp -R [project]/pasteme /var/www/
```
Kiểm tra nội dung
```
ls
cgi-bin  env  html  pasteme
```
> Cần lưu ý
 - Môi trường python chạy cho web: env
 - Project chạy: pasteme

#### Bước 2: Tạo mới file config
__Tạo mới file__
```
vi /etc/httpd/conf.d/django.conf
```
Nội dung
```
Alias /static /var/www/pasteme/static
<Directory /var/www/pasteme/static>
    Require all granted
</Directory>

<Directory /var/www/pasteme/pasteme>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

#WSGIDaemonProcess pasteme python-path=/var/www/html/pasteme:/var/www/html/env/lib/python3.6/site-packages

WSGIDaemonProcess pasteme python-path=/var/www/env/lib/python3.6/site-packages
WSGIProcessGroup pasteme
WSGIScriptAlias / /var/www/pasteme/pasteme/wsgi.py
```

#### Bước 3: Chạy project
```
systemctl restart httpd
systemctl enable httpd
```

__Kiểm tra__
```
http://localhost
http://[ip host]
http://[domain]
```
> Lưu ý: allow access tại file setting.py, không truy cập sẽ bị Block

__Nếu lỗi, hoặc không truy cập được trang web__
- Kiểm tra: `/var/log/httpd/error_log`
- Lưu ý các `Note` trong bài

## Nguồn:

https://www.server-world.info/en/note?os=CentOS_7&p=httpd&f=20
