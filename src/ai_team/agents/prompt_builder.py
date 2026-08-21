"""
Base prompt builder for AI agents.
"""

from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING

from ai_team.infrastructure.llm.messages import Conversation

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution
    from ai_team.context.models import ContextWindow
    from ai_team.memory.models import MemoryContext
    from ai_team.rag.models import RAGContext


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
        *,
        rag_context: RAGContext | None = None,
        memory_context: MemoryContext | None = None,
        context_window: ContextWindow | None = None,
    ) -> Conversation:
        """
        Build the primary conversation with optional context injection.
        """

        conversation = Conversation()

        conversation.add_system(
            cls.load_prompt("system.md"),
        )

        conversation.add_system(
            cls.load_prompt(cls.TASK_PROMPT),
        )

        if context_window is not None:
            context_text = cls._format_context_window(context_window)
            if context_text:
                conversation.add_system(context_text)

        if rag_context is not None:
            rag_text = cls._format_rag_context(rag_context)
            if rag_text:
                conversation.add_system(rag_text)

        if memory_context is not None:
            memory_text = cls._format_memory_context(memory_context)
            if memory_text:
                conversation.add_system(memory_text)

        conversation.add_user(
            execution.request.task,
        )

        return conversation

    @classmethod
    def build_refinement(
        cls,
        execution: AgentExecution,
        previous_output: str,
        *,
        rag_context: RAGContext | None = None,
        memory_context: MemoryContext | None = None,
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

        if rag_context is not None:
            rag_text = cls._format_rag_context(rag_context)
            if rag_text:
                conversation.add_system(rag_text)

        if memory_context is not None:
            memory_text = cls._format_memory_context(memory_context)
            if memory_text:
                conversation.add_system(memory_text)

        conversation.add_user(
            execution.request.task,
        )

        conversation.add_assistant(
            previous_output,
        )

        return conversation

    @classmethod
    def _format_rag_context(
        cls,
        rag_context: RAGContext,
    ) -> str:
        """
        Format RAG context for injection into prompts.
        """

        if not rag_context.chunks:
            return ""

        parts = ["Relevant code and documentation retrieved from the repository:"]

        for i, chunk in enumerate(rag_context.chunks, 1):
            source = f" ({chunk.uri})" if chunk.uri else ""
            parts.append(f"\n[{i}]{source}:\n{chunk.content}")

        if rag_context.summary:
            parts.append(f"\nSummary: {rag_context.summary}")

        return "\n".join(parts)

    @classmethod
    def _format_memory_context(
        cls,
        memory_context: MemoryContext,
    ) -> str:
        """
        Format memory context for injection into prompts.
        """

        if not memory_context.entries:
            return ""

        parts = ["Relevant memories from previous work:"]
        parts.extend(f"- {entry.content}" for entry in memory_context.entries)

        if memory_context.summary:
            parts.append(f"\nSummary: {memory_context.summary}")

        return "\n".join(parts)

    @classmethod
    def _format_context_window(
        cls,
        context_window: ContextWindow,
    ) -> str:
        """
        Format context window for injection into prompts.
        """

        parts = []

        if context_window.documents:
            parts.append("Relevant documents:")
            parts.extend(f"- {doc}" for doc in context_window.documents)

        if context_window.artifacts:
            parts.append("Shared project artifacts:")
            for name, content in context_window.artifacts.items():
                parts.append(f"\n--- {name} ---\n{content}")

        return "\n".join(parts)

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
