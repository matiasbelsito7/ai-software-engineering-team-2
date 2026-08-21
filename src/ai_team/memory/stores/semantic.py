"""
Semantic memory store.

Uses cosine similarity over embeddings for retrieval.
Future implementation: Qdrant / pgvector
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ai_team.memory.models import MemoryContext, MemorySearchResult
from ai_team.memory.stores.base import BaseMemoryStore

if TYPE_CHECKING:
    from ai_team.memory.models import (
        MemoryEntry,
        MemoryQuery,
    )


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


class SemanticMemoryStore(BaseMemoryStore):
    """
    Semantic memory backed by embeddings and cosine similarity.

    When entries have embeddings, ``search`` scores them against the
    query embedding and returns the most similar entries.
    Falls back to text-based filtering when embeddings are absent.
    """

    def __init__(self) -> None:
        self._entries: dict[str, MemoryEntry] = {}

    # ------------------------------------------------------------------
    # BaseMemoryStore
    # ------------------------------------------------------------------

    async def add(self, entry: MemoryEntry) -> None:
        self._entries[str(entry.id)] = entry

    async def update(self, entry: MemoryEntry) -> None:
        self._entries[str(entry.id)] = entry

    async def delete(self, memory_id: str) -> None:
        self._entries.pop(memory_id, None)

    async def get(self, memory_id: str) -> MemoryEntry | None:
        return self._entries.get(memory_id)

    async def search(self, query: MemoryQuery) -> MemorySearchResult:
        candidates = list(self._entries.values())

        if query.memory_types:
            candidates = [e for e in candidates if e.memory_type in query.memory_types]

        if query.agent is not None:
            candidates = [e for e in candidates if e.agent == query.agent]

        # Score by embedding similarity when available
        scored = []
        for entry in candidates:
            if entry.embedding is not None and query.embedding is not None:
                sim = _cosine_similarity(entry.embedding, query.embedding)
                scored.append((sim, entry))
            else:
                scored.append((entry.score, entry))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        results = [entry for _, entry in scored][: query.top_k]

        return MemorySearchResult(query=query, entries=results)

    async def build_context(self, query: MemoryQuery) -> MemoryContext:
        result = await self.search(query)
        return MemoryContext(entries=result.entries)

    async def clear(self) -> None:
        self._entries.clear()
