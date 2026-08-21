"""
Models used by the Architect agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ============================================================================
# Module
# ============================================================================


class ModuleDesign(BaseModel):
    """
    Represents a software module.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    description: str

    responsibilities: list[str] = Field(
        default_factory=list,
    )

    dependencies: list[str] = Field(
        default_factory=list,
    )


# ============================================================================
# Interface
# ============================================================================


class InterfaceDesign(BaseModel):
    """
    Represents a public interface.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    description: str

    owner: str


# ============================================================================
# Architectural Decision
# ============================================================================


class ArchitecturalDecision(BaseModel):
    """
    Represents an architectural or technology decision.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    title: str

    decision: str

    rationale: str

    consequences: list[str] = Field(
        default_factory=list,
    )


# ============================================================================
# Architecture Design
# ============================================================================


class ArchitectureDesign(BaseModel):
    """
    Complete architecture produced by the Architect agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    project_summary: str

    architecture_style: str

    modules: list[ModuleDesign] = Field(
        default_factory=list,
    )

    interfaces: list[InterfaceDesign] = Field(
        default_factory=list,
    )

    technology_decisions: list[ArchitecturalDecision] = Field(
        default_factory=list,
    )

    assumptions: list[str] = Field(
        default_factory=list,
    )

    risks: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )

    @property
    def total_modules(self) -> int:
        """
        Number of modules.
        """

        return len(self.modules)

    @property
    def total_interfaces(self) -> int:
        """
        Number of public interfaces.
        """

        return len(self.interfaces)
