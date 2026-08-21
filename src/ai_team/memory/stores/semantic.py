"""
Semantic memory store.

Future implementation:
    Qdrant
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.memory.models import MemoryContext, MemorySearchResult
from ai_team.memory.stores.base import BaseMemoryStore

if TYPE_CHECKING:
    from ai_team.memory.models import (
        MemoryEntry,
        MemoryQuery,
    )


class SemanticMemoryStore(BaseMemoryStore):
    """
    Semantic memory implementation.

    Uses vector embeddings to retrieve relevant
    memories through similarity search.
    """

    def __init__(self) -> None:
        self._entries: dict[str, MemoryEntry] = {}

    async def add(
        self,
        entry: MemoryEntry,
    ) -> None:
        self._entries[str(entry.id)] = entry

    async def update(
        self,
        entry: MemoryEntry,
    ) -> None:
        self._entries[str(entry.id)] = entry

    async def delete(
        self,
        memory_id: str,
    ) -> None:
        self._entries.pop(memory_id, None)

    async def get(
        self,
        memory_id: str,
    ) -> MemoryEntry | None:
        return self._entries.get(memory_id)

    async def search(
        self,
        query: MemoryQuery,
    ) -> MemorySearchResult:
        results = list(self._entries.values())

        if query.memory_types:
            results = [e for e in results if e.memory_type in query.memory_types]

        results = [e for e in results if e.score >= query.min_score]

        results.sort(key=lambda e: e.score, reverse=True)

        results = results[: query.top_k]

        return MemorySearchResult(query=query, entries=results)

    async def build_context(
        self,
        query: MemoryQuery,
    ) -> MemoryContext:
        result = await self.search(query)
        return MemoryContext(entries=result.entries)

    async def clear(self) -> None:
        self._entries.clear()
