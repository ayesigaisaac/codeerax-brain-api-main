import logging
import uuid

from .heart_client import dispatch_to_heart
from .schemas import BrainBuildOutputSchema, BrainBuildSchema
from heart.schemas import HeartExecuteSchema
from engines.auth_engine.builder import build_auth_engine
from .build_store import set_task, update_task


ENGINE_KEYWORDS = {
    "auth": ("auth", "login", "register", "password", "signup"),
    "profile": ("profile", "bio", "avatar", "account"),
    "dashboard": ("dashboard", "analytics", "overview", "stats", "metric", "chart", "insight", "activity"),
}


def _decide_engine(data: BrainBuildSchema) -> tuple[str, str]:
    if data.requested_engine:
        return (
            data.requested_engine,
            f"Used requested_engine '{data.requested_engine}' from the frontend request.",
        )

    match_text = f"{data.feature or ''} {data.prompt}".lower()

    for engine_name, keywords in ENGINE_KEYWORDS.items():
        if any(keyword in match_text for keyword in keywords):
            return (
                engine_name,
                f"Brain matched the request to '{engine_name}' based on feature/prompt keywords.",
            )

    return (
        "generic",
        "Brain could not find a strong engine match, so it routed the task to a generic builder.",
    )


def build_project(data: BrainBuildSchema) -> BrainBuildOutputSchema:
    project_id = data.project_id or str(uuid.uuid4())
    requested_engine, decision_reason = _decide_engine(data)
    # If the chosen engine is "auth", use the auth engine builder to prepare
    # a Heart payload and additional metadata (task_id, progress, config, etc.).
    if requested_engine == "auth":
        # Collect possible engine-specific inputs from metadata
        auth_input = {
            "app_name": data.metadata.get("app_name") if isinstance(data.metadata, dict) else None,
            "theme": data.metadata.get("theme") if isinstance(data.metadata, dict) else None,
            "config": data.metadata.get("config") if isinstance(data.metadata, dict) else None,
            "project_id": project_id,
            "user_id": data.user_id,
            "prompt": data.prompt,
        }

        builder_result = build_auth_engine(auth_input)
        heart_execute = builder_result.get("heart_execute")

        # Persist initial task state so clients can poll for progress
        set_task(builder_result.get("task_id"), {
            "task_id": builder_result.get("task_id"),
            "project_id": builder_result.get("project_id"),
            "status": builder_result.get("status"),
            "progress": builder_result.get("progress"),
            "progress_history": builder_result.get("progress_history"),
            "message": builder_result.get("message"),
            "config": builder_result.get("config"),
            "engines": builder_result.get("engines"),
        })

        # Move the task into an active state before Heart dispatch.
        update_task(builder_result.get("task_id"), {
            "status": "in_progress",
            "progress": 30,
            "message": "Auth engine build is running in Heart.",
        })

        try:
            heart_response = dispatch_to_heart(heart_execute)
        except Exception:
            # Log the raw exception server-side to preserve debug info
            logging.exception("Exception during Heart dispatch")

            # Sanitize error details to avoid leaking internal system information
            sanitized_error = "Heart dispatch failed"

            # Update stored task marking failure and include heart fields
            update_task(builder_result.get("task_id"), {
                "status": "failed",
                "progress": 100,
                "message": "Auth engine build failed while dispatching to Heart.",
                "error_message": sanitized_error,
                "heart_status": "failed",
                "runtime_url": "",
            })

            return {
                "project_id": project_id,
                "requested_engine": requested_engine,
                "decision_reason": decision_reason,
                "heart_status": "failed",
                "runtime_url": "",
                "message": "Auth engine build failed while dispatching to Heart.",
                "task_id": builder_result.get("task_id"),
                "status": "failed",
                "progress": 100,
                "progress_history": builder_result.get("progress_history"),
                "config": builder_result.get("config"),
                "engines": builder_result.get("engines"),
            }

        # Update stored task with Heart response
        update_task(builder_result.get("task_id"), {
            "status": "completed",
            "progress": 100,
            "message": "Auth engine build completed successfully.",
            "heart_status": heart_response.get("status"),
            "runtime_url": heart_response.get("runtime_url"),
        })

        # Compose response merging existing Brain output with builder metadata
        response = {
            "project_id": project_id,
            "requested_engine": requested_engine,
            "decision_reason": decision_reason,
            "heart_status": heart_response.get("status"),
            "runtime_url": heart_response.get("runtime_url"),
            "message": builder_result.get("message", "Brain processed the build request and dispatched it to Heart."),
            # New fields for engine flow visibility
            "task_id": builder_result.get("task_id"),
            "status": builder_result.get("status"),
            "progress": builder_result.get("progress"),
            "progress_history": builder_result.get("progress_history"),
            "config": builder_result.get("config"),
            "engines": builder_result.get("engines"),
        }

        return response

    # Generic flow for other engines
    task_id = str(uuid.uuid4())
    set_task(task_id, {
        "task_id": task_id,
        "project_id": project_id,
        "requested_engine": requested_engine,
        "status": "in_progress",
        "progress": 0,
        "progress_history": [],
        "message": f"Build request queued for {requested_engine} engine.",
        "config": {},
        "engines": [requested_engine],
        "heart_status": "",
        "runtime_url": "",
    })

    try:
        heart_response = dispatch_to_heart(
            HeartExecuteSchema(
                project_id=project_id,
                user_id=data.user_id,
                feature=data.feature,
                requested_engine=requested_engine,
                prompt=data.prompt,
                metadata=data.metadata,
            )
        )
    except Exception:
        logging.exception("Exception during Heart dispatch (generic flow)")

        update_task(task_id, {
            "status": "failed",
            "progress": 100,
            "message": "Build request failed while dispatching to Heart.",
            "heart_status": "failed",
            "runtime_url": "",
        })

        return {
            "project_id": project_id,
            "requested_engine": requested_engine,
            "decision_reason": decision_reason,
            "heart_status": "failed",
            "runtime_url": "",
            "message": "Build request failed while dispatching to Heart.",
            "task_id": task_id,
            "status": "failed",
        }

    update_task(task_id, {
        "status": "completed",
        "progress": 100,
        "message": "Brain processed the build request and dispatched it to Heart.",
        "heart_status": heart_response["status"],
        "runtime_url": heart_response["runtime_url"],
    })

    return {
        "project_id": project_id,
        "requested_engine": requested_engine,
        "decision_reason": decision_reason,
        "heart_status": heart_response["status"],
        "runtime_url": heart_response["runtime_url"],
        "message": "Brain processed the build request and dispatched it to Heart.",
        "task_id": task_id,
        "status": "completed",
    }

