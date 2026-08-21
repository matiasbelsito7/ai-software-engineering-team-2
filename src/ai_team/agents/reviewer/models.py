"""
Models used by the Reviewer agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from ai_team.agents.patches import CodePatch
    from ai_team.shared.enums.qa import Severity
    from ai_team.shared.enums.review import (
        ReviewCategory,
        ReviewStatus,
    )

# ============================================================================
# Review Finding
# ============================================================================


class ReviewFinding(BaseModel):
    """
    A single finding produced during the review.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    title: str

    description: str

    severity: Severity

    category: ReviewCategory

    recommendation: str

    location: str | None = None


# ============================================================================
# Review Summary
# ============================================================================


class ReviewSummary(BaseModel):
    """
    High-level review summary.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    status: ReviewStatus

    approved: bool

    score: float = Field(
        ge=0.0,
        le=10.0,
    )

    summary: str


# ============================================================================
# Reviewer Result
# ============================================================================


class ReviewerResult(BaseModel):
    """
    Result produced by the Reviewer agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    review: ReviewSummary

    findings: list[ReviewFinding] = Field(
        default_factory=list,
    )

    reviewed_patches: list[CodePatch] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )
