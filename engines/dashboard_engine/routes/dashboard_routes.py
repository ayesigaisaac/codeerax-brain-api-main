from django.urls import path

from engines.dashboard_engine.controllers.dashboard_controller import (
    DashboardSummaryView,
    DashboardView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),

    path("summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
]

