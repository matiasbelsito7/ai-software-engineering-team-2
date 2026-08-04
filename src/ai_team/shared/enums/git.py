"""
Enums shared by the Git agent.
"""

from __future__ import annotations

from enum import StrEnum


class GitOperation(StrEnum):
    """
    High-level Git operations.
    """

    ADD = "add"

    COMMIT = "commit"

    BRANCH = "branch"

    MERGE = "merge"

    REBASE = "rebase"

    TAG = "tag"

    PUSH = "push"

    PULL = "pull"


class GitChangeType(StrEnum):
    """
    File change type.
    """

    ADDED = "added"

    MODIFIED = "modified"

    DELETED = "deleted"

    RENAMED = "renamed"