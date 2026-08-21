"""
Logging manager.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from uuid import UUID

    from ai_team.observability.models import (
        AgentExecution,
        LLMCall,
        ToolCall,
    )


class LoggingManager:
    """
    Thin wrapper around the Python logging system.

    The implementation can later be replaced by Structlog
    without affecting the rest of the application.
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:

        self._logger = logger or logging.getLogger(
            "ai_team",
        )

    # ---------------------------------------------------------
    # Agent executions
    # ---------------------------------------------------------

    async def log_execution(
        self,
        execution: AgentExecution,
    ) -> None:

        self._logger.info(
            "Agent execution finished.",
            extra={
                "execution_id": str(
                    execution.execution_id,
                ),
                "agent": execution.agent,
                "status": execution.status,
                "started_at": execution.started_at,
                "finished_at": execution.finished_at,
            },
        )

    # ---------------------------------------------------------
    # LLM
    # ---------------------------------------------------------

    async def log_llm_call(
        self,
        call: LLMCall,
    ) -> None:

        self._logger.info(
            "LLM call.",
            extra={
                "execution_id": str(
                    call.execution_id,
                ),
                "agent": call.agent,
                "provider": call.provider,
                "model": call.model,
                "prompt_tokens": call.prompt_tokens,
                "completion_tokens": call.completion_tokens,
                "latency_ms": call.latency_ms,
            },
        )

    # ---------------------------------------------------------
    # Tools
    # ---------------------------------------------------------

    async def log_tool_call(
        self,
        call: ToolCall,
    ) -> None:

        self._logger.info(
            "Tool call.",
            extra={
                "execution_id": str(
                    call.execution_id,
                ),
                "agent": call.agent,
                "tool": call.tool,
                "latency_ms": call.latency_ms,
                "success": call.success,
            },
        )

    # ---------------------------------------------------------
    # Errors
    # ---------------------------------------------------------

    async def log_error(
        self,
        *,
        execution_id: UUID,
        agent: Any,
        error: Exception,
    ) -> None:

        self._logger.exception(
            str(error),
            extra={
                "execution_id": str(
                    execution_id,
                ),
                "agent": str(agent),
            },
        )

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    async def shutdown(
        self,
    ) -> None:
        """
        Flush log handlers.
        """

        logging.shutdown()
