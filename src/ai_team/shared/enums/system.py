"""
System-wide enumerations.
"""

from __future__ import annotations

from enum import Enum, StrEnum, auto


# ============================================================================
# Environment
# ============================================================================


class Environment(StrEnum):
    """
    Application runtime environments.
    """

    DEVELOPMENT = "development"

    TESTING = "testing"

    STAGING = "staging"

    PRODUCTION = "production"


# ============================================================================
# Task Lifecycle
# ============================================================================


class TaskStatus(StrEnum):
    """
    Task lifecycle.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


# ============================================================================
# Logging
# ============================================================================


class LogLevel(StrEnum):
    """
    Application log levels.
    """

    DEBUG = "debug"

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"


# ============================================================================
# Execution
# ============================================================================


class ExecutionStatus(Enum):
    """
    Generic execution outcome.
    """

    SUCCESS = auto()

    FAILURE = auto()

    RETRY = auto()