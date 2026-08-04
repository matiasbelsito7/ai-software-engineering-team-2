"""
Models shared by the RAG subsystem.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.shared.enums.rag import SourceType


# ============================================================================
# Document Source
# ============================================================================


class DocumentSource(BaseModel):
    """
    Origin of a document.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    uri: str

    type: SourceType

    title: str | None = None


# ============================================================================
# Document Metadata
# ============================================================================


class DocumentMetadata(BaseModel):
    """
    Additional metadata associated with a document.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    title: str | None = None

    language: str | None = None

    tags: list[str] = Field(
        default_factory=list,
    )


# ============================================================================
# Document
# ============================================================================


class Document(BaseModel):
    """
    Raw document before indexing.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    source: DocumentSource

    content: str

    metadata: DocumentMetadata

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


# ============================================================================
# Document Chunk
# ============================================================================


class DocumentChunk(BaseModel):
    """
    Indexed chunk of a document.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    document_id: UUID

    content: str

    embedding: list[float] | None = None

    metadata: DocumentMetadata

    chunk_index: int

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


# ============================================================================
# Retrieval Query
# ============================================================================


class RetrievalQuery(BaseModel):
    """
    Query submitted to the RAG system.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    query: str

    top_k: int = Field(
        default=5,
        ge=1,
        le=100,
    )


# ============================================================================
# Retrieved Chunk
# ============================================================================


class RetrievedChunk(BaseModel):
    """
    Retrieved chunk together with its relevance score.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    chunk: DocumentChunk

    score: float


# ============================================================================
# Retrieval Result
# ============================================================================


class RetrievalResult(BaseModel):
    """
    Result returned by a retriever.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    query: RetrievalQuery

    chunks: list[RetrievedChunk] = Field(
        default_factory=list,
    )


# ============================================================================
# RAG Context
# ============================================================================


class RAGContext(BaseModel):
    """
    Context injected into prompts.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    chunks: list[DocumentChunk] = Field(
        default_factory=list,
    )

    summary: str | None = None