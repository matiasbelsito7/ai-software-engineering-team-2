"""
Approval router for human-in-the-loop command execution.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from ai_team.app.api.exceptions.errors import TaskNotFoundError

if TYPE_CHECKING:
    from ai_team.app.api.task_store import TaskStore

logger = logging.getLogger(__name__)

router = APIRouter(tags=["approvals"])


class ApprovalResponse(BaseModel):
    """Request body for approving or rejecting a command."""

    model_config = ConfigDict(extra="forbid")

    approved: bool = Field(
        ...,
        description="True to approve, false to reject",
    )


class ApprovalRecord(BaseModel):
    """Response model for an approval record."""

    model_config = ConfigDict(extra="forbid")

    approval_id: str
    task_id: str
    command: str
    agent: str | None = None
    description: str | None = None
    status: str


def _get_task_store(request: Request) -> TaskStore:
    return request.app.state.task_store  # type: ignore[no-any-return]


@router.get(
    "/tasks/{task_id}/approvals",
    response_model=list[dict[str, Any]],
    summary="Get pending approvals for a task",
)
async def get_pending_approvals(
    task_id: str,
    request: Request,
) -> list[dict[str, Any]]:
    """
    Returns all pending approval requests for a task.
    """
    task_store = _get_task_store(request)

    record = await task_store.get(task_id)

    if record is None:
        raise TaskNotFoundError(task_id)

    return await task_store.get_pending_approvals(task_id)


@router.post(
    "/tasks/{task_id}/approvals/{approval_id}",
    response_model=ApprovalRecord,
    summary="Approve or reject a command",
)
async def resolve_approval(
    task_id: str,
    approval_id: str,
    body: ApprovalResponse,
    request: Request,
) -> ApprovalRecord:
    """
    Approve or reject a pending command execution.

    When a command requires human-in-the-loop approval, this endpoint
    is used to either approve or reject the command. The approval
    unblocks the agent that was waiting for the response.
    """
    task_store = _get_task_store(request)

    record = await task_store.get(task_id)

    if record is None:
        raise TaskNotFoundError(task_id)

    result = await task_store.resolve_approval(
        task_id,
        approval_id=approval_id,
        approved=body.approved,
    )

    if result is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail=f"Approval '{approval_id}' not found or already resolved.",
        )

    return ApprovalRecord(**result)
