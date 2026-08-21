"""
Base class for all AI agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar

from ai_team.agents.tool_policy import AgentToolPolicy
from ai_team.rag.models import RetrievalQuery
from ai_team.tools.models import ToolRequest, ToolResult

if TYPE_CHECKING:
    from ai_team.agents.dependencies import AgentDependencies
    from ai_team.agents.execution import AgentExecution
    from ai_team.agents.info import AgentInfo
    from ai_team.agents.parsers.base import BaseParser
    from ai_team.agents.prompt_builder import BasePromptBuilder
    from ai_team.agents.result import AgentResult
    from ai_team.context.models import ContextSelection
    from ai_team.infrastructure.llm import BaseLLM
    from ai_team.infrastructure.llm.responses import LLMResponse
    from ai_team.observability.manager import ObservationManager
    from ai_team.rag.models import RAGContext
    from ai_team.shared.enums.agents import AgentCapability
    from ai_team.tools.executor import ToolExecutor


class BaseAgent[T](ABC):
    """
    Base class for every AI agent.

    Provides:

    - LLM access
    - Context management
    - Memory access
    - RAG retrieval
    - Tool execution
    - Tool authorization
    - Observability hooks
    - Standard execution lifecycle
    """

    INFO: ClassVar[AgentInfo]

    PARSER: ClassVar[type[BaseParser[T]]]  # type: ignore[type-var]

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
        Validate required agent configuration.
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
    def memory(self) -> Any:
        return self.dependencies.memory

    @property
    def rag(self) -> Any:
        return self.dependencies.rag

    @property
    def context(self) -> Any:
        return self.dependencies.context

    @property
    def observations(self) -> ObservationManager | None:
        return self.dependencies.observability

    @property
    def tool_executor(self) -> ToolExecutor:
        return self.dependencies.tool_executor

    # ------------------------------------------------------------------
    # Context
    # ------------------------------------------------------------------

    async def build_context(
        self,
        execution: AgentExecution,
    ) -> ContextSelection:
        """
        Build the context required by the agent.

        The ContextManager currently operates on GraphState, so the
        orchestration layer is responsible for constructing the final
        GraphState. This method provides the agent-level extension
        point without introducing a second incompatible context API.
        """

        raise NotImplementedError(
            "Context construction requires the orchestration "
            "GraphState and must be implemented by the "
            "LangGraph orchestration layer."
        )

    async def retrieve_context(
        self,
        execution: AgentExecution,
    ) -> RAGContext | None:
        """
        Retrieve additional context from RAG.
        """

        task = execution.request.task.strip()

        if not task:
            return None

        return await self.rag.build_context(  # type: ignore[no-any-return]
            self._build_rag_query(
                task,
            ),
        )

    @staticmethod
    def _build_rag_query(
        task: str,
    ) -> RetrievalQuery:
        """
        Build a RAG retrieval query.

        Kept isolated so the retrieval contract can evolve without
        coupling concrete agents to the RAG implementation.
        """

        return RetrievalQuery(
            query=task,
        )

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    async def generate(
        self,
        execution: AgentExecution,
    ) -> LLMResponse:
        """
        Generate a response from the LLM.
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
    ) -> T:
        """
        Generate an LLM response and parse it into the
        agent-specific model.
        """

        response = await self.generate(
            execution,
        )

        return self.PARSER.parse(
            response,
        )

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------

    async def use_tool(
        self,
        *,
        tool_name: str,
        parameters: dict[str, Any],
    ) -> ToolResult:
        """
        Execute an authorized tool through the ToolExecutor.
        """

        AgentToolPolicy.validate(
            self.capability,
            tool_name,
        )

        request = ToolRequest(
            tool=tool_name,
            parameters=parameters,
        )

        return await self.tool_executor.execute(
            request,
        )

    def can_use_tool(
        self,
        tool_name: str,
    ) -> bool:
        """
        Return whether this agent is authorized to use a tool.
        """

        return AgentToolPolicy.can_use(
            self.capability,
            tool_name,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def execute(
        self,
        execution: AgentExecution,
    ) -> AgentExecution:
        """
        Execute the complete agent lifecycle.
        """

        self.validate(
            execution,
        )

        await self.before_execution(
            execution,
        )

        await self.prepare(
            execution,
        )

        result = await self.run(
            execution,
        )

        execution.result = result

        await self.after_execution(
            execution,
        )

        return execution

    # ------------------------------------------------------------------
    # Lifecycle Hooks
    # ------------------------------------------------------------------

    async def before_execution(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Hook executed before preparation.
        """

        return None

    def validate(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Validate the execution before starting.
        """

        return None

    async def prepare(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Prepare the agent execution.

        RAG retrieval is performed here. Context construction remains
        delegated to the orchestration layer because ContextManager
        currently consumes GraphState.
        """

        await self.retrieve_context(
            execution,
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

        raise NotImplementedError

    async def after_execution(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Hook executed after agent execution.
        """

        return None
