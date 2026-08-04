"""
Models shared by the memory subsystem.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.shared.enums import (
    AgentCapability,
    MemoryType,
)


# ============================================================================
# Memory Metadata
# ============================================================================


class MemoryMetadata(BaseModel):
    """
    Additional metadata associated with a memory.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    source: str | None = None

    tags: list[str] = Field(
        default_factory=list,
    )

    project_id: str | None = None

    task_id: str | None = None


# ============================================================================
# Memory Entry
# ============================================================================


class MemoryEntry(BaseModel):
    """
    Single memory item.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    memory_type: MemoryType

    content: str

    agent: AgentCapability | None = None

    score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    embedding: list[float] | None = None

    metadata: MemoryMetadata = Field(
        default_factory=MemoryMetadata,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


# ============================================================================
# Memory Query
# ============================================================================


class MemoryQuery(BaseModel):
    """
    Query used to retrieve memories.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    query: str

    memory_types: list[MemoryType] = Field(
        default_factory=list,
    )

    agent: AgentCapability | None = None

    top_k: int = Field(
        default=5,
        ge=1,
        le=100,
    )

    min_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


# ============================================================================
# Memory Search Result
# ============================================================================


class MemorySearchResult(BaseModel):
    """
    Result of a memory retrieval.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    query: MemoryQuery

    entries: list[MemoryEntry] = Field(
        default_factory=list,
    )


# ============================================================================
# Memory Context
# ============================================================================


class MemoryContext(BaseModel):
    """
    Context returned to an agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    entries: list[MemoryEntry] = Field(
        default_factory=list,
    )

    summary: str | None = None