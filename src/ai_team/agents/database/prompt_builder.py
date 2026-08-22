"""
Prompt builder for the Database agent.
"""

from ai_team.agents.prompt_builder import BasePromptBuilder


class DatabasePromptBuilder(BasePromptBuilder):
    """
    Builds prompts for the Database agent.
    """

    PROMPTS_PACKAGE = "ai_team.agents.database.prompts"

    TASK_PROMPT = "schema.md"
