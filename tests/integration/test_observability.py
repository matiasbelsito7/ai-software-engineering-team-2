"""
Integration tests for the observability subsystem.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from ai_team.observability.factory import build_observability


class TestObservabilityFactory:
    def test_build_returns_manager(self) -> None:
        mgr = build_observability()
        assert mgr is not None
        assert mgr.tracing is not None
        assert mgr.metrics is not None
        assert mgr.logging is not None
        assert mgr.token_usage is not None
        assert mgr.costs is not None


class TestObservabilityEndToEnd:
    """Simulate a multi-agent workflow through the full pipeline."""

    @pytest.fixture()
    def manager(self) -> object:
        return build_observability()

    async def test_full_agent_lifecycle(self, manager: object) -> None:
        mgr = manager  # type: ignore[assignment]
        exec_id = str(uuid4())

        # Start
        await mgr.start_execution(execution_id=exec_id, agent="coder")

        # Verify tracing
        active = mgr.tracing.active_executions()
        assert len(active) == 1
        assert active[0].agent == "coder"

        # Record LLM calls
        await mgr.record_llm_call(
            execution_id=exec_id,
            agent="coder",
            provider="openrouter",
            model="gpt-5.5",
            prompt_tokens=500,
            completion_tokens=200,
            latency_ms=150.0,
        )
        await mgr.record_llm_call(
            execution_id=exec_id,
            agent="coder",
            provider="openrouter",
            model="gpt-5.5-mini",
            prompt_tokens=300,
            completion_tokens=100,
            latency_ms=80.0,
        )

        # Record tool calls
        await mgr.record_tool_call(
            execution_id=exec_id,
            agent="coder",
            tool="filesystem",
            latency_ms=10.0,
            success=True,
        )
        await mgr.record_tool_call(
            execution_id=exec_id,
            agent="coder",
            tool="terminal",
            latency_ms=25.0,
            success=True,
        )

        # Record error
        await mgr.record_error(
            execution_id=exec_id,
            agent="coder",
            error=ValueError("test error"),
        )

        # Finish
        execution = mgr.get_execution(exec_id)
        assert execution is not None
        await mgr.finish_execution(execution=execution)

        # Verify token tracking
        assert mgr.token_usage.total_tokens == 1100
        assert mgr.token_usage.usage_by_agent()["coder"] == 1100

        # Verify costs
        assert mgr.costs.total_cost > 0
        assert "coder" in mgr.costs.cost_by_agent()

        # Verify metrics
        snap = mgr.metrics.snapshot()
        assert snap["executions"] == 1
        assert snap["llm_calls"] == 2
        assert snap["tool_calls"] == 2
        assert snap["errors"] == 1
        assert snap["tokens"] == 1100

    async def test_multiple_agents(self, manager: object) -> None:
        mgr = manager  # type: ignore[assignment]
        exec_id_1 = str(uuid4())
        exec_id_2 = str(uuid4())

        # Two agents run concurrently
        await mgr.start_execution(execution_id=exec_id_1, agent="coder")
        await mgr.start_execution(execution_id=exec_id_2, agent="reviewer")

        await mgr.record_llm_call(
            execution_id=exec_id_1,
            agent="coder",
            provider="openrouter",
            model="gpt-5.5",
            prompt_tokens=1000,
            completion_tokens=500,
            latency_ms=200.0,
        )
        await mgr.record_llm_call(
            execution_id=exec_id_2,
            agent="reviewer",
            provider="openrouter",
            model="gpt-5.5-mini",
            prompt_tokens=800,
            completion_tokens=300,
            latency_ms=120.0,
        )

        # Both active
        assert len(mgr.tracing.active_executions()) == 2

        # Finish both
        ex1 = mgr.get_execution(exec_id_1)
        ex2 = mgr.get_execution(exec_id_2)
        await mgr.finish_execution(execution=ex1)
        await mgr.finish_execution(execution=ex2)

        # Verify per-agent metrics
        snap = mgr.metrics.snapshot()
        assert snap["executions"] == 2
        assert snap["llm_calls"] == 2
        assert snap["agents"]["coder"] == 1
        assert snap["agents"]["reviewer"] == 1

        # Verify per-agent costs
        by_agent = mgr.costs.cost_by_agent()
        assert "coder" in by_agent
        assert "reviewer" in by_agent

    async def test_custom_prices(self, manager: object) -> None:
        mgr = manager  # type: ignore[assignment]
        exec_id = str(uuid4())

        mgr.costs.set_price("my-model", prompt_price=1.0, completion_price=1.0)

        await mgr.start_execution(execution_id=exec_id, agent="agent")
        await mgr.record_llm_call(
            execution_id=exec_id,
            agent="agent",
            provider="openrouter",
            model="my-model",
            prompt_tokens=1_000_000,
            completion_tokens=1_000_000,
            latency_ms=100.0,
        )

        assert mgr.costs.total_cost == pytest.approx(2.0)
