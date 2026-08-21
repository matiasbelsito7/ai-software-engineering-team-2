"""
Frontend agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.agents.base import BaseAgent
from ai_team.agents.frontend.prompt_builder import (
    FrontendPromptBuilder,
)
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.frontend import (
    FrontendParser,
)
from ai_team.shared.enums import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution
    from ai_team.agents.frontend.models import (
        FrontendResult,
    )


class FrontendAgent(BaseAgent[Any]):
    """
    Agent responsible for implementing the presentation layer
    of the application.
    """

    INFO = AgentInfo(
        name="frontend",
        capability=AgentCapability.FRONTEND,
        description=(
            "Implements user interfaces and reusable "
            "frontend components."
        ),
    )

    PARSER = FrontendParser

    PROMPT_BUILDER = FrontendPromptBuilder

    async def run(  # type: ignore[override]
        self,
        execution: AgentExecution,
    ) -> FrontendResult:
        """
        Execute the frontend workflow.
        """

        return await self.generate_and_parse(  # type: ignore[no-any-return]
            execution,
        )
