"""
Telemetry configuration.

Defines the configuration for logging, tracing, metrics and observability.

This module contains configuration only.

Implementations belong to:

    observability/
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelemetrySettings(BaseSettings):
    """
    Telemetry and observability configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="TELEMETRY_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Global
    ###########################################################################

    enabled: bool = Field(
        default=True,
        description="Enable observability.",
    )

    service_name: str = Field(
        default="ai-software-engineering-team",
        description="Service name reported by telemetry.",
    )

    service_version: str = Field(
        default="0.1.0",
        description="Application version.",
    )

    environment: str = Field(
        default="development",
        description="Deployment environment.",
    )

    ###########################################################################
    # Logging (Structlog)
    ###########################################################################

    enable_logging: bool = Field(
        default=True,
        description="Enable structured logging.",
    )

    log_level: str = Field(
        default="INFO",
        description="Application log level.",
    )

    json_logs: bool = Field(
        default=False,
        description="Emit logs as JSON.",
    )

    ###########################################################################
    # OpenTelemetry
    ###########################################################################

    enable_tracing: bool = Field(
        default=True,
        description="Enable distributed tracing.",
    )

    otlp_endpoint: str = Field(
        default="http://localhost:4317",
        description="OTLP collector endpoint.",
    )

    export_timeout: int = Field(
        default=30,
        gt=0,
        description="Exporter timeout in seconds.",
    )

    ###########################################################################
    # LangSmith
    ###########################################################################

    enable_langsmith: bool = Field(
        default=True,
        description="Enable LangSmith integration.",
    )

    langsmith_api_key: str = Field(
        default="",
        description="LangSmith API key.",
    )

    langsmith_project: str = Field(
        default="ai-software-engineering-team",
        description="LangSmith project name.",
    )

    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com",
        description="LangSmith endpoint.",
    )

    ###########################################################################
    # Metrics
    ###########################################################################

    enable_metrics: bool = Field(
        default=True,
        description="Enable metrics collection.",
    )

    metrics_port: int = Field(
        default=9090,
        ge=1,
        le=65535,
        description="Prometheus metrics port.",
    )

    ###########################################################################
    # Token Tracking
    ###########################################################################

    track_tokens: bool = Field(
        default=True,
        description="Track prompt and completion tokens.",
    )

    track_costs: bool = Field(
        default=True,
        description="Track estimated LLM costs.",
    )

    ###########################################################################
    # Performance
    ###########################################################################

    record_latency: bool = Field(
        default=True,
        description="Record request latency.",
    )

    record_memory_usage: bool = Field(
        default=True,
        description="Record memory usage.",
    )
