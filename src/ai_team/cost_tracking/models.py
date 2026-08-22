"""
Cost tracking models.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LLMProvider(StrEnum):
    """LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    LOCAL = "local"


class CostRecord(BaseModel):
    """Record of LLM usage cost."""

    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(..., min_length=1)
    task_id: str | None = None
    agent_name: str | None = None
    provider: LLMProvider
    model: str
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    total_tokens: int = Field(ge=0)
    input_cost: float = Field(ge=0.0)
    output_cost: float = Field(ge=0.0)
    total_cost: float = Field(ge=0.0)
    currency: str = "USD"
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(
        default_factory=lambda: __import__("datetime").datetime.utcnow().isoformat()
    )


class CostSummary(BaseModel):
    """Cost summary for a period or filter."""

    model_config = ConfigDict(extra="forbid")

    total_cost: float = 0.0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    total_requests: int = 0
    by_provider: dict[str, float] = Field(default_factory=dict)
    by_model: dict[str, float] = Field(default_factory=dict)
    by_agent: dict[str, float] = Field(default_factory=dict)
    by_task: dict[str, float] = Field(default_factory=dict)


class CostAlert(BaseModel):
    """Cost alert configuration."""

    model_config = ConfigDict(extra="forbid")

    alert_id: str
    name: str
    threshold: float = Field(gt=0.0)
    period: str = "daily"  # daily, weekly, monthly
    provider: LLMProvider | None = None
    model: str | None = None
    enabled: bool = True
    triggered: bool = False
    last_triggered: str | None = None


class CostBudget(BaseModel):
    """Budget configuration."""

    model_config = ConfigDict(extra="forbid")

    budget_id: str
    name: str
    limit: float = Field(gt=0.0)
    period: str = "monthly"  # daily, weekly, monthly
    provider: LLMProvider | None = None
    model: str | None = None
    current_usage: float = 0.0
    remaining: float = 0.0
    percentage_used: float = 0.0


class ModelPricing(BaseModel):
    """Model pricing information."""

    model_config = ConfigDict(extra="forbid")

    provider: LLMProvider
    model: str
    input_price_per_1k: float = Field(ge=0.0)
    output_price_per_1k: float = Field(ge=0.0)
    currency: str = "USD"
