"""
Exceptions used by the memory subsystem.
"""

from __future__ import annotations


class MemoryError(Exception):
    """
    Base exception for the memory subsystem.
    """


class MemoryNotFoundError(MemoryError):
    """
    Raised when a memory entry cannot be found.
    """


class MemoryStoreError(MemoryError):
    """
    Raised when a memory store operation fails.
    """


class MemoryRetrievalError(MemoryError):
    """
    Raised when memory retrieval fails.
    """


class MemorySerializationError(MemoryError):
    """
    Raised when a memory cannot be serialized or deserialized.
    """


class MemoryConfigurationError(MemoryError):
    """
    Raised when the memory subsystem is incorrectly configured.
    """