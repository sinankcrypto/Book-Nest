from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, RefreshTokenView, ProfileView, VerifyOTPView, ResendOTPView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("resend-otp/", ResendOTPView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", RefreshTokenView.as_view()),
    path("profile/", ProfileView.as_view()),

]
