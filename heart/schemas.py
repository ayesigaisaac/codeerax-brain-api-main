from dataclasses import dataclass, field
from typing import Any


@dataclass
class HeartExecuteSchema:
    project_id: str
    requested_engine: str
    prompt: str
    user_id: str | None = None
    feature: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HeartExecuteOutputSchema:
    project_id: str
    status: str
    runtime_url: str
    runtime_data: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeOutputSchema:
    project_id: str
    status: str
    requested_engine: str
    feature: str | None = None
    runtime_data: dict[str, Any] = field(default_factory=dict)
    updated_at: str | None = None

