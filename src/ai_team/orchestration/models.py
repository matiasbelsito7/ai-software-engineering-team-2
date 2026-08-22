"""
Multi-task orchestration models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(StrEnum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class OrchestrationTask(BaseModel):
    """A task in the orchestration pipeline."""

    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    task_prompt: str = Field(..., min_length=1)
    system_prompt: str | None = None
    dependencies: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=0, ge=0, le=10)
    timeout_seconds: int | None = None
    retry_count: int = 0
    max_retries: int = 3


class TaskExecutionState(BaseModel):
    """State of a task execution."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    duration_seconds: float | None = None
    attempt: int = 1


class PipelineStage(BaseModel):
    """A stage in the orchestration pipeline."""

    model_config = ConfigDict(extra="forbid")

    stage_id: str
    name: str
    tasks: list[str]  # Task IDs
    parallel: bool = True  # Run tasks in parallel within stage


class OrchestrationPlan(BaseModel):
    """Complete orchestration plan."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    name: str
    description: str | None = None
    tasks: dict[str, OrchestrationTask] = Field(default_factory=dict)
    stages: list[PipelineStage] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def get_task(self, task_id: str) -> OrchestrationTask | None:
        return self.tasks.get(task_id)

    def get_dependencies(self, task_id: str) -> list[str]:
        task = self.tasks.get(task_id)
        return task.dependencies if task else []

    def validate_dependencies(self) -> list[str]:
        """Validate all dependencies exist. Returns list of errors."""
        errors = [
            f"Task '{task_id}' depends on non-existent task '{dep}'"
            for task_id, task in self.tasks.items()
            for dep in task.dependencies
            if dep not in self.tasks
        ]
        return errors

    def topological_sort(self) -> list[list[str]]:
        """Sort tasks into execution stages based on dependencies."""
        in_degree: dict[str, int] = dict.fromkeys(self.tasks, 0)
        for task in self.tasks.values():
            for dep in task.dependencies:
                if dep in in_degree:
                    in_degree[task.task_id] += 1

        stages: list[list[str]] = []
        remaining = set(self.tasks.keys())

        while remaining:
            # Find tasks with no remaining dependencies
            ready = [t for t in remaining if in_degree[t] == 0]
            if not ready:
                errors = self.validate_dependencies()
                raise ValueError(f"Circular dependency detected: {errors}")

            stages.append(sorted(ready))
            for task_id in ready:
                remaining.remove(task_id)
                # Update in-degree for dependent tasks
                for other_id in remaining:
                    other = self.tasks[other_id]
                    if task_id in other.dependencies:
                        in_degree[other_id] -= 1

        return stages


class OrchestrationResult(BaseModel):
    """Result of orchestrating multiple tasks."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    status: TaskStatus
    task_states: dict[str, TaskExecutionState] = Field(default_factory=dict)
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    results: dict[str, Any] = Field(default_factory=dict)
    started_at: str | None = None
    completed_at: str | None = None
    duration_seconds: float | None = None
