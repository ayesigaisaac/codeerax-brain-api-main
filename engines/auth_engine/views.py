from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
    ResendVerificationSerializer,
    UpdatePasswordSerializer,
)
from .services import (
    register_user,
    login_user,
    get_current_user,
    logout_user,
    forgot_password,
    reset_password,
    verify_email,
    resend_verification_email,
    update_password,
)
from .utils.authentication import JWTAuthentication, IsAuthenticatedCustom
import logging
from .schemas import (
     RegisterSchema,
    LoginSchema,
    LogoutSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    UpdatePasswordSchema,
    VerifyEmailSchema,
    ResendVerificationSchema,
    AuthOutputSchema
)

logger = logging.getLogger("engines")


# ---------------------------
# 1️ Register
# ---------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        schema = RegisterSchema(**serializer.validated_data)
        data = register_user(schema)
        
        return Response(data, status=status.HTTP_201_CREATED)


# ---------------------------
# 2️ Login
# ---------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        schema = LoginSchema(**serializer.validated_data)
        data = login_user(schema)
        
        return Response(data, status=status.HTTP_200_OK)


# ---------------------------
# 3️ Current User
# ---------------------------
class MeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        data = get_current_user(request.user)

        return Response(data, status=status.HTTP_200_OK)


# ---------------------------
# 4️ Logout
# ---------------------------
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        token = request.auth  # JWT token
        
        schema = LogoutSchema(token=token)
        data = logout_user(schema)
        
        return Response(data, status=status.HTTP_200_OK)


# ---------------------------
# 5️ Forgot Password
# ---------------------------
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        schema = ForgotPasswordSchema(**serializer.validated_data)
        data = forgot_password(schema)
        
        return Response(data, status=status.HTTP_200_OK)


# ---------------------------
# 6️ Reset Password
# ---------------------------
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        schema = ResetPasswordSchema(**serializer.validated_data)
        data = reset_password(schema)
        
        return Response(data, status=status.HTTP_200_OK)


# ---------------------------
# 7️ Verify Email
# ---------------------------

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uid or not token:
            raise ValidationError({"detail": "UID and token are required."})

        schema = VerifyEmailSchema(uid=uid, token=token)
        verify_email(schema)

        return Response(
            {"message": "Email verified successfully"}, 
            status=status.HTTP_200_OK
        )

# ---------------------------
# 8️ Resend Verification Email
# ---------------------------
class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        schema = ResendVerificationSchema(**serializer.validated_data)  # Convert to schema
        data = resend_verification_email(schema)  # Pass the schema
        
        return Response(data, status=status.HTTP_200_OK)


# --------------------------
# 9️ Update Password
# ---------------------------
class UpdatePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        schema = UpdatePasswordSchema(**serializer.validated_data)  # Convert to schema
        data = update_password(request.user, schema)  # Pass the schema
        
        return Response(data, status=status.HTTP_200_OK)
