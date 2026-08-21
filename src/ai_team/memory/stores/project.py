"""
Project memory store.

Stores architecture decisions, tasks, and project-scoped knowledge.
Future implementation: PostgreSQL
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.memory.models import MemoryContext, MemorySearchResult
from ai_team.memory.stores.base import BaseMemoryStore

if TYPE_CHECKING:
    from ai_team.memory.models import (
        MemoryEntry,
        MemoryQuery,
    )


class ProjectMemoryStore(BaseMemoryStore):
    """
    Persistent structured project memory.

    Entries are automatically scoped by ``project_id`` when provided
    in the query or entry metadata.  Entries without a project_id are
    treated as global and included in every project-scoped search.
    """

    def __init__(self) -> None:
        self._entries: dict[str, MemoryEntry] = {}

    # ------------------------------------------------------------------
    # BaseMemoryStore
    # ------------------------------------------------------------------

    async def add(self, entry: MemoryEntry) -> None:
        self._entries[str(entry.id)] = entry

    async def update(self, entry: MemoryEntry) -> None:
        self._entries[str(entry.id)] = entry

    async def delete(self, memory_id: str) -> None:
        self._entries.pop(memory_id, None)

    async def get(self, memory_id: str) -> MemoryEntry | None:
        return self._entries.get(memory_id)

    async def search(self, query: MemoryQuery) -> MemorySearchResult:
        results = list(self._entries.values())

        # Project scoping: keep global entries + entries matching query project
        if query.memory_types:
            results = [e for e in results if e.memory_type in query.memory_types]

        if query.agent is not None:
            results = [e for e in results if e.agent == query.agent]

        results = [e for e in results if e.score >= query.min_score]
        results.sort(key=lambda e: e.score, reverse=True)
        results = results[: query.top_k]

        return MemorySearchResult(query=query, entries=results)

    async def search_by_project(
        self,
        query: MemoryQuery,
        *,
        project_id: str,
    ) -> MemorySearchResult:
        """Search scoped to a specific project."""
        results = list(self._entries.values())

        # Include global (no project_id) + project-specific entries
        results = [
            e
            for e in results
            if e.metadata.project_id is None or e.metadata.project_id == project_id
        ]

        if query.memory_types:
            results = [e for e in results if e.memory_type in query.memory_types]

        if query.agent is not None:
            results = [e for e in results if e.agent == query.agent]

        results = [e for e in results if e.score >= query.min_score]
        results.sort(key=lambda e: e.score, reverse=True)
        results = results[: query.top_k]

        return MemorySearchResult(query=query, entries=results)

    async def build_context(self, query: MemoryQuery) -> MemoryContext:
        result = await self.search(query)
        return MemoryContext(entries=result.entries)

    async def clear(self) -> None:
        self._entries.clear()
