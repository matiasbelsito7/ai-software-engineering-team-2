"""
Base class for all AI agents.
"""

from __future__ import annotations

import contextlib
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar

from ai_team.agents.tool_policy import AgentToolPolicy
from ai_team.memory.models import MemoryQuery
from ai_team.rag.models import RetrievalQuery
from ai_team.tools.models import ToolRequest, ToolResult

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ai_team.agents.dependencies import AgentDependencies
    from ai_team.agents.execution import AgentExecution
    from ai_team.agents.info import AgentInfo
    from ai_team.agents.parsers.base import BaseParser
    from ai_team.agents.prompt_builder import BasePromptBuilder
    from ai_team.agents.result import AgentResult
    from ai_team.context.models import ContextWindow
    from ai_team.infrastructure.llm import BaseLLM
    from ai_team.infrastructure.llm.responses import LLMResponse
    from ai_team.memory.models import MemoryContext
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
            raise RuntimeError(f"{cls.__name__} does not define INFO.")

        if getattr(cls, "PARSER", None) is None:
            raise RuntimeError(f"{cls.__name__} does not define PARSER.")

        if getattr(cls, "PROMPT_BUILDER", None) is None:
            raise RuntimeError(f"{cls.__name__} does not define PROMPT_BUILDER.")

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
    ) -> ContextWindow | None:
        """
        Build the context window using the ContextManager.

        Requires execution.graph_state to be set by the orchestration layer.
        """

        if execution.graph_state is None:
            return None

        try:
            return await self.context.build(  # type: ignore[no-any-return]
                execution.graph_state,
            )
        except Exception:
            return None

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

    async def retrieve_memory(
        self,
        execution: AgentExecution,
    ) -> MemoryContext | None:
        """
        Retrieve relevant memories for the current task.
        """

        task = execution.request.task.strip()

        if not task:
            return None

        query = MemoryQuery(
            query=task,
            agent=self.capability,
        )

        try:
            return await self.memory.build_context(  # type: ignore[no-any-return]
                query,
            )
        except Exception:
            return None

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
    # Feedback
    # ------------------------------------------------------------------

    async def request_feedback(
        self,
        execution: AgentExecution,
        *,
        feedback_type: str,
        question: str,
        context: str | None = None,
        options: list[str] | None = None,
    ) -> str:
        """
        Request feedback from the user during execution.

        Returns the user's response string.
        """
        import uuid

        from ai_team.agents.feedback import FeedbackRecord, FeedbackType

        if execution.graph_state is None:
            return ""

        feedback_id = str(uuid.uuid4())
        fb_type = FeedbackType(feedback_type)

        record = FeedbackRecord(
            feedback_id=feedback_id,
            task_id=str(execution.graph_state.execution.execution_id),
            agent=self.info.name,
            feedback_type=fb_type,
            question=question,
            context=context,
            options=options,
            status="pending",
        )

        execution.graph_state.feedback.add_pending(record)

        logger.info(
            "Agent %s requested feedback: %s",
            self.info.name,
            question[:100],
        )

        # In a real implementation, this would wait for the user response
        # For now, return the feedback_id for tracking
        return feedback_id

    def get_feedback_response(
        self,
        execution: AgentExecution,
        feedback_id: str,
    ) -> str | None:
        """
        Get the response to a previously requested feedback.
        """
        if execution.graph_state is None:
            return None

        for record in execution.graph_state.feedback.feedback_history:
            if record.feedback_id == feedback_id:
                return record.response
        return None

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

        Starts observability tracking for this agent execution.
        """

        if self.observations is not None:
            with contextlib.suppress(Exception):
                await self.observations.start_execution(
                    execution_id=str(execution.id),
                    agent=self.info.name,
                )

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

        Retrieves RAG context, memory context, builds the context
        window, and constructs the initial conversation prompt.
        """

        rag_context = await self.retrieve_context(
            execution,
        )

        memory_context = await self.retrieve_memory(
            execution,
        )

        context_window = await self.build_context(
            execution,
        )

        execution.conversation = self.PROMPT_BUILDER.build(
            execution,
            rag_context=rag_context,
            memory_context=memory_context,
            context_window=context_window,
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

        Finishes observability tracking and stores results in memory.
        """

        if self.observations is not None:
            with contextlib.suppress(Exception):
                obs_execution = self.observations.get_execution(
                    str(execution.id),
                )
                if obs_execution is not None:
                    await self.observations.finish_execution(
                        execution=obs_execution,
                    )

        if execution.successful and execution.result is not None:
            await self._store_result_in_memory(execution)

    async def _store_result_in_memory(
        self,
        execution: AgentExecution,
    ) -> None:
        """
        Store the agent result as a memory entry for future reference.
        """

        from ai_team.memory.models import MemoryEntry, MemoryMetadata
        from ai_team.shared.enums import MemoryType

        result = execution.result
        output = result.output if result is not None else None
        message = result.message if result is not None else ""
        output_str = str(output) if output is not None else str(message)

        entry = MemoryEntry(
            memory_type=MemoryType.PROJECT,
            content=f"[{self.info.name}] {execution.request.task}: {output_str[:500]}",
            agent=self.capability,
            metadata=MemoryMetadata(
                source=f"agent:{self.info.name}",
                tags=[self.info.name, "agent_result"],
            ),
        )

        with contextlib.suppress(Exception):
            await self.memory.add(entry)
