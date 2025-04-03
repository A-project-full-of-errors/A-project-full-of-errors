from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings
from .models import CustomUser
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm


# 회원가입 API
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


# 메일 인증 API
class VerifyEmailView(APIView):
    def get(self, request, token):
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

        try:  # 토큰 디코딩 및 검증
            email = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)  # 1시간 유효
        except SignatureExpired:
            return Response({'error': '인증 링크가 만료되었습니다. 다시 시도해 주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({'error': '인증 링크가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 조회
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'error': '존재하지 않는 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 이미 활성화된 계정인지 확인
        if user.is_active:
            return Response({'message': '이미 인증된 계정입니다.'}, status=status.HTTP_200_OK)

        # 계정 활성화 처리
        user.is_active = True
        user.save()

        return Response({'message': '이메일 인증이 완료되었습니다.'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.set_cookie('access_token', response.data['access'], httponly=True)
        response.set_cookie('refresh_token', response.data['refresh'], httponly=True)
        return response


class LogoutView(generics.GenericAPIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        response = Response(status=204)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {'message': 'Deleted successfully'}
        return response

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def profile_view(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('login')