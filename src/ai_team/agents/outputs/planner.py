"""
Typed output produced by the Planner Agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PlanStep(BaseModel):
    """
    Single step in an implementation plan.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: int

    title: str

    description: str

    agent: str

    dependencies: list[int] = Field(
        default_factory=list,
    )


class PlannerOutput(BaseModel):
    """
    Structured output produced by the Planner Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    goal: str

    summary: str

    steps: list[PlanStep] = Field(
        default_factory=list,
    )

    assumptions: list[str] = Field(
        default_factory=list,
    )

    risks: list[str] = Field(
        default_factory=list,
    )