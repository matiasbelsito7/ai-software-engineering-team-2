"""
Retrieval-Augmented Generation subsystem.
"""

from ai_team.rag.exceptions import (
    DocumentIndexingError,
    DocumentNotFoundError,
    EmbeddingGenerationError,
    RAGConfigurationError,
    RAGError,
    RetrievalError,
    VectorStoreError,
)
from ai_team.rag.factory import build_rag
from ai_team.rag.manager import RAGManager
from ai_team.rag.models import (
    Document,
    DocumentChunk,
    DocumentMetadata,
    RAGContext,
    RetrievalQuery,
    RetrievalResult,
    RetrievedChunk,
)

__all__ = [
    # Models
    "Document",
    "DocumentChunk",
    "DocumentIndexingError",
    "DocumentMetadata",
    "DocumentNotFoundError",
    "EmbeddingGenerationError",
    "RAGConfigurationError",
    "RAGContext",
    # Exceptions
    "RAGError",
    # Manager
    "RAGManager",
    "RetrievalError",
    "RetrievalQuery",
    "RetrievalResult",
    "RetrievedChunk",
    "VectorStoreError",
    # Factories
    "build_rag",
]
