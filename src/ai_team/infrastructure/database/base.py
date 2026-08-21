"""
SQLAlchemy declarative base.

Every ORM model in the project must inherit from this class.

Responsibilities
----------------
- Provide the Declarative Base.
- Define common metadata.

This module intentionally does NOT create:

- Engine
- Sessions
- Repositories
- Unit of Work

Those belong to their respective modules.
"""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Consistent naming conventions for Alembic migrations.
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": ("fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"),
    "pk": "pk_%(table_name)s",
}


metadata = MetaData(
    naming_convention=NAMING_CONVENTION,
)


class Base(DeclarativeBase):
    """
    Base class for every ORM model.
    """

    metadata = metadata
