"""
Models used by the Backend agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.patches import (
    CodePatch,
    PatchOperation,
)


# ============================================================================
# Dependency
# ============================================================================


class DependencyChange(BaseModel):
    """
    Represents a dependency added or updated.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    package: str

    version: str | None = None

    reason: str


# ============================================================================
# Backend Result
# ============================================================================


class BackendResult(BaseModel):
    """
    Result produced by the Backend agent.
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

    assumptions: list[str] = Field(
        default_factory=list,
    )

    warnings: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )

    @property
    def created_files(self) -> list[CodePatch]:
        """
        Files created by the agent.
        """

        return [
            patch
            for patch in self.patches
            if patch.operation == PatchOperation.CREATE
        ]

    @property
    def modified_files(self) -> list[CodePatch]:
        """
        Files modified by the agent.
        """

        return [
            patch
            for patch in self.patches
            if patch.operation == PatchOperation.MODIFY
        ]

    @property
    def deleted_files(self) -> list[CodePatch]:
        """
        Files deleted by the agent.
        """

        return [
            patch
            for patch in self.patches
            if patch.operation == PatchOperation.DELETE
        ]