"""
Models used by the QA agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.patches import CodePatch
from ai_team.shared.enums.qa import Severity

# ============================================================================
# QA Issue
# ============================================================================


class QAIssue(BaseModel):
    """
    Represents a quality issue detected during analysis.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    title: str

    description: str

    severity: Severity

    location: str | None = None

    recommendation: str


# ============================================================================
# Test Case
# ============================================================================


class TestCase(BaseModel):
    """
    Suggested test case.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    objective: str

    inputs: list[str] = Field(
        default_factory=list,
    )

    expected_behavior: str


# ============================================================================
# QA Summary
# ============================================================================


class QASummary(BaseModel):
    """
    High-level quality assessment.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    status: ReviewStatus

    score: float = Field(
        ge=0.0,
        le=10.0,
    )

    overview: str


# ============================================================================
# QA Result
# ============================================================================


class QAResult(BaseModel):
    """
    Result produced by the QA agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    summary: QASummary

    issues: list[QAIssue] = Field(
        default_factory=list,
    )

    suggested_tests: list[TestCase] = Field(
        default_factory=list,
    )

    code_patches: list[CodePatch] = Field(
        default_factory=list,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )