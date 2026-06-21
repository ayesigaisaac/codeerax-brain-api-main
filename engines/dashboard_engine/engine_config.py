from django.urls import include, path

from . import routes


dashboard_engine_urls = [
    path(
        "dashboard/",
        include((routes.urlpatterns, "dashboard_engine"), namespace="dashboard_engine"),
    ),
]


def register_dashboard_engine():
    return dashboard_engine_urls

