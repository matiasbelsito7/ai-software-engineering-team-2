"""
Planner Agent.
"""

from __future__ import annotations

from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.planner import PlannerParser
from ai_team.agents.planner.prompt_builder import PlannerPromptBuilder
from ai_team.shared.enums.agents import AgentCapability


class PlannerAgent(BaseAgent):
    """
    Agent responsible for decomposing a software-engineering
    task into an ordered implementation plan.
    """

    INFO = AgentInfo(
        name="planner",
        capability=AgentCapability.PLANNER,
        description=(
            "Analyzes a software-engineering task and produces "
            "an ordered implementation plan."
        ),
        version="1.0.0",
    )

    PARSER = PlannerParser

    PROMPT_BUILDER = PlannerPromptBuilder