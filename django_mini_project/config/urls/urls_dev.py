# config/urls/dev.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomTokenObtainPairView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    # 예: debug_toolbar
    # path('__debug__/', include('debug_toolbar.urls')),
    # 개발 환경에서만 사용하는 URL 패턴
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
