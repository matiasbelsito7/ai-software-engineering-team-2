"""
Agent feedback models for inter-agent communication.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FeedbackType(StrEnum):
    """Types of feedback an agent can request."""

    CLARIFICATION = "clarification"
    REVISION = "revision"
    APPROVAL = "approval"
    QUESTION = "question"


class AgentFeedback(BaseModel):
    """Feedback request from an agent during execution."""

    model_config = ConfigDict(extra="forbid")

    agent: str = Field(..., description="Name of the agent requesting feedback")
    feedback_type: FeedbackType
    question: str = Field(..., min_length=1, max_length=5000)
    context: str | None = Field(
        default=None,
        description="Additional context about why feedback is needed",
    )
    options: list[str] | None = Field(
        default=None,
        description="Suggested options for the user to choose from",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class FeedbackResponse(BaseModel):
    """User's response to an agent's feedback request."""

    model_config = ConfigDict(extra="forbid")

    feedback_id: str = Field(..., description="ID of the feedback being responded to")
    response: str = Field(..., min_length=1, max_length=10000)
    selected_option: str | None = Field(
        default=None,
        description="If options were provided, which one was selected",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class FeedbackRecord(BaseModel):
    """Record of a feedback interaction."""

    model_config = ConfigDict(extra="forbid")

    feedback_id: str
    task_id: str
    agent: str
    feedback_type: FeedbackType
    question: str
    context: str | None = None
    options: list[str] | None = None
    response: str | None = None
    selected_option: str | None = None
    status: str = "pending"  # pending, responded, timeout
    created_at: str = Field(
        default_factory=lambda: __import__("datetime").datetime.utcnow().isoformat()
    )
    responded_at: str | None = None
