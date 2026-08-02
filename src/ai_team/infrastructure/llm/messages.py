"""
Conversation models shared by all LLM providers.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Roles
# ============================================================================


class MessageRole(StrEnum):
    """
    Supported message roles.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


# ============================================================================
# Message
# ============================================================================


class Message(BaseModel):
    """
    Single chat message.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    role: MessageRole

    content: str


# ============================================================================
# Conversation
# ============================================================================


class Conversation(BaseModel):
    """
    Mutable conversation exchanged with an LLM.
    """

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )

    messages: list[Message] = Field(
        default_factory=list,
    )

    # ------------------------------------------------------------------
    # Add messages
    # ------------------------------------------------------------------

    def add_system(
        self,
        content: str,
    ) -> None:
        self.messages.append(
            Message(
                role=MessageRole.SYSTEM,
                content=content,
            )
        )

    def add_user(
        self,
        content: str,
    ) -> None:
        self.messages.append(
            Message(
                role=MessageRole.USER,
                content=content,
            )
        )

    def add_assistant(
        self,
        content: str,
    ) -> None:
        self.messages.append(
            Message(
                role=MessageRole.ASSISTANT,
                content=content,
            )
        )

    def add_tool(
        self,
        content: str,
    ) -> None:
        self.messages.append(
            Message(
                role=MessageRole.TOOL,
                content=content,
            )
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def last_message(self) -> Message | None:
        """
        Return the last message in the conversation.
        """
        if not self.messages:
            return None

        return self.messages[-1]

    @property
    def system_prompt(self) -> str | None:
        """
        Return the first system prompt if present.
        """
        for message in self.messages:
            if message.role is MessageRole.SYSTEM:
                return message.content

        return None

    def clear(self) -> None:
        """
        Remove every message.
        """
        self.messages.clear()

    def copy(self) -> "Conversation":
        """
        Deep copy of the conversation.
        """
        return self.model_copy(deep=True)

    def to_openai(self) -> list[dict[str, str]]:
        """
        Convert the conversation into the OpenAI-compatible format.
        """
        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in self.messages
        ]

    def __len__(self) -> int:
        return len(self.messages)