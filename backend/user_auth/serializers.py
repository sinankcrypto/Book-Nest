from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import EmailOTP

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=8)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )
        
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False
        )
    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs["email"]
        otp = attrs["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "User not found."}
            )

        otp_obj = (
            EmailOTP.objects
            .filter(user=user)
            .first()
        )

        if not otp_obj:
            raise serializers.ValidationError(
                {"otp": "OTP not found."}
            )

        if otp_obj.is_expired():
            raise serializers.ValidationError(
                {"otp": "OTP expired."}
            )

        if otp_obj.otp != otp:
            raise serializers.ValidationError(
                {"otp": "Invalid OTP."}
            )

        attrs["user"] = user
        attrs["otp_obj"] = otp_obj

        return attrs
    
    def save(self):
        user = self.validated_data["user"]
        otp_obj = self.validated_data["otp_obj"]

        user.is_active = True
        user.save()

        otp_obj.delete()

        return user
    
class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials."
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                "Account not verified."
            )
        
        attrs["user"] = user
        return attrs
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email"
        ]
