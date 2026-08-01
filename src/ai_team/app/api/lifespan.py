```python
"""
Abstract interface for Large Language Models.

Every provider (OpenRouter, Ollama, Anthropic, OpenAI, etc.)
must implement this contract.

Agents should depend ONLY on BaseLLM and never on a concrete
provider implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLM(ABC):
    """
    Base interface for every LLM provider.
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
    ) -> str:
        """
        Generate a text completion.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: type[Any],
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Generate a structured response validated
        against a Pydantic schema.
        """
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        **kwargs: Any,
    ):
        """
        Stream generated tokens.
        """
        raise NotImplementedError
```
