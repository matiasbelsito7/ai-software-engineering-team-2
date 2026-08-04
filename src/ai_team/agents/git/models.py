"""
Models used by the Git agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.models import CodePatch
from ai_team.shared.enums.git import (
    GitChangeType,
    GitOperation,
)


# ============================================================================
# Git File Change
# ============================================================================


class GitFileChange(BaseModel):
    """
    Represents a file modified by the Git agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    path: str

    change_type: GitChangeType

    description: str


# ============================================================================
# Commit
# ============================================================================


class GitCommit(BaseModel):
    """
    Represents a commit to be created.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    message: str

    description: str | None = None


# ============================================================================
# Git Action
# ============================================================================


class GitAction(BaseModel):
    """
    A Git operation requested by the agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    operation: GitOperation

    commit: GitCommit | None = None

    files: list[GitFileChange] = Field(
        default_factory=list,
    )


# ============================================================================
# Git Result
# ============================================================================


class GitResult(BaseModel):
    """
    Result produced by the Git agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    actions: list[GitAction] = Field(
        default_factory=list,
    )

    code_patches: list[CodePatch] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )