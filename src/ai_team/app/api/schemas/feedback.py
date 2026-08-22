"""
Feedback API schemas.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FeedbackRequestSchema(BaseModel):
    """Request to submit feedback for a task."""

    model_config = ConfigDict(extra="forbid")

    response: str = Field(..., min_length=1, max_length=10000)
    selected_option: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class FeedbackRecordSchema(BaseModel):
    """Feedback record response."""

    model_config = ConfigDict(extra="forbid")

    feedback_id: str
    task_id: str
    agent: str
    feedback_type: str
    question: str
    context: str | None = None
    options: list[str] | None = None
    response: str | None = None
    selected_option: str | None = None
    status: str
    created_at: str
    responded_at: str | None = None


class FeedbackListResponse(BaseModel):
    """List of feedback records."""

    model_config = ConfigDict(extra="forbid")

    pending: list[FeedbackRecordSchema]
    history: list[FeedbackRecordSchema]
    total_pending: int
    total_history: int
