from django.urls import path

from .views import BrainBuildView, BrainHealthView, BrainAuthBuildView, BuildStatusView


app_name = "brain"


urlpatterns = [
    path("health/", BrainHealthView.as_view(), name="health"),
    path("build/", BrainBuildView.as_view(), name="build"),
    path("build/auth/", BrainAuthBuildView.as_view(), name="build-auth"),
    path("build/status/<str:task_id>/", BuildStatusView.as_view(), name="build-status"),
]

