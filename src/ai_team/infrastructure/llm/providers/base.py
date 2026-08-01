"""
Shared implementation for all LLM providers.

This class contains the infrastructure common to every provider:
- HTTP communication
- Error translation
- Response construction
- Latency measurement
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import AsyncIterator
from time import perf_counter
from typing import Any

import httpx

from ai_team.infrastructure.http.client import HTTPClient
from ai_team.infrastructure.llm.base import BaseLLM
from ai_team.infrastructure.llm.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InvalidRequestError,
    InvalidResponseError,
    ModelNotFoundError,
    ProviderUnavailableError,
    RateLimitError,
    ResponseParsingError,
    ServiceUnavailableError,
    TimeoutError,
)
from ai_team.infrastructure.llm.responses import (
    GenerationMetadata,
    LLMResponse,
    LLMStreamChunk,
    TokenUsage,
)


class ProviderBase(BaseLLM):
    """
    Base implementation shared by every LLM provider.
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
    def client(self):
        return self._client

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def close(self) -> None:
        await self.client.aclose()

    # ------------------------------------------------------------------
    # HTTP
    # ------------------------------------------------------------------

    async def _post(
        self,
        *,
        endpoint: str,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> tuple[dict[str, Any], float]:

        start = perf_counter()

        try:

            response = await self.client.post(
                endpoint,
                json=payload,
                headers=headers,
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
                    "Requested model not found.",
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

    # ------------------------------------------------------------------
    # Response helpers
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
    # Abstract API
    # ------------------------------------------------------------------

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
        ...

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: type[Any],
        *,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> Any:
        ...

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
        ...