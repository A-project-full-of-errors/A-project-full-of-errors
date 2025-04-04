from rest_framework import serializers
from .models import CustomUser
from django.db import transaction
import re
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
from itsdangerous import URLSafeTimedSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone_number')
        read_only_fields = ('email',) #수정방지


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')

    # 이메일 형식 검증
    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("유효한 이메일 주소를 입력해 주세요.")
        return value

    # 닉네임 형식 검증
    def validate_nickname(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("닉네임은 영문자, 숫자, 밑줄(_)만 포함할 수 있습니다.")
        return value

    @transaction.atomic
    def create(self, validated_data):

        # 전화번호는 선택적 필드로 처리
        phone_number = validated_data.get('phone_number', None)

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            name=validated_data['name'],
            phone_number=phone_number,
        )

        # 이메일 인증 토큰 생성 및 전송
        self.send_verification_email(user)

        return user

    def send_verification_email(self, user):
        try:
            # 토큰 생성
            serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
            token = serializer.dumps(user.email, salt='email-confirmation-salt')

            # 이메일 전송
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
            subject = "이메일 인증 요청"
            message = f"다음 링크를 클릭하여 이메일을 인증하세요: {verification_url}"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        except Exception as e:
            raise ValidationError(f"이메일 전송에 실패했습니다: {str(e)}")