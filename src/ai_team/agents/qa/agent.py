"""
Quality Assurance agent.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.execution import AgentExecution
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.qa import QAParser
from ai_team.agents.qa.models import QAResult
from ai_team.agents.qa.prompt_builder import (
    QAPromptBuilder,
)
from ai_team.shared.enums import AgentCapability


class QAAgent(BaseAgent):
    """
    Agent responsible for validating the quality
    of the software artifacts produced by the team.
    """

    INFO = AgentInfo(
        name="qa",
        capability=AgentCapability.QA,
        description=(
            "Validates software quality and proposes "
            "quality improvements."
        ),
    )

    PARSER = QAParser

    PROMPT_BUILDER = QAPromptBuilder

    async def run(
        self,
        execution: AgentExecution,
    ) -> QAResult:
        """
        Execute the QA workflow.
        """

        self.build_conversation(execution)

        return await self.generate_and_parse(
            execution,
        )