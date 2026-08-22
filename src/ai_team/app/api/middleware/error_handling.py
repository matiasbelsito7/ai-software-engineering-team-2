"""
Error handling middleware.
"""

from __future__ import annotations

import logging
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request  # noqa: TC002
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Catches unhandled exceptions and returns JSON error responses."""

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        try:
            response: Response = await call_next(request)
            return response

        except Exception as exc:
            logger.exception("Unhandled exception in middleware: %s", exc)

            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_code": "internal_error",
                },
            )
