"""
Memory manager.

Coordinates memory stores and retrieval strategies.
"""

from __future__ import annotations

from ai_team.memory.stores.base import BaseMemoryStore
from ai_team.memory.models import (
    MemoryContext,
    MemoryEntry,
    MemoryQuery,
    MemorySearchResult,
)
from ai_team.memory.retrieval.base import BaseRetriever
from ai_team.shared.enums import MemoryType


class MemoryManager:
    """
    High-level interface used by agents to interact
    with the memory subsystem.
    """

    def __init__(
        self,
        *,
        short_term: BaseMemoryStore,
        project: BaseMemoryStore,
        retriever: BaseRetriever,
    ) -> None:
        self._stores = {
            MemoryType.SHORT_TERM: short_term,
            MemoryType.PROJECT: project,
        }

        self._retriever = retriever

    # ------------------------------------------------------------------
    # Store Selection
    # ------------------------------------------------------------------

    def store(
        self,
        memory_type: MemoryType,
    ) -> BaseMemoryStore:
        """
        Return the appropriate memory store.
        """

        return self._stores[memory_type]

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def add(
        self,
        entry: MemoryEntry,
    ) -> None:
        """
        Store a memory entry.
        """

        await self.store(
            entry.memory_type,
        ).add(entry)

    async def update(
        self,
        entry: MemoryEntry,
    ) -> None:
        """
        Update a memory entry.
        """

        await self.store(
            entry.memory_type,
        ).update(entry)

    async def delete(
        self,
        memory_type: MemoryType,
        memory_id: str,
    ) -> None:
        """
        Delete a memory entry.
        """

        await self.store(
            memory_type,
        ).delete(memory_id)

    async def get(
        self,
        memory_type: MemoryType,
        memory_id: str,
    ) -> MemoryEntry | None:
        """
        Retrieve a memory entry.
        """

        return await self.store(
            memory_type,
        ).get(memory_id)

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    async def search(
        self,
        query: MemoryQuery,
    ) -> MemorySearchResult:
        """
        Retrieve memories.
        """

        return await self._retriever.search(
            query,
        )

    async def build_context(
        self,
        query: MemoryQuery,
    ) -> MemoryContext:
        """
        Build the context supplied to an agent.
        """

        return await self._retriever.build_context(
            query,
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    async def clear(self) -> None:
        """
        Clear every configured memory store.
        """

        for store in self._stores.values():
            await store.clear()