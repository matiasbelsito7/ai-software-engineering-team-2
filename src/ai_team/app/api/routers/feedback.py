"""
Feedback router - manage agent feedback interactions.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Request

from ai_team.app.api.exceptions.errors import NotFoundError
from ai_team.app.api.schemas.feedback import (
    FeedbackListResponse,
    FeedbackRecordSchema,
    FeedbackRequestSchema,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["feedback"])


def _record_to_schema(record: Any) -> FeedbackRecordSchema:
    """Convert a FeedbackRecord to a schema."""
    return FeedbackRecordSchema(
        feedback_id=record.feedback_id,
        task_id=record.task_id,
        agent=record.agent,
        feedback_type=record.feedback_type,
        question=record.question,
        context=record.context,
        options=record.options,
        response=record.response,
        selected_option=record.selected_option,
        status=record.status,
        created_at=record.created_at,
        responded_at=record.responded_at,
    )


@router.get(
    "/tasks/{task_id}/feedback",
    response_model=FeedbackListResponse,
    summary="Get feedback status for a task",
)
async def get_task_feedback(
    task_id: str,
    request: Request,
) -> FeedbackListResponse:
    """
    Get all pending and historical feedback for a task.
    """
    task_store = request.app.state.task_store
    record = await task_store.get(task_id)

    if record is None:
        raise NotFoundError(detail=f"Task '{task_id}' not found")

    # Get feedback from task metadata if available
    feedback_data = record.metadata.get("feedback", {}) if record.metadata else {}
    pending = feedback_data.get("pending", [])
    history = feedback_data.get("history", [])

    return FeedbackListResponse(
        pending=[FeedbackRecordSchema(**f) for f in pending],
        history=[FeedbackRecordSchema(**f) for f in history],
        total_pending=len(pending),
        total_history=len(history),
    )


@router.post(
    "/tasks/{task_id}/feedback/{feedback_id}",
    status_code=200,
    summary="Submit feedback response",
)
async def submit_feedback(
    task_id: str,
    feedback_id: str,
    request_body: FeedbackRequestSchema,
    request: Request,
) -> dict[str, str]:
    """
    Submit a response to a feedback request from an agent.
    """
    task_store = request.app.state.task_store
    record = await task_store.get(task_id)

    if record is None:
        raise NotFoundError(detail=f"Task '{task_id}' not found")

    # Store feedback response in task metadata
    if record.metadata is None:
        record.metadata = {}

    feedback_data = record.metadata.get("feedback", {})
    history = feedback_data.get("history", [])

    # Add to history
    history.append(
        {
            "feedback_id": feedback_id,
            "task_id": task_id,
            "response": request_body.response,
            "selected_option": request_body.selected_option,
            "status": "responded",
        }
    )

    record.metadata["feedback"] = {
        "pending": [
            f for f in feedback_data.get("pending", []) if f.get("feedback_id") != feedback_id
        ],
        "history": history,
    }

    logger.info(
        "Feedback submitted for task %s, feedback %s",
        task_id,
        feedback_id,
    )

    return {"status": "ok", "feedback_id": feedback_id}
