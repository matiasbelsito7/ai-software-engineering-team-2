"""
Ollama embedding provider.
"""

from __future__ import annotations

import httpx

from ai_team.rag.embedding.base import (
    BaseEmbeddingProvider,
)
from ai_team.rag.embedding.models import (
    EMBEDDING_MODELS,
    EmbeddingModel
)


class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    """
    Embedding provider backed by Ollama.
    """

    def __init__(
        self,
        *,
        model: str,
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ) -> None:
        if model not in EMBEDDING_MODELS:
            raise ValueError(
                f"Unsupported embedding model: {model}"
            )

        self._model = model

        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def model(
        self,
    ) -> str:
        return self._model

    @property
    def dimensions(
        self,
    ) -> int:
        return EMBEDDING_MODELS[self._model]

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    async def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        response = await self._client.post(
            "/api/embed",
            json={
                "model": self._model,
                "input": text,
            },
        )

        response.raise_for_status()

        payload = response.json()

        embedding = payload["embeddings"][0]

        if len(embedding) != self.dimensions:
            raise RuntimeError(
                "Embedding dimension mismatch."
            )

        return embedding

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        if not texts:
            return []

        response = await self._client.post(
            "/api/embed",
            json={
                "model": self._model,
                "input": texts,
            },
        )

        response.raise_for_status()

        payload = response.json()

        embeddings = payload["embeddings"]

        for embedding in embeddings:
            if len(embedding) != self.dimensions:
                raise RuntimeError(
                    "Embedding dimension mismatch."
                )

        return embeddings

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def health(
        self,
    ) -> bool:
        """
        Check whether Ollama is available.
        """

        try:
            response = await self._client.get(
                "/api/tags",
            )

            return response.is_success

        except Exception:
            return False

    async def close(
        self,
    ) -> None:
        """
        Close the underlying HTTP client.
        """

        await self._client.aclose()