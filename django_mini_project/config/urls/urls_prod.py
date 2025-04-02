# config/urls/prod.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    # 배포 환경에서 필요한 URL 패턴
]
