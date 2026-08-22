"""
Request logging middleware.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request  # noqa: TC002
from starlette.responses import Response  # noqa: TC002

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs request method, path, status code, and duration."""

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        start = time.perf_counter()

        method = request.method
        path = request.url.path

        logger.info("→ %s %s", method, path)

        response: Response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "← %s %s %d (%.1fms)",
            method,
            path,
            response.status_code,
            elapsed_ms,
        )

        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.1f}"

        return response
