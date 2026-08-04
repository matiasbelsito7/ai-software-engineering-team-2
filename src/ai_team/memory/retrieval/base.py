"""
Base interface for memory retrieval strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ai_team.memory.models import (
    MemoryContext,
    MemoryEntry,
    MemoryQuery,
    MemorySearchResult,
)

class BaseRetriever(ABC):
    """
    Base interface implemented by every memory retrieval strategy.
    """

    @abstractmethod
    async def search(
        self,
        query: MemoryQuery,
    ) -> MemorySearchResult:
        """
        Retrieve memories.
        """
        ...

    @abstractmethod
    async def build_context(
        self,
        query: MemoryQuery,
    ) -> MemoryContext:
        """
        Build the context supplied to an agent.
        """
        ...

