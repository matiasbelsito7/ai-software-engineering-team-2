"""
Base interface for memory store strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.memory.models import (
        MemoryContext,
        MemoryEntry,
        MemoryQuery,
        MemorySearchResult,
    )


class BaseMemoryStore(ABC):
    """
    Base interface implemented by every memory backend.
    """

    @abstractmethod
    async def add(
        self,
        entry: MemoryEntry,
    ) -> None:
        """
        Store a memory entry.
        """
        ...

    @abstractmethod
    async def update(
        self,
        entry: MemoryEntry,
    ) -> None:
        """
        Update an existing memory entry.
        """
        ...

    @abstractmethod
    async def delete(
        self,
        memory_id: str,
    ) -> None:
        """
        Remove a memory entry.
        """
        ...

    @abstractmethod
    async def get(
        self,
        memory_id: str,
    ) -> MemoryEntry | None:
        """
        Retrieve a memory by its identifier.
        """
        ...

    @abstractmethod
    async def search(
        self,
        query: MemoryQuery,
    ) -> MemorySearchResult:
        """
        Search memories.
        """
        ...

    @abstractmethod
    async def build_context(
        self,
        query: MemoryQuery,
    ) -> MemoryContext:
        """
        Build the context supplied to an agent.
        """
        ...

    @abstractmethod
    async def clear(self) -> None:
        """
        Remove every stored memory.
        """
        ...
