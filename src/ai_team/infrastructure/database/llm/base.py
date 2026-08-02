"""
Abstract interface for all Large Language Model providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import TypeVar

from ai_team.infrastructure.llm.config import GenerationConfig
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
    # Text Generation
    # ------------------------------------------------------------------

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        config: GenerationConfig | None = None,
    ) -> LLMResponse:
        """
        Generate a text response.
        """
        ...

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: type[SchemaT],
        *,
        system_prompt: str | None = None,
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
        prompt: str,
        *,
        system_prompt: str | None = None,
        config: GenerationConfig | None = None,
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Stream the model output.
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