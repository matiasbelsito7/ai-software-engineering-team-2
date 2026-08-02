"""
Shared dependencies for AI agents.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from ai_team.infrastructure.llm.factory import LLMFactory

if TYPE_CHECKING:
    from ai_team.memory.base import BaseMemory
    from ai_team.rag.base import BaseRAG
    from ai_team.observability.telemetry import TelemetryService
    from ai_team.tools.registry import ToolRegistry


class AgentDependencies(BaseModel):
    """
    Shared services available to every agent.

    New services can be added here without changing
    the constructor of every agent.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
    )

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    llm_factory: LLMFactory

    # ------------------------------------------------------------------
    # Optional Services
    # ------------------------------------------------------------------

    memory: "BaseMemory | None" = None

    rag: "BaseRAG | None" = None

    telemetry: "TelemetryService | None" = None

    tools: "ToolRegistry | None" = None