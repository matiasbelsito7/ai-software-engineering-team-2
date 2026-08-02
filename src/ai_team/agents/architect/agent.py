"""
Architect agent implementation.
"""

from __future__ import annotations

from ai_team.agents.architect.models import ArchitectureDesign
from ai_team.agents.architect.prompt_builder import (
    ArchitectPromptBuilder,
)
from ai_team.agents.base import BaseAgent
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.agents.parsers import ArchitectParser
from ai_team.shared.enums import AgentCapability


class ArchitectAgent(BaseAgent):
    """
    AI agent responsible for designing the software architecture.
    """

    INFO = AgentInfo(
        name="architect",
        capability=AgentCapability.ARCHITECTURE,
        description=(
            "Designs the software architecture for "
            "the multi-agent system."
        ),
    )

    PARSER = ArchitectParser

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Build the architect conversation.
        """

        execution.conversation = (
            ArchitectPromptBuilder.build(
                execution,
            )
        )

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Generate the architecture design.
        """

        architecture: ArchitectureDesign = (
            await self.generate_and_parse(
                execution,
            )
        )

        return AgentResult(
            success=True,
            output=architecture,
        )