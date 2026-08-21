"""
Context exceptions.
"""

from __future__ import annotations


class ContextError(Exception):
    """
    Base exception for the context subsystem.
    """


class ContextSelectionError(ContextError):
    """
    Raised when context selection fails.
    """


class ContextCompressionError(ContextError):
    """
    Raised when context compression fails.
    """


class ContextSummarizationError(ContextError):
    """
    Raised when conversation summarization fails.
    """
