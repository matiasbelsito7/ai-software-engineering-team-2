"""
Spec agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.spec import SpecParser
from ai_team.agents.result import AgentResult
from ai_team.agents.spec.models import AppSpecification
from ai_team.agents.spec.prompt_builder import SpecPromptBuilder
from ai_team.shared.enums.agents import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class SpecAgent(BaseAgent[AppSpecification]):
    """
    Agent responsible for generating a technical specification
    from a natural language application description.
    """

    INFO = AgentInfo(
        name="spec",
        capability=AgentCapability.SPEC,
        description=(
            "Transforms a natural language app description into a "
            "structured technical specification."
        ),
        version="1.0.0",
    )

    PARSER = SpecParser

    PROMPT_BUILDER = SpecPromptBuilder

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Validate the Spec execution.
        """

        super().validate(execution)

        if execution.capability is not self.capability:
            raise ValueError(
                f"SpecAgent received an execution for capability "
                f"'{execution.capability.value}'."
            )

        if not execution.request.task.strip():
            raise ValueError("SpecAgent requires a non-empty task.")

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the specification generation.

        The LLM response is parsed into an AppSpecification.
        """

        spec = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=spec,
            message=f"Specification generated for '{spec.app_name}'.",
        )
