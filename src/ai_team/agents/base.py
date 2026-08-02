"""
Base class for all AI agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from ai_team.agents.dependencies import AgentDependencies
from ai_team.agents.models import (
    AgentExecution,
    AgentInfo,
    AgentResult,
)
from ai_team.infrastructure.llm import BaseLLM
from ai_team.infrastructure.llm.responses import LLMResponse
from ai_team.shared.enums import AgentCapability


class BaseAgent(ABC):
    """
    Base class for every AI agent.

    Implements the Template Method pattern:
    execute() defines the execution lifecycle while run()
    contains the agent-specific implementation.
    """

    INFO: ClassVar[AgentInfo]

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
        """
        Static metadata describing this agent.
        """
        return self.INFO

    @property
    def capability(self) -> AgentCapability:
        """
        Capability implemented by this agent.
        """
        return self.INFO.capability

    # ------------------------------------------------------------------
    # Dependencies
    # ------------------------------------------------------------------

    @property
    def dependencies(self) -> AgentDependencies:
        """
        Shared services available to this agent.
        """
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
        Create or retrieve an LLM instance.
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
        Generate a response using an LLM.

        This method centralizes every interaction with the
        language model.
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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def execute(
        self,
        execution: AgentExecution,
    ) -> AgentExecution:
        """
        Execute the complete lifecycle of an agent.
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
        Validate the execution before running.

        Subclasses may override this method.
        """
        return None

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Prepare the execution before running.

        Typical responsibilities:

        - Build the conversation
        - Load memory
        - Retrieve RAG context
        - Initialize telemetry
        - Configure tools
        """
        return None

    async def finalize(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Finalize the execution.

        Typical responsibilities:

        - Persist memory
        - Emit telemetry
        - Store evaluation data
        - Cleanup temporary resources
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

        Every concrete agent must implement this method.
        """
        ...