"""
LLM Factory.

Creates the appropriate LLM provider based on the application
configuration.

Responsibilities
----------------
- Read provider configuration.
- Instantiate the correct provider.

This module intentionally does NOT contain:

- Retry logic
- Telemetry
- Token accounting
- Caching
- Rate limiting
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.infrastructure.config.settings import settings
from ai_team.infrastructure.llm.exceptions import UnsupportedProviderError

if TYPE_CHECKING:
    from ai_team.infrastructure.llm.base import BaseLLM


class LLMFactory:
    """
    Factory responsible for creating LLM providers.
    """

    @staticmethod
    def create(
        *,
        provider: str | None = None,
        model: str | None = None,
    ) -> BaseLLM:
        """
        Create an LLM provider instance.

        If provider or model are omitted, the application defaults
        defined in the settings are used.
        """

        provider = provider or settings.llm.default_provider

        match provider.lower():
            case "openrouter":
                from ai_team.infrastructure.llm.providers.openrouter import (
                    OpenRouterLLM,
                )

                return OpenRouterLLM(
                    model=model or settings.llm.openrouter_model,
                )

            case "ollama":
                from ai_team.infrastructure.llm.providers.ollama import (
                    OllamaLLM,
                )

                return OllamaLLM(
                    model=model or settings.llm.ollama_model,
                )

            case _:
                raise UnsupportedProviderError(f"Unsupported LLM provider: {provider}")
