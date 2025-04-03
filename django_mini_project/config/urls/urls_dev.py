# config/urls/dev.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls'))
    # 예: debug_toolbar
    # path('__debug__/', include('debug_toolbar.urls')),
    # 개발 환경에서만 사용하는 URL 패턴
]
