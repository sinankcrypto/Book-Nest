from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    MessageResponseSerializer,
    VerifyOTPResponseSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
    ProfileSerializer
)

register_schema = extend_schema(
        summary="Register a new user",
        description=(
            "Creates a new inactive user account and sends "
            "a 6-digit OTP to the user's email address. "
            "The user must verify the OTP before the account "
            "can be activated."
        ),
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                response=MessageResponseSerializer,
                description="User registered successfully.",
                examples=[
                    OpenApiExample(
                        "Successful registration",
                        value={
                            "message": (
                                "User registered. Please verify "
                                "OTP sent to email."
                            )
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description=(
                    "Validation error. The username or email "
                    "may already exist, or the request may "
                    "contain invalid data."
                ),
                examples=[
                    OpenApiExample(
                        "Duplicate email",
                        value={
                            "email": [
                                "Email already exists."
                            ]
                        },
                    ),
                    OpenApiExample(
                        "Duplicate username",
                        value={
                            "username": [
                                "Username already exists."
                            ]
                        },
                    ),
                ],
            ),
        },
        tags=["Authentication"],
    )

verify_otp_schema = extend_schema(
        summary="Verify email OTP",
        description=(
            "Verifies the 6-digit OTP sent to the user's "
            "email during registration. "
            "On successful verification, the user account "
            "is activated and JWT access and refresh tokens "
            "are set as HttpOnly cookies."
        ),
        request=VerifyOTPSerializer,
        responses={
            200: OpenApiResponse(
                response=VerifyOTPResponseSerializer,
                description=(
                    "Email verified successfully. "
                    "JWT access and refresh tokens are "
                    "set as HttpOnly cookies."
                ),
                examples=[
                    OpenApiExample(
                        "Successful verification",
                        value={
                            "message": (
                                "Email verified successfully."
                            ),
                            "user": {
                                "id": 1,
                                "username": "sinan",
                                "email": "sinan@example.com",
                            },
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="OTP verification failed.",
                examples=[
                    OpenApiExample(
                        "Invalid OTP",
                        value={
                            "otp": [
                                "Invalid OTP."
                            ]
                        },
                    ),
                ],
            ),
        },
        tags=["Authentication"],
    )

resend_otp_schema = extend_schema(
        summary="Resend email verification OTP",
        description=(
            "Generates and sends a new 6-digit OTP to the "
            "user's registered email address. "
            "This endpoint can only be used for accounts "
            "that have not yet been verified."
        ),
        request=ResendOTPSerializer,
        responses={
            200: OpenApiResponse(
                response=MessageResponseSerializer,
                description=(
                    "A new OTP was generated and sent "
                    "successfully."
                ),
                examples=[
                    OpenApiExample(
                        "OTP sent successfully",
                        value={
                            "message": (
                                "OTP sent successfully."
                            )
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description=(
                    "The request is invalid or the account "
                    "has already been verified."
                ),
                examples=[
                    OpenApiExample(
                        "Account already verified",
                        value={
                            "detail": (
                                "Account already verified."
                            )
                        },
                    ),
                    OpenApiExample(
                        "Invalid email",
                        value={
                            "email": [
                                "Enter a valid email address."
                            ]
                        },
                    ),
                ],
            ),
            404: OpenApiResponse(
                description=(
                    "No user was found with the provided "
                    "email address."
                ),
                examples=[
                    OpenApiExample(
                        "User not found",
                        value={
                            "detail": "Not found."
                        },
                    )
                ],
            ),
        },
        tags=["Authentication"],
    )

login_schema = extend_schema(
        summary="Log in a user",
        description=(
            "Authenticates a user using their username "
            "and password. The user's account must be "
            "verified before login is allowed. "
            "On successful authentication, JWT access "
            "and refresh tokens are set as HttpOnly cookies."
        ),
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response=MessageResponseSerializer,
                description=(
                    "Login successful. JWT access and "
                    "refresh tokens are set as HttpOnly cookies."
                ),
                examples=[
                    OpenApiExample(
                        "Successful login",
                        value={
                            "message": "Login successful"
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description=(
                    "Authentication failed or the user's "
                    "account has not been verified."
                ),
                examples=[
                    OpenApiExample(
                        "Invalid credentials",
                        value={
                            "non_field_errors": [
                                "Invalid credentials."
                            ]
                        },
                    ),
                    OpenApiExample(
                        "Account not verified",
                        value={
                            "non_field_errors": [
                                "Account not verified."
                            ]
                        },
                    ),
                ],
            ),
        },
        tags=["Authentication"],
    )

refresh_token_schema = extend_schema(
        summary="Refresh access token",
        description=(
            "Generates a new JWT access token using the "
            "refresh token stored in the user's HttpOnly "
            "refresh_token cookie. "
            "The new access token is returned as an "
            "HttpOnly cookie. "
            "No request body is required."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                response=MessageResponseSerializer,
                description=(
                    "A new access token was generated "
                    "and set as an HttpOnly cookie."
                ),
                examples=[
                    OpenApiExample(
                        "Token refreshed",
                        value={
                            "message": "Token refreshed."
                        },
                    )
                ],
            ),
            401: OpenApiResponse(
                description=(
                    "The refresh token is missing or invalid."
                ),
                examples=[
                    OpenApiExample(
                        "Refresh token missing",
                        value={
                            "detail": (
                                "Refresh token missing."
                            )
                        },
                    ),
                    OpenApiExample(
                        "Invalid refresh token",
                        value={
                            "detail": (
                                "Invalid refresh token."
                            )
                        },
                    ),
                ],
            ),
        },
        tags=["Authentication"],
    )

logout_schema = extend_schema(
        summary="Log out the current user",
        description=(
            "Logs out the currently authenticated user by "
            "deleting the access_token and refresh_token "
            "HttpOnly cookies. "
            "Authentication is required to access this endpoint."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                response=MessageResponseSerializer,
                description=(
                    "User logged out successfully. "
                    "The access and refresh token cookies "
                    "are deleted."
                ),
                examples=[
                    OpenApiExample(
                        "Successful logout",
                        value={
                            "message": (
                                "Logged out successfully."
                            )
                        },
                    )
                ],
            ),
            401: OpenApiResponse(
                description=(
                    "Authentication credentials are missing "
                    "or invalid."
                ),
                examples=[
                    OpenApiExample(
                        "Not authenticated",
                        value={
                            "detail": (
                                "Authentication credentials "
                                "were not provided."
                            )
                        },
                    )
                ],
            ),
        },
        tags=["Authentication"],
    )

profile_schema = extend_schema(
        summary="Get current user's profile",
        description=(
            "Returns the profile information of the currently "
            "authenticated user. Authentication is required. "
            "The access token is read from the HttpOnly "
            "access_token cookie."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                response=ProfileSerializer,
                description=(
                    "The authenticated user's profile."
                ),
                examples=[
                    OpenApiExample(
                        "User profile",
                        value={
                            "id": 1,
                            "username": "sinan",
                            "email": "sinan@example.com",
                        },
                    )
                ],
            ),
            401: OpenApiResponse(
                description=(
                    "Authentication credentials are missing "
                    "or invalid."
                ),
                examples=[
                    OpenApiExample(
                        "Not authenticated",
                        value={
                            "detail": (
                                "Authentication credentials "
                                "were not provided."
                            )
                        },
                    )
                ],
            ),
        },
        tags=["Authentication"],
    )
