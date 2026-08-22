"""
Cost tracking API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CostRecordSchema(BaseModel):
    """Cost record schema."""

    model_config = ConfigDict(extra="forbid")

    record_id: str
    task_id: str | None = None
    agent_name: str | None = None
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float
    currency: str = "USD"
    timestamp: str


class CostRecordRequest(BaseModel):
    """Request to record cost."""

    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(..., min_length=1)
    provider: str
    model: str
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    task_id: str | None = None
    agent_name: str | None = None


class CostSummarySchema(BaseModel):
    """Cost summary schema."""

    model_config = ConfigDict(extra="forbid")

    total_cost: float
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int
    total_requests: int
    by_provider: dict[str, float]
    by_model: dict[str, float]
    by_agent: dict[str, float]
    by_task: dict[str, float]


class CostAlertSchema(BaseModel):
    """Cost alert schema."""

    model_config = ConfigDict(extra="forbid")

    alert_id: str
    name: str
    threshold: float
    period: str = "daily"
    provider: str | None = None
    model: str | None = None
    enabled: bool = True
    triggered: bool = False
    last_triggered: str | None = None


class CostAlertRequest(BaseModel):
    """Request to create alert."""

    model_config = ConfigDict(extra="forbid")

    alert_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    threshold: float = Field(gt=0.0)
    period: str = "daily"
    provider: str | None = None
    model: str | None = None


class CostBudgetSchema(BaseModel):
    """Cost budget schema."""

    model_config = ConfigDict(extra="forbid")

    budget_id: str
    name: str
    limit: float
    period: str = "monthly"
    provider: str | None = None
    model: str | None = None
    current_usage: float
    remaining: float
    percentage_used: float


class CostBudgetRequest(BaseModel):
    """Request to create budget."""

    model_config = ConfigDict(extra="forbid")

    budget_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    limit: float = Field(gt=0.0)
    period: str = "monthly"
    provider: str | None = None
    model: str | None = None


class ModelPricingSchema(BaseModel):
    """Model pricing schema."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    input_price_per_1k: float
    output_price_per_1k: float
    currency: str = "USD"


class CostStatsResponse(BaseModel):
    """Overall cost statistics."""

    model_config = ConfigDict(extra="forbid")

    total_cost: float
    total_records: int
    alerts_count: int
    budgets_count: int
    active_alerts: int
    budgets_exceeded: int
