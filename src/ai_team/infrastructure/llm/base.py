"""
Abstract interface for all Large Language Model providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ai_team.infrastructure.llm.config import GenerationConfig
    from ai_team.infrastructure.llm.messages import Conversation
    from ai_team.infrastructure.llm.responses import (
        LLMResponse,
        LLMStreamChunk,
        StructuredLLMResponse,
    )

SchemaT = TypeVar("SchemaT")


class BaseLLM(ABC):
    """
    Abstract interface implemented by every LLM provider.

    Every provider (OpenRouter, Ollama, OpenAI, Anthropic, etc.)
    must implement this contract.
    """

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Provider identifier.

        Examples:
            - openrouter
            - openai
            - anthropic
            - ollama
        """
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Current model identifier.
        """
        ...

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    @abstractmethod
    async def generate(
        self,
        conversation: Conversation,
        *,
        config: GenerationConfig | None = None,
    ) -> LLMResponse:
        """
        Generate a response from a conversation.
        """
        ...

    @abstractmethod
    async def generate_structured(
        self,
        conversation: Conversation,
        schema: type[SchemaT],
        *,
        config: GenerationConfig | None = None,
    ) -> StructuredLLMResponse[SchemaT]:
        """
        Generate and validate structured output.

        Returns both the parsed object and the original
        LLM response metadata.
        """
        ...

    @abstractmethod
    async def stream(
        self,
        conversation: Conversation,
        *,
        config: GenerationConfig | None = None,
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Stream the model response.
        """
        ...

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    async def close(self) -> None:
        """
        Release resources owned by the provider.
        """
        ...
