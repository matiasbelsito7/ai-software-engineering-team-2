"""
Code review models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ReviewSeverity(StrEnum):
    """Review issue severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ReviewCategory(StrEnum):
    """Review categories."""

    BUG = "bug"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    DOCUMENTATION = "documentation"
    TEST = "test"
    ARCHITECTURE = "architecture"


class InlineComment(BaseModel):
    """An inline comment on a specific line of code."""

    model_config = ConfigDict(extra="forbid")

    file_path: str = Field(..., min_length=1)
    line_number: int = Field(..., ge=1)
    severity: ReviewSeverity
    category: ReviewCategory
    message: str = Field(..., min_length=1, max_length=2000)
    suggestion: str | None = Field(
        default=None,
        description="Suggested fix for the issue",
    )
    code_snippet: str | None = Field(
        default=None,
        description="The problematic code snippet",
    )


class FileReview(BaseModel):
    """Review results for a single file."""

    model_config = ConfigDict(extra="forbid")

    file_path: str
    comments: list[InlineComment] = Field(default_factory=list)
    summary: str | None = None
    score: float = Field(default=1.0, ge=0.0, le=1.0)

    @property
    def issue_count(self) -> int:
        return len(self.comments)

    @property
    def has_critical(self) -> bool:
        return any(c.severity == ReviewSeverity.CRITICAL for c in self.comments)


class ReviewResult(BaseModel):
    """Complete code review result."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    files: list[FileReview] = Field(default_factory=list)
    overall_score: float = Field(default=1.0, ge=0.0, le=1.0)
    summary: str = ""
    approved: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def total_comments(self) -> int:
        return sum(f.issue_count for f in self.files)

    @property
    def critical_issues(self) -> int:
        return sum(
            1 for f in self.files for c in f.comments if c.severity == ReviewSeverity.CRITICAL
        )

    def calculate_score(self) -> None:
        """Calculate overall score based on issues."""
        if not self.files:
            self.overall_score = 1.0
            self.approved = True
            return

        issue_weight: float = 0.0

        weights = {
            ReviewSeverity.INFO: 0.01,
            ReviewSeverity.WARNING: 0.05,
            ReviewSeverity.ERROR: 0.15,
            ReviewSeverity.CRITICAL: 0.5,
        }

        for f in self.files:
            for c in f.comments:
                issue_weight += weights.get(c.severity, 0.1)

        penalty = min(issue_weight, 1.0)
        self.overall_score = max(0.0, 1.0 - penalty)
        self.approved = self.overall_score >= 0.7 and self.critical_issues == 0


class ReviewRequest(BaseModel):
    """Request for code review."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    files: dict[str, str] = Field(
        ...,
        description="Dict of file_path -> content",
    )
    context: str | None = Field(
        default=None,
        description="Additional context for the review",
    )
    focus_areas: list[ReviewCategory] | None = None
