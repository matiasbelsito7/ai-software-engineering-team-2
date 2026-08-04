"""
Prompt builder for the Documentation agent.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.agents.models import AgentExecution
from ai_team.agents.prompt_builder import BasePromptBuilder


class DocumentationPromptBuilder(BasePromptBuilder):
    """
    Prompt builder used by the Documentation agent.
    """

    PROMPTS_DIR = (
        Path(__file__).parent / "prompts"
    )

    SYSTEM_PROMPT = "system.md"

    TASK_PROMPT = "documentation.md"

    REFINEMENT_PROMPT = "refinement.md"

    @classmethod
    def build_user_prompt(
        cls,
        execution: AgentExecution,
    ) -> str:
        """
        Build the user prompt.
        """

        return cls.render_context(execution)