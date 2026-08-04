"""
Git agent.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.git.models import (
    GitResult,
)
from ai_team.agents.git.parser import (
    GitParser,
)
from ai_team.agents.git.prompt_builder import (
    GitPromptBuilder,
)
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
)
from ai_team.shared.enums import AgentCapability


class GitAgent(BaseAgent):
    """
    Agent responsible for organizing version control
    operations and project history.
    """

    INFO = AgentInfo(
        name="git",
        capability=AgentCapability.GIT,
        description=(
            "Organizes version control operations and "
            "project history."
        ),
    )

    PARSER = GitParser

    PROMPT_BUILDER = GitPromptBuilder

    async def run(
        self,
        execution: AgentExecution,
    ) -> GitResult:
        """
        Execute the Git workflow.
        """

        self.build_conversation(execution)

        return await self.generate_and_parse(
            execution,
        )