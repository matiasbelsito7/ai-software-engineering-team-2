"""
Exceptions used by the RAG subsystem.
"""

from __future__ import annotations


class RAGError(Exception):
    """
    Base exception for the RAG subsystem.
    """


class DocumentNotFoundError(RAGError):
    """
    Raised when a document cannot be found.
    """


class DocumentIndexingError(RAGError):
    """
    Raised when document indexing fails.
    """


class RetrievalError(RAGError):
    """
    Raised when document retrieval fails.
    """


class EmbeddingGenerationError(RAGError):
    """
    Raised when an embedding cannot be generated.
    """


class VectorStoreError(RAGError):
    """
    Raised when the vector store fails.
    """


class RAGConfigurationError(RAGError):
    """
    Raised when the RAG subsystem is incorrectly configured.
    """
