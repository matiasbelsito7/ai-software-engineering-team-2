"""
Patch domain models.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class PatchOperation(StrEnum):
    """
    Supported file operations.
    """

    CREATE = "create"

    MODIFY = "modify"

    DELETE = "delete"


class CodePatch(BaseModel):
    """
    Represents a source code modification.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    path: str

    operation: PatchOperation

    content: str | None = None

    reason: str


class DependencyChange(BaseModel):
    """
    Represents a dependency modification.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    package: str

    version: str | None = None

    reason: str
