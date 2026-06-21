import threading
from typing import Any, Dict

_lock = threading.Lock()
_store: Dict[str, Dict[str, Any]] = {}


def set_task(task_id: str, data: Dict[str, Any]) -> None:
    with _lock:
        _store[task_id] = data.copy()


def update_task(task_id: str, updates: Dict[str, Any]) -> None:
    with _lock:
        if task_id in _store:
            _store[task_id].update(updates)


def get_task(task_id: str):
    with _lock:
        return _store.get(task_id)


def clear_all():
    with _lock:
        _store.clear()
