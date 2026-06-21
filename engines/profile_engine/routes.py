from django.urls import path

from .views import (
    CreateProfileView,
    MyProfileView,
    PublicProfileView,
    UpdateProfileView,
)


app_name = "profile_engine"


urlpatterns = [
    path("create/", CreateProfileView.as_view(), name="create"),
    path("me/", MyProfileView.as_view(), name="me"),
    path("update/", UpdateProfileView.as_view(), name="update"),
    path("public/<uuid:user_id>/", PublicProfileView.as_view(), name="public-profile"),
]

