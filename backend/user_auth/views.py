from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework_simplejwt.tokens import (
    RefreshToken
)
from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
    LoginSerializer,
    ProfileSerializer
)
from .models import EmailOTP
from .utils import send_otp_email

# Create your views here.

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        otp_obj = EmailOTP.objects.create(
            user=user
        )

        otp_obj.generate_otp()

        send_otp_email(user=user, otp=otp_obj.otp)

        return Response(
            {
                "message": "User registered. Please verify OTP sent to email."
            },
            status=status.HTTP_201_CREATED
        )
    
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response = Response(
            {
                "message": "Email verified successfully.",
                "user": ProfileSerializer(user).data
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
        )

        return response
    
class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = get_object_or_404(User, email=email)

        if user.is_active:
            return Response(
                {"detail": "Account already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        otp_obj, _ = EmailOTP.objects.get_or_create(user=user)
        otp_obj.generate_otp()

        send_otp_email(user=user, otp=otp_obj.otp)

        return Response(
            {
                "message": "OTP sent successfully."
            }
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(
            {
                "message": "Login successful"
            }
        )

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE
        )

        return response
    
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing."},
                status=401
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            response = Response(
                {"message": "Token refreshed."}
            )

            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=settings.SESSION_COOKIE_SECURE,
                samesite=settings.SESSION_COOKIE_SAMESITE
            )

            return response
        
        except Exception:
            return Response(
                {"detail": "Invalid refresh token."},
                status=401
            )
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(
            {"message": "Logged out successfully."}
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)

        return Response(serializer.data)