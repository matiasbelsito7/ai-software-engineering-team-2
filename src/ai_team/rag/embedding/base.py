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
    # Properties
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def model(
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
        Dimension of the embedding vectors produced by the model.
        """
        ...

    # ------------------------------------------------------------------
    # Embeddings
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
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    async def health(
        self,
    ) -> bool:
        """
        Check whether the provider is available.
        """
        ...

    @abstractmethod
    async def close(
        self,
    ) -> None:
        """
        Release any underlying resources.
        """
        ...
