"""
Application settings composition.

This module exposes the global Settings object used across the application.

Configuration is intentionally split into multiple files to keep each concern
isolated and maintainable.

Example
-------
from ai_team.infrastructure.config import settings

print(settings.app.name)
print(settings.llm.default_provider)
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import BaseModel

from ai_team.infrastructure.config.app import AppSettings
from ai_team.infrastructure.config.database import DatabaseSettings
from ai_team.infrastructure.config.docker import DockerSettings
from ai_team.infrastructure.config.evaluation import EvaluationSettings
from ai_team.infrastructure.config.http import HttpSettings
from ai_team.infrastructure.config.llm import LLMSettings
from ai_team.infrastructure.config.qdrant import QdrantSettings
from ai_team.infrastructure.config.redis import RedisSettings
from ai_team.infrastructure.config.telemetry import TelemetrySettings


class Settings(BaseModel):
    """
    Root application configuration.

    Aggregates every configuration domain into a single object.
    """

    app: AppSettings = AppSettings()

    docker: DockerSettings = DockerSettings()

    llm: LLMSettings = LLMSettings()

    database: DatabaseSettings = DatabaseSettings()

    redis: RedisSettings = RedisSettings()

    qdrant: QdrantSettings = QdrantSettings()

    telemetry: TelemetrySettings = TelemetrySettings()

    evaluation: EvaluationSettings = EvaluationSettings()

    http: HttpSettings = HttpSettings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the singleton application settings.

    The configuration is loaded once and cached for the lifetime of the
    process.
    """

    return Settings()


settings = get_settings()
