"""
Security headers middleware.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses.

    Headers include:
    - Strict-Transport-Security (HSTS)
    - X-Content-Type-Options
    - X-Frame-Options
    - X-XSS-Protection
    - Content-Security-Policy
    - Referrer-Policy
    - Permissions-Policy
    - Cache-Control
    - X-Request-Id (if present in request)
    """

    def __init__(
        self,
        app: Any,
        *,
        hsts_max_age: int = 31536000,
        content_security_policy: str = "default-src 'none'",
    ) -> None:
        super().__init__(app)
        self._hsts_max_age = hsts_max_age
        self._csp = content_security_policy

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        response: Response = await call_next(request)

        response.headers["Strict-Transport-Security"] = (
            f"max-age={self._hsts_max_age}; includeSubDomains"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"
        response.headers["Content-Security-Policy"] = self._csp
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), "
            "gyroscope=(), magnetometer=(), microphone=(), "
            "payment=(), usb=()"
        )
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"

        request_id = request.headers.get("x-request-id")
        if request_id:
            response.headers["X-Request-Id"] = request_id

        return response
