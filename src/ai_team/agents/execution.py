"""
Agent execution models.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.infrastructure.llm.messages import Conversation

if TYPE_CHECKING:
    from ai_team.agents.result import AgentResult
    from ai_team.graph.state import GraphState
    from ai_team.infrastructure.llm.responses import LLMResponse
    from ai_team.shared.enums.agents import AgentCapability


class AgentStatus(StrEnum):
    """
    Execution status.
    """

    PENDING = "pending"

    RUNNING = "running"

    SUCCESS = "success"

    FAILED = "failed"

    CANCELLED = "cancelled"


# =====================================================================


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


# =====================================================================


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


# =====================================================================


class AgentExecution(BaseModel):
    """
    Represents one complete execution of an agent.
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

    graph_state: GraphState | None = None

    attempt: int = 1

    metadata: AgentMetadata = Field(
        default_factory=AgentMetadata,
    )

    @property
    def completed(
        self,
    ) -> bool:

        return self.result is not None

    @property
    def successful(
        self,
    ) -> bool:

        return self.result is not None and self.result.success
