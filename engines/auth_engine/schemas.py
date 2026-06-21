from dataclasses import dataclass
from typing import Optional


# ---------------------------
# User Registration Input
# ---------------------------
@dataclass
class RegisterSchema:
    email: str
    password: str
    username: Optional[str] = None


# ---------------------------
# User Login Input
# ---------------------------
@dataclass
class LoginSchema:
    email: str
    password: str
    
    
@dataclass
class LogoutSchema:
    token: str


# ---------------------------
# Password Reset Request
# ---------------------------
@dataclass
class ForgotPasswordSchema:
    email: str


# ---------------------------
# Password Reset Confirm
# ---------------------------
@dataclass
class ResetPasswordSchema:
    uid: str
    token: str
    new_password: str


# ---------------------------
# Update Password (logged-in user)
# ---------------------------
@dataclass
class UpdatePasswordSchema:
    old_password: str
    new_password: str


# ---------------------------
# Email Verification
# ---------------------------
@dataclass
class VerifyEmailSchema:
    uid: str
    token: str


# ---------------------------
# Resend Verification Email
# ---------------------------
@dataclass
class ResendVerificationSchema:
    email: str


# ---------------------------
# Output Schemas
# ---------------------------
@dataclass
class AuthOutputSchema:
    user_id: str
    email: str
    username: Optional[str] = None
    token: Optional[str] = None
    message: Optional[str] = None


@dataclass
class CurrentUserOutputSchema:
    user_id: str
    email: str
    username: Optional[str] = None
    is_active: bool = False
    is_staff: bool = False
    date_joined: Optional[str] = None
    last_login: Optional[str] = None
