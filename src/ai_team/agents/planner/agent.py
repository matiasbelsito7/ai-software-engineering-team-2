"""
Planner agent implementation.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.agents.parsers import PlannerParser
from ai_team.agents.planner.prompt_builder import (
    PlannerPromptBuilder,
)
from ai_team.shared.enums import AgentCapability


class PlannerAgent(BaseAgent):
    """
    AI agent responsible for generating execution plans.
    """

    INFO = AgentInfo(
        name="planner",
        capability=AgentCapability.PLANNING,
        description=(
            "Generates structured execution plans "
            "for the multi-agent system."
        ),
    )

    PARSER = PlannerParser

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Build the planner conversation.
        """

        execution.conversation = (
            PlannerPromptBuilder.build(
                execution,
            )
        )

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Generate an execution plan.
        """

        plan = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=plan,
        )