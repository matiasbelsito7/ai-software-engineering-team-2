"""
Embedding provider factory.
"""

from __future__ import annotations

from ai_team.rag.embedding.base import BaseEmbeddingProvider
from ai_team.rag.embedding.ollama import (
    OllamaEmbeddingProvider,
)
from ai_team.rag.embedding.openrouter import (
    OpenRouterEmbeddingProvider,
)
from ai_team.shared.enums import EmbeddingProvider


class EmbeddingFactory:
    """
    Factory responsible for creating embedding providers.
    """

    def create(
        self,
        *,
        provider: EmbeddingProvider,
        model: str,
    ) -> BaseEmbeddingProvider:
        """
        Create an embedding provider.
        """

        match provider:
            case EmbeddingProvider.OLLAMA:
                return OllamaEmbeddingProvider(
                    model=model,
                )

            case EmbeddingProvider.OPENROUTER:
                return OpenRouterEmbeddingProvider(
                    model=model,
                )

            case _:
                raise ValueError(
                    f"Unsupported embedding provider: "
                    f"{provider!r}"
                )