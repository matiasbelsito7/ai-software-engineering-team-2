"""
Knowledge base router.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Query

from ai_team.app.api.exceptions.errors import NotFoundError
from ai_team.app.api.schemas.knowledge import (
    KnowledgeCreateRequest,
    KnowledgeEntrySchema,
    KnowledgeListResponse,
    KnowledgeSearchResponse,
    KnowledgeSearchResultSchema,
    KnowledgeStatsSchema,
)
from ai_team.knowledge.models import KnowledgeEntry, KnowledgeType
from ai_team.knowledge.store import KnowledgeStore

logger = logging.getLogger(__name__)

router = APIRouter(tags=["knowledge"])

_store = KnowledgeStore()


def _entry_to_schema(entry: KnowledgeEntry) -> KnowledgeEntrySchema:
    return KnowledgeEntrySchema(
        entry_id=entry.entry_id,
        title=entry.title,
        content=entry.content,
        knowledge_type=entry.knowledge_type,
        tags=entry.tags,
        category=entry.category,
        source=entry.source,
        version=entry.version,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
    )


@router.post(
    "/knowledge",
    status_code=201,
    summary="Add knowledge entry",
)
async def add_knowledge(
    request_body: KnowledgeCreateRequest,
) -> dict[str, str]:
    """Add a new knowledge entry."""
    entry = KnowledgeEntry(
        entry_id=request_body.entry_id,
        title=request_body.title,
        content=request_body.content,
        knowledge_type=KnowledgeType(request_body.knowledge_type),
        tags=request_body.tags,
        category=request_body.category,
        source=request_body.source,
    )
    _store.add(entry)
    return {"status": "ok", "entry_id": entry.entry_id}


@router.get(
    "/knowledge/search",
    response_model=KnowledgeSearchResponse,
    summary="Search knowledge base",
)
async def search_knowledge(
    q: str = Query(..., min_length=1, description="Search query"),
    type: str | None = Query(None, description="Filter by knowledge type"),
    category: str | None = Query(None, description="Filter by category"),
    tags: str | None = Query(None, description="Comma-separated tags"),
    limit: int = Query(10, ge=1, le=100),
) -> KnowledgeSearchResponse:
    """Search the knowledge base."""
    knowledge_type = KnowledgeType(type) if type else None
    tag_list = [t.strip() for t in tags.split(",")] if tags else None

    results = _store.search(
        query=q,
        knowledge_type=knowledge_type,
        category=category,
        tags=tag_list,
        limit=limit,
    )

    return KnowledgeSearchResponse(
        query=q,
        results=[
            KnowledgeSearchResultSchema(
                entry=_entry_to_schema(r.entry),
                score=r.score,
                highlights=r.highlights,
            )
            for r in results
        ],
        total=len(results),
    )


@router.get(
    "/knowledge",
    response_model=KnowledgeListResponse,
    summary="List knowledge entries",
)
async def list_knowledge(
    type: str | None = Query(None),
    category: str | None = Query(None),
    tags: str | None = Query(None),
) -> KnowledgeListResponse:
    """List all knowledge entries."""
    knowledge_type = KnowledgeType(type) if type else None
    tag_list = [t.strip() for t in tags.split(",")] if tags else None

    entries = _store.list_entries(
        knowledge_type=knowledge_type,
        category=category,
        tags=tag_list,
    )

    return KnowledgeListResponse(
        entries=[_entry_to_schema(e) for e in entries],
        total=len(entries),
    )


@router.get(
    "/knowledge/{entry_id}",
    response_model=KnowledgeEntrySchema,
    summary="Get knowledge entry",
)
async def get_knowledge(entry_id: str) -> KnowledgeEntrySchema:
    """Get a specific knowledge entry."""
    entry = _store.get(entry_id)
    if entry is None:
        raise NotFoundError(detail=f"Knowledge entry '{entry_id}' not found")
    return _entry_to_schema(entry)


@router.delete(
    "/knowledge/{entry_id}",
    status_code=204,
    summary="Delete knowledge entry",
)
async def delete_knowledge(entry_id: str) -> None:
    """Delete a knowledge entry."""
    deleted = _store.delete(entry_id)
    if not deleted:
        raise NotFoundError(detail=f"Knowledge entry '{entry_id}' not found")


@router.get(
    "/knowledge/stats",
    response_model=KnowledgeStatsSchema,
    summary="Knowledge base statistics",
)
async def knowledge_stats() -> KnowledgeStatsSchema:
    """Get knowledge base statistics."""
    stats = _store.get_stats()
    return KnowledgeStatsSchema(
        total_entries=stats.total_entries,
        by_type=stats.by_type,
        by_category=stats.by_category,
        total_tags=stats.total_tags,
    )
