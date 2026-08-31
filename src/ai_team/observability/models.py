"""
Observability models.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.shared.enums.observability import (
    ExecutionStatus,
    LLMProvider,
    ToolType,
)


class AgentExecution(BaseModel):
    """
    Represents one agent execution.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    execution_id: UUID

    agent: str

    status: ExecutionStatus = ExecutionStatus.RUNNING

    started_at: datetime

    finished_at: datetime | None = None


class LLMCall(BaseModel):
    """
    Represents one LLM invocation.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    execution_id: UUID

    agent: str

    provider: LLMProvider

    model: str

    prompt_tokens: int

    completion_tokens: int

    latency_ms: float

    timestamp: datetime

    @property
    def total_tokens(
        self,
    ) -> int:
        return self.prompt_tokens + self.completion_tokens


class ToolCall(BaseModel):
    """
    Represents one tool invocation.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    execution_id: UUID

    agent: str

    tool: ToolType

    latency_ms: float

    success: bool

    timestamp: datetime
