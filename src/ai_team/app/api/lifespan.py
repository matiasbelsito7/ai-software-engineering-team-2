"""
FastAPI application lifespan.

Manages startup and shutdown of shared application resources.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the application lifecycle.

    Args:
        app: The FastAPI application instance.
    """

    from ai_team.app.api.dependencies import (
        get_container,
        get_graph,
    )

    logger.info("Starting AI Software Engineering Team…")

    container = get_container()
    await container.initialize()

    graph = get_graph()
    app.state.container = container
    app.state.graph = graph

    logger.info("Application ready.")

    yield

    logger.info("Shutting down…")

    await container.shutdown()

    logger.info("Shutdown complete.")
