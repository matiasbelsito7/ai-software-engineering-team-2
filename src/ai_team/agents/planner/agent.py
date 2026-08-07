"""
Planner agent implementation.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers import PlannerParser
from ai_team.agents.planner.prompt_builder import PlannerPromptBuilder
from ai_team.shared.enums.agents import AgentCapability


class PlannerAgent(BaseAgent):
    """
    AI agent responsible for planning software projects.
    """

    INFO = AgentInfo(
    name="planner",
    capability=AgentCapability.PLANNER,
    description=(
        "Creates implementation plans for software projects."
    ),
    )

    PARSER = PlannerParser

    PROMPT_BUILDER = PlannerPromptBuilder