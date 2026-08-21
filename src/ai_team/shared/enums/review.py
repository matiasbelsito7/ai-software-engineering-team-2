"""
Review-related enumerations.
"""

from __future__ import annotations

from enum import StrEnum


class ReviewStatus(StrEnum):
    """
    Final outcome of a review.
    """

    APPROVED = "approved"

    APPROVED_WITH_CHANGES = "approved_with_changes"

    CHANGES_REQUESTED = "changes_requested"

    REJECTED = "rejected"


class ReviewCategory(StrEnum):
    """
    Categories of review findings.
    """

    ARCHITECTURE = "architecture"

    CODE_QUALITY = "code_quality"

    PERFORMANCE = "performance"

    SECURITY = "security"

    MAINTAINABILITY = "maintainability"

    TESTING = "testing"

    DOCUMENTATION = "documentation"

    DATABASE = "database"

    STYLE = "style"
