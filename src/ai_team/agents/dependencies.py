"""
Shared dependencies for AI agents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai_team.agents.tools import AgentTools
    from ai_team.context.manager import ContextManager
    from ai_team.infrastructure.llm.base import BaseLLM
    from ai_team.memory.manager import MemoryManager
    from ai_team.rag.manager import RAGManager
    from ai_team.tools.executor import ToolExecutor


@dataclass(slots=True)
class AgentDependencies:
    """
    Shared dependencies injected into every agent.
    """

    # =========================================================================
    # Core Infrastructure
    # =========================================================================

    llm: BaseLLM

    # =========================================================================
    # Agent Tools
    # =========================================================================

    tools: AgentTools

    tool_executor: ToolExecutor

    # =========================================================================
    # Context / Knowledge
    # =========================================================================

    context: ContextManager

    memory: MemoryManager

    rag: RAGManager

    # =========================================================================
    # Optional Infrastructure
    # =========================================================================

    logger: Any | None = None

    settings: Any | None = None

    event_bus: Any | None = None

    telemetry: Any | None = None

    observability: Any | None = None
