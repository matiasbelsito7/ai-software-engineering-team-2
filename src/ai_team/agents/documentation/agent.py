"""
Documentation agent.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.documentation.models import (
    DocumentationResult,
)
from ai_team.agents.parsers.documentation import (
    DocumentationParser,
)
from ai_team.agents.documentation.prompt_builder import (
    DocumentationPromptBuilder,
)
from ai_team.agents.execution import AgentExecution
from ai_team.agents.info import AgentInfo
from ai_team.shared.enums import AgentCapability


class DocumentationAgent(BaseAgent):
    """
    Agent responsible for generating technical documentation
    from the artifacts produced by the software engineering team.
    """

    INFO = AgentInfo(
        name="documentation",
        capability=AgentCapability.DOCUMENTATION,
        description=(
            "Generates technical documentation for software projects."
        ),
    )

    PARSER = DocumentationParser

    PROMPT_BUILDER = DocumentationPromptBuilder

    async def run(
        self,
        execution: AgentExecution,
    ) -> DocumentationResult:
        """
        Execute the documentation workflow.
        """

        self.build_conversation(execution)

        return await self.generate_and_parse(
            execution,
        )