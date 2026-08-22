"""
Unit tests for agent feedback system.
"""

from __future__ import annotations

from ai_team.agents.feedback import (
    AgentFeedback,
    FeedbackRecord,
    FeedbackResponse,
    FeedbackType,
)


class TestFeedbackType:
    def test_feedback_types(self) -> None:
        assert FeedbackType.CLARIFICATION == "clarification"
        assert FeedbackType.REVISION == "revision"
        assert FeedbackType.APPROVAL == "approval"
        assert FeedbackType.QUESTION == "question"


class TestAgentFeedback:
    def test_create_feedback(self) -> None:
        feedback = AgentFeedback(
            agent="backend",
            feedback_type=FeedbackType.CLARIFICATION,
            question="Which database should I use?",
            context="The task requires a database",
            options=["postgresql", "mysql", "sqlite"],
        )
        assert feedback.agent == "backend"
        assert feedback.feedback_type == FeedbackType.CLARIFICATION
        assert feedback.options == ["postgresql", "mysql", "sqlite"]

    def test_feedback_without_options(self) -> None:
        feedback = AgentFeedback(
            agent="reviewer",
            feedback_type=FeedbackType.APPROVAL,
            question="Please approve this design",
        )
        assert feedback.options is None


class TestFeedbackRecord:
    def test_create_record(self) -> None:
        record = FeedbackRecord(
            feedback_id="fb-123",
            task_id="task-456",
            agent="backend",
            feedback_type=FeedbackType.QUESTION,
            question="What format do you prefer?",
        )
        assert record.feedback_id == "fb-123"
        assert record.status == "pending"
        assert record.response is None

    def test_respond_to_record(self) -> None:
        record = FeedbackRecord(
            feedback_id="fb-123",
            task_id="task-456",
            agent="backend",
            feedback_type=FeedbackType.QUESTION,
            question="What format?",
        )
        record.response = "JSON"
        record.status = "responded"
        assert record.response == "JSON"
        assert record.status == "responded"


class TestFeedbackState:
    def test_empty_state(self) -> None:
        from ai_team.agents.feedback_state import FeedbackState

        state = FeedbackState()
        assert len(state.pending_feedback) == 0
        assert len(state.feedback_history) == 0

    def test_add_pending(self) -> None:
        from ai_team.agents.feedback_state import FeedbackState

        state = FeedbackState()
        record = FeedbackRecord(
            feedback_id="fb-1",
            task_id="task-1",
            agent="backend",
            feedback_type=FeedbackType.CLARIFICATION,
            question="Which one?",
        )
        state.add_pending(record)
        assert len(state.pending_feedback) == 1
        assert state.pending_feedback[0].feedback_id == "fb-1"

    def test_resolve_feedback(self) -> None:
        from ai_team.agents.feedback_state import FeedbackState

        state = FeedbackState()
        record = FeedbackRecord(
            feedback_id="fb-1",
            task_id="task-1",
            agent="backend",
            feedback_type=FeedbackType.CLARIFICATION,
            question="Which one?",
        )
        state.add_pending(record)

        resolved = state.resolve_feedback("fb-1", "Option A", "Option A")
        assert resolved is not None
        assert resolved.response == "Option A"
        assert resolved.selected_option == "Option A"
        assert resolved.status == "responded"
        assert len(state.pending_feedback) == 0
        assert len(state.feedback_history) == 1

    def test_resolve_nonexistent(self) -> None:
        from ai_team.agents.feedback_state import FeedbackState

        state = FeedbackState()
        resolved = state.resolve_feedback("nonexistent", "response")
        assert resolved is None

    def test_get_pending_filtered(self) -> None:
        from ai_team.agents.feedback_state import FeedbackState

        state = FeedbackState()
        record1 = FeedbackRecord(
            feedback_id="fb-1",
            task_id="task-1",
            agent="backend",
            feedback_type=FeedbackType.QUESTION,
            question="Q1?",
        )
        record2 = FeedbackRecord(
            feedback_id="fb-2",
            task_id="task-1",
            agent="frontend",
            feedback_type=FeedbackType.QUESTION,
            question="Q2?",
        )
        state.add_pending(record1)
        state.add_pending(record2)

        backend_pending = state.get_pending(agent="backend")
        assert len(backend_pending) == 1
        assert backend_pending[0].agent == "backend"

        all_pending = state.get_pending()
        assert len(all_pending) == 2


class TestFeedbackResponse:
    def test_create_response(self) -> None:
        response = FeedbackResponse(
            feedback_id="fb-123",
            response="Use PostgreSQL",
            selected_option="postgresql",
        )
        assert response.feedback_id == "fb-123"
        assert response.response == "Use PostgreSQL"
        assert response.selected_option == "postgresql"
