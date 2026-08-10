"""
Typed output produced by the Database Agent.
"""

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict, Field

from ai_team.agents.patches import (
    CodePatch,
    DependencyChange,
)


class DatabaseChange(BaseModel):
    """
    Database-specific schema or migration change.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    description: str

    migration: str | None = None


class DatabaseOutput(BaseModel):
    """
    Structured output produced by the Database Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: str

    changes: list[DatabaseChange] = Field(
        default_factory=list,
    )

    patches: list[CodePatch] = Field(
        default_factory=list,
    )

    dependencies: list[DependencyChange] = Field(
        default_factory=list,
    )

    migrations: list[str] = Field(
        default_factory=list,
    )

    notes: list[str] = Field(
        default_factory=list,
    )