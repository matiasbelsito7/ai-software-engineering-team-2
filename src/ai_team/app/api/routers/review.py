"""
Code review router.
"""

from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Request

from ai_team.app.api.schemas.review import (
    ReviewFileSchema,
    ReviewInlineCommentSchema,
    ReviewRequestSchema,
    ReviewResultSchema,
)
from ai_team.review.engine import ReviewEngine
from ai_team.review.models import ReviewRequest

logger = logging.getLogger(__name__)

router = APIRouter(tags=["review"])

_engine = ReviewEngine()


@router.post(
    "/review",
    response_model=ReviewResultSchema,
    summary="Perform code review",
)
async def perform_review(
    request_body: ReviewRequestSchema,
    request: Request,
) -> ReviewResultSchema:
    """
    Perform automated code review with inline comments.
    """
    task_id = str(uuid.uuid4())

    review_request = ReviewRequest(
        task_id=task_id,
        files=request_body.files,
        context=request_body.context,
    )

    result = await _engine.review(review_request)

    return ReviewResultSchema(
        task_id=result.task_id,
        files=[
            ReviewFileSchema(
                file_path=f.file_path,
                comments=[
                    ReviewInlineCommentSchema(
                        file_path=c.file_path,
                        line_number=c.line_number,
                        severity=c.severity,
                        category=c.category,
                        message=c.message,
                        suggestion=c.suggestion,
                        code_snippet=c.code_snippet,
                    )
                    for c in f.comments
                ],
                summary=f.summary,
                score=f.score,
            )
            for f in result.files
        ],
        overall_score=result.overall_score,
        summary=result.summary,
        approved=result.approved,
        total_comments=result.total_comments,
        critical_issues=result.critical_issues,
    )
