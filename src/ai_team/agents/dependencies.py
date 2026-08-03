"""
Shared dependencies for AI agents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ai_team.agents.tools import AgentTools
from ai_team.infrastructure.llm.base import BaseLLM


@dataclass(slots=True)
class AgentDependencies:
    """
    Shared dependencies injected into every agent.
    """

    # =========================================================================
    # Core Infrastructure
    # =========================================================================

    llm: BaseLLM

    logger: Any | None = None

    settings: Any | None = None

    # =========================================================================
    # Agent Tools
    # =========================================================================

    tools: AgentTools

    # =========================================================================
    # Optional Services
    # =========================================================================

    event_bus: Any | None = None

    telemetry: Any | None = None