"""
Semantic retrieval strategy.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.memory.retrieval.base import (
    BaseRetriever,
)

if TYPE_CHECKING:
    from ai_team.memory.models import (
        MemoryContext,
        MemoryQuery,
        MemorySearchResult,
    )
    from ai_team.memory.stores.semantic import (
        SemanticMemoryStore,
    )


class SemanticRetriever(BaseRetriever):
    """
    Retrieves memories using semantic similarity.
    """

    def __init__(
        self,
        store: SemanticMemoryStore,
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
