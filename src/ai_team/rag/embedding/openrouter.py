"""
OpenRouter embedding provider.
"""

from __future__ import annotations

from ai_team.rag.embedding.base import BaseEmbeddingProvider


class OpenRouterEmbeddingProvider(BaseEmbeddingProvider):
    """
    Embedding provider backed by OpenRouter.
    """

    def __init__(
        self,
        *,
        model: str,
    ) -> None:
        self._model = model

    async def embed(
        self,
        text: str,
    ) -> list[float]:
        raise NotImplementedError

    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        raise NotImplementedError

    @property
    def model_name(
        self,
    ) -> str:
        return self._model

    @property
    def dimensions(
        self,
    ) -> int:
        raise NotImplementedError