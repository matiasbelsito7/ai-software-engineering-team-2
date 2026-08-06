"""
Application dependency container.
"""

from __future__ import annotations

# ------------------------------------------------------------------
# Factories
# ------------------------------------------------------------------

from ai_team.memory.factory import build_memory
from ai_team.observability.factory import build_observability
from ai_team.rag.factory import build_rag
from ai_team.infrastructure.workspace import Workspace
from ai_team.tools.factory import build_tools

# ------------------------------------------------------------------
# Agents
# ------------------------------------------------------------------

from ai_team.agents.architect.agent import ArchitectAgent
from ai_team.agents.backend.agent import BackendAgent
from ai_team.agents.devops.agent import DevOpsAgent
from ai_team.agents.documentation.agent import DocumentationAgent
from ai_team.agents.frontend.agent import FrontendAgent
from ai_team.agents.git.agent import GitAgent
from ai_team.agents.planner.agent import PlannerAgent
from ai_team.agents.qa.agent import QAAgent
from ai_team.agents.reviewer.agent import ReviewerAgent

# ------------------------------------------------------------------
# Docker
# ------------------------------------------------------------------

import docker

from ai_team.tools.docker.factory import (
    build_docker_tool,
)

class Container:
    """
    Application composition root.

    Creates every singleton service and agent.
    """

    def __init__(self) -> None:

        # ---------------------------------------------------------
        # Shared infrastructure
        # ---------------------------------------------------------

        self.embedding_provider = None
        self.vector_store = None
        self.redis = None
        self.database = None
        self.event_bus = None
        self.llm_provider = None
        self.workspace = Workspace(
            root="./workspace"
        )
        self.tools = build_tools(
          workspace=self.workspace,
        )

        # ---------------------------------------------------------
        # Shared services
        # ---------------------------------------------------------

        self.observation = build_observability()

        self.memory = build_memory(
            vector_store=self.vector_store,
        )

        self.rag = build_rag(
            vector_store=self.vector_store,
            embedding_provider=self.embedding_provider,
        )

        # ---------------------------------------------------------
        # Agents
        # ---------------------------------------------------------

        self.planner = PlannerAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.architect = ArchitectAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.backend = BackendAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.frontend = FrontendAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.reviewer = ReviewerAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.qa = QAAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.documentation = DocumentationAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.devops = DevOpsAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        self.git = GitAgent(
            memory=self.memory,
            rag=self.rag,
            observation=self.observation,
        )

        # ---------------------------------------------------------
        # Docker
        # ---------------------------------------------------------

        self.docker_client = docker.from_env()

        self.docker_manager = DockerManager(
            client=self.docker_client,
        )

        self.docker_tool = build_docker_tool(
            manager=self.docker_manager,
        )

        # ---------------------------------------------------------
        # Tools
        # ---------------------------------------------------------

        self.tools = build_tools(
            workspace=self.workspace,
            terminal=self.terminal_tool,
            git=self.git_tool,
            python=self.python_tool,
            docker=self.docker_tool,
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