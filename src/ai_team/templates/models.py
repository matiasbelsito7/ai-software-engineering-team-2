"""
Task template models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ParameterType(StrEnum):
    """Template parameter types."""

    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    CHOICE = "choice"


class TemplateParameter(BaseModel):
    """A single template parameter."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    param_type: ParameterType = Field(default=ParameterType.STRING)
    default: Any = None
    required: bool = True
    choices: list[str] | None = None
    min_value: int | None = None
    max_value: int | None = None

    def validate_value(self, value: Any) -> Any:
        """Validate and coerce a parameter value."""
        if value is None:
            if self.required and self.default is None:
                raise ValueError(f"Parameter '{self.name}' is required")
            return self.default

        if self.param_type == ParameterType.STRING:
            return str(value)
        if self.param_type == ParameterType.INTEGER:
            val = int(value)
            if self.min_value is not None and val < self.min_value:
                raise ValueError(f"Value must be >= {self.min_value}")
            if self.max_value is not None and val > self.max_value:
                raise ValueError(f"Value must be <= {self.max_value}")
            return val
        if self.param_type == ParameterType.BOOLEAN:
            return bool(value)
        # ParameterType.CHOICE
        if self.choices and value not in self.choices:
            raise ValueError(f"Value must be one of: {self.choices}")
        return str(value)


class TemplateCategory(StrEnum):
    """Template categories."""

    API = "api"
    MICROSERVICE = "microservice"
    DATA = "data"
    CLI = "cli"
    WEB = "web"
    UTILITY = "utility"


class TaskTemplate(BaseModel):
    """A reusable task template."""

    template_id: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9_]+$")
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    category: TemplateCategory
    parameters: list[TemplateParameter] = Field(default_factory=list)
    task_prompt: str = Field(..., min_length=1, max_length=50000)
    system_prompt: str | None = None
    tags: list[str] = Field(default_factory=list)
    version: str = "1.0.0"
    author: str | None = None

    def render(self, params: dict[str, Any]) -> tuple[str, str | None]:
        """Render the template with given parameters, returning (task, system_prompt)."""
        if self.parameters:
            validated: dict[str, Any] = {}
            for param in self.parameters:
                value = params.get(param.name)
                validated[param.name] = param.validate_value(value)
        else:
            validated = params

        task = self.task_prompt.format(**validated) if validated else self.task_prompt
        system_prompt = (
            self.system_prompt.format(**validated)
            if self.system_prompt and validated
            else self.system_prompt
        )
        return task, system_prompt

    def list_parameters(self) -> list[dict[str, Any]]:
        """List all parameters with their metadata."""
        return [
            {
                "name": p.name,
                "description": p.description,
                "type": p.param_type,
                "default": p.default,
                "required": p.required,
                "choices": p.choices,
            }
            for p in self.parameters
        ]
