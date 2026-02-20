from django.urls import path
from .views import (
    SignUpView,
    VerifyCodeView,
    GetVerifyCodeView,
    UpdateInformationView,
    UpdatePhotoView,
    LoginView,
    ResetPasswordView,
    ForgotPasswordView,
    LogoutView,
    GetUserView,
)

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/',SignUpView.as_view()),
    path('verify-code/',VerifyCodeView.as_view()),
    path('resend-verify-code/',GetVerifyCodeView.as_view()),
    path('update/',UpdateInformationView.as_view()),
    path('upload/',UpdatePhotoView.as_view()),
    path('login/',LoginView.as_view()),
    path('reset-password/',ResetPasswordView.as_view()),
    path('forgot-password/',ForgotPasswordView.as_view()),
    path('refresh-token/',TokenRefreshView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('me/',GetUserView.as_view()),
]