"""
DevOps agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.agents.base import BaseAgent
from ai_team.agents.devops.prompt_builder import (
    DevOpsPromptBuilder,
)
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.devops import (
    DevOpsParser,
)
from ai_team.shared.enums import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.devops.models import (
        DevOpsResult,
    )
    from ai_team.agents.execution import AgentExecution


class DevOpsAgent(BaseAgent[Any]):
    """
    Agent responsible for generating deployment and
    infrastructure artifacts.
    """

    INFO = AgentInfo(
        name="devops",
        capability=AgentCapability.DEVOPS,
        description=(
            "Generates deployment infrastructure and "
            "CI/CD artifacts."
        ),
    )

    PARSER = DevOpsParser

    PROMPT_BUILDER = DevOpsPromptBuilder

    async def run(  # type: ignore[override]
        self,
        execution: AgentExecution,
    ) -> DevOpsResult:
        """
        Execute the DevOps workflow.
        """

        return await self.generate_and_parse(  # type: ignore[no-any-return]
            execution,
        )
