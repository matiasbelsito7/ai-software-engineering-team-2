"""
Memory module factory.
"""

from __future__ import annotations

from ai_team.memory.manager import MemoryManager
from ai_team.memory.stores.project import ProjectMemoryStore
from ai_team.memory.stores.semantic import SemanticMemoryStore
from ai_team.memory.stores.short_term import ShortTermMemoryStore
from ai_team.memory.retrieval.hybrid import HybridRetriever


def build_memory() -> MemoryManager:
    """
    Build the memory subsystem.
    """

    short_term = ShortTermMemoryStore()

    project_store = ProjectMemoryStore()

    semantic_store = SemanticMemoryStore()

    retriever = HybridRetriever(
        semantic_store=semantic_store,
    )

    return MemoryManager(
        short_term=short_term,
        project_store=project_store,
        semantic_store=semantic_store,
        retriever=retriever,
    )