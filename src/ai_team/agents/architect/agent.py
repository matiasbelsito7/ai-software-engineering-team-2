"""
Architect agent implementation.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.models import AgentInfo
from ai_team.agents.architect.prompt_builder import (
    ArchitectPromptBuilder,
)
from ai_team.agents.parsers import ArchitectParser
from ai_team.shared.enums import AgentCapability


class ArchitectAgent(BaseAgent):
    """
    AI agent responsible for designing software architectures.
    """

    INFO = AgentInfo(
        name="architect",
        capability=AgentCapability.ARCHITECT,
        description=(
            "Designs software architecture based on the execution plan."
        ),
    )

    PARSER = ArchitectParser

    PROMPT_BUILDER = ArchitectPromptBuilder