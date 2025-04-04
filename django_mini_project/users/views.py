from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    UserProfileSerializer,  # ✅ 프로필용 직렬화기
)


# ✅ 회원가입 폼 페이지 (HTML 렌더링)
class SignupPageView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_form")
        return render(request, "signup.html", {"form": form})


# ✅ 로그인 폼 페이지 (HTML 렌더링 & 로그인 처리)
class LoginPageView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile_page")
        return render(request, "login.html", {"form": form})


# ✅ 프로필 페이지 (HTML 렌더링)
class ProfilePageView(View):
    def get(self, request):
        return render(request, "profile.html")

    def post(self, request):
        method = request.POST.get('_method')

        if method == 'PATCH':
            request.user.name = request.POST.get('name')
            request.user.save()
            return redirect('profile_page')

        elif method == 'DELETE':
            request.user.delete()
            return redirect('home')

        return render(request, "profile.html")



# ✅ 회원가입 API (회원가입 성공 시 로그인 페이지로 이동)
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
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")

        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ 로그아웃 API (쿠키 삭제 & 토큰 블랙리스트 추가)
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        logout(request)

        response = redirect("home")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


# ✅ 유저 정보 조회, 수정, 삭제 API + 폼 POST 수동 처리
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        method = request.POST.get('_method')

        if method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif method == 'DELETE':
            return self.delete(request, *args, **kwargs)

        return Response({"error": "Method not allowed"}, status=405)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
