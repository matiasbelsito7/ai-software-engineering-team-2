"""
Cost tracking API router.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Query

from ai_team.app.api.exceptions.errors import NotFoundError, ValidationError
from ai_team.app.api.schemas.cost_tracking import (
    CostAlertRequest,
    CostAlertSchema,
    CostBudgetRequest,
    CostBudgetSchema,
    CostRecordRequest,
    CostRecordSchema,
    CostStatsResponse,
    CostSummarySchema,
)
from ai_team.cost_tracking.models import CostAlert, CostBudget, LLMProvider
from ai_team.cost_tracking.tracker import CostTracker

logger = logging.getLogger(__name__)

router = APIRouter(tags=["cost-tracking"])

_tracker = CostTracker()


@router.post(
    "/cost-tracking/records",
    status_code=201,
    summary="Record LLM usage",
)
async def record_usage(
    request_body: CostRecordRequest,
) -> CostRecordSchema:
    """Record LLM usage cost."""
    try:
        provider = LLMProvider(request_body.provider)
    except ValueError as err:
        raise ValidationError(detail=f"Invalid provider: {request_body.provider}") from err

    record = _tracker.record_usage(
        record_id=request_body.record_id,
        provider=provider,
        model=request_body.model,
        input_tokens=request_body.input_tokens,
        output_tokens=request_body.output_tokens,
        task_id=request_body.task_id,
        agent_name=request_body.agent_name,
    )

    return CostRecordSchema(
        record_id=record.record_id,
        task_id=record.task_id,
        agent_name=record.agent_name,
        provider=record.provider,
        model=record.model,
        input_tokens=record.input_tokens,
        output_tokens=record.output_tokens,
        total_tokens=record.total_tokens,
        input_cost=record.input_cost,
        output_cost=record.output_cost,
        total_cost=record.total_cost,
        currency=record.currency,
        timestamp=record.timestamp,
    )


@router.get(
    "/cost-tracking/summary",
    response_model=CostSummarySchema,
    summary="Get cost summary",
)
async def get_summary(
    task_id: str | None = Query(None),
    agent_name: str | None = Query(None),
    provider: str | None = Query(None),
    model: str | None = Query(None),
) -> CostSummarySchema:
    """Get cost summary with optional filters."""
    llm_provider = LLMProvider(provider) if provider else None
    summary = _tracker.get_summary(
        task_id=task_id,
        agent_name=agent_name,
        provider=llm_provider,
        model=model,
    )
    return CostSummarySchema(
        total_cost=summary.total_cost,
        total_input_tokens=summary.total_input_tokens,
        total_output_tokens=summary.total_output_tokens,
        total_tokens=summary.total_tokens,
        total_requests=summary.total_requests,
        by_provider=summary.by_provider,
        by_model=summary.by_model,
        by_agent=summary.by_agent,
        by_task=summary.by_task,
    )


@router.get(
    "/cost-tracking/records",
    summary="List cost records",
)
async def list_records(
    task_id: str | None = Query(None),
    agent_name: str | None = Query(None),
    provider: str | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
) -> dict[str, object]:
    """List cost records with filters."""
    llm_provider = LLMProvider(provider) if provider else None
    records = _tracker.list_records(
        task_id=task_id,
        agent_name=agent_name,
        provider=llm_provider,
        limit=limit,
    )
    return {
        "records": [
            CostRecordSchema(
                record_id=r.record_id,
                task_id=r.task_id,
                agent_name=r.agent_name,
                provider=r.provider,
                model=r.model,
                input_tokens=r.input_tokens,
                output_tokens=r.output_tokens,
                total_tokens=r.total_tokens,
                input_cost=r.input_cost,
                output_cost=r.output_cost,
                total_cost=r.total_cost,
                currency=r.currency,
                timestamp=r.timestamp,
            )
            for r in records
        ],
        "total": len(records),
    }


@router.get(
    "/cost-tracking/stats",
    response_model=CostStatsResponse,
    summary="Get cost statistics",
)
async def get_stats() -> CostStatsResponse:
    """Get overall cost statistics."""
    alerts = _tracker.list_alerts()
    budgets = _tracker.list_budgets()
    return CostStatsResponse(
        total_cost=_tracker.total_cost,
        total_records=_tracker.total_records,
        alerts_count=len(alerts),
        budgets_count=len(budgets),
        active_alerts=sum(1 for a in alerts if a.enabled and not a.triggered),
        budgets_exceeded=sum(1 for b in budgets if b.percentage_used >= 100),
    )


# --- Alerts ---


@router.post(
    "/cost-tracking/alerts",
    status_code=201,
    summary="Create cost alert",
)
async def create_alert(
    request_body: CostAlertRequest,
) -> CostAlertSchema:
    """Create a cost alert."""
    alert = CostAlert(
        alert_id=request_body.alert_id,
        name=request_body.name,
        threshold=request_body.threshold,
        period=request_body.period,
        provider=LLMProvider(request_body.provider) if request_body.provider else None,
        model=request_body.model,
    )
    _tracker.add_alert(alert)
    return CostAlertSchema(
        alert_id=alert.alert_id,
        name=alert.name,
        threshold=alert.threshold,
        period=alert.period,
        provider=alert.provider,
        model=alert.model,
        enabled=alert.enabled,
        triggered=alert.triggered,
        last_triggered=alert.last_triggered,
    )


@router.get(
    "/cost-tracking/alerts",
    summary="List cost alerts",
)
async def list_alerts() -> dict[str, object]:
    """List all cost alerts."""
    alerts = _tracker.list_alerts()
    return {
        "alerts": [
            CostAlertSchema(
                alert_id=a.alert_id,
                name=a.name,
                threshold=a.threshold,
                period=a.period,
                provider=a.provider,
                model=a.model,
                enabled=a.enabled,
                triggered=a.triggered,
                last_triggered=a.last_triggered,
            )
            for a in alerts
        ],
        "total": len(alerts),
    }


@router.delete(
    "/cost-tracking/alerts/{alert_id}",
    status_code=204,
    summary="Delete cost alert",
)
async def delete_alert(alert_id: str) -> None:
    """Delete a cost alert."""
    deleted = _tracker.delete_alert(alert_id)
    if not deleted:
        raise NotFoundError(detail=f"Alert '{alert_id}' not found")


# --- Budgets ---


@router.post(
    "/cost-tracking/budgets",
    status_code=201,
    summary="Create cost budget",
)
async def create_budget(
    request_body: CostBudgetRequest,
) -> CostBudgetSchema:
    """Create a cost budget."""
    budget = CostBudget(
        budget_id=request_body.budget_id,
        name=request_body.name,
        limit=request_body.limit,
        period=request_body.period,
        provider=LLMProvider(request_body.provider) if request_body.provider else None,
        model=request_body.model,
        remaining=request_body.limit,
    )
    _tracker.add_budget(budget)
    return CostBudgetSchema(
        budget_id=budget.budget_id,
        name=budget.name,
        limit=budget.limit,
        period=budget.period,
        provider=budget.provider,
        model=budget.model,
        current_usage=budget.current_usage,
        remaining=budget.remaining,
        percentage_used=budget.percentage_used,
    )


@router.get(
    "/cost-tracking/budgets",
    summary="List cost budgets",
)
async def list_budgets() -> dict[str, object]:
    """List all cost budgets."""
    budgets = _tracker.list_budgets()
    return {
        "budgets": [
            CostBudgetSchema(
                budget_id=b.budget_id,
                name=b.name,
                limit=b.limit,
                period=b.period,
                provider=b.provider,
                model=b.model,
                current_usage=b.current_usage,
                remaining=b.remaining,
                percentage_used=b.percentage_used,
            )
            for b in budgets
        ],
        "total": len(budgets),
    }


@router.delete(
    "/cost-tracking/budgets/{budget_id}",
    status_code=204,
    summary="Delete cost budget",
)
async def delete_budget(budget_id: str) -> None:
    """Delete a cost budget."""
    deleted = _tracker.delete_budget(budget_id)
    if not deleted:
        raise NotFoundError(detail=f"Budget '{budget_id}' not found")
