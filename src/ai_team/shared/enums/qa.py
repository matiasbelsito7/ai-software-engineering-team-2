"""
Quality assurance enumerations.
"""

from __future__ import annotations

from enum import StrEnum


class Severity(StrEnum):
    """
    Severity levels used by QA and Reviewer.
    """

    INFO = "info"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"
