"""
Typed output produced by the DevOps Agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.patches import (
    CodePatch,
    DependencyChange,
)


class DevOpsOutput(BaseModel):
    """
    Structured output produced by the DevOps Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: str

    patches: list[CodePatch] = Field(
        default_factory=list,
    )

    dependencies: list[DependencyChange] = Field(
        default_factory=list,
    )

    commands: list[str] = Field(
        default_factory=list,
    )

    environment_changes: list[str] = Field(
        default_factory=list,
    )

    notes: list[str] = Field(
        default_factory=list,
    )