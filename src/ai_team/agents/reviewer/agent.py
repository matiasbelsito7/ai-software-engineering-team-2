"""
Reviewer agent implementation.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers import ReviewerParser
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
            "Reviews software artifacts and provides actionable feedback."
        ),
    )

    PARSER = ReviewerParser

    PROMPT_BUILDER = ReviewerPromptBuilder