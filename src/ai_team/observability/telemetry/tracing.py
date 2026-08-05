"""
Execution tracing manager.
"""

from __future__ import annotations

from uuid import UUID

from ai_team.observability.models import AgentExecution


class TracingManager:
    """
    Tracks active agent executions.
    """

    def __init__(self) -> None:
        self._executions: dict[
            UUID,
            AgentExecution,
        ] = {}

    # ---------------------------------------------------------
    # Execution lifecycle
    # ---------------------------------------------------------

    async def start_execution(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Register a new execution.
        """

        self._executions[
            execution.execution_id
        ] = execution

    async def finish_execution(
        self,
        execution_id: UUID,
    ) -> AgentExecution | None:
        """
        Finish an execution and remove it from the active traces.
        """

        return self._executions.pop(
            execution_id,
            None,
        )

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def get_execution(
        self,
        execution_id: UUID,
    ) -> AgentExecution | None:
        """
        Return an active execution.
        """

        return self._executions.get(
            execution_id,
        )

    def active_executions(
        self,
    ) -> list[AgentExecution]:
        """
        Return every active execution.
        """

        return list(
            self._executions.values(),
        )