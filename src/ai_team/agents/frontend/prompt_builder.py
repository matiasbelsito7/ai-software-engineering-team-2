"""
Prompt builder for the Frontend agent.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.agents.execution import AgentExecution
from ai_team.agents.prompt_builder import BasePromptBuilder


class FrontendPromptBuilder(BasePromptBuilder):
    """
    Prompt builder used by the Frontend agent.
    """

    PROMPTS_DIR = (
        Path(__file__).parent / "prompts"
    )

    SYSTEM_PROMPT = "system.md"

    TASK_PROMPT = "frontend.md"

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