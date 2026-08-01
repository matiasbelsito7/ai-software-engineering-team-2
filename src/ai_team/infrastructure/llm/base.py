"""
Abstract interface for Large Language Models.

Every provider (OpenRouter, Ollama, Anthropic, OpenAI, etc.)
must implement this contract.

The rest of the application must depend exclusively on this
abstraction and never on concrete provider implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any, TypeVar

from ai_team.infrastructure.llm.responses import (
    LLMResponse,
    LLMStreamChunk,
)

SchemaT = TypeVar("SchemaT")


class BaseLLM(ABC):
    """
    Abstract interface implemented by every LLM provider.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Active model name.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """
        Generate a text response.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: type[SchemaT],
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> SchemaT:
        """
        Generate a structured response validated
        against the supplied schema.
        """
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Stream the generated response.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Release any resources owned by the provider.
        """
        raise NotImplementedError