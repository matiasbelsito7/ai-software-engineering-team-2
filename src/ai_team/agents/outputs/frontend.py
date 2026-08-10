"""
Typed output produced by the Frontend Agent.
"""

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict, Field

from ai_team.agents.patches import (
    CodePatch,
    DependencyChange,
)


class UIComponent(BaseModel):
    """
    Frontend component proposed or modified by the agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    path: str

    description: str


class FrontendOutput(BaseModel):
    """
    Structured output produced by the Frontend Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: str

    components: list[UIComponent] = Field(
        default_factory=list,
    )

    patches: list[CodePatch] = Field(
        default_factory=list,
    )

    dependencies: list[DependencyChange] = Field(
        default_factory=list,
    )

    notes: list[str] = Field(
        default_factory=list,
    )