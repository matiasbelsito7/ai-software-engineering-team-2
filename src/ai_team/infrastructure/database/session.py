"""
SQLAlchemy async session management.

This module centralizes session creation for the entire application.

Responsibilities
----------------
- Create the async session factory.
- Provide session generators.
- Expose context managers for transactional work.

This module intentionally does NOT contain:

- Repository implementations
- Unit of Work
- Business logic
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from ai_team.infrastructure.database.engine import engine

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# ---------------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------------

SessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


# ---------------------------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------------------------


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield a database session.

    Intended for dependency injection.
    """

    async with SessionFactory() as session:
        yield session


# ---------------------------------------------------------------------------
# Generic Context Manager
# ---------------------------------------------------------------------------


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a transactional scope.

    Commits on success.
    Rolls back on failure.
    Always closes the session.
    """

    async with SessionFactory() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()
