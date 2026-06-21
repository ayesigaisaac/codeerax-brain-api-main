from django.urls import path

from .views import HeartExecuteAliasView, HeartExecuteView, RuntimeAliasView, RuntimeView


app_name = "heart"


urlpatterns = [
    path("internal/execute/", HeartExecuteView.as_view(), name="execute"),
    path("internal/execute", HeartExecuteAliasView.as_view(), name="execute-no-slash"),
    path("runtime/<str:project_id>/", RuntimeView.as_view(), name="runtime"),
    path("runtime/<str:project_id>", RuntimeAliasView.as_view(), name="runtime-no-slash"),
]
