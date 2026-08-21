"""
Database-related enumerations.
"""

from __future__ import annotations

from enum import StrEnum


class RelationshipType(StrEnum):
    """
    Supported relationship types.
    """

    ONE_TO_ONE = "one_to_one"

    ONE_TO_MANY = "one_to_many"

    MANY_TO_ONE = "many_to_one"

    MANY_TO_MANY = "many_to_many"
