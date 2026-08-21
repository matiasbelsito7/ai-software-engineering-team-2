"""
FastAPI application dependencies.

Provides singletons for the Container and the compiled LangGraph.
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ai_team.infrastructure.container import Container


@lru_cache(maxsize=1)
def get_container() -> Container:
    """Return the singleton Container."""

    from ai_team.infrastructure.container import Container

    return Container()


@lru_cache(maxsize=1)
def get_graph() -> Any:
    """Build and compile the LangGraph workflow once."""

    from ai_team.graph.builder import GraphBuilder

    container = get_container()

    builder = GraphBuilder(
        planner=container.planner,
        architect=container.architect,
        backend=container.backend,
        frontend=container.frontend,
        reviewer=container.reviewer,
        qa=container.qa,
        documentation=container.documentation,
        devops=container.devops,
        git=container.git_agent,
    )

    return builder.build()
