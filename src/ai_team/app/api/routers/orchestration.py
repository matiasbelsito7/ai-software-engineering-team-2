"""
Orchestration API router.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter

from ai_team.app.api.exceptions.errors import NotFoundError, ValidationError
from ai_team.app.api.schemas.orchestration import (
    OrchestrationListResponse,
    OrchestrationPlanResponse,
    OrchestrationPlanSchema,
    OrchestrationResultSchema,
    OrchestrationTaskSchema,
    TaskExecutionStateSchema,
)
from ai_team.orchestration.engine import OrchestrationEngine
from ai_team.orchestration.models import (
    OrchestrationPlan,
    OrchestrationResult,
    OrchestrationTask,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["orchestration"])

_engine = OrchestrationEngine()


def _plan_to_schema(plan: OrchestrationPlan) -> OrchestrationPlanSchema:
    tasks = [
        OrchestrationTaskSchema(
            task_id=t.task_id,
            name=t.name,
            description=t.description,
            task_prompt=t.task_prompt,
            system_prompt=t.system_prompt,
            dependencies=t.dependencies,
            priority=t.priority,
            timeout_seconds=t.timeout_seconds,
            max_retries=t.max_retries,
        )
        for t in plan.tasks.values()
    ]
    return OrchestrationPlanSchema(
        plan_id=plan.plan_id,
        name=plan.name,
        description=plan.description,
        tasks=tasks,
        metadata=plan.metadata,
    )


def _result_to_schema(result: OrchestrationResult) -> OrchestrationResultSchema:
    task_states = {
        tid: TaskExecutionStateSchema(
            task_id=s.task_id,
            status=s.status,
            result=s.result,
            error=s.error,
            started_at=s.started_at,
            completed_at=s.completed_at,
            duration_seconds=s.duration_seconds,
            attempt=s.attempt,
        )
        for tid, s in result.task_states.items()
    }
    return OrchestrationResultSchema(
        plan_id=result.plan_id,
        status=result.status,
        task_states=task_states,
        total_tasks=result.total_tasks,
        completed_tasks=result.completed_tasks,
        failed_tasks=result.failed_tasks,
        results=result.results,
        started_at=result.started_at,
        completed_at=result.completed_at,
        duration_seconds=result.duration_seconds,
    )


@router.post(
    "/orchestration/plans",
    status_code=201,
    summary="Create orchestration plan",
)
async def create_plan(
    request_body: OrchestrationPlanSchema,
) -> OrchestrationPlanResponse:
    """Create a new orchestration plan."""
    tasks = {
        t.task_id: OrchestrationTask(
            task_id=t.task_id,
            name=t.name,
            description=t.description,
            task_prompt=t.task_prompt,
            system_prompt=t.system_prompt,
            dependencies=t.dependencies,
            priority=t.priority,
            timeout_seconds=t.timeout_seconds,
            max_retries=t.max_retries,
        )
        for t in request_body.tasks
    }

    plan = OrchestrationPlan(
        plan_id=request_body.plan_id,
        name=request_body.name,
        description=request_body.description,
        tasks=tasks,
        metadata=request_body.metadata,
    )

    try:
        _engine.create_plan(plan)
    except ValueError as e:
        raise ValidationError(detail=str(e)) from e

    _engine.build_result(plan)
    execution_order = _engine.get_execution_order(plan)

    return OrchestrationPlanResponse(
        plan_id=plan.plan_id,
        status="created",
        total_tasks=len(plan.tasks),
        execution_order=execution_order,
    )


@router.get(
    "/orchestration/plans",
    response_model=OrchestrationListResponse,
    summary="List orchestration plans",
)
async def list_plans() -> OrchestrationListResponse:
    """List all orchestration plans."""
    plans = _engine.list_plans()
    return OrchestrationListResponse(
        plans=[_plan_to_schema(p) for p in plans],
        total=len(plans),
    )


@router.get(
    "/orchestration/plans/{plan_id}",
    response_model=OrchestrationPlanSchema,
    summary="Get orchestration plan",
)
async def get_plan(plan_id: str) -> OrchestrationPlanSchema:
    """Get a specific orchestration plan."""
    plan = _engine.get_plan(plan_id)
    if plan is None:
        raise NotFoundError(detail=f"Plan '{plan_id}' not found")
    return _plan_to_schema(plan)


@router.get(
    "/orchestration/plans/{plan_id}/result",
    response_model=OrchestrationResultSchema,
    summary="Get orchestration result",
)
async def get_result(plan_id: str) -> OrchestrationResultSchema:
    """Get the result of an orchestration plan."""
    result = _engine.get_result(plan_id)
    if result is None:
        raise NotFoundError(detail=f"Result for plan '{plan_id}' not found")
    return _result_to_schema(result)


@router.get(
    "/orchestration/plans/{plan_id}/execution-order",
    summary="Get execution order",
)
async def get_execution_order(
    plan_id: str,
) -> dict[str, list[list[str]]]:
    """Get the execution order for a plan."""
    plan = _engine.get_plan(plan_id)
    if plan is None:
        raise NotFoundError(detail=f"Plan '{plan_id}' not found")

    try:
        order = _engine.get_execution_order(plan)
    except ValueError as e:
        raise ValidationError(detail=str(e)) from e

    return {"plan_id": plan_id, "stages": order}  # type: ignore[dict-item]


@router.get(
    "/orchestration/plans/{plan_id}/runnable",
    summary="Get runnable tasks",
)
async def get_runnable_tasks(plan_id: str) -> dict[str, list[str]]:
    """Get tasks that can currently run."""
    plan = _engine.get_plan(plan_id)
    if plan is None:
        raise NotFoundError(detail=f"Plan '{plan_id}' not found")

    result = _engine.get_result(plan_id)
    if result is None:
        raise NotFoundError(detail=f"Result for plan '{plan_id}' not found")

    runnable = _engine.get_runnable_tasks(plan, result)
    return {"plan_id": plan_id, "runnable_tasks": runnable}  # type: ignore[dict-item]


@router.delete(
    "/orchestration/plans/{plan_id}",
    status_code=204,
    summary="Delete orchestration plan",
)
async def delete_plan(plan_id: str) -> None:
    """Delete an orchestration plan."""
    deleted = _engine.delete_plan(plan_id)
    if not deleted:
        raise NotFoundError(detail=f"Plan '{plan_id}' not found")
