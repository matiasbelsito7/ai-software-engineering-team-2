"""
Ollama provider implementation.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import httpx

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


class OllamaLLM(ProviderBase):
    """
    Ollama provider for local LLM inference.
    """

    CHAT_ENDPOINT = "/api/chat"

    def __init__(
        self,
        *,
        model: str,
    ) -> None:
        super().__init__(
            model=model,
            base_url=settings.llm.ollama_base_url.rstrip("/"),
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def provider_name(self) -> str:
        return "ollama"

    # ------------------------------------------------------------------
    # Payload
    # ------------------------------------------------------------------

    def _build_payload(
        self,
        conversation: Conversation,
        config: GenerationConfig | None,
    ) -> dict[str, Any]:
        messages = self._conversation_to_messages(conversation)

        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
        }

        if config is not None:
            if config.temperature is not None:
                payload.setdefault("options", {})["temperature"] = config.temperature
            if config.max_tokens is not None:
                payload.setdefault("options", {})["num_predict"] = config.max_tokens

        return payload

    def _build_stream_payload(
        self,
        conversation: Conversation,
        config: GenerationConfig | None,
    ) -> dict[str, Any]:
        payload = self._build_payload(conversation, config)
        payload["stream"] = True
        return payload

    # ------------------------------------------------------------------
    # Response
    # ------------------------------------------------------------------

    def _parse_response(
        self,
        data: dict[str, Any],
        latency_ms: float,
    ) -> LLMResponse:
        message = data.get("message", {})
        content = message.get("content", "")

        prompt_tokens = data.get("prompt_eval_count", 0)
        completion_tokens = data.get("eval_count", 0)

        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )

        metadata = GenerationMetadata(
            request_id=None,
            created=None,
            finish_reason="stop" if data.get("done") else None,
            extra={
                "total_duration_ns": data.get("total_duration"),
                "load_duration_ns": data.get("load_duration"),
                "model": data.get("model"),
            },
        )

        return self._build_response(
            content=content,
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
        payload = self._build_payload(conversation, config)

        data, latency = await self._post(
            endpoint=self.CHAT_ENDPOINT,
            payload=payload,
        )

        return self._parse_response(data, latency)

    async def stream(  # type: ignore[misc,override]
        self,
        conversation: Conversation,
        *,
        config: GenerationConfig | None = None,
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Stream response tokens from Ollama.
        """
        payload = self._build_stream_payload(conversation, config)

        try:
            async with self.client.stream(
                "POST",
                self.CHAT_ENDPOINT,
                json=payload,
            ) as response:
                self._raise_for_status(response)

                async for line in response.aiter_lines():
                    if not line.strip():
                        continue

                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    message = data.get("message", {})
                    content = message.get("content", "")

                    if content:
                        is_finished = data.get("done", False)
                        yield LLMStreamChunk(
                            content=content,
                            is_finished=is_finished,
                        )

        except httpx.TimeoutException as exc:
            from ai_team.infrastructure.llm.exceptions import TimeoutError

            raise TimeoutError(
                "Streaming request timed out.",
                provider=self.provider_name,
                model=self.model_name,
            ) from exc

        except httpx.HTTPError as exc:
            from ai_team.infrastructure.llm.exceptions import (
                ProviderUnavailableError,
            )

            raise ProviderUnavailableError(
                str(exc),
                provider=self.provider_name,
                model=self.model_name,
            ) from exc
