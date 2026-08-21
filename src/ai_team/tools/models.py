"""
Tool models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ToolRequest(BaseModel):
    """
    Generic tool execution request.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    tool: str = ""

    parameters: dict[str, Any] = Field(
        default_factory=dict,
    )


class ToolResult(BaseModel):
    """
    Generic tool execution result.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    success: bool

    output: Any | None = None

    error: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ToolDefinition(BaseModel):
    """
    Tool metadata.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    name: str

    description: str

    category: str

    enabled: bool = True
