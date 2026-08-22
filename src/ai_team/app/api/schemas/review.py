"""
Code review API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ReviewInlineCommentSchema(BaseModel):
    """Inline comment schema."""

    model_config = ConfigDict(extra="forbid")

    file_path: str
    line_number: int
    severity: str
    category: str
    message: str
    suggestion: str | None = None
    code_snippet: str | None = None


class ReviewFileSchema(BaseModel):
    """File review schema."""

    model_config = ConfigDict(extra="forbid")

    file_path: str
    comments: list[ReviewInlineCommentSchema]
    summary: str | None = None
    score: float


class ReviewResultSchema(BaseModel):
    """Review result schema."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    files: list[ReviewFileSchema]
    overall_score: float
    summary: str
    approved: bool
    total_comments: int
    critical_issues: int


class ReviewRequestSchema(BaseModel):
    """Request for code review."""

    model_config = ConfigDict(extra="forbid")

    files: dict[str, str] = Field(
        ...,
        description="Dict of file_path -> content",
    )
    context: str | None = None
    focus_areas: list[str] | None = None
