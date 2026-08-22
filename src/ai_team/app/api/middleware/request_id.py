"""
Request ID middleware.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Inject a unique request ID into every request/response.

    If the client sends an X-Request-Id header, it is preserved.
    Otherwise, a new UUID4 is generated. The ID is added to
    response headers and can be accessed via request.state.request_id.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())

        request.state.request_id = request_id

        response: Response = await call_next(request)

        response.headers["X-Request-Id"] = request_id

        return response
