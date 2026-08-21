"""
Prompt builder for the QA agent.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ai_team.agents.prompt_builder import BasePromptBuilder

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class QAPromptBuilder(BasePromptBuilder):
    """
    Prompt builder used by the QA agent.
    """

    PROMPTS_DIR = Path(__file__).parent / "prompts"

    SYSTEM_PROMPT = "system.md"

    TASK_PROMPT = "quality.md"

    REFINEMENT_PROMPT = "refinement.md"

    @classmethod
    def render_context(
        cls,
        execution: AgentExecution,
    ) -> str:
        conversation = cls.build(execution)
        return "\n\n".join(msg.content for msg in conversation.messages)

    @classmethod
    def build_user_prompt(
        cls,
        execution: AgentExecution,
    ) -> str:
        """
        Build the user prompt.
        """

        return cls.render_context(execution)
