"""
Backend agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.agents.backend.models import BackendResult
from ai_team.agents.backend.prompt_builder import BackendPromptBuilder
from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.backend import BackendParser
from ai_team.agents.result import AgentResult
from ai_team.shared.enums.agents import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class BackendAgent(BaseAgent[BackendResult]):
    """
    Agent responsible for implementing backend functionality.

    Produces source-code patches and dependency changes required
    to implement the assigned backend task.
    """

    INFO = AgentInfo(
        name="backend",
        capability=AgentCapability.BACKEND,
        description=(
            "Implements backend functionality and produces "
            "validated source-code patches and dependency changes."
        ),
        version="1.0.0",
    )

    PARSER = BackendParser

    PROMPT_BUILDER = BackendPromptBuilder

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Validate the Backend execution.
        """

        super().validate(execution)

        if execution.capability is not self.capability:
            raise ValueError(
                "BackendAgent received an execution for "
                f"capability '{execution.capability.value}'."
            )

        if not execution.request.task.strip():
            raise ValueError(
                "BackendAgent requires a non-empty task."
            )

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the backend implementation process.

        The LLM response is parsed into a BackendResult.
        """

        result = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=result,
            message="Backend implementation completed successfully.",
        )
