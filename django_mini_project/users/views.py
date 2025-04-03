from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy

# ✅ 회원가입 폼 페이지 (HTML 렌더링)
class SignupPageView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)  # 폼 데이터 받기
        if form.is_valid():
            form.save()  # 유저 생성
            return redirect("login_form")  # 🚀 회원가입 성공하면 로그인 페이지로 이동
        return render(request, "signup.html", {"form": form})  # 실패 시 다시 폼 표시

# ✅ 로그인 폼 페이지 (HTML 렌더링 & 로그인 처리)
class LoginPageView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # 로그인 처리
            return redirect("profile_page")  # ✅ 로그인 성공 시 프로필 페이지로 이동
        return render(request, "login.html", {"form": form})  # 로그인 실패 시 다시 로그인 페이지


# ✅ 프로필 페이지 (HTML 렌더링)
class ProfilePageView(View):
    def get(self, request):
        return render(request, "profile.html")


# ✅ 회원가입 API (회원가입 성공 시 로그인 페이지로 이동)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201:  # 회원가입 성공 시
            return redirect(reverse_lazy("login_form"))  # 🚀 더 안전한 리디렉트

        return response  # 실패 시 기존 응답 반환


# ✅ 로그인 API (JWT + 쿠키 저장)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        # ✅ email과 password로 사용자 인증
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)  # 로그인 처리
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ 로그아웃 API (쿠키 삭제 & 토큰 블랙리스트 추가)
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # 토큰 블랙리스트 처리

        logout(request)  # Django 로그아웃

        response = redirect("home")
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


# ✅ 유저 정보 조회 및 수정 API
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user