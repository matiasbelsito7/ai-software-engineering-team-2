"""
OpenRouter provider implementation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ai_team.infrastructure.config.settings import settings
from ai_team.infrastructure.llm.providers.base import ProviderBase
from ai_team.infrastructure.llm.responses import (
    GenerationMetadata,
    LLMResponse,
    LLMStreamChunk,
    TokenUsage,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ai_team.infrastructure.llm.config import GenerationConfig
    from ai_team.infrastructure.llm.messages import Conversation


class OpenRouterLLM(ProviderBase):
    """
    OpenRouter implementation of the LLM provider.
    """

    CHAT_COMPLETIONS_ENDPOINT = "/chat/completions"

    def __init__(
        self,
        *,
        model: str,
    ) -> None:

        super().__init__(
            model=model,
            base_url=settings.llm.openrouter_base_url,
            headers={
                "Authorization": (f"Bearer {settings.llm.openrouter_api_key}"),
                "Content-Type": "application/json",
                "HTTP-Referer": f"http://{settings.app.host}:{settings.app.port}",
                "X-Title": settings.app.name,
            },
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def provider_name(self) -> str:
        return "openrouter"

    # ------------------------------------------------------------------
    # Payload
    # ------------------------------------------------------------------

    def _build_payload(
        self,
        conversation: Conversation,
        config: GenerationConfig | None,
    ) -> dict[str, Any]:

        payload = {
            "model": self.model_name,
            "messages": self._conversation_to_messages(
                conversation,
            ),
        }

        return self._apply_generation_config(
            payload,
            config,
        )

    # ------------------------------------------------------------------
    # Response
    # ------------------------------------------------------------------

    def _parse_response(
        self,
        data: dict[str, Any],
        latency_ms: float,
    ) -> LLMResponse:

        choice = data["choices"][0]

        usage_json = data.get("usage", {})

        usage = TokenUsage(
            prompt_tokens=usage_json.get(
                "prompt_tokens",
                0,
            ),
            completion_tokens=usage_json.get(
                "completion_tokens",
                0,
            ),
            total_tokens=usage_json.get(
                "total_tokens",
                0,
            ),
        )

        metadata = GenerationMetadata(
            request_id=data.get("id"),
            created=data.get("created"),
            finish_reason=choice.get(
                "finish_reason",
            ),
            extra={
                "provider": data.get("provider"),
            },
        )

        return self._build_response(
            content=choice["message"]["content"],
            usage=usage,
            metadata=metadata,
            latency_ms=latency_ms,
            raw_response=data,
        )

    # ------------------------------------------------------------------
    # BaseLLM
    # ------------------------------------------------------------------

    async def generate(
        self,
        conversation: Conversation,
        *,
        config: GenerationConfig | None = None,
    ) -> LLMResponse:

        payload = self._build_payload(
            conversation,
            config,
        )

        data, latency = await self._post(
            endpoint=self.CHAT_COMPLETIONS_ENDPOINT,
            payload=payload,
        )

        return self._parse_response(
            data,
            latency,
        )

    async def stream(
        self,
        conversation: Conversation,
        *,
        config: GenerationConfig | None = None,
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Streaming support will be implemented in a future version.
        """
        raise NotImplementedError("Streaming is not implemented.")
