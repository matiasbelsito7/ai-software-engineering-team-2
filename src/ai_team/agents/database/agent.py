"""
Database agent implementation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.agents.base import BaseAgent
from ai_team.agents.database.models import DatabaseResult
from ai_team.agents.database.prompt_builder import (
    DatabasePromptBuilder,
)
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.database import DatabaseParser
from ai_team.agents.result import AgentResult
from ai_team.shared.enums import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class DatabaseAgent(BaseAgent[DatabaseResult]):
    """
    AI agent responsible for designing the persistence layer.
    """

    INFO = AgentInfo(
        name="database",
        capability=AgentCapability.DATABASE,
        description=(
            "Designs database schemas, entities, relationships and persistence strategies."
        ),
        version="1.0.0",
    )

    PARSER = DatabaseParser

    PROMPT_BUILDER = DatabasePromptBuilder

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        super().validate(execution)

        if execution.capability is not self.capability:
            raise ValueError(
                f"DatabaseAgent received an execution for capability "
                f"'{execution.capability.value}'."
            )

        if not execution.request.task.strip():
            raise ValueError("DatabaseAgent requires a non-empty task.")

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the database design process.

        The LLM response is parsed into a DatabaseResult.
        """

        result = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=result,
            message="Database design completed successfully.",
        )
