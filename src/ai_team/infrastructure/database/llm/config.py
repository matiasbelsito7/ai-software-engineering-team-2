"""
Generation configuration shared by every LLM provider.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GenerationConfig(BaseModel):
    """
    Provider-agnostic generation parameters.

    This model represents the common configuration accepted by
    every LLM provider. Provider-specific options can be passed
    through `extra_options`.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    # ------------------------------------------------------------------
    # Sampling
    # ------------------------------------------------------------------

    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
    )

    top_p: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    seed: int | None = None

    # ------------------------------------------------------------------
    # Length
    # ------------------------------------------------------------------

    max_tokens: int | None = Field(
        default=None,
        gt=0,
    )

    stop_sequences: list[str] = Field(
        default_factory=list,
    )

    # ------------------------------------------------------------------
    # Tool Calling
    # ------------------------------------------------------------------

    tools: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    tool_choice: str | None = None

    parallel_tool_calls: bool | None = None

    # ------------------------------------------------------------------
    # Structured Output
    # ------------------------------------------------------------------

    response_format: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Reasoning Models
    # ------------------------------------------------------------------

    reasoning_effort: str | None = None

    # ------------------------------------------------------------------
    # Provider-specific extensions
    # ------------------------------------------------------------------

    extra_options: dict[str, Any] = Field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def to_provider_dict(self) -> dict[str, Any]:
        """
        Convert the configuration into a dictionary suitable for
        provider APIs, omitting unset or empty values.
        """

        data = self.model_dump(
            exclude_none=True,
        )

        if not data.get("stop_sequences"):
            data.pop("stop_sequences", None)

        if not data.get("tools"):
            data.pop("tools", None)

        extra = data.pop("extra_options", {})

        data.update(extra)

        return data