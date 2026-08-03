"""
Shared database models used across AI agents.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Column
# ============================================================================


class DatabaseColumn(BaseModel):
    """
    Represents a database column.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    data_type: str

    nullable: bool = False

    primary_key: bool = False

    unique: bool = False

    default: str | None = None

    description: str | None = None


# ============================================================================
# Foreign Key
# ============================================================================


class ForeignKey(BaseModel):
    """
    Represents a foreign key constraint.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    column: str

    references_table: str

    references_column: str


# ============================================================================
# Index
# ============================================================================


class DatabaseIndex(BaseModel):
    """
    Represents a database index.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    columns: list[str]

    unique: bool = False


# ============================================================================
# Relationship
# ============================================================================


class DatabaseRelationship(BaseModel):
    """
    Relationship between two entities.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    source: str

    target: str

    relationship: str

    foreign_key: str


# ============================================================================
# Entity
# ============================================================================


class DatabaseEntity(BaseModel):
    """
    Represents a database entity (table).
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    description: str | None = None

    columns: list[DatabaseColumn]

    foreign_keys: list[ForeignKey] = Field(
        default_factory=list,
    )

    indexes: list[DatabaseIndex] = Field(
        default_factory=list,
    )