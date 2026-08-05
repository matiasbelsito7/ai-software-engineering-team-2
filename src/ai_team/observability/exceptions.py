"""
Observability exceptions.
"""

from __future__ import annotations


class ObservabilityError(Exception):
    """
    Base exception for the observability subsystem.
    """


class TracingError(ObservabilityError):
    """
    Raised when trace creation or management fails.
    """


class MetricsError(ObservabilityError):
    """
    Raised when metrics cannot be collected or exported.
    """


class LoggingError(ObservabilityError):
    """
    Raised when structured logging fails.
    """


class TokenUsageError(ObservabilityError):
    """
    Raised when token usage cannot be computed.
    """


class CostCalculationError(ObservabilityError):
    """
    Raised when execution cost cannot be calculated.
    """