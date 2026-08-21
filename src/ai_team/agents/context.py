"""
Agent execution context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from ai_team.context.manager import ContextManager
    from ai_team.graph.state import GraphState
    from ai_team.memory.manager import MemoryManager
    from ai_team.observability.manager import ObservationManager
    from ai_team.rag.manager import RAGManager
    from ai_team.tools.executor import ToolExecutor


@dataclass(slots=True)
class AgentContext:
    """
    Runtime context shared by every agent execution.

    It exposes the execution state together with every service
    an agent may need during its lifecycle.
    """

    state: GraphState

    tools: ToolExecutor

    memory: MemoryManager

    rag: RAGManager

    context: ContextManager

    observations: ObservationManager

    execution_id: UUID = field(
        default_factory=uuid4,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Read execution metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store execution metadata.
        """

        self.metadata[key] = value

    def update(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Update execution metadata.
        """

        self.metadata.update(
            kwargs,
        )

    def clear_metadata(
        self,
    ) -> None:
        """
        Remove every metadata entry.
        """

        self.metadata.clear()
