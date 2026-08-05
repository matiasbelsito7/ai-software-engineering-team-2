"""
Application dependency container.
"""

from __future__ import annotations

from ai_team.memory.factory import build_memory
from ai_team.observability.factory import build_observability
from ai_team.rag.factory import build_rag


class Container:
    """
    Composition root of the application.
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

        # ---------------------------------------------------------
        # Application modules
        # ---------------------------------------------------------

        self.observation = build_observability()

        self.memory = build_memory(
            vector_store=self.vector_store,
        )

        self.rag = build_rag(
            vector_store=self.vector_store,
            embedding_provider=self.embedding_provider,
        )

    async def initialize(self) -> None:
        """
        Initialize managed services.
        """

        for service in (
            self.observation,
            self.memory,
            self.rag,
        ):
            initialize = getattr(service, "initialize", None)

            if initialize is not None:
                await initialize()

    async def shutdown(self) -> None:
        """
        Shutdown managed services.
        """

        for service in (
            self.rag,
            self.memory,
            self.observation,
        ):
            shutdown = getattr(service, "shutdown", None)

            if shutdown is not None:
                await shutdown()