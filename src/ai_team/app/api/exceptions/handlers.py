"""
FastAPI exception handlers.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse

from ai_team.app.api.exceptions.errors import APIError
from ai_team.app.api.schemas.tasks import ErrorResponse

if TYPE_CHECKING:
    from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""

    @app.exception_handler(APIError)
    async def api_error_handler(
        request: Request,
        exc: APIError,
    ) -> JSONResponse:
        body = ErrorResponse(
            detail=exc.detail,
            error_code=exc.error_code,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=body.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)

        body = ErrorResponse(
            detail="Internal server error",
            error_code="internal_error",
        )

        return JSONResponse(
            status_code=500,
            content=body.model_dump(),
        )
