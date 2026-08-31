"""
Application dependency container.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# ------------------------------------------------------------------
# Agents
# ------------------------------------------------------------------
from ai_team.agents.architect.agent import ArchitectAgent
from ai_team.agents.backend.agent import BackendAgent
from ai_team.agents.dependencies import AgentDependencies
from ai_team.agents.devops.agent import DevOpsAgent
from ai_team.agents.documentation.agent import DocumentationAgent
from ai_team.agents.frontend.agent import FrontendAgent
from ai_team.agents.git.agent import GitAgent
from ai_team.agents.planner.agent import PlannerAgent
from ai_team.agents.qa.agent import QAAgent
from ai_team.agents.reviewer.agent import ReviewerAgent
from ai_team.agents.spec.agent import SpecAgent
from ai_team.agents.tools import AgentTools

# ------------------------------------------------------------------
# Factories
# ------------------------------------------------------------------
from ai_team.context.factory import build_context
from ai_team.infrastructure.llm.factory import LLMFactory
from ai_team.infrastructure.workspace import Workspace
from ai_team.memory.factory import build_memory
from ai_team.memory.retrieval.keyword import (
    KeywordRetriever as MemoryKeywordRetriever,
)
from ai_team.memory.retrieval.semantic import (
    SemanticRetriever as MemorySemanticRetriever,
)
from ai_team.memory.stores.semantic import SemanticMemoryStore
from ai_team.observability.factory import build_observability
from ai_team.rag.factory import build_rag
from ai_team.rag.retrieval.keyword import KeywordRetriever
from ai_team.rag.retrieval.semantic import SemanticRetriever
from ai_team.rag.stores.memory import InMemoryVectorStore
from ai_team.tools.docker.factory import (
    build_docker_tool,
)
from ai_team.tools.docker.manager import DockerManager
from ai_team.tools.executor import ToolExecutor
from ai_team.tools.filesystem import FilesystemTool
from ai_team.tools.git import GitTool
from ai_team.tools.manager import ToolManager
from ai_team.tools.memory_tool import MemoryTool
from ai_team.tools.python import PythonTool
from ai_team.tools.rag_tool import RAGTool
from ai_team.tools.terminal import TerminalTool

if TYPE_CHECKING:
    from ai_team.tools.docker.docker import DockerTool


class _NoOpChunkingPipeline:
    def process(self, document):  # type: ignore[no-untyped-def]
        from ai_team.rag.models import DocumentChunk

        return [
            DocumentChunk(
                document_id=document.id,
                content=document.content,
                uri=document.source.uri,
                source_type=document.source.type,
                metadata=document.metadata,
                chunk_index=0,
            ),
        ]


class _NoOpEmbeddingProvider:
    @property
    def model(self) -> str:
        return "noop"

    @property
    def dimensions(self) -> int:
        return 0

    async def embed(self, text: str) -> list[float]:
        return []

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [[] for _ in texts]

    async def health(self) -> bool:
        return True

    async def close(self) -> None:
        pass


class Container:
    """
    Application composition root.

    Creates every singleton service and agent.
    """

    def __init__(self) -> None:

        self.workspace = Workspace(root="./workspace")

        self.observation = build_observability()

        semantic_store = SemanticMemoryStore()

        memory_semantic = MemorySemanticRetriever(
            store=semantic_store,
        )

        memory_keyword = MemoryKeywordRetriever(
            store=semantic_store,
        )

        self.memory = build_memory(
            semantic_retriever=memory_semantic,
            keyword_retriever=memory_keyword,
        )

        rag_store = InMemoryVectorStore()

        rag_embedding: Any = _NoOpEmbeddingProvider()

        rag_semantic = SemanticRetriever(
            store=rag_store,
            embedding=rag_embedding,
        )

        rag_keyword = KeywordRetriever(
            store=rag_store,
        )

        self.rag = build_rag(
            chunking=_NoOpChunkingPipeline(),  # type: ignore[arg-type]
            embedding=rag_embedding,
            semantic=rag_semantic,
            keyword=rag_keyword,
            store=rag_store,
        )

        self.llm = LLMFactory.create()

        self.context = build_context(
            llm=self.llm,
        )

        # ---------------------------------------------------------
        # Tools
        # ---------------------------------------------------------

        self.terminal_tool = TerminalTool(
            workspace=self.workspace,
        )

        self.git_tool = GitTool(
            terminal=self.terminal_tool,
        )

        self.python_tool = PythonTool(
            terminal=self.terminal_tool,
        )

        self.filesystem_tool = FilesystemTool(
            workspace=self.workspace,
        )

        # ---------------------------------------------------------
        # Docker
        # ---------------------------------------------------------

        from ai_team.infrastructure.config.settings import settings as app_settings

        self.docker_tool: DockerTool | None = None
        self.docker_client: Any = None
        self.docker_manager: Any = None

        try:
            import docker

            self.docker_client = docker.from_env(
                timeout=app_settings.docker.timeout,
            )

            self.docker_manager = DockerManager(
                client=self.docker_client,
            )

            self.docker_tool = build_docker_tool(
                manager=self.docker_manager,
                blocked_images=app_settings.docker.blocked_images,
                privileged=app_settings.docker.privileged,
            )
        except Exception:
            self.docker_client = None
            self.docker_manager = None

        self.tool_manager = ToolManager()

        for tool in (
            self.filesystem_tool,
            self.terminal_tool,
            self.git_tool,
            self.python_tool,
        ):
            self.tool_manager.register(tool)

        rag_tool = RAGTool(rag=self.rag)
        self.tool_manager.register(rag_tool)

        memory_tool = MemoryTool(memory=self.memory)
        self.tool_manager.register(memory_tool)

        if self.docker_tool is not None:
            self.tool_manager.register(self.docker_tool)

        # HTTP tool
        try:
            import httpx

            from ai_team.tools.http.factory import build_http_tool
            from ai_team.tools.http.manager import HttpManager

            http_client = httpx.AsyncClient()
            http_manager = HttpManager(client=http_client)
            http_tool = build_http_tool(manager=http_manager)
            self.tool_manager.register(http_tool)
        except Exception:
            pass

        # Browser tool
        try:
            from ai_team.tools.browser.factory import build_browser_tool
            from ai_team.tools.browser.manager import BrowserManager

            browser_manager = BrowserManager()
            browser_tool = build_browser_tool(manager=browser_manager)
            self.tool_manager.register(browser_tool)
        except Exception:
            pass

        self.tool_executor = ToolExecutor(
            manager=self.tool_manager,
            observations=self.observation,
        )

        # ---------------------------------------------------------
        # Agents
        # ---------------------------------------------------------

        self.agent_deps = AgentDependencies(
            llm=self.llm,
            tools=AgentTools(
                filesystem=self.filesystem_tool,
                rag=self.rag,
                memory=self.memory,
            ),
            tool_executor=self.tool_executor,
            context=self.context,
            memory=self.memory,
            rag=self.rag,
            observability=self.observation,
        )

        self.spec = SpecAgent(
            dependencies=self.agent_deps,
        )

        self.planner = PlannerAgent(
            dependencies=self.agent_deps,
        )

        self.architect = ArchitectAgent(
            dependencies=self.agent_deps,
        )

        self.backend = BackendAgent(
            dependencies=self.agent_deps,
        )

        self.frontend = FrontendAgent(
            dependencies=self.agent_deps,
        )

        self.reviewer = ReviewerAgent(
            dependencies=self.agent_deps,
        )

        self.qa = QAAgent(
            dependencies=self.agent_deps,
        )

        self.documentation = DocumentationAgent(
            dependencies=self.agent_deps,
        )

        self.devops = DevOpsAgent(
            dependencies=self.agent_deps,
        )

        self.git_agent = GitAgent(
            dependencies=self.agent_deps,
        )

    async def initialize(self) -> None:

        for service in (
            self.observation,
            self.memory,
            self.rag,
        ):
            initialize = getattr(service, "initialize", None)

            if initialize is not None:
                await initialize()

    async def shutdown(self) -> None:

        for service in (
            self.rag,
            self.memory,
            self.observation,
        ):
            shutdown = getattr(service, "shutdown", None)

            if shutdown is not None:
                await shutdown()

        if self.docker_manager is not None:
            self.docker_manager.close()

    def set_approval_context(
        self,
        *,
        task_store: Any = None,
        task_id: str | None = None,
        agent: str | None = None,
    ) -> None:
        """Set human-in-the-loop approval context on the terminal tool."""

        self.terminal_tool.set_approval_context(
            task_store=task_store,
            task_id=task_id,
            agent=agent,
        )
