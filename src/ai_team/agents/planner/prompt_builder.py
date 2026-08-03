"""
Prompt builder for the Planner agent.
"""

from ai_team.agents.prompt_builder import BasePromptBuilder


class PlannerPromptBuilder(BasePromptBuilder):

    PROMPT_PACKAGE = "ai_team.agents.planner.prompts"

    TASK_PROMPT = "planning.md"