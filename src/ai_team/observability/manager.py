"""
Observability manager.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from ai_team.observability.models import (
    AgentExecution,
    LLMCall,
    ToolCall,
)
from ai_team.shared.enums.observability import (
    LLMProvider,
    ToolType,
)

if TYPE_CHECKING:
    from ai_team.observability.costs import CostTracker
    from ai_team.observability.telemetry.logging import LoggingManager
    from ai_team.observability.telemetry.metrics import MetricsManager
    from ai_team.observability.telemetry.tracing import TracingManager
    from ai_team.observability.token_usage import TokenUsageTracker

logger = logging.getLogger("ai_team.observability")


class ObservationManager:
    """
    Coordinates the observability subsystem.

    This class exposes a stable API to the rest of the
    application while internally building the observability
    models.
    """

    def __init__(
        self,
        *,
        tracing: TracingManager,
        metrics: MetricsManager,
        logging: LoggingManager,
        token_usage: TokenUsageTracker,
        costs: CostTracker,
    ) -> None:

        self._tracing = tracing
        self._metrics = metrics
        self._logging = logging
        self._token_usage = token_usage
        self._costs = costs

    # ---------------------------------------------------------
    # Agent lifecycle
    # ---------------------------------------------------------

    async def start_execution(
        self,
        *,
        execution_id: str,
        agent: str,
    ) -> AgentExecution:
        """
        Start observing an agent execution.
        """

        execution = AgentExecution(
            execution_id=UUID(execution_id),
            agent=agent,
            started_at=datetime.now(UTC),
        )

        await self._tracing.start_execution(
            execution,
        )

        return execution

    def get_execution(
        self,
        execution_id: str,
    ) -> AgentExecution | None:
        """
        Retrieve an active execution by ID.
        """

        return self._tracing.get_execution(
            UUID(execution_id),
        )

    async def finish_execution(
        self,
        *,
        execution: AgentExecution,
    ) -> None:
        """
        Finish observing an agent execution.
        """

        execution.finished_at = datetime.now(
            UTC,
        )

        await self._tracing.finish_execution(
            execution.execution_id,
        )

        await self._metrics.record_execution(
            execution,
        )

        await self._logging.log_execution(
            execution,
        )

    # ---------------------------------------------------------
    # LLM
    # ---------------------------------------------------------

    async def record_llm_call(
        self,
        *,
        execution_id: str,
        agent: str,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
    ) -> None:
        """
        Record an LLM invocation.
        """

        call = LLMCall(
            execution_id=UUID(execution_id),
            agent=agent,
            provider=LLMProvider(provider),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_ms=latency_ms,
            timestamp=datetime.now(UTC),
        )

        await self._token_usage.record(call)

        await self._costs.record(call)

        await self._metrics.record_llm_call(call)

        await self._logging.log_llm_call(call)

    # ---------------------------------------------------------
    # Tools
    # ---------------------------------------------------------

    async def record_tool_call(
        self,
        *,
        execution_id: str,
        agent: str,
        tool: str,
        latency_ms: float,
        success: bool,
    ) -> None:
        """
        Record a tool invocation.
        """

        call = ToolCall(
            execution_id=UUID(execution_id),
            agent=agent,
            tool=ToolType(tool),
            latency_ms=latency_ms,
            success=success,
            timestamp=datetime.now(UTC),
        )

        await self._metrics.record_tool_call(
            call,
        )

        await self._logging.log_tool_call(
            call,
        )

    # ---------------------------------------------------------
    # Errors
    # ---------------------------------------------------------

    async def record_error(
        self,
        *,
        execution_id: str,
        agent: str,
        error: Exception,
    ) -> None:
        """
        Record an execution error.
        """

        await self._metrics.record_error(
            execution_id=execution_id,
            agent=agent,
            error=error,
        )

        await self._logging.log_error(
            execution_id=UUID(execution_id),
            agent=agent,
            error=error,
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    async def initialize(
        self,
        *,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize observability resources.
        """

        logger.setLevel(log_level)
        logger.info("Observability subsystem initialized.")

    async def shutdown(
        self,
    ) -> None:
        """
        Shutdown observability resources.
        """

        await self._logging.shutdown()

    # ---------------------------------------------------------
    # Accessors
    # ---------------------------------------------------------

    @property
    def tracing(self) -> TracingManager:
        return self._tracing

    @property
    def metrics(self) -> MetricsManager:
        return self._metrics

    @property
    def logging(self) -> LoggingManager:
        return self._logging

    @property
    def token_usage(self) -> TokenUsageTracker:
        return self._token_usage

    @property
    def costs(self) -> CostTracker:
        return self._costs
