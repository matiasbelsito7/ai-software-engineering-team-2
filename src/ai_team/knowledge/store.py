"""
Knowledge base store - persistent knowledge storage.
"""

from __future__ import annotations

import logging
import re

from ai_team.knowledge.models import (
    KnowledgeEntry,
    KnowledgeSearchResult,
    KnowledgeStats,
    KnowledgeType,
)

logger = logging.getLogger(__name__)


class KnowledgeStore:
    """In-memory knowledge base store with search capabilities."""

    def __init__(self) -> None:
        self._entries: dict[str, KnowledgeEntry] = {}
        self._tags: dict[str, set[str]] = {}
        self._categories: dict[str, set[str]] = {}

    def add(self, entry: KnowledgeEntry) -> None:
        """Add or update a knowledge entry."""
        if entry.entry_id in self._entries:
            existing = self._entries[entry.entry_id]
            # Update tags index
            for tag in existing.tags:
                if tag in self._tags:
                    self._tags[tag].discard(entry.entry_id)
            for cat in (existing.category,):
                if cat and cat in self._categories:
                    self._categories[cat].discard(entry.entry_id)

        self._entries[entry.entry_id] = entry

        # Update indexes
        for tag in entry.tags:
            if tag not in self._tags:
                self._tags[tag] = set()
            self._tags[tag].add(entry.entry_id)

        if entry.category:
            if entry.category not in self._categories:
                self._categories[entry.category] = set()
            self._categories[entry.category].add(entry.entry_id)

        logger.info("Added knowledge entry: %s", entry.entry_id)

    def get(self, entry_id: str) -> KnowledgeEntry | None:
        """Get a knowledge entry by ID."""
        return self._entries.get(entry_id)

    def delete(self, entry_id: str) -> bool:
        """Delete a knowledge entry."""
        if entry_id not in self._entries:
            return False

        entry = self._entries.pop(entry_id)

        # Clean up indexes
        for tag in entry.tags:
            if tag in self._tags:
                self._tags[tag].discard(entry_id)
        if entry.category and entry.category in self._categories:
            self._categories[entry.category].discard(entry_id)

        logger.info("Deleted knowledge entry: %s", entry_id)
        return True

    def search(
        self,
        query: str,
        knowledge_type: KnowledgeType | None = None,
        category: str | None = None,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[KnowledgeSearchResult]:
        """Search knowledge base with scoring."""
        results: list[KnowledgeSearchResult] = []

        query_lower = query.lower()
        query_words = set(query_lower.split())

        for entry in self._entries.values():
            # Filter by type
            if knowledge_type and entry.knowledge_type != knowledge_type:
                continue

            # Filter by category
            if category and entry.category != category:
                continue

            # Filter by tags
            if tags:
                entry_tags = set(entry.tags)
                if not set(tags).intersection(entry_tags):
                    continue

            # Calculate relevance score
            score = self._calculate_score(entry, query_lower, query_words)

            if score > 0:
                highlights = self._extract_highlights(entry, query_words)
                results.append(
                    KnowledgeSearchResult(
                        entry=entry,
                        score=score,
                        highlights=highlights,
                    )
                )

        # Sort by score descending
        results.sort(key=lambda r: r.score, reverse=True)

        return results[:limit]

    def _calculate_score(
        self,
        entry: KnowledgeEntry,
        query_lower: str,
        query_words: set[str],
    ) -> float:
        """Calculate relevance score for an entry."""
        score = 0.0

        # Title match (highest weight)
        title_lower = entry.title.lower()
        if query_lower in title_lower:
            score += 1.0
        elif query_words.issubset(set(title_lower.split())):
            score += 0.8

        # Content match
        content_lower = entry.content.lower()
        if query_lower in content_lower:
            score += 0.6
        else:
            word_matches = sum(1 for w in query_words if w in content_lower)
            if word_matches:
                score += 0.3 * (word_matches / len(query_words))

        # Tag match
        tag_matches = len(set(entry.tags).intersection(query_words))
        if tag_matches:
            score += 0.2 * (tag_matches / len(query_words))

        # Exact tag match
        for tag in entry.tags:
            if query_lower in tag.lower():
                score += 0.4

        return min(score, 1.0)

    def _extract_highlights(
        self,
        entry: KnowledgeEntry,
        query_words: set[str],
    ) -> list[str]:
        """Extract relevant snippets from entry."""
        highlights = []

        # Check title
        if any(w in entry.title.lower() for w in query_words):
            highlights.append(entry.title)

        # Check content for relevant sentences
        sentences = re.split(r"[.!?]+", entry.content)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(w in sentence.lower() for w in query_words) and len(sentence) > 20:
                highlights.append(sentence[:200])
                if len(highlights) >= 3:
                    break

        return highlights

    def list_entries(
        self,
        knowledge_type: KnowledgeType | None = None,
        category: str | None = None,
        tags: list[str] | None = None,
    ) -> list[KnowledgeEntry]:
        """List entries with optional filters."""
        entries = list(self._entries.values())

        if knowledge_type:
            entries = [e for e in entries if e.knowledge_type == knowledge_type]
        if category:
            entries = [e for e in entries if e.category == category]
        if tags:
            tag_set = set(tags)
            entries = [e for e in entries if tag_set.intersection(e.tags)]

        return sorted(entries, key=lambda e: e.entry_id)

    def get_stats(self) -> KnowledgeStats:
        """Get knowledge base statistics."""
        by_type: dict[str, int] = {}
        by_category: dict[str, int] = {}
        all_tags: set[str] = set()

        for entry in self._entries.values():
            by_type[entry.knowledge_type] = by_type.get(entry.knowledge_type, 0) + 1
            if entry.category:
                by_category[entry.category] = by_category.get(entry.category, 0) + 1
            all_tags.update(entry.tags)

        return KnowledgeStats(
            total_entries=len(self._entries),
            by_type=by_type,
            by_category=by_category,
            total_tags=len(all_tags),
        )

    @property
    def count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        """Clear all entries."""
        self._entries.clear()
        self._tags.clear()
        self._categories.clear()
