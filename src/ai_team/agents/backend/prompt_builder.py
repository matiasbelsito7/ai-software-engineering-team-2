"""
Prompt builder for the Backend agent.
"""

from __future__ import annotations

from importlib.resources import files

from ai_team.agents.models import AgentExecution
from ai_team.infrastructure.llm.messages import Conversation


class BackendPromptBuilder:
    """
    Builds conversations for the Backend agent.
    """

    _PROMPTS_PACKAGE = "ai_team.agents.backend.prompts"

    @classmethod
    def build(
        cls,
        execution: AgentExecution,
    ) -> Conversation:
        """
        Build a conversation for backend implementation.
        """

        conversation = Conversation()

        conversation.add_system(
            cls._load_prompt("system.md"),
        )

        conversation.add_system(
            cls._load_prompt("implementation.md"),
        )

        conversation.add_user(
            execution.input,
        )

        return conversation

    @classmethod
    def build_refinement(
        cls,
        execution: AgentExecution,
        current_implementation: str,
    ) -> Conversation:
        """
        Build a conversation for backend refinement.
        """

        conversation = Conversation()

        conversation.add_system(
            cls._load_prompt("system.md"),
        )

        conversation.add_system(
            cls._load_prompt("refinement.md"),
        )

        conversation.add_user(
            execution.input,
        )

        conversation.add_assistant(
            current_implementation,
        )

        return conversation

    @classmethod
    def _load_prompt(
        cls,
        filename: str,
    ) -> str:
        """
        Load a prompt file.
        """

        return (
            files(cls._PROMPTS_PACKAGE)
            .joinpath(filename)
            .read_text(encoding="utf-8")
        )