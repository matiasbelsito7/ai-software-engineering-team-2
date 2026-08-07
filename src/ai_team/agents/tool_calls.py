"""
Tool call models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field   


class AgentToolCall(BaseModel):
    """
    Tool invocation requested by an agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    arguments: dict[str, Any] = Field(
        default_factory=dict,
    )


class AgentToolResult(BaseModel):
    """
    Result returned by a tool.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str

    output: Any

    success: bool = True