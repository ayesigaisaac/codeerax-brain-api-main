from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlencode


# ---------------------------
# Send Verification Email
# ---------------------------
def send_verification_email(user):
    """
    Sends an email with a verification link containing the user's token.
    """
    # During automated tests we avoid sending real emails.
    try:
        from django.conf import settings
        if getattr(settings, "TESTING", False):
            # In testing mode, skip sending external emails.
            return
    except Exception:
        pass
    subject = "Verify Your Email"
    # Build verification link (frontend_url should point to your frontend page)
    params = urlencode({"uid": str(user.id), "token": str(user.email_verification_token)})
    verification_link = f"{settings.FRONTEND_URL.rstrip('/')}/auth/verify-email/?{params}"
   
    message = f"Hi {user.username or user.email},\n\n"
    message += "Please verify your email by clicking the link below:\n"
    message += verification_link
    message += "\n\nThis link will expire in 24 hours."

    send_mail(
        subject,
        message,
        settings.EMAIL_FROM,
        [user.email],
        fail_silently=False,
    )


# ---------------------------
# Send Password Reset Email
# ---------------------------
def send_password_reset_email(user, uid, token):
    """
    Sends a password reset link via email.
    """
    # During automated tests we avoid sending real emails.
    try:
        from django.conf import settings
        if getattr(settings, "TESTING", False):
            return
    except Exception:
        pass
    subject = "Reset Your Password"
    params = urlencode({"uid": uid, "token": str(token)})
    reset_link = f"{settings.FRONTEND_URL}/reset-password/?{params}"

    message = f"Hi {user.username or user.email},\n\n"
    message += "You requested a password reset. Click the link below to set a new password:\n"
    message += reset_link
    message += "\n\nIf you did not request this, you can ignore this email."

    send_mail(
        subject,
        message,
        settings.EMAIL_FROM,
        [user.email],
        fail_silently=False,
    )