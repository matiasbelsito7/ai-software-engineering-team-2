"""
Shared infrastructure for all LLM providers.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import AsyncIterator
from time import perf_counter
from typing import Any, TypeVar

import httpx

from ai_team.infrastructure.http.client import HTTPClient
from ai_team.infrastructure.llm.base import BaseLLM
from ai_team.infrastructure.llm.config import GenerationConfig
from ai_team.infrastructure.llm.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InvalidRequestError,
    ModelNotFoundError,
    ProviderUnavailableError,
    RateLimitError,
    ResponseParsingError,
    ServiceUnavailableError,
    TimeoutError,
)
from ai_team.infrastructure.llm.messages import Conversation
from ai_team.infrastructure.llm.responses import (
    GenerationMetadata,
    LLMResponse,
    LLMStreamChunk,
    StructuredLLMResponse,
    TokenUsage,
)

SchemaT = TypeVar("SchemaT")


class ProviderBase(BaseLLM):
    """
    Base implementation shared by every LLM provider.

    This class centralizes:

    - HTTP communication
    - Error translation
    - Latency measurement
    - Response construction
    - Structured generation
    """

    def __init__(
        self,
        *,
        model: str,
        base_url: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._model = model

        self._client = HTTPClient.create(
            base_url=base_url,
            headers=headers,
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def close(self) -> None:
        """
        Release HTTP resources.
        """
        await self.client.aclose()

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    async def _post(
        self,
        *,
        endpoint: str,
        payload: dict[str, Any],
    ) -> tuple[dict[str, Any], float]:
        """
        Execute a POST request and return both the JSON response
        and the request latency in milliseconds.
        """

        start = perf_counter()

        try:
            response = await self.client.post(
                endpoint,
                json=payload,
            )

            latency_ms = (perf_counter() - start) * 1000

            self._raise_for_status(response)

            try:
                data = response.json()

            except ValueError as exc:
                raise ResponseParsingError(
                    "Provider returned invalid JSON.",
                    provider=self.provider_name,
                    model=self.model_name,
                ) from exc

            return data, latency_ms

        except httpx.TimeoutException as exc:
            raise TimeoutError(
                "LLM request timed out.",
                provider=self.provider_name,
                model=self.model_name,
            ) from exc

        except httpx.HTTPError as exc:
            raise ProviderUnavailableError(
                str(exc),
                provider=self.provider_name,
                model=self.model_name,
            ) from exc

    def _raise_for_status(
        self,
        response: httpx.Response,
    ) -> None:
        """
        Translate HTTP status codes into domain exceptions.
        """

        status = response.status_code

        if status < 400:
            return

        match status:
            case 400:
                raise InvalidRequestError(
                    "Invalid request.",
                    provider=self.provider_name,
                    model=self.model_name,
                )

            case 401:
                raise AuthenticationError(
                    "Authentication failed.",
                    provider=self.provider_name,
                    model=self.model_name,
                )

            case 403:
                raise AuthorizationError(
                    "Access denied.",
                    provider=self.provider_name,
                    model=self.model_name,
                )

            case 404:
                raise ModelNotFoundError(
                    "Model not found.",
                    provider=self.provider_name,
                    model=self.model_name,
                )

            case 429:
                raise RateLimitError(
                    "Rate limit exceeded.",
                    provider=self.provider_name,
                    model=self.model_name,
                )

            case 503:
                raise ServiceUnavailableError(
                    "Service unavailable.",
                    provider=self.provider_name,
                    model=self.model_name,
                )

            case _:
                raise ProviderUnavailableError(
                    f"Provider returned HTTP {status}.",
                    provider=self.provider_name,
                    model=self.model_name,
                )

from pydantic import TypeAdapter


    # ------------------------------------------------------------------
    # Conversation
    # ------------------------------------------------------------------

    def _conversation_to_messages(
        self,
        conversation: Conversation,
    ) -> list[dict[str, Any]]:
        """
        Convert an internal Conversation into the provider
        message format.
        """

        return [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in conversation.messages
        ]

    # ------------------------------------------------------------------
    # Generation Config
    # ------------------------------------------------------------------

    def _apply_generation_config(
        self,
        payload: dict[str, Any],
        config: GenerationConfig | None,
    ) -> dict[str, Any]:
        """
        Apply generation parameters to a provider payload.
        """

        if config is None:
            return payload

        payload.update(
            config.to_provider_dict(),
        )

        return payload

    # ------------------------------------------------------------------
    # Response
    # ------------------------------------------------------------------

    def _build_response(
        self,
        *,
        content: str,
        usage: TokenUsage | None = None,
        metadata: GenerationMetadata | None = None,
        latency_ms: float | None = None,
        raw_response: dict[str, Any] | None = None,
    ) -> LLMResponse:
        """
        Build a normalized LLM response.
        """

        return LLMResponse(
            content=content,
            provider=self.provider_name,
            model=self.model_name,
            usage=usage or TokenUsage(),
            metadata=metadata or GenerationMetadata(),
            latency_ms=latency_ms,
            raw_response=raw_response,
        )

    # ------------------------------------------------------------------
    # Structured Generation
    # ------------------------------------------------------------------

    async def generate_structured(
        self,
        conversation: Conversation,
        schema: type[SchemaT],
        *,
        config: GenerationConfig | None = None,
    ) -> StructuredLLMResponse[SchemaT]:
        """
        Generate and validate structured output.

        Every provider automatically inherits this behavior.
        """

        response = await self.generate(
            conversation=conversation,
            config=config,
        )

        adapter = TypeAdapter(schema)

        parsed = adapter.validate_json(
            response.content,
        )

        return StructuredLLMResponse(
            data=parsed,
            response=response,
        )

    # ------------------------------------------------------------------
    # Message Conversion
    # ------------------------------------------------------------------

    def _message_to_provider_format(
        self,
        message: ChatMessage,
    ) -> dict[str, Any]:
        """
        Convert a ChatMessage into the provider-specific format.

        Providers with custom message formats (for example,
        Anthropic or Gemini) may override this method without
        reimplementing the entire conversation conversion.
        """

        payload: dict[str, Any] = {
            "role": message.role.value,
            "content": message.content,
        }

        if message.name:
            payload["name"] = message.name

        if message.tool_call_id:
            payload["tool_call_id"] = message.tool_call_id

        return payload

    # ------------------------------------------------------------------
    # Abstract API
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
    async def stream(
        self,
        conversation: Conversation,
        *,
        config: GenerationConfig | None = None,
    ) -> AsyncIterator[LLMStreamChunk]:
        """
        Stream a response from the provider.
        """
        ...