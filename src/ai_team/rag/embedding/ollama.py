"""
Ollama embedding provider.
"""

from __future__ import annotations

import httpx

from ai_team.rag.embedding.base import BaseEmbeddingProvider
from ai_team.rag.embedding.models import (
    EMBEDDING_MODELS,
    EmbeddingModel,
)
from ai_team.shared.enums.rag import (
    EmbeddingProviderType,
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

        embedding_model = EMBEDDING_MODELS[model]

        if embedding_model.provider != EmbeddingProviderType.OLLAMA:
            raise ValueError(
                f"{model} is not an Ollama embedding model."
            )

        self._model: EmbeddingModel = embedding_model

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
        return self._model.name

    @property
    def dimensions(
        self,
    ) -> int:
        return self._model.dimensions

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        response = await self._client.post(
            "/api/embed",
            json={
                "model": self.model,
                "input": text,
            },
        )

        response.raise_for_status()

        embedding = response.json()["embeddings"][0]

        if len(embedding) != self.dimensions:
            raise RuntimeError(
                "Embedding dimension mismatch."
            )

        return embedding

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        response = await self._client.post(
            "/api/embed",
            json={
                "model": self.model,
                "input": texts,
            },
        )

        response.raise_for_status()

        embeddings = response.json()["embeddings"]

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

        await self._client.aclose()