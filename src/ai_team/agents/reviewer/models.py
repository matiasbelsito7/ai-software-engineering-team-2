"""
Models used by the Reviewer agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.models import CodePatch


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