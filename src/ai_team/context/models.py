"""
Context models.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ContextWindow(BaseModel):
    """
    Context delivered to an agent.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    system_prompt: str | None = None

    conversation: list[str] = Field(
        default_factory=list,
    )

    memory: list[str] = Field(
        default_factory=list,
    )

    rag_documents: list[str] = Field(
        default_factory=list,
    )

    artifacts: list[str] = Field(
        default_factory=list,
    )


class ContextSummary(BaseModel):
    """
    Compressed conversation summary.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    summary: str

    source_messages: int

    compression_ratio: float


class ContextSelection(BaseModel):
    """
    Result of the context selection process.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    selected_messages: list[str] = Field(
        default_factory=list,
    )

    selected_memory: list[str] = Field(
        default_factory=list,
    )

    selected_documents: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )