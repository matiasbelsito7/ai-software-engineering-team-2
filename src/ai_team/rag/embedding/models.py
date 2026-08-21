"""
Embedding model registry.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from ai_team.shared.enums.rag import (
    EmbeddingProviderType,
)


class EmbeddingModel(BaseModel):
    """
    Metadata describing an embedding model.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    dimensions: int

    provider: EmbeddingProviderType


EMBEDDING_MODELS: dict[str, EmbeddingModel] = {

    #
    # Ollama
    #

    "nomic-embed-text": EmbeddingModel(
        name="nomic-embed-text",
        dimensions=768,
        provider=EmbeddingProviderType.OLLAMA,
    ),

    "mxbai-embed-large": EmbeddingModel(
        name="mxbai-embed-large",
        dimensions=1024,
        provider=EmbeddingProviderType.OLLAMA,
    ),

    "bge-m3": EmbeddingModel(
        name="bge-m3",
        dimensions=1024,
        provider=EmbeddingProviderType.OLLAMA,
    ),

    #
    # OpenRouter
    #

    "text-embedding-3-small": EmbeddingModel(
        name="text-embedding-3-small",
        dimensions=1536,
        provider=EmbeddingProviderType.OPENROUTER,
    ),

    "text-embedding-3-large": EmbeddingModel(
        name="text-embedding-3-large",
        dimensions=3072,
        provider=EmbeddingProviderType.OPENROUTER,
    ),
}
