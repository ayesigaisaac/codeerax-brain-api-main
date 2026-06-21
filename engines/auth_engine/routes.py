from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    LogoutView,
    ForgotPasswordView,
    ResetPasswordView,
    VerifyEmailView,
    ResendVerificationEmailView,
    UpdatePasswordView,
)

app_name = "auth_engine"

urlpatterns = [
    # ---------------------------
    # Public Endpoints
    # ---------------------------
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationEmailView.as_view(), name="resend-verification"),

    # ---------------------------
    # Protected Endpoints
    # ---------------------------
    path("me/", MeView.as_view(), name="me"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("update-password/", UpdatePasswordView.as_view(), name="update-password"),
]
