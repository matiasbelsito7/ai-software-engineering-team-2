"""
Template registry - manages available task templates.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai_team.templates.models import TaskTemplate

logger = logging.getLogger(__name__)


class TemplateRegistry:
    """Registry for task templates."""

    def __init__(self) -> None:
        self._templates: dict[str, TaskTemplate] = {}

    def register(self, template: TaskTemplate) -> None:
        """Register a template."""
        if template.template_id in self._templates:
            logger.warning(
                "Template '%s' already registered, overwriting",
                template.template_id,
            )
        self._templates[template.template_id] = template
        logger.info("Registered template: %s", template.template_id)

    def unregister(self, template_id: str) -> bool:
        """Unregister a template. Returns True if it existed."""
        if template_id in self._templates:
            del self._templates[template_id]
            logger.info("Unregistered template: %s", template_id)
            return True
        return False

    def get(self, template_id: str) -> TaskTemplate | None:
        """Get a template by ID."""
        return self._templates.get(template_id)

    def list_templates(
        self,
        category: str | None = None,
        tags: list[str] | None = None,
    ) -> list[TaskTemplate]:
        """List all templates, optionally filtered by category or tags."""
        templates = list(self._templates.values())

        if category is not None:
            templates = [t for t in templates if t.category == category]

        if tags is not None:
            tag_set = set(tags)
            templates = [t for t in templates if tag_set.intersection(t.tags)]

        return sorted(templates, key=lambda t: t.template_id)

    def search(self, query: str) -> list[TaskTemplate]:
        """Search templates by name or description."""
        query_lower = query.lower()
        return [
            t
            for t in self._templates.values()
            if query_lower in t.name.lower() or query_lower in t.description.lower()
        ]

    def render(
        self,
        template_id: str,
        params: dict[str, Any],
    ) -> tuple[str, str | None]:
        """Render a template with parameters."""
        template = self.get(template_id)
        if template is None:
            raise KeyError(f"Template '{template_id}' not found")
        return template.render(params)

    @property
    def count(self) -> int:
        """Number of registered templates."""
        return len(self._templates)

    def clear(self) -> None:
        """Remove all templates."""
        self._templates.clear()
