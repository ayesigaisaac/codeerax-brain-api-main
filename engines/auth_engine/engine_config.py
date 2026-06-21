from django.urls import include, path

# Import your auth routes
from . import routes

# Prefix all auth endpoints with 'auth/'
auth_engine_urls = [
    path("auth/", include((routes.urlpatterns, "auth_engine"), namespace="auth_engine")),
]

def register_auth_engine():
    """
    Returns URL patterns for inclusion in API gateway.
    Can be extended to register middleware, signals, or other engine-specific configs.
    """
    return auth_engine_urls