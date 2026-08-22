"""
Templates router - CRUD for task templates.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Query

from ai_team.app.api.exceptions.errors import NotFoundError, ValidationError
from ai_team.app.api.schemas.templates import (
    CreateTaskFromTemplateRequest,
    TemplateListResponse,
    TemplateParameterSchema,
    TemplateRenderRequest,
    TemplateRenderResponse,
    TemplateResponse,
)
from ai_team.templates.builtin import builtin_registry

if TYPE_CHECKING:
    from ai_team.templates.models import TaskTemplate
    from ai_team.templates.registry import TemplateRegistry

logger = logging.getLogger(__name__)

router = APIRouter(tags=["templates"])

# Global registry instance (could be injected via DI)
_registry: TemplateRegistry | None = None


def _get_registry() -> TemplateRegistry:
    """Get or create the template registry."""
    global _registry
    if _registry is None:
        _registry = builtin_registry
    return _registry


def _template_to_response(template: TaskTemplate) -> TemplateResponse:
    """Convert a TaskTemplate to a TemplateResponse."""
    return TemplateResponse(
        template_id=template.template_id,
        name=template.name,
        description=template.description,
        category=template.category,
        parameters=[
            TemplateParameterSchema(
                name=p.name,
                description=p.description,
                type=p.param_type,
                default=p.default,
                required=p.required,
                choices=p.choices,
            )
            for p in template.parameters
        ],
        tags=template.tags,
        version=template.version,
        author=template.author,
    )


@router.get(
    "/templates",
    response_model=TemplateListResponse,
    summary="List all templates",
)
async def list_templates(
    category: str | None = Query(None, description="Filter by category"),
    tags: str | None = Query(None, description="Comma-separated tags to filter"),
    search: str | None = Query(None, description="Search by name or description"),
) -> TemplateListResponse:
    """List all available task templates."""
    registry = _get_registry()

    if search:
        templates = registry.search(search)
    else:
        tag_list = [t.strip() for t in tags.split(",")] if tags else None
        templates = registry.list_templates(category=category, tags=tag_list)

    return TemplateListResponse(
        templates=[_template_to_response(t) for t in templates],
        total=len(templates),
    )


@router.get(
    "/templates/{template_id}",
    response_model=TemplateResponse,
    summary="Get a template",
)
async def get_template(template_id: str) -> TemplateResponse:
    """Get a specific template by ID."""
    registry = _get_registry()
    template = registry.get(template_id)

    if template is None:
        raise NotFoundError(detail=f"Template '{template_id}' not found")

    return _template_to_response(template)


@router.post(
    "/templates/{template_id}/render",
    response_model=TemplateRenderResponse,
    summary="Render a template",
)
async def render_template(
    template_id: str,
    request: TemplateRenderRequest,
) -> TemplateRenderResponse:
    """Render a template with the given parameters."""
    registry = _get_registry()

    try:
        task, system_prompt = registry.render(template_id, request.params)
    except KeyError as e:
        raise NotFoundError(detail=str(e)) from e
    except ValueError as e:
        raise ValidationError(detail=str(e)) from e

    return TemplateRenderResponse(
        template_id=template_id,
        task=task,
        system_prompt=system_prompt,
    )


@router.post(
    "/templates/{template_id}/create-task",
    status_code=202,
    summary="Create a task from a template",
)
async def create_task_from_template(
    template_id: str,
    request: CreateTaskFromTemplateRequest,
) -> dict[str, Any]:
    """Create a new task by rendering a template with parameters."""
    registry = _get_registry()

    try:
        task, system_prompt = registry.render(template_id, request.params)
    except KeyError as e:
        raise NotFoundError(detail=str(e)) from e
    except ValueError as e:
        raise ValidationError(detail=str(e)) from e

    # Import here to avoid circular imports
    from ai_team.app.api.schemas.tasks import CreateTaskRequest

    # Create the task using the existing task creation logic
    _task_request = CreateTaskRequest(
        task=task,
        system_prompt=system_prompt,
        metadata=request.metadata or {},
    )

    # We need to call the create_task endpoint logic
    # For now, return the rendered task details
    return {
        "template_id": template_id,
        "task": task,
        "system_prompt": system_prompt,
        "metadata": request.metadata,
        "message": "Task rendered successfully. Use POST /tasks to create the task.",
    }
