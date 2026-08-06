"""
Graph state models.
"""

from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.models import AgentResult
from ai_team.memory.models import MemoryContext
from ai_team.rag.models import RAGContext


class ConversationState(BaseModel):
    """
    Conversation shared across all agents.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    user_request: str

    system_prompt: str | None = None

    conversation_history: list[str] = Field(
        default_factory=list,
    )


class ExecutionState(BaseModel):
    """
    Runtime execution metadata.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    execution_id: UUID = Field(
        default_factory=uuid4,
    )

    current_agent: str | None = None

    previous_agent: str | None = None

    iteration: int = 0

    max_iterations: int = 20

    completed: bool = False


class ArtifactState(BaseModel):
    """
    Generated artifacts.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    results: list[AgentResult] = Field(
        default_factory=list,
    )

    shared_files: dict[str, str] = Field(
        default_factory=dict,
    )


class GraphState(BaseModel):
    """
    Global state shared by every LangGraph node.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    conversation: ConversationState

    execution: ExecutionState

    memory: MemoryContext | None = None

    rag: RAGContext | None = None

    artifacts: ArtifactState = Field(
        default_factory=ArtifactState,
    )