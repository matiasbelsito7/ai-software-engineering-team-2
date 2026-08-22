"""
Feedback state for agent-user interactions.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.feedback import FeedbackRecord  # noqa: TC001


class FeedbackState(BaseModel):
    """
    Feedback interactions between agents and users.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    pending_feedback: list[FeedbackRecord] = Field(
        default_factory=list,
    )

    feedback_history: list[FeedbackRecord] = Field(
        default_factory=list,
    )

    def add_pending(self, record: FeedbackRecord) -> None:
        """Add a feedback request to pending queue."""
        self.pending_feedback.append(record)

    def resolve_feedback(
        self, feedback_id: str, response: str, selected_option: str | None = None
    ) -> FeedbackRecord | None:
        """Resolve a pending feedback request."""
        for i, record in enumerate(self.pending_feedback):
            if record.feedback_id == feedback_id:
                resolved = self.pending_feedback.pop(i)
                resolved.response = response
                resolved.selected_option = selected_option
                resolved.status = "responded"
                self.feedback_history.append(resolved)
                return resolved
        return None

    def get_pending(self, agent: str | None = None) -> list[FeedbackRecord]:
        """Get pending feedback requests, optionally filtered by agent."""
        if agent is None:
            return list(self.pending_feedback)
        return [r for r in self.pending_feedback if r.agent == agent]
