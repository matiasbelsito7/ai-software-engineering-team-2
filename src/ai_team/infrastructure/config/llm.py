"""
LLM configuration.

Defines the configuration required by language model providers.

This module is intentionally configuration-only.
Provider implementations belong in:

    infrastructure/llm/providers/
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_team.shared.enums import LLMProvider


class LLMSettings(BaseSettings):
    """
    Language Model configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="LLM_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ###########################################################################
    # Provider
    ###########################################################################

    default_provider: LLMProvider = Field(
        default=LLMProvider.OPENROUTER,
        description="Default LLM provider.",
    )

    ###########################################################################
    # OpenRouter
    ###########################################################################

    openrouter_api_key: str = Field(
        default="",
        description="OpenRouter API key.",
    )

    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API endpoint.",
    )

    openrouter_model: str = Field(
        default="anthropic/claude-sonnet-4",
        description="Default OpenRouter model.",
    )

    ###########################################################################
    # Ollama
    ###########################################################################

    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL.",
    )

    ollama_model: str = Field(
        default="qwen3:latest",
        description="Default local model.",
    )

    ###########################################################################
    # Generation
    ###########################################################################

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="Default generation temperature.",
    )

    max_tokens: int = Field(
        default=4096,
        gt=0,
        description="Maximum generated tokens.",
    )

    top_p: float = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="Top-p sampling.",
    )

    frequency_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Frequency penalty.",
    )

    presence_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Presence penalty.",
    )

    ###########################################################################
    # Timeouts
    ###########################################################################

    timeout: int = Field(
        default=120,
        gt=0,
        description="Request timeout in seconds.",
    )

    max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum retry attempts.",
    )

    ###########################################################################
    # Streaming
    ###########################################################################

    enable_streaming: bool = Field(
        default=True,
        description="Enable streaming responses.",
    )

    ###########################################################################
    # Cost Tracking
    ###########################################################################

    track_token_usage: bool = Field(
        default=True,
        description="Track prompt/completion token usage.",
    )

    track_costs: bool = Field(
        default=True,
        description="Track estimated request cost.",
    )
