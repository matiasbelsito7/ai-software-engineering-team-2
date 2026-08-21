"""
Unit of Work implementation.

Coordinates repositories and transaction boundaries.

Responsibilities
----------------
- Create a database session.
- Manage transactions.
- Commit or rollback changes.
- Expose repositories.

Concrete repositories should be attached by subclasses or composition.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.infrastructure.database.session import SessionFactory

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    """
    Base Unit of Work.
    """

    def __init__(self) -> None:
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession:
        """
        Return the active session.
        """
        if self._session is None:
            raise RuntimeError(
                "UnitOfWork has not been entered."
            )

        return self._session

    async def __aenter__(self) -> UnitOfWork:
        """
        Start a new transaction.
        """
        self._session = SessionFactory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """
        Commit or rollback the current transaction.
        """
        assert self._session is not None

        try:
            if exc is None:
                await self._session.commit()
            else:
                await self._session.rollback()

        finally:
            await self._session.close()

    async def rollback(self) -> None:
        """
        Roll back the active transaction.
        """
        await self.session.rollback()

    async def commit(self) -> None:
        """
        Commit the active transaction.
        """
        await self.session.commit()

    async def flush(self) -> None:
        """
        Flush pending changes.
        """
        await self.session.flush()

    async def refresh(self, entity: object) -> None:
        """
        Refresh an entity.
        """
        await self.session.refresh(entity)
