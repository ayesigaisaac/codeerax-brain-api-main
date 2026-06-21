import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# ---------------------------
# Password Hashing
# ---------------------------
def hash_password(raw_password: str) -> str:
    """
    Hashes the plain password using Django's built-in hasher.
    """
    return make_password(raw_password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    """
    Checks if the provided raw password matches the hashed password.
    """
    return check_password(raw_password, hashed_password)


# ---------------------------
# JWT Token Generation
# ---------------------------
def create_jwt_token(user, expiry_hours: int = 24) -> str:
    """
    Generates a JWT token for the given user.
    """
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=expiry_hours),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt_token(token: str) -> dict:
    """
    Decodes a JWT token and returns the payload.
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on failure.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")