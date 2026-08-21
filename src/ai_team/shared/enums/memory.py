"""
Memory-related enumerations.
"""

from __future__ import annotations

from enum import StrEnum


class MemoryType(StrEnum):
    """
    Supported memory scopes.
    """

    SHORT_TERM = "short_term"

    PROJECT = "project"
