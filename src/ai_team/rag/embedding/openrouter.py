"""
OpenRouter embedding provider.
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


class OpenRouterEmbeddingProvider(BaseEmbeddingProvider):
    """
    Embedding provider backed by OpenRouter.
    """

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        base_url: str = "https://openrouter.ai/api/v1",
        timeout: float = 120.0,
    ) -> None:

        if model not in EMBEDDING_MODELS:
            raise ValueError(
                f"Unsupported embedding model: {model}"
            )

        model_info = EMBEDDING_MODELS[model]

        if model_info.provider != "openrouter":
            raise ValueError(
                f"{model} is not an OpenRouter model."
            )

        self._model = model

        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
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
        return EMBEDDING_MODELS[
            self._model
        ].dimensions

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        response = await self._client.post(
            "/embeddings",
            json={
                "model": self._model,
                "input": text,
            },
        )

        response.raise_for_status()

        payload = response.json()

        embedding = payload["data"][0]["embedding"]

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
            "/embeddings",
            json={
                "model": self._model,
                "input": texts,
            },
        )

        response.raise_for_status()

        payload = response.json()

        embeddings = [
            item["embedding"]
            for item in payload["data"]
        ]

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
                "/models",
            )

            return response.is_success

        except Exception:
            return False

    async def close(
        self,
    ) -> None:

        await self._client.aclose()