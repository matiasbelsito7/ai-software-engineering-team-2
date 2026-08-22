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
    APIKeyAuthMiddleware,
    ErrorHandlingMiddleware,
    RateLimitMiddleware,
    RequestIDMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from ai_team.app.api.routers import (
    feedback_router,
    health_router,
    streaming_router,
    tasks_router,
    templates_router,
    ws_router,
)
from ai_team.app.api.security.audit import SecurityAuditLogger
from ai_team.app.api.task_store import TaskStore
from ai_team.infrastructure.config.app import AppSettings
from ai_team.infrastructure.config.security import SecuritySettings

logger = logging.getLogger(__name__)

app_settings = AppSettings()
sec_settings = SecuritySettings()

audit = SecurityAuditLogger()


# =====================================================================
# Application
# =====================================================================


def create_app() -> FastAPI:
    application = FastAPI(
        title="AI Software Engineering Team",
        version=app_settings.version,
        docs_url=app_settings.docs_url,
        redoc_url=app_settings.redoc_url,
        openapi_url=app_settings.openapi_url,
        lifespan=lifespan,
    )

    # --- State ---
    application.state.task_store = TaskStore()

    # --- Middleware (order matters: last added = first executed) ---
    # Security headers (outermost response)
    if sec_settings.security_headers_enabled:
        application.add_middleware(
            SecurityHeadersMiddleware,
            hsts_max_age=sec_settings.hsts_max_age,
            content_security_policy=sec_settings.content_security_policy,
        )

    # Request ID
    application.add_middleware(RequestIDMiddleware)

    # Rate limiting
    if sec_settings.rate_limit_enabled:
        application.add_middleware(
            RateLimitMiddleware,
            per_ip=sec_settings.rate_limit_per_ip,
            per_key=sec_settings.rate_limit_per_key,
            burst=sec_settings.rate_limit_burst,
            audit_logger=audit._logger,
        )

    # API key authentication
    if sec_settings.auth_enabled and sec_settings.api_keys:
        application.add_middleware(
            APIKeyAuthMiddleware,
            api_keys=sec_settings.api_keys,
            header=sec_settings.auth_header,
            audit_logger=audit._logger,
        )

    # Request logging
    application.add_middleware(RequestLoggingMiddleware)

    # Error handling (innermost)
    application.add_middleware(ErrorHandlingMiddleware)

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.allowed_origins,
        allow_methods=app_settings.allowed_methods,
        allow_headers=app_settings.allowed_headers,
        allow_credentials=app_settings.allow_credentials,
    )

    # --- Exception handlers ---
    register_exception_handlers(application)

    # --- Routers ---
    application.include_router(health_router, prefix=app_settings.api_prefix)
    application.include_router(tasks_router, prefix=app_settings.api_prefix)
    application.include_router(templates_router, prefix=app_settings.api_prefix)
    application.include_router(streaming_router, prefix=app_settings.api_prefix)
    application.include_router(feedback_router, prefix=app_settings.api_prefix)
    application.include_router(ws_router, prefix=app_settings.api_prefix)

    return application


app = create_app()
