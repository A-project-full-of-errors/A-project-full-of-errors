import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # 비밀번호 암호화
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)  # 선택적 필드로 처리
    is_active = models.BooleanField(default=False)  # 이메일 인증 후 활성화
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name'] 

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자들"
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def clean(self):
        # 전화번호 유효성 검사 (선택 사항)
        if self.phone_number:
            from phonenumbers import parse, is_valid_number, NumberParseException
            try:
                phone = parse(self.phone_number, None)  # 국가 코드를 자동 감지
                if not is_valid_number(phone):
                    raise ValidationError("유효하지 않은 전화번호입니다.")
            except NumberParseException:
                raise ValidationError("전화번호를 올바른 형식으로 입력해 주세요.")