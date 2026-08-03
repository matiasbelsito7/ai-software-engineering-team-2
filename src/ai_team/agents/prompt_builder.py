"""
Base prompt builder for AI agents.
"""

from __future__ import annotations

from abc import ABC
from importlib.resources import files

from ai_team.agents.models import AgentExecution
from ai_team.infrastructure.llm.messages import Conversation


class BasePromptBuilder(ABC):
    """
    Base class for prompt builders.
    """

    PROMPTS_PACKAGE: str = ""

    TASK_PROMPT: str = ""

    @classmethod
    def build(
        cls,
        execution: AgentExecution,
    ) -> Conversation:
        """
        Build the primary conversation.
        """

        conversation = Conversation()

        conversation.add_system(
            cls.load_prompt("system.md"),
        )

        conversation.add_system(
            cls.load_prompt(cls.TASK_PROMPT),
        )

        conversation.add_user(
            execution.input,
        )

        return conversation

    @classmethod
    def build_refinement(
        cls,
        execution: AgentExecution,
        previous_output: str,
    ) -> Conversation:
        """
        Build a refinement conversation.
        """

        conversation = Conversation()

        conversation.add_system(
            cls.load_prompt("system.md"),
        )

        conversation.add_system(
            cls.load_prompt("refinement.md"),
        )

        conversation.add_user(
            execution.input,
        )

        conversation.add_assistant(
            previous_output,
        )

        return conversation

    @classmethod
    def load_prompt(
        cls,
        filename: str,
    ) -> str:
        """
        Load a prompt file.
        """

        return (
            files(cls.PROMPTS_PACKAGE)
            .joinpath(filename)
            .read_text(encoding="utf-8")
        )