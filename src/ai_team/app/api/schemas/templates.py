"""
API schemas for task templates.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TemplateParameterSchema(BaseModel):
    """Template parameter metadata."""

    name: str
    description: str
    type: str
    default: Any = None
    required: bool = True
    choices: list[str] | None = None

    model_config = {"extra": "forbid"}


class TemplateResponse(BaseModel):
    """Template response schema."""

    template_id: str
    name: str
    description: str
    category: str
    parameters: list[TemplateParameterSchema]
    tags: list[str]
    version: str
    author: str | None = None

    model_config = {"extra": "forbid"}


class TemplateListResponse(BaseModel):
    """List of templates response."""

    templates: list[TemplateResponse]
    total: int

    model_config = {"extra": "forbid"}


class TemplateRenderRequest(BaseModel):
    """Request to render a template with parameters."""

    params: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "forbid"}


class TemplateRenderResponse(BaseModel):
    """Rendered template response."""

    template_id: str
    task: str
    system_prompt: str | None = None

    model_config = {"extra": "forbid"}


class CreateTaskFromTemplateRequest(BaseModel):
    """Request to create a task from a template."""

    params: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] | None = None

    model_config = {"extra": "forbid"}
