"""
Embedding model registry.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class EmbeddingModel(BaseModel):
    """
    Embedding model metadata.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    dimensions: int

    provider: str


EMBEDDING_MODELS: dict[str, EmbeddingModel] = {

    #
    # Ollama
    #

    "nomic-embed-text": EmbeddingModel(
        name="nomic-embed-text",
        dimensions=768,
        provider="ollama",
    ),

    "mxbai-embed-large": EmbeddingModel(
        name="mxbai-embed-large",
        dimensions=1024,
        provider="ollama",
    ),

    "bge-m3": EmbeddingModel(
        name="bge-m3",
        dimensions=1024,
        provider="ollama",
    ),

    #
    # OpenRouter
    #

    "text-embedding-3-small": EmbeddingModel(
        name="text-embedding-3-small",
        dimensions=1536,
        provider="openrouter",
    ),

    "text-embedding-3-large": EmbeddingModel(
        name="text-embedding-3-large",
        dimensions=3072,
        provider="openrouter",
    ),
}