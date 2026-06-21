from typing import Any, Dict, Optional

from brain.models import BuildTask


def set_task(task_id: str, data: Dict[str, Any]) -> None:
    fields = {k: v for k, v in data.items() if k != "task_id"}
    BuildTask.objects.update_or_create(task_id=task_id, defaults=fields)


def update_task(task_id: str, updates: Dict[str, Any]) -> None:
    try:
        task = BuildTask.objects.get(task_id=task_id)
    except BuildTask.DoesNotExist:
        return
    for key, value in updates.items():
        setattr(task, key, value)
    task.save(update_fields=list(updates.keys()) + ["updated_at"])


def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    try:
        task = BuildTask.objects.get(task_id=task_id)
    except BuildTask.DoesNotExist:
        return None
    return {
        "task_id": str(task.task_id),
        "project_id": task.project_id,
        "user_id": task.user_id,
        "status": task.status,
        "progress": task.progress,
        "progress_history": task.progress_history,
        "message": task.message,
        "config": task.config,
        "engines": task.engines,
        "heart_status": task.heart_status,
        "runtime_url": task.runtime_url,
    }


def clear_all() -> None:
    BuildTask.objects.all().delete()
