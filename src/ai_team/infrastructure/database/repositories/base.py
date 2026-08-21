"""
Base repository.

Provides the common CRUD operations shared by all repositories.

Concrete repositories should inherit from this class and implement
domain-specific queries.

Responsibilities
----------------
- CRUD operations
- Session access
- Generic entity retrieval

This module intentionally does NOT contain:

- Business logic
- Complex queries
- Transactions
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from ai_team.infrastructure.database.base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[ModelT: Base]:
    """
    Generic SQLAlchemy repository.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """
        Expose the underlying SQLAlchemy session.
        """
        return self._session

    async def add(self, entity: ModelT) -> ModelT:
        """
        Add a new entity to the current session.
        """
        self.session.add(entity)
        return entity

    async def get(
        self,
        model: type[ModelT],
        entity_id: object,
    ) -> ModelT | None:
        """
        Retrieve an entity by its primary key.
        """
        return await self.session.get(model, entity_id)

    async def list(
        self,
        model: type[ModelT],
    ) -> list[ModelT]:
        """
        Return every entity of the given model.
        """
        result = await self.session.scalars(select(model))
        return list(result)

    async def delete(
        self,
        entity: ModelT,
    ) -> None:
        """
        Delete an entity.
        """
        await self.session.delete(entity)

    async def flush(self) -> None:
        """
        Flush pending changes.
        """
        await self.session.flush()

    async def refresh(
        self,
        entity: ModelT,
    ) -> None:
        """
        Refresh an entity from the database.
        """
        await self.session.refresh(entity)

    async def exists(
        self,
        model: type[ModelT],
        entity_id: object,
    ) -> bool:
        """
        Check whether an entity exists.
        """
        entity = await self.get(model, entity_id)
        return entity is not None
