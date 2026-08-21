"""
Git agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.agents.base import BaseAgent
from ai_team.agents.git.prompt_builder import (
    GitPromptBuilder,
)
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.git import (
    GitParser,
)
from ai_team.shared.enums import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution
    from ai_team.agents.git.models import (
        GitResult,
    )


class GitAgent(BaseAgent[Any]):
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

    async def run(  # type: ignore[override]
        self,
        execution: AgentExecution,
    ) -> GitResult:
        """
        Execute the Git workflow.
        """

        return await self.generate_and_parse(  # type: ignore[no-any-return]
            execution,
        )
