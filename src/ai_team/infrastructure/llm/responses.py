"""
Common response models for every LLM provider.

All providers should map their native API responses into these
models before returning them to the application.

This guarantees that agents, graph nodes, evaluations and
observability remain provider-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class StructuredLLMResponse(Generic[T]):
    """
    Structured response returned by an LLM.
    """

    data: T
    response: LLMResponse

# ---------------------------------------------------------------------------
# Token Usage
# ---------------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class TokenUsage:
    """
    Token accounting information.
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class GenerationMetadata:
    """
    Provider-specific metadata.

    Unknown values are stored inside `extra`.
    """

    request_id: str | None = None
    finish_reason: str | None = None
    created: int | None = None

    extra: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Streaming
# ---------------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class LLMStreamChunk:
    """
    One streamed chunk produced by an LLM.
    """

    content: str
    is_finished: bool = False


# ---------------------------------------------------------------------------
# Final Response
# ---------------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """
    Standard response returned by every LLM provider.
    """

    content: str

    provider: str
    model: str

    usage: TokenUsage = field(default_factory=TokenUsage)

    latency_ms: float | None = None

    metadata: GenerationMetadata = field(
        default_factory=GenerationMetadata
    )

    raw_response: dict[str, Any] | None = None