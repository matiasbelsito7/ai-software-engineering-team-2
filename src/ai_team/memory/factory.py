"""
Memory module factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.memory.manager import MemoryManager
from ai_team.memory.retrieval.hybrid import HybridRetriever
from ai_team.memory.stores.project import ProjectMemoryStore
from ai_team.memory.stores.short_term import ShortTermMemoryStore

if TYPE_CHECKING:
    from ai_team.memory.retrieval.keyword import KeywordRetriever
    from ai_team.memory.retrieval.reranker import MemoryReranker
    from ai_team.memory.retrieval.semantic import SemanticRetriever


def build_memory(
    *,
    semantic_retriever: SemanticRetriever,
    keyword_retriever: KeywordRetriever,
    reranker: MemoryReranker | None = None,
) -> MemoryManager:
    """
    Build the memory subsystem.
    """

    short_term = ShortTermMemoryStore()

    project_store = ProjectMemoryStore()

    retriever = HybridRetriever(
        semantic=semantic_retriever,
        keyword=keyword_retriever,
        reranker=reranker,
    )

    return MemoryManager(
        short_term=short_term,
        project=project_store,
        retriever=retriever,
    )
