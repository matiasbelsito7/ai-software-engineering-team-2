"""
Models used by the Planner agent.
"""

from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.shared.enums import AgentCapability


# ============================================================================
# Planning Task
# ============================================================================


class PlanningTask(BaseModel):
    """
    Single executable task produced by the planner.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(default_factory=uuid4)

    title: str

    description: str

    capability: AgentCapability

    depends_on: list[UUID] = Field(default_factory=list)

    estimated_tokens: int | None = None

    estimated_cost: float | None = None

    metadata: dict[str, object] = Field(default_factory=dict)


# ============================================================================
# Planning Phase
# ============================================================================


class PlanningPhase(BaseModel):
    """
    Group of tasks that may execute together.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    tasks: list[PlanningTask] = Field(default_factory=list)


# ============================================================================
# Execution Plan
# ============================================================================


class ExecutionPlan(BaseModel):
    """
    Complete execution plan produced by the Planner.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    objective: str

    summary: str

    phases: list[PlanningPhase] = Field(default_factory=list)

    estimated_tokens: int | None = None

    estimated_cost: float | None = None

    metadata: dict[str, object] = Field(default_factory=dict)

    @property
    def tasks(self) -> list[PlanningTask]:
        """
        Return every task in execution order.
        """
        return [
            task
            for phase in self.phases
            for task in phase.tasks
        ]

    @property
    def total_tasks(self) -> int:
        """
        Total number of tasks.
        """
        return len(self.tasks)

    @property
    def capabilities(self) -> set[AgentCapability]:
        """
        Capabilities required by the plan.
        """
        return {
            task.capability
            for task in self.tasks
        }