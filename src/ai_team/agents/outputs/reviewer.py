"""
Typed output produced by the Reviewer Agent.
"""

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from ai_team.agents.review import ReviewIssue


class ReviewerOutput(BaseModel):
    """
    Structured output produced by the Reviewer Agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    approved: bool

    summary: str

    issues: list[ReviewIssue] = Field(
        default_factory=list,
    )

    required_changes: list[str] = Field(
        default_factory=list,
    )

    recommendations: list[str] = Field(
        default_factory=list,
    )