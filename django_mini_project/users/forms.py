from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# 회원가입 폼
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'phone_number', 'password1', 'password2')

# 로그인 폼
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # email을 username처럼 사용