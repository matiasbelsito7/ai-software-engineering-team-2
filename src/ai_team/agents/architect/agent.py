"""
Architect agent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ai_team.agents.architect.models import ArchitectureDesign
from ai_team.agents.architect.prompt_builder import ArchitectPromptBuilder
from ai_team.agents.base import BaseAgent
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.architect import ArchitectParser
from ai_team.agents.result import AgentResult
from ai_team.shared.enums.agents import AgentCapability

if TYPE_CHECKING:
    from ai_team.agents.execution import AgentExecution


class ArchitectAgent(BaseAgent[ArchitectureDesign]):
    """
    Agent responsible for designing the architecture and
    technical structure required to implement a planned task.
    """

    INFO = AgentInfo(
        name="architect",
        capability=AgentCapability.ARCHITECT,
        description=(
            "Designs the technical architecture and structure "
            "required to implement a software-engineering task."
        ),
        version="1.0.0",
    )

    PARSER = ArchitectParser

    PROMPT_BUILDER = ArchitectPromptBuilder

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Validate the Architect execution.
        """

        super().validate(execution)

        if execution.capability is not self.capability:
            raise ValueError(
                "ArchitectAgent received an execution for "
                f"capability '{execution.capability.value}'."
            )

        if not execution.request.task.strip():
            raise ValueError(
                "ArchitectAgent requires a non-empty task."
            )

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the architecture design process.

        The LLM response is parsed into an ArchitectureDesign.
        """

        architecture = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=architecture,
            message="Architecture design completed successfully.",
        )
