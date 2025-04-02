# config/settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# 개발 환경에서는 development용 urls.py 사용
ROOT_URLCONF = 'config.urls.development'

# 개발용 추가 앱이나 미들웨어 (예: debug_toolbar)
INSTALLED_APPS += [
    # 'debug_toolbar',
]

# 예시: 개발 환경에서만 사용하는 DB (필요 시)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'dev_db.sqlite3',
#     }
# }
