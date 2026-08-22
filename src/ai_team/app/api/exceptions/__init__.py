"""
API exceptions package.
"""

from ai_team.app.api.exceptions.errors import (
    APIError,
    InternalError,
    NotFoundError,
    RateLimitError,
    TaskConflictError,
    TaskNotFoundError,
    ValidationError,
)
from ai_team.app.api.exceptions.handlers import register_exception_handlers

__all__ = [
    "APIError",
    "InternalError",
    "NotFoundError",
    "RateLimitError",
    "TaskConflictError",
    "TaskNotFoundError",
    "ValidationError",
    "register_exception_handlers",
]
