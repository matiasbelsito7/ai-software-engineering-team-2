"""
Typed output produced by the Documentation Agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DocumentationFile(BaseModel):
    """
    Documentation artifact produced by the Documentation Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    path: str

    content: str

    description: str


class DocumentationOutput(BaseModel):
    """
    Structured output produced by the Documentation Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: str

    files: list[DocumentationFile] = Field(
        default_factory=list,
    )

    updated_sections: list[str] = Field(
        default_factory=list,
    )

    recommendations: list[str] = Field(
        default_factory=list,
    )