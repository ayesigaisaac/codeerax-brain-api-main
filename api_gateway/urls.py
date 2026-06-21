from django.urls import path, include
from engines.auth_engine.engine_config import register_auth_engine
from engines.dashboard_engine.engine_config import register_dashboard_engine
from engines.profile_engine.engine_config import register_profile_engine

urlpatterns = [
    # Register all auth engine URLs
    *register_auth_engine(),
    *register_dashboard_engine(),
    *register_profile_engine(),
]
