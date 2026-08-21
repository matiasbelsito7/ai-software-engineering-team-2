"""
Models used by the Frontend agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ai_team.agents.patches import CodePatch
    from ai_team.shared.enums.frontend import (
        InteractionType,
        ResponsiveBreakpoint,
        UIComponentType,
    )

# ============================================================================
# UI Interaction
# ============================================================================


class UIInteraction(BaseModel):
    """
    User interaction supported by a component.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    type: InteractionType

    description: str


# ============================================================================
# UI Component
# ============================================================================


class UIComponent(BaseModel):
    """
    Frontend component produced by the agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    component_type: UIComponentType

    path: str

    description: str

    interactions: list[UIInteraction] = Field(
        default_factory=list,
    )

    breakpoints: list[ResponsiveBreakpoint] = Field(
        default_factory=list,
    )


# ============================================================================
# Frontend Summary
# ============================================================================


class FrontendSummary(BaseModel):
    """
    High-level frontend implementation summary.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: str

    components: int

    pages: int


# ============================================================================
# Frontend Result
# ============================================================================


class FrontendResult(BaseModel):
    """
    Result produced by the Frontend agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    frontend: FrontendSummary

    ui_components: list[UIComponent] = Field(
        default_factory=list,
    )

    code_patches: list[CodePatch] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )
