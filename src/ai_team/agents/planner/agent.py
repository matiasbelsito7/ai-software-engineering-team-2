"""
Planner agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.planner import PlannerParser
from ai_team.agents.planner.models import ExecutionPlan
from ai_team.agents.planner.prompt_builder import PlannerPromptBuilder
from ai_team.agents.result import AgentResult
from ai_team.shared.enums.agents import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class PlannerAgent(BaseAgent[ExecutionPlan]):
    """
    Agent responsible for decomposing a software-engineering
    task into an ordered execution plan.
    """

    INFO = AgentInfo(
        name="planner",
        capability=AgentCapability.PLANNER,
        description=(
            "Analyzes a software-engineering task and produces "
            "an ordered execution plan."
        ),
        version="1.0.0",
    )

    PARSER = PlannerParser

    PROMPT_BUILDER = PlannerPromptBuilder

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Validate the Planner execution.
        """

        super().validate(execution)

        if execution.capability is not self.capability:
            raise ValueError(
                "PlannerAgent received an execution for "
                f"capability '{execution.capability.value}'."
            )

        if not execution.request.task.strip():
            raise ValueError(
                "PlannerAgent requires a non-empty task."
            )

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the planning process.

        The LLM response is parsed into an ExecutionPlan.
        """

        plan = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=plan,
            message="Planning completed successfully.",
        )
