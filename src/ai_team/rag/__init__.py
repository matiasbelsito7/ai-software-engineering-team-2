"""
Retrieval-Augmented Generation subsystem.
"""

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

__all__ = [
    # Manager
    "RAGManager",

    # Models
    "Document",
    "DocumentMetadata",
    "DocumentChunk",
    "RetrievalQuery",
    "RetrievalResult",
    "RAGContext",
    "RetrievedChunk",

    # Exceptions
    "RAGError",
    "DocumentNotFoundError",
    "DocumentIndexingError",
    "RetrievalError",
    "EmbeddingGenerationError",
    "VectorStoreError",
    "RAGConfigurationError",

    # Factories
    "build_rag",
]