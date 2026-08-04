"""
Semantic memory store.

Future implementation:
    Qdrant
"""

from __future__ import annotations

from ai_team.memory.stores.base import BaseMemoryStore
from ai_team.memory.models import (
    MemoryContext,
    MemoryEntry,
    MemoryQuery,
    MemorySearchResult,
)


class SemanticMemoryStore(BaseMemoryStore):
    """
    Semantic memory implementation.

    Uses vector embeddings to retrieve relevant
    memories through similarity search.
    """

    async def add(
        self,
        entry: MemoryEntry,
    ) -> None:
        raise NotImplementedError

    async def update(
        self,
        entry: MemoryEntry,
    ) -> None:
        raise NotImplementedError

    async def delete(
        self,
        memory_id: str,
    ) -> None:
        raise NotImplementedError

    async def get(
        self,
        memory_id: str,
    ) -> MemoryEntry | None:
        raise NotImplementedError

    async def search(
        self,
        query: MemoryQuery,
    ) -> MemorySearchResult:
        raise NotImplementedError

    async def build_context(
        self,
        query: MemoryQuery,
    ) -> MemoryContext:
        raise NotImplementedError

    async def clear(self) -> None:
        raise NotImplementedError