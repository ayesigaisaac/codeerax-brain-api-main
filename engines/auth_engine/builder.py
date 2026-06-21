import uuid
from typing import Any

from heart.schemas import HeartExecuteSchema


def _merge_configs(default: dict[str, Any], override: dict[str, Any] | None) -> dict[str, Any]:
    result = default.copy()
    if not override:
        return result
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = {**result.get(k, {}), **v}
        else:
            result[k] = v
    return result


def build_auth_engine(input_data) -> dict:
    """Build wrapper for the Auth engine.

    Accepts either a dict or an object with attributes:
      - app_name (str)
      - theme (dict) optional
      - config (dict) optional
      - project_id (str) optional
      - user_id (str) optional

    Returns a dict with keys:
      - task_id, status, progress, message, config, engines, heart_execute

    The `heart_execute` value is a `HeartExecuteSchema` instance ready to dispatch.
    """
    # Normalize input
    if isinstance(input_data, dict):
        app_name = input_data.get("app_name")
        theme = input_data.get("theme")
        config = input_data.get("config") or {}
        project_id = input_data.get("project_id")
        user_id = input_data.get("user_id")
        prompt = input_data.get("prompt") or f"Build Auth Engine for {app_name}"
    else:
        app_name = getattr(input_data, "app_name", None)
        theme = getattr(input_data, "theme", None)
        config = getattr(input_data, "config", None) or {}
        project_id = getattr(input_data, "project_id", None)
        user_id = getattr(input_data, "user_id", None)
        prompt = getattr(input_data, "prompt", f"Build Auth Engine for {app_name}")

    task_id = str(uuid.uuid4())
    project_id = project_id or str(uuid.uuid4())

    default_config = {
        "password_policy": {"min_length": 8, "require_special": False},
        "allow_signup": True,
        "preseed_admin": False,
    }

    merged_config = _merge_configs(default_config, config)

    engines = ["auth"]
    if merged_config.get("include_profile"):
        engines.append("profile")

    # Simulated progress steps (frontend may choose to consume progress_history)
    progress_history = [30, 70, 100]

    # Prepare Heart payload
    heart_execute = HeartExecuteSchema(
        project_id=project_id,
        requested_engine="auth",
        prompt=prompt,
        user_id=user_id,
        feature="auth_build",
        metadata={
            "task_id": task_id,
            "app_name": app_name,
            "theme": theme,
            "config": merged_config,
            "progress_history": progress_history,
            "engines": engines,
        },
    )

    result = {
        "task_id": task_id,
        "status": "queued",
        "progress": 0,
        "progress_history": progress_history,
        "message": "Auth engine build queued for Heart execution.",
        "config": merged_config,
        "engines": engines,
        "project_id": project_id,
        "heart_execute": heart_execute,
    }

    return result
