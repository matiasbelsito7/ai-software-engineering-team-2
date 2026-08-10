"""
Typed output produced by the Backend Agent.
"""

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from ai_team.agents.patches import (
    CodePatch,
    DependencyChange,
)


class BackendOutput(BaseModel):
    """
    Structured output produced by the Backend Agent.
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

    tests: list[CodePatch] = Field(
        default_factory=list,
    )

    notes: list[str] = Field(
        default_factory=list,
    )