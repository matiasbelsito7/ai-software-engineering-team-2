"""
Shared protocol definitions for the AI Software Engineering Team project.

Protocols define contracts between components while keeping them loosely coupled.

Guidelines
----------
- Use Protocol instead of ABC whenever possible.
- Do not implement business logic.
- Do not import project modules.
- Keep dependencies limited to the standard library.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from ai_team.shared.types import (
        Embedding,
        Metadata,
        Prompt,
        ToolArguments,
        ToolResult,
    )

###############################################################################
# LLM
###############################################################################


@runtime_checkable
class LLMProtocol(Protocol):
    """Contract implemented by every LLM provider."""

    async def generate(
        self,
        prompt: Prompt,
        **kwargs: Any,
    ) -> str: ...

    async def stream(
        self,
        prompt: Prompt,
        **kwargs: Any,
    ) -> Any: ...


###############################################################################
# Embeddings
###############################################################################


@runtime_checkable
class EmbeddingProtocol(Protocol):
    """Contract implemented by embedding providers."""

    async def embed(
        self,
        text: str,
    ) -> Embedding: ...


###############################################################################
# Vector Store
###############################################################################


@runtime_checkable
class VectorStoreProtocol(Protocol):
    """Contract implemented by every vector database."""

    async def add(
        self,
        documents: list[str],
        metadata: list[Metadata],
    ) -> None: ...

    async def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[Any]: ...


###############################################################################
# Memory
###############################################################################


@runtime_checkable
class MemoryProtocol(Protocol):
    """Contract for memory implementations."""

    async def save(
        self,
        key: str,
        value: Any,
    ) -> None: ...

    async def load(
        self,
        key: str,
    ) -> Any: ...


###############################################################################
# Tool
###############################################################################


@runtime_checkable
class ToolProtocol(Protocol):
    """Contract implemented by every tool."""

    @property
    def name(self) -> str: ...

    async def execute(
        self,
        arguments: ToolArguments,
    ) -> ToolResult: ...


###############################################################################
# Agent
###############################################################################


@runtime_checkable
class AgentProtocol(Protocol):
    """Contract implemented by every agent."""

    @property
    def name(self) -> str: ...

    async def run(
        self,
        task: str,
        **kwargs: Any,
    ) -> Any: ...


###############################################################################
# Retriever
###############################################################################


@runtime_checkable
class RetrieverProtocol(Protocol):
    """Contract implemented by retrieval systems."""

    async def retrieve(
        self,
        query: str,
    ) -> list[Any]: ...


###############################################################################
# Logger
###############################################################################


@runtime_checkable
class LoggerProtocol(Protocol):
    """Logging abstraction."""

    def debug(self, message: str, **kwargs: Any) -> None: ...

    def info(self, message: str, **kwargs: Any) -> None: ...

    def warning(self, message: str, **kwargs: Any) -> None: ...

    def error(self, message: str, **kwargs: Any) -> None: ...


###############################################################################
# Event Bus
###############################################################################


@runtime_checkable
class EventBusProtocol(Protocol):
    """Simple event bus contract."""

    async def publish(
        self,
        event: Any,
    ) -> None: ...

    async def subscribe(
        self,
        event_type: type,
        handler: Any,
    ) -> None: ...
