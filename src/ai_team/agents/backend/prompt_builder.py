"""
Prompt builder for the Backend agent.
"""

from ai_team.agents.prompt_builder import BasePromptBuilder


class BackendPromptBuilder(BasePromptBuilder):
    PROMPTS_PACKAGE = "ai_team.agents.backend.prompts"

    TASK_PROMPT = "implementation.md"
