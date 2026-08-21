"""
Prompt builder for the Architect agent.
"""

from ai_team.agents.prompt_builder import BasePromptBuilder


class ArchitectPromptBuilder(BasePromptBuilder):
    PROMPT_PACKAGE = "ai_team.agents.architect.prompts"

    TASK_PROMPT = "architecture.md"
