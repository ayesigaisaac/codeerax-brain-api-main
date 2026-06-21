import uuid
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .models import User
from .utils.auth import create_jwt_token, hash_password, verify_password
from .utils.email import send_verification_email, send_password_reset_email
from .utils.logout import blacklist_token
from .schemas import (
    RegisterSchema,
    LoginSchema,
    LogoutSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    UpdatePasswordSchema,
    VerifyEmailSchema,
    ResendVerificationSchema,
    AuthOutputSchema,
    CurrentUserOutputSchema,
)


# ---------------------------
# 1️Register User
# ---------------------------
def register_user(data: RegisterSchema) -> AuthOutputSchema:
    email = data.email
    password = data.password
    username = data.username
    
    if User.objects.filter(email=email).exists():
        raise ValidationError({"email": "Email already exists."})

    hashed_password = hash_password(password)

    user = User.objects.create(
        id=uuid.uuid4(),
        email=email,
        username=username,
        password=hashed_password,
        is_active=False
    )

    user.generate_email_verification()
    user.save(update_fields=['email_verification_token', 'email_verification_expiry'])

    send_verification_email(user)

    return {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "message": "Registration successful. Please verify your email."
    }


# ---------------------------
#Login User
# ---------------------------
def login_user(data: LoginSchema) -> AuthOutputSchema:
    email = data.email
    password = data.password
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise AuthenticationFailed("Invalid email or password.")

    if not verify_password(password, user.password):
        raise AuthenticationFailed("Invalid email or password.")

    if not user.is_active:
        raise AuthenticationFailed("Account inactive. Verify your email.")

    token = create_jwt_token(user)
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])

    return {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "token": token
    }


# ---------------------------
# Current User
# ---------------------------
def get_current_user(user) -> CurrentUserOutputSchema:
    return {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "date_joined": user.date_joined.isoformat() if user.date_joined else None,
        "last_login": user.last_login.isoformat() if user.last_login else None,
    }


# ---------------------------
# 3️ Logout User
# ---------------------------
def logout_user(data: LogoutSchema) -> AuthOutputSchema:
    token = data.token
    blacklist_token(token)
    return {"message": "Successfully logged out."}


# ---------------------------
# 4️ Forgot Password (Request Reset)
# ---------------------------
def forgot_password(data: ForgotPasswordSchema) -> AuthOutputSchema:
    email = data.email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValidationError("Email not found.")

    token = default_token_generator.make_token(user)
    uid = str(user.id)

    send_password_reset_email(user, uid, token)

    return {"message": "If the email exists, a reset link has been sent."}


# ---------------------------
# 5️ Reset Password
# ---------------------------
def reset_password(data: ResetPasswordSchema) -> AuthOutputSchema:
    uid = data.uid
    token = data.token
    new_password = data.new_password
    
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        raise ValidationError("Invalid reset link.")

    if not default_token_generator.check_token(user, token):
        raise ValidationError("Reset token invalid or expired.")

    user.password = hash_password(new_password)
    user.save(update_fields=['password'])

    return {"message": "Password has been reset successfully."}


# ---------------------------
# 6️Verify Email
# ---------------------------
def verify_email(data: VerifyEmailSchema) -> AuthOutputSchema:
    uid = data.uid
    token = data.token
    
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        raise ValidationError("Invalid verification link.")

    try:
        token_uuid = uuid.UUID(token)
    except ValueError:
        raise ValidationError("Invalid verification token.")

    if user.email_verification_token != token_uuid:  
        raise ValidationError("Verification token invalid.")

    if timezone.now() > user.email_verification_expiry:
        raise ValidationError("Verification token expired.")

    user.is_active = True
    user.email_verification_token = None
    user.email_verification_expiry = None
    user.save(update_fields=['is_active', 'email_verification_token', 'email_verification_expiry'])

    return {"message": "Email verified successfully."}


# ---------------------------
# 7️ Resend Verification Email
# ---------------------------
def resend_verification_email(data: ResendVerificationSchema) -> AuthOutputSchema:
    email = data.email
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValidationError("Email not found.")

    if user.is_active:
        return {"message": "Email already verified."}

    user.generate_email_verification()
    user.save(update_fields=['email_verification_token', 'email_verification_expiry'])

    send_verification_email(user)

    return {"message": "Verification email resent."}


# ---------------------------
# 8️ Update Password (Logged In User)
# ---------------------------
def update_password(user, data: UpdatePasswordSchema) -> AuthOutputSchema:
    old_password = data.old_password
    new_password = data.new_password

    if not verify_password(old_password, user.password):
        raise ValidationError("Old password is incorrect.")

    user.set_password(new_password) 
    user.save(update_fields=['password'])

    return {"message": "Password updated successfully."}
