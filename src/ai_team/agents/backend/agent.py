"""
Backend agent implementation.
"""

from __future__ import annotations

from ai_team.agents.backend.models import BackendResult
from ai_team.agents.backend.prompt_builder import (
    BackendPromptBuilder,
)
from ai_team.agents.base import BaseAgent
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.agents.parsers import BackendParser
from ai_team.shared.enums import AgentCapability


class BackendAgent(BaseAgent):
    """
    AI agent responsible for implementing backend functionality.
    """

    INFO = AgentInfo(
        name="backend",
        capability=AgentCapability.BACKEND,
        description=(
            "Implements backend functionality following "
            "the approved architecture."
        ),
    )

    PARSER = BackendParser

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Build the backend conversation.
        """

        execution.conversation = (
            BackendPromptBuilder.build(
                execution,
            )
        )

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Generate backend implementation.
        """

        implementation: BackendResult = (
            await self.generate_and_parse(
                execution,
            )
        )

        return AgentResult(
            success=True,
            output=implementation,
        )