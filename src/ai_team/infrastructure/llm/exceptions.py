"""
LLM-specific exceptions.

The rest of the application should never depend on provider
or HTTP client exceptions directly. Providers are responsible
for translating external errors into these domain exceptions.
"""

from __future__ import annotations

from typing import Any


class LLMError(Exception):
    """
    Base exception for every LLM-related error.
    """

    def __init__(
        self,
        message: str,
        *,
        provider: str | None = None,
        model: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)

        self.provider = provider
        self.model = model
        self.details = details or {}


# ---------------------------------------------------------------------
# Authentication / Authorization
# ---------------------------------------------------------------------


class AuthenticationError(LLMError):
    """
    Invalid or missing credentials.
    """


class AuthorizationError(LLMError):
    """
    Authenticated but not authorized.
    """


# ---------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------


class RateLimitError(LLMError):
    """
    Provider rate limit exceeded.
    """


# ---------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------


class ProviderUnavailableError(LLMError):
    """
    Provider is temporarily unavailable.
    """


class ServiceUnavailableError(LLMError):
    """
    Upstream service unavailable.
    """


class TimeoutError(LLMError):
    """
    Request exceeded the configured timeout.
    """


# ---------------------------------------------------------------------
# Request / Response
# ---------------------------------------------------------------------


class InvalidRequestError(LLMError):
    """
    Invalid request sent to the provider.
    """


class InvalidResponseError(LLMError):
    """
    Provider returned an invalid response.
    """


class ResponseParsingError(LLMError):
    """
    Failed to parse the provider response.
    """


# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------


class ModelNotFoundError(LLMError):
    """
    Requested model does not exist.
    """


class ModelCapabilityError(LLMError):
    """
    Requested model does not support the
    required capability.
    """


# ---------------------------------------------------------------------
# Tool Calling
# ---------------------------------------------------------------------


class ToolExecutionError(LLMError):
    """
    Tool execution failed.
    """


class ToolValidationError(LLMError):
    """
    Tool arguments failed validation.
    """


# ---------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------


class StreamingError(LLMError):
    """
    Streaming operation failed.
    """


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------


class ConfigurationError(LLMError):
    """
    Invalid LLM configuration.
    """