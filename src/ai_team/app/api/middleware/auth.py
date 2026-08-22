"""
API key authentication middleware.
"""

from __future__ import annotations

import logging
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request  # noqa: TC002
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)

# Endpoints that bypass authentication
_OPEN_ENDPOINTS: frozenset[str] = frozenset(
    {
        "/api/v1/health",
        "/docs",
        "/redoc",
        "/openapi.json",
    }
)


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """
    Validate API keys from request headers.

    When enabled, requests must include a valid API key in the
    configured header (default: X-API-Key). Open endpoints
    (health, docs) are always accessible.
    """

    def __init__(
        self,
        app: Any,
        *,
        api_keys: list[str],
        header: str = "X-API-Key",
        audit_logger: logging.Logger | None = None,
    ) -> None:
        super().__init__(app)
        self._valid_keys = set(api_keys)
        self._header = header.lower()
        self._audit = audit_logger or logging.getLogger(__name__)

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        path = request.url.path

        if path in _OPEN_ENDPOINTS:
            response: Response = await call_next(request)
            return response

        if path.startswith("/docs") or path.startswith("/redoc"):
            response = await call_next(request)
            return response

        if path.startswith("/openapi"):
            response = await call_next(request)
            return response

        api_key = request.headers.get(self._header)

        if not api_key:
            self._audit.warning(
                "AUTH_FAIL missing_key path=%s ip=%s",
                path,
                request.client.host if request.client else "unknown",
            )
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Missing API key.",
                    "error_code": "missing_api_key",
                },
            )

        if api_key not in self._valid_keys:
            self._audit.warning(
                "AUTH_FAIL invalid_key path=%s ip=%s",
                path,
                request.client.host if request.client else "unknown",
            )
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid API key.",
                    "error_code": "invalid_api_key",
                },
            )

        self._audit.info(
            "AUTH_OK key=***%s path=%s",
            api_key[-4:] if len(api_key) >= 4 else "****",
            path,
        )

        response = await call_next(request)
        return response
