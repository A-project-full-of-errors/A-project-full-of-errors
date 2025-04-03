from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings
from .models import CustomUser
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer

# 회원가입 API
class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    
# 메일 인증 API
class VerifyEmailView(APIView):
    def get(self, request, token):
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        
        try: #토큰 디코딩 및 검증
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