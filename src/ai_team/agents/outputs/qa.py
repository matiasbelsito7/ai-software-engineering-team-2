"""
Typed output produced by the QA Agent.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.review import ReviewIssue


class TestResult(BaseModel):
    """
    Result of an individual test or test group.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    passed: bool

    duration_ms: float | None = None

    output: str | None = None

    error: str | None = None


class QAOutput(BaseModel):
    """
    Structured output produced by the QA Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    passed: bool

    summary: str

    tests: list[TestResult] = Field(
        default_factory=list,
    )

    issues: list[ReviewIssue] = Field(
        default_factory=list,
    )

    recommendations: list[str] = Field(
        default_factory=list,
    )