"""
DevOps agent.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.devops.models import (
    DevOpsResult,
)
from ai_team.agents.devops.parser import (
    DevOpsParser,
)
from ai_team.agents.devops.prompt_builder import (
    DevOpsPromptBuilder,
)
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
)
from ai_team.shared.enums import AgentCapability


class DevOpsAgent(BaseAgent):
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

    async def run(
        self,
        execution: AgentExecution,
    ) -> DevOpsResult:
        """
        Execute the DevOps workflow.
        """

        self.build_conversation(execution)

        return await self.generate_and_parse(
            execution,
        )