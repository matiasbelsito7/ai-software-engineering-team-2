"""
Models used by the Documentation agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Documentation Section
# ============================================================================


class DocumentationSection(BaseModel):
    """
    A section of a generated document.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    title: str

    content: str


# ============================================================================
# Documentation File
# ============================================================================


class DocumentationFile(BaseModel):
    """
    Represents a generated documentation file.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    path: str

    description: str

    content: str


# ============================================================================
# Documentation Result
# ============================================================================


class DocumentationResult(BaseModel):
    """
    Result produced by the Documentation agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: str

    files: list[DocumentationFile] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )