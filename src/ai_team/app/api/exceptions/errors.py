"""
Custom exception classes for the API layer.
"""

from __future__ import annotations


class APIError(Exception):
    """Base class for all API errors."""

    def __init__(
        self,
        *,
        detail: str,
        status_code: int = 500,
        error_code: str | None = None,
    ) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code


class NotFoundError(APIError):
    """Resource not found."""

    def __init__(
        self,
        *,
        detail: str = "Resource not found",
        error_code: str = "not_found",
    ) -> None:
        super().__init__(
            detail=detail,
            status_code=404,
            error_code=error_code,
        )


class TaskNotFoundError(NotFoundError):
    """Task not found."""

    def __init__(self, task_id: str) -> None:
        super().__init__(
            detail=f"Task '{task_id}' not found.",
            error_code="task_not_found",
        )


class ValidationError(APIError):
    """Request validation error."""

    def __init__(
        self,
        *,
        detail: str = "Validation error",
        error_code: str = "validation_error",
    ) -> None:
        super().__init__(
            detail=detail,
            status_code=422,
            error_code=error_code,
        )


class TaskConflictError(APIError):
    """Task state conflict."""

    def __init__(self, detail: str = "Task state conflict") -> None:
        super().__init__(
            detail=detail,
            status_code=409,
            error_code="task_conflict",
        )


class RateLimitError(APIError):
    """Rate limit exceeded."""

    def __init__(
        self,
        *,
        detail: str = "Rate limit exceeded. Try again later.",
        retry_after: int = 60,
    ) -> None:
        super().__init__(
            detail=detail,
            status_code=429,
            error_code="rate_limit_exceeded",
        )
        self.retry_after = retry_after


class InternalError(APIError):
    """Internal server error."""

    def __init__(
        self,
        *,
        detail: str = "Internal server error",
        error_code: str = "internal_error",
    ) -> None:
        super().__init__(
            detail=detail,
            status_code=500,
            error_code=error_code,
        )
