"""
Embedding provider factory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.rag.embedding.ollama import (
    OllamaEmbeddingProvider,
)
from ai_team.rag.embedding.openrouter import (
    OpenRouterEmbeddingProvider,
)
from ai_team.shared.enums.rag import EmbeddingProviderType

if TYPE_CHECKING:
    from ai_team.rag.embedding.base import BaseEmbeddingProvider


class EmbeddingFactory:
    """
    Factory responsible for creating embedding providers.
    """

    def create(
        self,
        *,
        provider: EmbeddingProviderType,
        model: str,
    ) -> BaseEmbeddingProvider:
        """
        Create an embedding provider.
        """

        match provider:
            case EmbeddingProviderType.OLLAMA:
                return OllamaEmbeddingProvider(
                    model=model,
                )

            case EmbeddingProviderType.OPENROUTER:
                from ai_team.infrastructure.config.settings import (
                    settings,
                )

                return OpenRouterEmbeddingProvider(
                    api_key=settings.llm.openrouter_api_key,
                    model=model,
                )

            case _:
                raise ValueError(
                    f"Unsupported embedding provider: "
                    f"{provider!r}"
                )
