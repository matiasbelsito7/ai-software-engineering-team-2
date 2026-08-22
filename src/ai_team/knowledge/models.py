"""
Knowledge base models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeType(StrEnum):
    """Types of knowledge entries."""

    CONCEPT = "concept"
    PROCEDURE = "procedure"
    REFERENCE = "reference"
    TROUBLESHOOTING = "troubleshooting"
    BEST_PRACTICE = "best_practice"
    PATTERN = "pattern"
    DECISION = "decision"


class KnowledgeEntry(BaseModel):
    """A single knowledge base entry."""

    model_config = ConfigDict(extra="forbid")

    entry_id: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1, max_length=50000)
    knowledge_type: KnowledgeType
    tags: list[str] = Field(default_factory=list)
    category: str | None = None
    source: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    related_entries: list[str] = Field(default_factory=list)
    version: int = 1
    created_at: str = Field(
        default_factory=lambda: __import__("datetime").datetime.utcnow().isoformat()
    )
    updated_at: str | None = None


class KnowledgeSearchResult(BaseModel):
    """Search result from knowledge base."""

    model_config = ConfigDict(extra="forbid")

    entry: KnowledgeEntry
    score: float = Field(ge=0.0, le=1.0)
    highlights: list[str] = Field(default_factory=list)


class KnowledgeStats(BaseModel):
    """Knowledge base statistics."""

    model_config = ConfigDict(extra="forbid")

    total_entries: int = 0
    by_type: dict[str, int] = Field(default_factory=dict)
    by_category: dict[str, int] = Field(default_factory=dict)
    total_tags: int = 0
