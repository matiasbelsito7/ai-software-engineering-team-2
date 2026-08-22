"""
AI Software Engineering Team - FastAPI application.

Run with:
    uvicorn ai_team.app.api.main:app --reload
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_team.app.api.exceptions.handlers import register_exception_handlers
from ai_team.app.api.lifespan import lifespan
from ai_team.app.api.middleware import (
    ErrorHandlingMiddleware,
    RequestLoggingMiddleware,
)
from ai_team.app.api.routers import health_router, tasks_router, ws_router
from ai_team.app.api.task_store import TaskStore
from ai_team.infrastructure.config.app import AppSettings

logger = logging.getLogger(__name__)

settings = AppSettings()


# =====================================================================
# Application
# =====================================================================


def create_app() -> FastAPI:
    application = FastAPI(
        title="AI Software Engineering Team",
        version=settings.version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        openapi_url=settings.openapi_url,
        lifespan=lifespan,
    )

    # --- State ---
    application.state.task_store = TaskStore()

    # --- Middleware (order matters: last added = first executed) ---
    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(ErrorHandlingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
        allow_credentials=settings.allow_credentials,
    )

    # --- Exception handlers ---
    register_exception_handlers(application)

    # --- Routers ---
    application.include_router(health_router, prefix=settings.api_prefix)
    application.include_router(tasks_router, prefix=settings.api_prefix)
    application.include_router(ws_router, prefix=settings.api_prefix)

    return application


app = create_app()
