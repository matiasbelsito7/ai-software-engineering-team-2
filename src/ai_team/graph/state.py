"""
Graph state models.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ai_team.agents.feedback_state import FeedbackState

if TYPE_CHECKING:
    from ai_team.agents.result import AgentResult
    from ai_team.agents.spec.models import AppSpecification
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


class BudgetState(BaseModel):
    """
    Budget and tier configuration for the workflow.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    tier: str = "free"

    tokens_budget: int = 50_000

    tokens_used: int = 0

    max_iterations: int = 2

    iterations_used: int = 0

    project_id: str | None = None

    @property
    def tokens_remaining(self) -> int:
        """Remaining token budget."""
        return max(0, self.tokens_budget - self.tokens_used)

    @property
    def budget_exhausted(self) -> bool:
        """Check if budget is exhausted."""
        return self.tokens_used >= self.tokens_budget

    @property
    def iterations_exhausted(self) -> bool:
        """Check if iteration limit is reached."""
        return self.iterations_used >= self.max_iterations


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

    feedback: FeedbackState = Field(
        default_factory=FeedbackState,
    )

    budget: BudgetState = Field(
        default_factory=BudgetState,
    )

    specification: AppSpecification | None = None
