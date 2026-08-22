"""
Orchestration API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OrchestrationTaskSchema(BaseModel):
    """Task schema for orchestration."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    name: str
    description: str | None = None
    task_prompt: str
    system_prompt: str | None = None
    dependencies: list[str] = Field(default_factory=list)
    priority: int = 0
    timeout_seconds: int | None = None
    max_retries: int = 3


class OrchestrationPlanSchema(BaseModel):
    """Orchestration plan schema."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    name: str
    description: str | None = None
    tasks: list[OrchestrationTaskSchema]
    metadata: dict[str, object] = Field(default_factory=dict)


class OrchestrationPlanResponse(BaseModel):
    """Response for plan creation."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    status: str
    total_tasks: int
    execution_order: list[list[str]]


class TaskExecutionStateSchema(BaseModel):
    """Task execution state."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    status: str
    result: object = None
    error: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    duration_seconds: float | None = None
    attempt: int = 1


class OrchestrationResultSchema(BaseModel):
    """Orchestration result schema."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    status: str
    task_states: dict[str, TaskExecutionStateSchema]
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    results: dict[str, object]
    started_at: str | None = None
    completed_at: str | None = None
    duration_seconds: float | None = None


class OrchestrationListResponse(BaseModel):
    """List of orchestration plans."""

    model_config = ConfigDict(extra="forbid")

    plans: list[OrchestrationPlanSchema]
    total: int
