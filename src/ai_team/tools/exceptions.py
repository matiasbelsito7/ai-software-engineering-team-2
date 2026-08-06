"""
Tool exceptions.
"""

from __future__ import annotations


class ToolError(Exception):
    """
    Base exception for the tool subsystem.
    """


class ToolNotFoundError(ToolError):
    """
    Raised when a tool cannot be found.
    """


class ToolExecutionError(ToolError):
    """
    Raised when tool execution fails.
    """


class ToolValidationError(ToolError):
    """
    Raised when a tool request is invalid.
    """


class ToolPermissionError(ToolError):
    """
    Raised when a tool is not allowed to execute
    the requested operation.
    """


class ToolTimeoutError(ToolError):
    """
    Raised when tool execution exceeds the
    configured timeout.
    """