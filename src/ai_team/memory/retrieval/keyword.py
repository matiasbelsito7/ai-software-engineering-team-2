"""
Keyword retrieval strategy.
"""

from __future__ import annotations

from ai_team.memory.stores.base import BaseMemoryStore
from ai_team.memory.models import (
    MemoryContext,
    MemoryQuery,
    MemorySearchResult,
)
from ai_team.memory.retrieval.base import (
    BaseRetriever,
)


class KeywordRetriever(BaseRetriever):
    """
    Retrieves memories using keyword matching.
    """

    def __init__(
        self,
        store: BaseMemoryStore,
    ) -> None:
        self._store = store

    async def search(
        self,
        query: MemoryQuery,
    ) -> MemorySearchResult:
        return await self._store.search(query)

    async def build_context(
        self,
        query: MemoryQuery,
    ) -> MemoryContext:
        return await self._store.build_context(query)