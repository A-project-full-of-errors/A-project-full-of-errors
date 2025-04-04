from django.urls import path
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    LogoutView,
    UserDetailView,
    SignupPageView,
    LoginPageView,
    ProfilePageView,
    EditProfileView,
    DeleteUserView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", LoginPageView.as_view(), name="home"),  # 기본 페이지 로그인 화면
    path("signup/", RegisterView.as_view(), name="signup"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("signup-form/", SignupPageView.as_view(), name="signup_form"),
    path("login-form/", LoginPageView.as_view(), name="login_form"),

    path("profile/<int:pk>/", ProfilePageView.as_view(), name="profile_page"),
    path("profile/<int:pk>/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("profile/<int:pk>/delete/", DeleteUserView.as_view(), name="delete_user"),
    path("me/", UserDetailView.as_view(), name="user_detail"),
]