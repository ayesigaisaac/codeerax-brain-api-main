from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from .auth import decode_jwt_token
from .logout import is_token_blacklisted
from rest_framework.permissions import BasePermission


User = get_user_model()


# ---------------------------
# JWT Authentication Class
# ---------------------------
class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication for DRF.
    Reads the token from the `Authorization` header: 'Bearer <token>'.
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # DRF will continue to check other authentication classes

        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed("Invalid Authorization header format.")

        token = parts[1]

        if is_token_blacklisted(token):
            raise exceptions.AuthenticationFailed("Token has been revoked.")

        try:
            payload = decode_jwt_token(token)
        except ValueError as e:
            raise exceptions.AuthenticationFailed(str(e))

        try:
            user = User.objects.get(id=payload["user_id"], email=payload["email"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found.")

        return (user, token)

    def authenticate_header(self, request):
        return self.keyword


# DRF Permission Class Example

class IsAuthenticatedCustom(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
