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

    async def record_tool_call(
        self,
        call: ToolCall,
    ) -> None:

        self._tool_calls += 1

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
        }
