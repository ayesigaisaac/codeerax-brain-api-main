from dataclasses import dataclass, field
from typing import Any


@dataclass
class BrainBuildSchema:
    prompt: str
    project_id: str | None = None
    user_id: str | None = None
    feature: str | None = None
    requested_engine: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BrainBuildOutputSchema:
    project_id: str
    requested_engine: str
    decision_reason: str
    heart_status: str
    runtime_url: str
    message: str


# ---------------------------
# Auth Engine Build Input
# ---------------------------
@dataclass
class AuthEngineBuildSchema:
    app_name: str
    theme: dict[str, Any] | None = None
    config: dict[str, Any] = field(default_factory=dict)
    project_id: str | None = None
    user_id: str | None = None

