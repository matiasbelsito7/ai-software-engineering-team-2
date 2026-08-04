"""
Hybrid retrieval strategy.
"""

from __future__ import annotations

from ai_team.memory.models import (
    MemoryContext,
    MemoryQuery,
    MemorySearchResult,
)
from ai_team.memory.retrieval.base import (
    BaseRetriever,
)
from ai_team.memory.retrieval.keyword import (
    KeywordRetriever,
)
from ai_team.memory.retrieval.reranker import (
    MemoryReranker,
)
from ai_team.memory.retrieval.semantic import (
    SemanticRetriever,
)


class HybridRetriever(BaseRetriever):
    """
    Combines semantic and keyword retrieval.
    """

    def __init__(
        self,
        *,
        semantic: SemanticRetriever,
        keyword: KeywordRetriever,
        reranker: MemoryReranker | None = None,
    ) -> None:
        self._semantic = semantic
        self._keyword = keyword
        self._reranker = reranker

    async def search(
        self,
        query: MemoryQuery,
    ) -> MemorySearchResult:
        semantic = await self._semantic.search(query)
        keyword = await self._keyword.search(query)

        merged = [
            *semantic.entries,
            *keyword.entries,
        ]

        unique = {
            entry.id: entry
            for entry in merged
        }

        entries = list(unique.values())

        if self._reranker is not None:
            entries = await self._reranker.rerank(
                query=query,
                entries=entries,
            )

        return MemorySearchResult(
            query=query,
            entries=entries,
        )

    async def build_context(
        self,
        query: MemoryQuery,
    ) -> MemoryContext:
        result = await self.search(query)

        return MemoryContext(
            entries=result.entries,
        )