import re
from rest_framework.exceptions import ValidationError


# ---------------------------
# Password Validator
# ---------------------------
def validate_password(password: str):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")
    return password


# ---------------------------
# Email Validator
# ---------------------------
def validate_email(email: str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValidationError("Invalid email address.")
    return email