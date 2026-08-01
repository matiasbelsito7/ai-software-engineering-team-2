```python
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

from ai_team.infrastructure.config.settings import settings
from ai_team.infrastructure.llm.base import BaseLLM
from ai_team.infrastructure.llm.providers.ollama import OllamaLLM
from ai_team.infrastructure.llm.providers.openrouter import OpenRouterLLM


class LLMFactory:
    """
    Factory responsible for creating LLM providers.
    """

    @staticmethod
    def create() -> BaseLLM:
        """
        Create the configured LLM provider.
        """

        provider = settings.llm.provider.lower()

        match provider:
            case "openrouter":
                return OpenRouterLLM(
                    model=settings.llm.model,
                )

            case "ollama":
                return OllamaLLM(
                    model=settings.llm.model,
                )

            case _:
                raise ValueError(
                    f"Unsupported LLM provider: '{provider}'."
                )
```
