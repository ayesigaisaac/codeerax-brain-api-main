from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import RuntimeProject
from .schemas import HeartExecuteOutputSchema, HeartExecuteSchema, RuntimeOutputSchema


def _build_auth_runtime(data: HeartExecuteSchema) -> dict:
    return {
        "project_id": data.project_id,
        "engine": "auth",
        "feature": data.feature or "auth",
        "build_summary": "Heart prepared a mock runtime for the auth flow.",
        "prompt": data.prompt,
        "screens": ["login", "register", "forgot-password"],
        "components": ["auth-form", "password-field", "email-field"],
        "routes": ["/login", "/register", "/forgot-password"],
        "status": "completed",
    }


def _build_profile_runtime(data: HeartExecuteSchema) -> dict:
    return {
        "project_id": data.project_id,
        "engine": "profile",
        "feature": data.feature or "profile",
        "build_summary": "Heart prepared a mock runtime for the profile flow.",
        "prompt": data.prompt,
        "screens": ["profile-overview", "profile-edit"],
        "components": ["profile-card", "profile-form", "avatar-block"],
        "routes": ["/profile", "/profile/edit"],
        "status": "completed",
    }


def _build_dashboard_runtime(data: HeartExecuteSchema) -> dict:
    return {
        "project_id": data.project_id,
        "engine": "dashboard",
        "feature": data.feature or "dashboard",
        "build_summary": "Heart prepared a rich mock runtime for the dashboard flow.",
        "prompt": data.prompt,
        "status": "completed",
        "layout": {
            "type": "dashboard",
            "sidebar": True,
            "topbar": True,
            "default_route": "/dashboard",
        },
        "navigation": [
            {"id": "overview", "label": "Overview", "path": "/dashboard", "icon": "layout-grid"},
            {"id": "analytics", "label": "Analytics", "path": "/dashboard/analytics", "icon": "bar-chart-3"},
            {"id": "projects", "label": "Projects", "path": "/dashboard/projects", "icon": "folder-kanban"},
            {"id": "settings", "label": "Settings", "path": "/dashboard/settings", "icon": "settings"},
        ],
        "pages": [
            {
                "id": "dashboard-home",
                "title": "Overview",
                "route": "/dashboard",
                "sections": ["hero", "kpi-grid", "charts", "recent-activity"],
            },
            {
                "id": "dashboard-analytics",
                "title": "Analytics",
                "route": "/dashboard/analytics",
                "sections": ["traffic-chart", "conversion-chart", "top-sources"],
            },
        ],
        "widgets": [
            {"id": "total-users", "type": "stat-card", "label": "Total Users", "value": "12,480", "trend": "+12.4%"},
            {"id": "active-projects", "type": "stat-card", "label": "Active Projects", "value": "318", "trend": "+5.1%"},
            {"id": "completion-rate", "type": "stat-card", "label": "Completion Rate", "value": "84%", "trend": "+2.3%"},
            {"id": "response-time", "type": "stat-card", "label": "Avg Response Time", "value": "1.2s", "trend": "-0.3s"},
        ],
        "charts": [
            {
                "id": "weekly-traffic",
                "type": "line",
                "title": "Weekly Traffic",
                "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "series": [{"name": "Visitors", "data": [120, 180, 160, 220, 260, 210, 290]}],
            },
            {
                "id": "conversion-breakdown",
                "type": "bar",
                "title": "Conversion Breakdown",
                "labels": ["Signup", "Onboarding", "Activation", "Upgrade"],
                "series": [{"name": "Rate", "data": [78, 61, 43, 18]}],
            },
        ],
        "recent_activity": [
            {"id": "act-1", "title": "New workspace created", "time": "5 mins ago", "type": "project"},
            {"id": "act-2", "title": "Profile engine deployed", "time": "18 mins ago", "type": "deployment"},
            {"id": "act-3", "title": "3 new users invited", "time": "1 hour ago", "type": "team"},
        ],
        "quick_actions": [
            {"id": "new-project", "label": "Create Project", "path": "/dashboard/projects/new"},
            {"id": "invite-team", "label": "Invite Team", "path": "/dashboard/team/invite"},
            {"id": "open-settings", "label": "Open Settings", "path": "/dashboard/settings"},
        ],
    }


def _build_generic_runtime(data: HeartExecuteSchema) -> dict:
    return {
        "project_id": data.project_id,
        "engine": data.requested_engine,
        "feature": data.feature or data.requested_engine,
        "build_summary": f"Heart prepared a mock runtime for the {data.requested_engine} flow.",
        "prompt": data.prompt,
        "screens": ["landing-page", "shared-layout"],
        "components": ["hero-section", "content-grid", "cta-block"],
        "status": "completed",
    }


def _build_mock_runtime(data: HeartExecuteSchema) -> dict:
    builders = {
        "auth": _build_auth_runtime,
        "profile": _build_profile_runtime,
        "dashboard": _build_dashboard_runtime,
    }
    return builders.get(data.requested_engine, _build_generic_runtime)(data)


def _serialize_runtime(runtime: RuntimeProject) -> RuntimeOutputSchema:
    return {
        "project_id": runtime.project_id,
        "status": runtime.status,
        "requested_engine": runtime.requested_engine,
        "feature": runtime.feature,
        "runtime_data": runtime.runtime_data,
        "updated_at": runtime.updated_at.isoformat() if runtime.updated_at else None,
    }


def execute_internal_task(data: HeartExecuteSchema) -> HeartExecuteOutputSchema:
    runtime_data = _build_mock_runtime(data)

    runtime, _ = RuntimeProject.objects.update_or_create(
        project_id=data.project_id,
        defaults={
            "user_id": data.user_id,
            "feature": data.feature,
            "requested_engine": data.requested_engine,
            "prompt": data.prompt,
            "metadata": data.metadata,
            "status": "completed",
            "runtime_data": runtime_data,
            "heart_payload": {
                "project_id": data.project_id,
                "user_id": data.user_id,
                "feature": data.feature,
                "requested_engine": data.requested_engine,
                "prompt": data.prompt,
                "metadata": data.metadata,
            },
            "last_executed_at": timezone.now(),
        },
    )

    return {
        "project_id": runtime.project_id,
        "status": runtime.status,
        "runtime_url": f"/runtime/{runtime.project_id}/",
        "runtime_data": runtime.runtime_data,
    }


def get_runtime(project_id: str) -> RuntimeOutputSchema:
    try:
        runtime = RuntimeProject.objects.get(project_id=project_id)
    except RuntimeProject.DoesNotExist:
        raise ValidationError({"project_id": "Runtime project not found."})

    return _serialize_runtime(runtime)
