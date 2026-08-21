"""
Base prompt builder for AI agents.
"""

from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING

from ai_team.infrastructure.llm.messages import Conversation

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class BasePromptBuilder:
    """
    Base class for prompt builders.

    Subclasses must define ``PROMPTS_PACKAGE`` and ``TASK_PROMPT``.
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
            execution.request.task,
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
            execution.request.task,
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

        if not cls.PROMPTS_PACKAGE:
            raise RuntimeError(f"{cls.__name__} does not define PROMPTS_PACKAGE.")

        if not cls.TASK_PROMPT:
            raise RuntimeError(f"{cls.__name__} does not define TASK_PROMPT.")

        return (
            files(cls.PROMPTS_PACKAGE)
            .joinpath(filename)
            .read_text(
                encoding="utf-8",
            )
        )
