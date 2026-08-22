"""
Knowledge base API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeEntrySchema(BaseModel):
    """Knowledge entry schema."""

    model_config = ConfigDict(extra="forbid")

    entry_id: str
    title: str
    content: str
    knowledge_type: str
    tags: list[str]
    category: str | None = None
    source: str | None = None
    version: int = 1
    created_at: str
    updated_at: str | None = None


class KnowledgeSearchResultSchema(BaseModel):
    """Knowledge search result schema."""

    model_config = ConfigDict(extra="forbid")

    entry: KnowledgeEntrySchema
    score: float
    highlights: list[str]


class KnowledgeSearchResponse(BaseModel):
    """Knowledge search response."""

    model_config = ConfigDict(extra="forbid")

    query: str
    results: list[KnowledgeSearchResultSchema]
    total: int


class KnowledgeCreateRequest(BaseModel):
    """Request to create knowledge entry."""

    model_config = ConfigDict(extra="forbid")

    entry_id: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1, max_length=50000)
    knowledge_type: str
    tags: list[str] = Field(default_factory=list)
    category: str | None = None
    source: str | None = None


class KnowledgeListResponse(BaseModel):
    """List of knowledge entries."""

    model_config = ConfigDict(extra="forbid")

    entries: list[KnowledgeEntrySchema]
    total: int


class KnowledgeStatsSchema(BaseModel):
    """Knowledge base statistics."""

    model_config = ConfigDict(extra="forbid")

    total_entries: int
    by_type: dict[str, int]
    by_category: dict[str, int]
    total_tags: int
