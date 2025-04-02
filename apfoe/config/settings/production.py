# config/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# 배포 환경에서는 production용 urls.py 사용
ROOT_URLCONF = 'config.urls.production'

# 예시: PostgreSQL 등 실제 서비스 DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'dbname'),
        'USER': os.getenv('POSTGRES_USER', 'dbuser'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'dbpassword'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# 배포 환경에서 권장되는 보안 설정
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000  # 1년 (필요 시 사용)
