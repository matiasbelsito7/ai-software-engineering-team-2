"""
Embedding providers.
"""

from ai_team.rag.embedding.base import BaseEmbeddingProvider
from ai_team.rag.embedding.factory import EmbeddingFactory
from ai_team.rag.embedding.ollama import OllamaEmbeddingProvider
from ai_team.rag.embedding.openrouter import (
    OpenRouterEmbeddingProvider,
)
from ai_team.rag.embedding.models import EMBEDDING_MODELS, EmbeddingModel

__all__ = [
    "BaseEmbeddingProvider",
    "EmbeddingFactory",
    "OllamaEmbeddingProvider",
    "OpenRouterEmbeddingProvider",
    "EMBEDDING_MODELS"
    "EmbeddingModel"
]