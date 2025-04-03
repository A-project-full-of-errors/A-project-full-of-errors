from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


INSTALLED_APPS += [
    "drf_yasg",
    "users",
]

FRONTEND_URL = 'http://localhost:3000'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_VERIFICATION_TOKEN_MAX_AGE = 3600