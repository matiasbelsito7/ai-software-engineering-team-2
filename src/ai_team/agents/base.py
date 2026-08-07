"""
Base class for all AI agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from ai_team.agents.dependencies import AgentDependencies
from ai_team.agents.execution import (
    AgentExecution,
    AgentResult,
)
from ai_team.agents.info import AgentInfo
from ai_team.agents.parsers.base import BaseParser
from ai_team.agents.prompt_builder import BasePromptBuilder
from ai_team.context.models import ContextSelection
from ai_team.infrastructure.llm import BaseLLM
from ai_team.infrastructure.llm.responses import LLMResponse
from ai_team.observability.manager import ObservationManager
from ai_team.rag.models import RetrievedContext
from ai_team.shared.enums.agents import AgentCapability
from ai_team.tools.executor import ToolExecutor


class BaseAgent(ABC):
    """
    Base class for every AI agent.

    Provides:
    - LLM access
    - Context management
    - Memory access
    - RAG retrieval
    - Tool execution
    - Observability hooks
    - Standard execution lifecycle
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

        self._tool_executor = ToolExecutor(
            dependencies.tools,
        )

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    @classmethod
    def _validate_configuration(cls) -> None:

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
    def memory(self):
        return self.dependencies.memory

    @property
    def rag(self):
        return self.dependencies.rag

    @property
    def context(self):
        return self.dependencies.context

    @property
    def observations(self) -> ObservationManager:
        return self.dependencies.observability

    @property
    def tool_executor(self) -> ToolExecutor:
        return self._tool_executor

    # ------------------------------------------------------------------
    # Context
    # ------------------------------------------------------------------

    async def build_context(
        self,
        execution: AgentExecution,
    ) -> ContextSelection:
        """
        Build the agent context.
        """

        return await self.context.build(
            conversation=execution.conversation.messages,
            memories=[],
            documents=[],
        )

    async def retrieve_context(
        self,
        execution: AgentExecution,
    ) -> RetrievedContext | None:
        """
        Retrieve additional context from RAG.
        """

        if not execution.query:
            return None

        return await self.rag.retrieve(
            execution.query,
        )

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    async def generate(
        self,
        execution: AgentExecution,
    ) -> LLMResponse:

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

        response = await self.generate(
            execution,
        )

        return self.PARSER.parse(response)

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------

    async def use_tool(
        self,
        *,
        tool_name: str,
        parameters: dict[str, Any],
    ):
        """
        Execute a tool through the ToolExecutor.
        """

        return await self.tool_executor.execute(
            tool_name=tool_name,
            parameters=parameters,
        )

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

        await self.before_execution(execution)

        await self.prepare(execution)

        result = await self.run(execution)

        execution.result = result

        await self.after_execution(execution)

        return execution

    # ------------------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------------------

    async def before_execution(
        self,
        execution: AgentExecution,
    ) -> None:
        return None

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        return None

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:

        execution.context = await self.build_context(
            execution,
        )

        execution.retrieved_context = (
            await self.retrieve_context(execution)
        )

        execution.conversation = (
            self.PROMPT_BUILDER.build(
                execution,
            )
        )

    @abstractmethod
    async def run(
        self,
        execution: AgentExecution,
    ) -> AgentResult:
        """
        Execute the agent-specific logic.
        """

    async def after_execution(
        self,
        execution: AgentExecution,
    ) -> None:
        return None