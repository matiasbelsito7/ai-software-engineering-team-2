"""
API request and response schemas.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# =====================================================================
# Request schemas
# =====================================================================


class CreateTaskRequest(BaseModel):
    """Request body for POST /tasks."""

    model_config = ConfigDict(extra="forbid")

    task: str = Field(
        ...,
        min_length=1,
        max_length=10_000,
        description="Natural-language task description.",
    )

    system_prompt: str | None = Field(
        default=None,
        max_length=50_000,
        description="Optional system prompt override.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary metadata attached to the task.",
    )


# =====================================================================
# Response schemas
# =====================================================================


class HealthResponse(BaseModel):
    """Health check response."""

    model_config = ConfigDict(extra="forbid")

    status: str = "ok"

    version: str = ""

    uptime_seconds: float = 0.0


class AgentResultResponse(BaseModel):
    """Single agent result inside a task response."""

    model_config = ConfigDict(from_attributes=True)

    agent: str = ""

    success: bool = False

    output: Any = None

    message: str | None = None

    next_agent: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    """Response body for a task."""

    model_config = ConfigDict(extra="forbid")

    task_id: str

    status: str

    created_at: str | None = None

    updated_at: str | None = None

    results: list[AgentResultResponse] = Field(
        default_factory=list,
    )

    files: dict[str, str] = Field(
        default_factory=dict,
    )

    error: str | None = None


class TaskListResponse(BaseModel):
    """Paginated task list response."""

    model_config = ConfigDict(extra="forbid")

    tasks: list[TaskResponse] = Field(
        default_factory=list,
    )

    total: int = 0

    offset: int = 0

    limit: int = 0


class ErrorResponse(BaseModel):
    """Standard error response."""

    model_config = ConfigDict(extra="forbid")

    detail: str

    error_code: str | None = None


# =====================================================================
# WebSocket schemas
# =====================================================================


class TaskProgressMessage(BaseModel):
    """WebSocket message for task progress updates."""

    model_config = ConfigDict(extra="forbid")

    task_id: str

    status: str

    agent: str | None = None

    message: str | None = None

    progress: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Progress fraction (0.0 to 1.0).",
    )

    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
    )


class TaskCompleteMessage(BaseModel):
    """WebSocket message sent when a task completes."""

    model_config = ConfigDict(extra="forbid")

    task_id: str

    status: str

    results: list[AgentResultResponse] = Field(
        default_factory=list,
    )

    files: dict[str, str] = Field(
        default_factory=dict,
    )

    error: str | None = None

    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
    )


class TaskErrorMessage(BaseModel):
    """WebSocket message sent when a task fails."""

    model_config = ConfigDict(extra="forbid")

    task_id: str

    error: str

    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
    )
