"""
Documentation agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.agents.base import BaseAgent
from ai_team.agents.documentation.prompt_builder import (
    DocumentationPromptBuilder,
)
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.documentation import (
    DocumentationParser,
)
from ai_team.shared.enums import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.documentation.models import (
        DocumentationResult,
    )
    from ai_team.agents.execution import AgentExecution


class DocumentationAgent(BaseAgent[Any]):
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

    async def run(  # type: ignore[override]
        self,
        execution: AgentExecution,
    ) -> DocumentationResult:
        """
        Execute the documentation workflow.
        """

        return await self.generate_and_parse(  # type: ignore[no-any-return]
            execution,
        )
