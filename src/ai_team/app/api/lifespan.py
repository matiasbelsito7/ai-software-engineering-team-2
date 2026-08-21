"""
FastAPI application lifespan.

Manages startup and shutdown of shared application resources.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage the application lifecycle.

    Args:
        app: The FastAPI application instance.
    """
    # Startup
    yield
    # Shutdown
