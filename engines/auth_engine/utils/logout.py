from django.db import models
from django.utils import timezone
from datetime import timedelta
from ..models import BlacklistedToken

# ---------------------------
# Utility Functions
# ---------------------------
def blacklist_token(token: str, expiry_hours: int = 24):
    """
    Blacklists the given JWT token.
    """
    expires_at = timezone.now() + timedelta(hours=expiry_hours)
    BlacklistedToken.objects.create(token=token, expires_at=expires_at)


def is_token_blacklisted(token: str) -> bool:
    """
    Checks if the token is blacklisted.
    """
    return BlacklistedToken.objects.filter(token=token, expires_at__gt=timezone.now()).exists()