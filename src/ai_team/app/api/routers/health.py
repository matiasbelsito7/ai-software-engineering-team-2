"""
Health check router.
"""

from __future__ import annotations

import time

from fastapi import APIRouter

from ai_team.app.api.schemas.tasks import HealthResponse

router = APIRouter(tags=["health"])

_start_time = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
async def health_check() -> HealthResponse:
    """Return service health status and uptime."""

    return HealthResponse(
        status="ok",
        version="0.1.0",
        uptime_seconds=round(time.time() - _start_time, 2),
    )
