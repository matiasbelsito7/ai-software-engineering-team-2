"""
Typed output produced by the Architect Agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ArchitectureComponent(BaseModel):
    """
    Component proposed by the Architect Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    responsibility: str

    path: str

    dependencies: list[str] = Field(
        default_factory=list,
    )


class ArchitectureDecision(BaseModel):
    """
    Architectural decision made by the Architect Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    decision: str

    rationale: str

    alternatives: list[str] = Field(
        default_factory=list,
    )


class ArchitectOutput(BaseModel):
    """
    Structured output produced by the Architect Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: str

    components: list[ArchitectureComponent] = Field(
        default_factory=list,
    )

    decisions: list[ArchitectureDecision] = Field(
        default_factory=list,
    )

    constraints: list[str] = Field(
        default_factory=list,
    )

    risks: list[str] = Field(
        default_factory=list,
    )