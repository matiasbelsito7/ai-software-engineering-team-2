"""
Reviewer agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.reviewer import ReviewerParser
from ai_team.agents.result import AgentResult
from ai_team.agents.reviewer.models import ReviewerResult
from ai_team.agents.reviewer.prompt_builder import ReviewerPromptBuilder
from ai_team.shared.enums.agents import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class ReviewerAgent(BaseAgent[ReviewerResult]):
    """
    Agent responsible for reviewing source-code changes.

    Analyzes patches, identifies issues, evaluates their severity
    and category, and determines whether the changes should be
    approved.
    """

    INFO = AgentInfo(
        name="reviewer",
        capability=AgentCapability.REVIEWER,
        description=(
            "Reviews source-code changes, identifies issues, "
            "and determines whether the implementation should "
            "be approved."
        ),
        version="1.0.0",
    )

    PARSER = ReviewerParser

    PROMPT_BUILDER = ReviewerPromptBuilder

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Validate the Reviewer execution.
        """

        super().validate(execution)

        if execution.capability is not self.capability:
            raise ValueError(
                "ReviewerAgent received an execution for "
                f"capability '{execution.capability.value}'."
            )

        if not execution.request.task.strip():
            raise ValueError(
                "ReviewerAgent requires a non-empty task."
            )

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the review process.

        The LLM response is parsed into a ReviewerResult.
        """

        review = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=review,
            message="Code review completed successfully.",
        )
