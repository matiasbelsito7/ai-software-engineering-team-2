"""
Base interface for embedding providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseEmbeddingProvider(ABC):
    """
    Base interface implemented by every embedding provider.
    """

    # ------------------------------------------------------------------
    # Single Embedding
    # ------------------------------------------------------------------

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """
        ...

    # ------------------------------------------------------------------
    # Batch Embedding
    # ------------------------------------------------------------------

    @abstractmethod
    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        ...

    # ------------------------------------------------------------------
    # Information
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def model_name(
        self,
    ) -> str:
        """
        Name of the embedding model.
        """
        ...

    @property
    @abstractmethod
    def dimensions(
        self,
    ) -> int:
        """
        Embedding dimensionality.
        """
        ...