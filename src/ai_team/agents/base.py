"""
Base class for all AI agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from ai_team.agents.dependencies import AgentDependencies
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.agents.parsers.base import BaseParser
from ai_team.infrastructure.llm import BaseLLM
from ai_team.infrastructure.llm.responses import LLMResponse
from ai_team.shared.enums import AgentCapability


class BaseAgent(ABC):
    """
    Base class for every AI agent.

    Implements the Template Method pattern.
    """

    INFO: ClassVar[AgentInfo]

    PARSER: ClassVar[type[BaseParser[Any]] | None] = None

    def __init__(
        self,
        dependencies: AgentDependencies,
    ) -> None:
        self._dependencies = dependencies

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
    def memory(self):
        return self.dependencies.memory

    @property
    def rag(self):
        return self.dependencies.rag

    @property
    def telemetry(self):
        return self.dependencies.telemetry

    @property
    def tools(self):
        return self.dependencies.tools

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    def get_llm(
        self,
        *,
        provider: str | None = None,
        model: str | None = None,
    ) -> BaseLLM:
        """
        Create an LLM instance.
        """

        return self.dependencies.llm_factory.create(
            provider=provider,
            model=model,
        )

    async def generate(
        self,
        execution: AgentExecution,
        *,
        provider: str | None = None,
        model: str | None = None,
    ) -> LLMResponse:
        """
        Generate a raw response from the LLM.
        """

        llm = self.get_llm(
            provider=provider,
            model=model,
        )

        response = await llm.generate(
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
        *,
        provider: str | None = None,
        model: str | None = None,
    ) -> Any:
        """
        Generate a response and parse it using the configured parser.
        """

        if self.PARSER is None:
            raise RuntimeError(
                f"{self.__class__.__name__} "
                "does not define a PARSER."
            )

        response = await self.generate(
            execution,
            provider=provider,
            model=model,
        )

        return self.PARSER.parse(response)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def execute(
        self,
        execution: AgentExecution,
    ) -> AgentExecution:
        """
        Execute the agent lifecycle.
        """

        self.validate(execution)

        await self.prepare(execution)

        result = await self.run(execution)

        execution.result = result

        await self.finalize(execution)

        return execution

    # ------------------------------------------------------------------
    # Lifecycle Hooks
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
        Prepare the execution.
        """

        return None

    async def finalize(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Finalize the execution.
        """

        return None

    # ------------------------------------------------------------------
    # Agent Logic
    # ------------------------------------------------------------------

    @abstractmethod
    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the agent-specific logic.
        """
        ...