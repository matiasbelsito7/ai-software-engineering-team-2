"""
Prompt builder for the Spec agent.
"""

from ai_team.agents.prompt_builder import BasePromptBuilder


class SpecPromptBuilder(BasePromptBuilder):
    PROMPTS_PACKAGE = "ai_team.agents.spec.prompts"

    TASK_PROMPT = "generate_spec.md"
