"""
Shared domain models for the multi-agent system.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.infrastructure.llm.messages import Conversation
from ai_team.infrastructure.llm.responses import LLMResponse

class AgentStatus(StrEnum):
    """
    Execution status.
    """

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============================================================================
# Metadata
# ============================================================================


class AgentMetadata(BaseModel):
    """
    Execution metadata.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    finished_at: datetime | None = None

    duration_ms: float | None = None

    tokens: int | None = None

    cost: float | None = None


# ============================================================================
# Tool Calls
# ============================================================================


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


# ============================================================================
# Request
# ============================================================================


class AgentRequest(BaseModel):
    """
    Input received by an agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    task: str

    context: dict[str, Any] = Field(
        default_factory=dict,
    )


# ============================================================================
# Result
# ============================================================================


class AgentResult(BaseModel):
    """
    Result produced by an agent.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    status: AgentStatus

    output: str

    metadata: AgentMetadata = Field(
        default_factory=AgentMetadata,
    )

    tool_calls: list[AgentToolCall] = Field(
        default_factory=list,
    )

    tool_results: list[AgentToolResult] = Field(
        default_factory=list,
    )

    artifacts: dict[str, Any] = Field(
        default_factory=dict,
    )


# ============================================================================
# Execution
# ============================================================================


class AgentExecution(BaseModel):
    """
    Represents the complete lifecycle of an agent execution.

    This object is the central unit exchanged between the
    orchestration layer (LangGraph), the agents, the memory
    system and the observability layer.
    """

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )

    id: UUID = Field(
        default_factory=uuid4,
    )

    capability: AgentCapability

    request: AgentRequest

    conversation: Conversation = Field(
        default_factory=Conversation,
    )

    llm_response: LLMResponse | None = None

    result: AgentResult | None = None

    retries: int = 0

    metadata: AgentMetadata = Field(
        default_factory=AgentMetadata,
    )

    @property
    def completed(self) -> bool:
        """
        Whether the execution has completed.
        """
        return self.result is not None

    @property
    def successful(self) -> bool:
        """
        Whether the execution completed successfully.
        """
        return (
            self.result is not None
            and self.result.status is AgentStatus.SUCCESS
        )

class AgentInfo(BaseModel):
    name: str
    capability: AgentCapability
    description: str
    version: str = "1.0.0"