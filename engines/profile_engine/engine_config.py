from django.urls import include, path

from . import routes


profile_engine_urls = [
    path(
        "profile/",
        include((routes.urlpatterns, "profile_engine"), namespace="profile_engine"),
    ),
]


def register_profile_engine():
    """
    Returns URL patterns for inclusion in API gateway.
    Can be extended to register middleware, signals, or other engine-specific configs.
    """
    return profile_engine_urls

