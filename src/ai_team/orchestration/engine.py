"""
Multi-task orchestration engine.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from ai_team.orchestration.models import (
    OrchestrationPlan,
    OrchestrationResult,
    TaskExecutionState,
    TaskStatus,
)

logger = logging.getLogger(__name__)


class OrchestrationEngine:
    """Orchestrates multiple tasks with dependency resolution."""

    def __init__(self) -> None:
        self._plans: dict[str, OrchestrationPlan] = {}
        self._results: dict[str, OrchestrationResult] = {}

    def create_plan(self, plan: OrchestrationPlan) -> None:
        """Create and validate an orchestration plan."""
        errors = plan.validate_dependencies()
        if errors:
            raise ValueError(f"Invalid plan: {errors}")

        self._plans[plan.plan_id] = plan
        logger.info(
            "Created orchestration plan '%s' with %d tasks",
            plan.plan_id,
            len(plan.tasks),
        )

    def get_plan(self, plan_id: str) -> OrchestrationPlan | None:
        return self._plans.get(plan_id)

    def get_result(self, plan_id: str) -> OrchestrationResult | None:
        return self._results.get(plan_id)

    def list_plans(self) -> list[OrchestrationPlan]:
        return list(self._plans.values())

    def delete_plan(self, plan_id: str) -> bool:
        if plan_id in self._plans:
            del self._plans[plan_id]
            return True
        return False

    def build_result(self, plan: OrchestrationPlan) -> OrchestrationResult:
        """Build initial result for a plan."""
        result = OrchestrationResult(
            plan_id=plan.plan_id,
            status=TaskStatus.PENDING,
            total_tasks=len(plan.tasks),
        )
        for task_id in plan.tasks:
            result.task_states[task_id] = TaskExecutionState(
                task_id=task_id,
                status=TaskStatus.PENDING,
            )
        self._results[plan.plan_id] = result
        return result

    def get_execution_order(self, plan: OrchestrationPlan) -> list[list[str]]:
        """Get execution order (stages) for a plan."""
        return plan.topological_sort()

    def mark_running(self, plan_id: str, task_id: str) -> None:
        result = self._results.get(plan_id)
        if result and task_id in result.task_states:
            state = result.task_states[task_id]
            state.status = TaskStatus.RUNNING
            state.started_at = datetime.now(UTC).isoformat()
            result.status = TaskStatus.RUNNING

    def mark_completed(self, plan_id: str, task_id: str, result_data: object = None) -> None:
        result = self._results.get(plan_id)
        if result and task_id in result.task_states:
            state = result.task_states[task_id]
            state.status = TaskStatus.COMPLETED
            state.result = result_data
            state.completed_at = datetime.now(UTC).isoformat()
            if state.started_at:
                started = datetime.fromisoformat(state.started_at)
                completed = datetime.fromisoformat(state.completed_at)
                state.duration_seconds = (completed - started).total_seconds()
            result.completed_tasks += 1
            result.results[task_id] = result_data

            self._update_plan_status(result)

    def mark_failed(self, plan_id: str, task_id: str, error: str) -> None:
        result = self._results.get(plan_id)
        if result and task_id in result.task_states:
            state = result.task_states[task_id]
            state.status = TaskStatus.FAILED
            state.error = error
            state.completed_at = datetime.now(UTC).isoformat()
            result.failed_tasks += 1

            self._update_plan_status(result)

    def _update_plan_status(self, result: OrchestrationResult) -> None:
        """Update overall plan status based on task states."""
        all_done = all(
            s.status in (TaskStatus.COMPLETED, TaskStatus.FAILED)
            for s in result.task_states.values()
        )
        any_failed = any(s.status == TaskStatus.FAILED for s in result.task_states.values())

        if all_done:
            result.status = TaskStatus.FAILED if any_failed else TaskStatus.COMPLETED
            result.completed_at = datetime.now(UTC).isoformat()
            if result.started_at:
                started = datetime.fromisoformat(result.started_at)
                completed = datetime.fromisoformat(result.completed_at)
                result.duration_seconds = (completed - started).total_seconds()

    def can_run_task(
        self,
        plan: OrchestrationPlan,
        task_id: str,
        result: OrchestrationResult,
    ) -> bool:
        """Check if a task can run (all dependencies completed)."""
        task = plan.get_task(task_id)
        if not task:
            return False

        state = result.task_states.get(task_id)
        if state and state.status != TaskStatus.PENDING:
            return False

        for dep_id in task.dependencies:
            dep_state = result.task_states.get(dep_id)
            if not dep_state or dep_state.status != TaskStatus.COMPLETED:
                return False

        return True

    def get_runnable_tasks(
        self,
        plan: OrchestrationPlan,
        result: OrchestrationResult,
    ) -> list[str]:
        """Get all tasks that can currently run."""
        runnable = [task_id for task_id in plan.tasks if self.can_run_task(plan, task_id, result)]
        return sorted(
            runnable,
            key=lambda t: plan.tasks[t].priority,
            reverse=True,
        )
