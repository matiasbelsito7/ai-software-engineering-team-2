"""
Embedding providers.
"""

from ai_team.rag.embedding.base import BaseEmbeddingProvider
from ai_team.rag.embedding.factory import EmbeddingFactory
from ai_team.rag.embedding.ollama import OllamaEmbeddingProvider
from ai_team.rag.embedding.openrouter import (
    OpenRouterEmbeddingProvider,
)

__all__ = [
    "BaseEmbeddingProvider",
    "EmbeddingFactory",
    "OllamaEmbeddingProvider",
    "OpenRouterEmbeddingProvider",
]