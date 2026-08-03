"""
Base class for all AI agents.
"""

from __future__ import annotations

from typing import Any, ClassVar

from ai_team.agents.dependencies import AgentDependencies
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.agents.parsers.base import BaseParser
from ai_team.agents.prompt_builder import BasePromptBuilder
from ai_team.infrastructure.llm import BaseLLM
from ai_team.infrastructure.llm.responses import LLMResponse
from ai_team.shared.enums.agents import AgentCapability


class BaseAgent:
    """
    Base class for every AI agent.

    Implements the Template Method pattern.
    """

    INFO: ClassVar[AgentInfo]

    PARSER: ClassVar[type[BaseParser[Any]]]

    PROMPT_BUILDER: ClassVar[type[BasePromptBuilder]]

    def __init__(
        self,
        dependencies: AgentDependencies,
    ) -> None:
        self._validate_configuration()

        self._dependencies = dependencies

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @classmethod
    def _validate_configuration(cls) -> None:
        """
        Validate that the agent declares all required class attributes.
        """

        if getattr(cls, "INFO", None) is None:
            raise RuntimeError(
                f"{cls.__name__} does not define INFO."
            )

        if getattr(cls, "PARSER", None) is None:
            raise RuntimeError(
                f"{cls.__name__} does not define PARSER."
            )

        if getattr(cls, "PROMPT_BUILDER", None) is None:
            raise RuntimeError(
                f"{cls.__name__} does not define PROMPT_BUILDER."
            )

    # ------------------------------------------------------------------
    # Agent Information
    # ------------------------------------------------------------------

    @property
    def info(self) -> AgentInfo:
        return self.INFO

    @property
    def capability(self) -> AgentCapability:
        return self.INFO.capability

    # ------------------------------------------------------------------
    # Dependencies
    # ------------------------------------------------------------------

    @property
    def dependencies(self) -> AgentDependencies:
        return self._dependencies

    @property
    def llm(self) -> BaseLLM:
        return self.dependencies.llm

    @property
    def tools(self):
        return self.dependencies.tools

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    async def generate(
        self,
        execution: AgentExecution,
    ) -> LLMResponse:
        """
        Generate a raw response from the LLM.
        """

        response = await self.llm.generate(
            execution.conversation,
        )

        execution.llm_response = response

        execution.conversation.add_assistant(
            response.content,
        )

        return response

    async def generate_and_parse(
        self,
        execution: AgentExecution,
    ) -> Any:
        """
        Generate a response and parse it.
        """

        response = await self.generate(execution)

        return self.PARSER.parse(response)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def execute(
        self,
        execution: AgentExecution,
    ) -> AgentExecution:
        """
        Execute the complete lifecycle.
        """

        self.validate(execution)

        await self.prepare(execution)

        result = await self.run(execution)

        execution.result = result

        await self.finalize(execution)

        return execution

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Validate the execution.
        """

        return None

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Build the conversation.
        """

        execution.conversation = (
            self.PROMPT_BUILDER.build(
                execution,
            )
        )

    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the agent.
        """

        output = await self.generate_and_parse(
            execution,
        )

        return AgentResult(
            success=True,
            output=output,
        )

    async def finalize(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Finalize the execution.
        """

        return None