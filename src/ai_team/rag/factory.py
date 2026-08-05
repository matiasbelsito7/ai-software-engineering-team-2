"""
RAG module factory.
"""

from __future__ import annotations

from ai_team.rag.manager import RAGManager
from ai_team.rag.indexing.pipeline import IndexingPipeline
from ai_team.rag.retrieval.hybrid import HybridRetriever


def build_rag() -> RAGManager:
    """
    Build the RAG subsystem.
    """

    indexing = IndexingPipeline()

    retrieval = HybridRetriever()

    return RAGManager(
        indexing=indexing,
        retrieval=retrieval,
    )