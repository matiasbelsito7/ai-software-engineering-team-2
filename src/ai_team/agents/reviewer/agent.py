"""
Reviewer agent implementation.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.agents.parsers import ReviewerParser
from ai_team.agents.reviewer.models import ReviewerResult
from ai_team.agents.reviewer.prompt_builder import (
    ReviewerPromptBuilder,
)
from ai_team.shared.enums import AgentCapability


class ReviewerAgent(BaseAgent):
    """
    AI agent responsible for reviewing software artifacts.
    """

    INFO = AgentInfo(
        name="reviewer",
        capability=AgentCapability.REVIEWER,
        description=(
            "Reviews software artifacts and provides "
            "actionable feedback."
        ),
    )

    PARSER = ReviewerParser

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Build the reviewer conversation.
        """

        execution.conversation = (
            ReviewerPromptBuilder.build(
                execution,
            )
        )

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Review the provided artifacts.
        """

        review: ReviewerResult = (
            await self.generate_and_parse(
                execution,
            )
        )

        return AgentResult(
            success=True,
            output=review,
        )