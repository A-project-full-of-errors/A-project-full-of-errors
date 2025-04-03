from django.urls import path
from .views import VerifyEmailView


urlpatterns = [
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
]