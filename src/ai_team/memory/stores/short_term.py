"""
Short-term memory store.

Uses an in-memory dict with TTL-based eviction and max size.
Future implementation: Redis
"""

from __future__ import annotations

from time import monotonic
from typing import TYPE_CHECKING

from ai_team.memory.models import MemoryContext, MemorySearchResult
from ai_team.memory.stores.base import BaseMemoryStore

if TYPE_CHECKING:
    from ai_team.memory.models import (
        MemoryEntry,
        MemoryQuery,
    )

_DEFAULT_TTL_SECONDS = 600.0
_DEFAULT_MAX_SIZE = 500


class ShortTermMemoryStore(BaseMemoryStore):
    """
    Short-term memory with time-to-live eviction and max size.

    Entries older than ``ttl_seconds`` are evicted on access.
    When the store exceeds ``max_size``, the oldest entries are dropped.
    """

    def __init__(
        self,
        *,
        ttl_seconds: float = _DEFAULT_TTL_SECONDS,
        max_size: int = _DEFAULT_MAX_SIZE,
    ) -> None:
        self._entries: dict[str, MemoryEntry] = {}
        self._timestamps: dict[str, float] = {}
        self._ttl = ttl_seconds
        self._max_size = max_size

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _evict_expired(self) -> None:
        now = monotonic()
        expired = [mid for mid, ts in self._timestamps.items() if now - ts > self._ttl]
        for mid in expired:
            self._entries.pop(mid, None)
            self._timestamps.pop(mid, None)

    def _enforce_max_size(self) -> None:
        while len(self._entries) > self._max_size:
            oldest_id = min(self._timestamps, key=self._timestamps.get)  # type: ignore[arg-type]
            self._entries.pop(oldest_id, None)
            self._timestamps.pop(oldest_id, None)

    # ------------------------------------------------------------------
    # BaseMemoryStore
    # ------------------------------------------------------------------

    async def add(self, entry: MemoryEntry) -> None:
        self._evict_expired()
        key = str(entry.id)
        self._entries[key] = entry
        self._timestamps[key] = monotonic()
        self._enforce_max_size()

    async def update(self, entry: MemoryEntry) -> None:
        key = str(entry.id)
        self._entries[key] = entry
        self._timestamps[key] = monotonic()

    async def delete(self, memory_id: str) -> None:
        self._entries.pop(memory_id, None)
        self._timestamps.pop(memory_id, None)

    async def get(self, memory_id: str) -> MemoryEntry | None:
        self._evict_expired()
        return self._entries.get(memory_id)

    async def search(self, query: MemoryQuery) -> MemorySearchResult:
        self._evict_expired()
        results = list(self._entries.values())

        if query.memory_types:
            results = [e for e in results if e.memory_type in query.memory_types]

        if query.agent is not None:
            results = [e for e in results if e.agent == query.agent]

        results = [e for e in results if e.score >= query.min_score]
        results.sort(key=lambda e: e.score, reverse=True)
        results = results[: query.top_k]

        return MemorySearchResult(query=query, entries=results)

    async def build_context(self, query: MemoryQuery) -> MemoryContext:
        result = await self.search(query)
        return MemoryContext(entries=result.entries)

    async def clear(self) -> None:
        self._entries.clear()
        self._timestamps.clear()
