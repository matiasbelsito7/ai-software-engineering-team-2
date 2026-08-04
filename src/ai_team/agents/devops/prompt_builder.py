"""
Prompt builder for the DevOps agent.
"""

from __future__ import annotations

from pathlib import Path

from ai_team.agents.models import AgentExecution
from ai_team.agents.prompt_builder import BasePromptBuilder


class DevOpsPromptBuilder(BasePromptBuilder):
    """
    Prompt builder used by the DevOps agent.
    """

    PROMPTS_DIR = (
        Path(__file__).parent / "prompts"
    )

    SYSTEM_PROMPT = "system.md"

    TASK_PROMPT = "deployment.md"

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