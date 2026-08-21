"""
Runtime metrics manager.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.observability.models import (
        AgentExecution,
        LLMCall,
        ToolCall,
    )


class LatencyHistogram:
    """
    Simple in-memory latency histogram with min/max/avg/p95.
    """

    def __init__(self) -> None:
        self._values: list[float] = []

    def record(self, value: float) -> None:
        self._values.append(value)

    @property
    def count(self) -> int:
        return len(self._values)

    @property
    def min_ms(self) -> float:
        return min(self._values) if self._values else 0.0

    @property
    def max_ms(self) -> float:
        return max(self._values) if self._values else 0.0

    @property
    def avg_ms(self) -> float:
        return sum(self._values) / len(self._values) if self._values else 0.0

    @property
    def p95_ms(self) -> float:
        if not self._values:
            return 0.0
        sorted_vals = sorted(self._values)
        idx = int(len(sorted_vals) * 0.95)
        return sorted_vals[min(idx, len(sorted_vals) - 1)]

    def reset(self) -> None:
        self._values.clear()

    def snapshot(self) -> dict[str, float]:
        return {
            "count": self.count,
            "min_ms": self.min_ms,
            "max_ms": self.max_ms,
            "avg_ms": self.avg_ms,
            "p95_ms": self.p95_ms,
        }


class MetricsManager:
    """
    Collects runtime metrics.
    """

    def __init__(
        self,
    ) -> None:

        self._executions = 0

        self._llm_calls = 0

        self._tool_calls = 0

        self._errors = 0

        self._tokens = 0

        self._agent_calls: defaultdict[
            str,
            int,
        ] = defaultdict(int)

        self._llm_latency = LatencyHistogram()
        self._tool_latency = LatencyHistogram()

    # ---------------------------------------------------------
    # Recording
    # ---------------------------------------------------------

    async def record_execution(
        self,
        execution: AgentExecution,
    ) -> None:

        self._executions += 1

        self._agent_calls[execution.agent] += 1

    async def record_llm_call(
        self,
        call: LLMCall,
    ) -> None:

        self._llm_calls += 1

        self._tokens += call.total_tokens

        self._llm_latency.record(call.latency_ms)

    async def record_tool_call(
        self,
        call: ToolCall,
    ) -> None:

        self._tool_calls += 1

        self._tool_latency.record(call.latency_ms)

    async def record_error(
        self,
        *,
        execution_id: str,
        agent: str,
        error: Exception,
    ) -> None:

        self._errors += 1

    # ---------------------------------------------------------
    # Snapshot
    # ---------------------------------------------------------

    def snapshot(
        self,
    ) -> dict[str, object]:
        """
        Return current runtime metrics.
        """

        return {
            "executions": self._executions,
            "llm_calls": self._llm_calls,
            "tool_calls": self._tool_calls,
            "errors": self._errors,
            "tokens": self._tokens,
            "agents": dict(
                self._agent_calls,
            ),
            "llm_latency": self._llm_latency.snapshot(),
            "tool_latency": self._tool_latency.snapshot(),
        }
