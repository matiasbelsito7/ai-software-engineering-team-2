"""
Review domain models.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ReviewSeverity(StrEnum):
    """
    Severity of a review issue.
    """

    INFO = "info"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


class ReviewIssue(BaseModel):
    """
    Represents a code review finding.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    title: str

    description: str

    severity: ReviewSeverity

    file: str | None = None

    line: int | None = None

    suggestion: str | None = None
