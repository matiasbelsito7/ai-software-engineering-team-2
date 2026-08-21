"""
Base interface for document retrieval.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.rag.models import (
        RAGContext,
        RetrievalQuery,
        RetrievalResult,
    )


class BaseRetriever(ABC):
    """
    Base interface implemented by every retriever.
    """

    @abstractmethod
    async def search(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """
        Retrieve relevant document chunks.
        """
        ...

    @abstractmethod
    async def build_context(
        self,
        query: RetrievalQuery,
    ) -> RAGContext:
        """
        Build the context injected into prompts.
        """
        ...
