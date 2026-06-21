from rest_framework import serializers
from .models import User
from .utils.validators import validate_password, validate_email
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


# ---------------------------
# 1️Registration Serializer
# ---------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email = serializers.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        from .services import register_user
        
        data = RegisterSchema(**validated_data)
        return register_user(data)
        


# ---------------------------
# 2️ Login Serializer
# ---------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    data = LoginSchema(email=email, password=password)
    


# ---------------------------
# 3️ Forgot Password Serializer
# ---------------------------
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


# ---------------------------
# 4️Reset Password Serializer
# ---------------------------
class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


# ---------------------------
# 5️ Update Password Serializer (logged-in user)
# ---------------------------
class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


# ---------------------------
# 6️ Verify Email Serializer
# ---------------------------
class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    token = serializers.CharField()


# ---------------------------
# 7️ Resend Verification Email Serializer
# ---------------------------
class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()