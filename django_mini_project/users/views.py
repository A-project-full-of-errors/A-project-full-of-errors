from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic.edit import FormView

# ✅ 회원가입 폼 페이지 (HTML 렌더링)
class SignupPageView(FormView):
    template_name = "signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login_form")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# ✅ 로그인 폼 페이지 (HTML 렌더링 & 로그인 처리)
class LoginPageView(FormView):
    template_name = "login.html"
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect("profile_page", pk=user.pk)

# ✅ 프로필 페이지 (HTML 렌더링)
class ProfilePageView(DetailView):
    queryset = CustomUser.objects.all()
    template_name = "users/profile.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("You do not have permission to view this profile.")
        return obj

# ✅ 프로필 수정 (pk를 경로로 받아, 로그인한 유저 본인만 수정 가능)
class EditProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    template_name = "users/edit_profile.html"

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("본인만 수정할 수 있습니다.")
        return obj

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return self.render_to_response({'user_profile': user})

    def post(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return redirect("profile_page", pk=self.get_object().pk)

# ✅ 회원 탈퇴
class DeleteUserView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("본인만 탈퇴할 수 있습니다.")
        return obj

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        logout(request)
        user.delete()
        return redirect("home")

# ✅ 회원가입 API
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            return redirect(reverse_lazy("login_form"))
        return response

# ✅ 로그인 API (JWT + 쿠키 저장)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ 로그아웃 API
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        logout(request)
        response = redirect("home")
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


# ✅ 프로필 조회 (로그인 유저만 자신의 정보 확인 가능)
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user