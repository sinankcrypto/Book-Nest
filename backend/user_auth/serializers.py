import re
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import EmailOTP

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )

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
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Username cannot be empty."
            )
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )
        if len(value) > 30:
            raise serializers.ValidationError(
                "Username cannot exceed 30 characters."
            )
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )
        if not re.search(r"[a-zA-Z]", value):
            raise serializers.ValidationError(
                "Username must contain at least one letter."
            )
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )
        return value

    def validate(self, attrs):
        user = User(
            username=attrs.get("username"),
            email=attrs.get("email")
        )
        try:
            validate_password(attrs.get("password"), user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False
        )
    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.RegexField(regex=r"^\d{6}$")

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
    username = serializers.CharField(required=True, max_length=30)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email"
        ]
        read_only_fields = ["id", "email"]

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Username cannot be empty."
            )
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )
        if len(value) > 30:
            raise serializers.ValidationError(
                "Username cannot exceed 30 characters."
            )
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )
        if not re.search(r"[a-zA-Z]", value):
            raise serializers.ValidationError(
                "Username must contain at least one letter."
            )
        query = User.objects.filter(username__iexact=value)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError(
                "Username already exists."
            )
        return value


class MessageResponseSerializer(
    serializers.Serializer
):
    message = serializers.CharField()

class VerifyOTPResponseSerializer(
    serializers.Serializer
):
    message = serializers.CharField()
    user = ProfileSerializer()