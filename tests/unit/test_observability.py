"""
Unit tests for the observability subsystem.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from ai_team.observability.costs import CostTracker
from ai_team.observability.exceptions import CostCalculationError
from ai_team.observability.models import (
    AgentExecution,
    LLMCall,
    ToolCall,
)
from ai_team.observability.telemetry.logging import LoggingManager
from ai_team.observability.telemetry.metrics import LatencyHistogram, MetricsManager
from ai_team.observability.telemetry.tracing import TracingManager
from ai_team.observability.token_usage import TokenUsageTracker
from ai_team.shared.enums.observability import (
    ExecutionStatus,
    LLMProvider,
    ToolType,
)

# ======================================================================
# Helpers
# ======================================================================


def _llm_call(
    *,
    agent: str = "coder",
    provider: LLMProvider = LLMProvider.OPENROUTER,
    model: str = "gpt-5.5",
    prompt_tokens: int = 100,
    completion_tokens: int = 50,
    latency_ms: float = 250.0,
) -> LLMCall:
    return LLMCall(
        execution_id=uuid4(),
        agent=agent,
        provider=provider,
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        latency_ms=latency_ms,
        timestamp=datetime.now(UTC),
    )


def _tool_call(
    *,
    agent: str = "coder",
    tool: ToolType = ToolType.FILESYSTEM,
    latency_ms: float = 15.0,
    success: bool = True,
) -> ToolCall:
    return ToolCall(
        execution_id=uuid4(),
        agent=agent,
        tool=tool,
        latency_ms=latency_ms,
        success=success,
        timestamp=datetime.now(UTC),
    )


def _execution(
    *,
    agent: str = "coder",
) -> AgentExecution:
    return AgentExecution(
        execution_id=uuid4(),
        agent=agent,
        started_at=datetime.now(UTC),
    )


# ======================================================================
# Models
# ======================================================================


class TestAgentExecution:
    def test_create(self) -> None:
        ex = _execution()
        assert ex.agent == "coder"
        assert ex.status == ExecutionStatus.RUNNING
        assert ex.finished_at is None

    def test_finish(self) -> None:
        ex = _execution()
        ex.finished_at = datetime.now(UTC)
        assert ex.finished_at is not None

    def test_forbid_extra(self) -> None:
        with pytest.raises(ValueError):
            AgentExecution(
                execution_id=uuid4(),
                agent="x",
                started_at=datetime.now(UTC),
                foo="bar",  # type: ignore[arg-type]
            )


class TestLLMCall:
    def test_total_tokens(self) -> None:
        call = _llm_call(prompt_tokens=100, completion_tokens=50)
        assert call.total_tokens == 150

    def test_zero_tokens(self) -> None:
        call = _llm_call(prompt_tokens=0, completion_tokens=0)
        assert call.total_tokens == 0


class TestToolCall:
    def test_create(self) -> None:
        tc = _tool_call(success=True)
        assert tc.success is True
        assert tc.tool == ToolType.FILESYSTEM


# ======================================================================
# Token Usage Tracker
# ======================================================================


class TestTokenUsageTracker:
    async def test_record(self) -> None:
        tracker = TokenUsageTracker()
        call = _llm_call(prompt_tokens=100, completion_tokens=50)
        await tracker.record(call)
        assert tracker.prompt_tokens == 100
        assert tracker.completion_tokens == 50
        assert tracker.total_tokens == 150

    async def test_usage_by_agent(self) -> None:
        tracker = TokenUsageTracker()
        c1 = _llm_call(agent="coder", prompt_tokens=100, completion_tokens=50)
        c2 = _llm_call(agent="reviewer", prompt_tokens=200, completion_tokens=100)
        await tracker.record(c1)
        await tracker.record(c2)
        usage = tracker.usage_by_agent()
        assert usage["coder"] == 150
        assert usage["reviewer"] == 300

    async def test_reset(self) -> None:
        tracker = TokenUsageTracker()
        call = _llm_call(prompt_tokens=100, completion_tokens=50)
        await tracker.record(call)
        tracker.reset()
        assert tracker.total_tokens == 0
        assert tracker.usage_by_agent() == {}


# ======================================================================
# Cost Tracker
# ======================================================================


class TestCostTracker:
    async def test_record_known_model(self) -> None:
        tracker = CostTracker()
        call = _llm_call(
            provider=LLMProvider.OPENROUTER,
            model="gpt-5.5",
            prompt_tokens=1_000_000,
            completion_tokens=1_000_000,
        )
        await tracker.record(call)
        assert tracker.total_cost == pytest.approx(10.0)

    async def test_record_unknown_model(self) -> None:
        tracker = CostTracker()
        call = _llm_call(model="unknown-model")
        await tracker.record(call)
        assert tracker.total_cost == 0.0

    async def test_ollama_free(self) -> None:
        tracker = CostTracker()
        call = _llm_call(provider=LLMProvider.OLLAMA, model="llama3")
        await tracker.record(call)
        assert tracker.total_cost == 0.0

    def test_set_price(self) -> None:
        tracker = CostTracker()
        tracker.set_price("custom-model", prompt_price=1.0, completion_price=2.0)
        assert tracker.get_price("custom-model") == (1.0, 2.0)

    def test_set_price_negative_raises(self) -> None:
        tracker = CostTracker()
        with pytest.raises(CostCalculationError):
            tracker.set_price("m", prompt_price=-1.0, completion_price=1.0)

    async def test_cost_by_agent(self) -> None:
        tracker = CostTracker()
        c1 = _llm_call(
            agent="coder",
            provider=LLMProvider.OPENROUTER,
            model="gpt-5.5",
            prompt_tokens=1_000_000,
            completion_tokens=0,
        )
        c2 = _llm_call(
            agent="reviewer",
            provider=LLMProvider.OPENROUTER,
            model="gpt-5.5",
            prompt_tokens=2_000_000,
            completion_tokens=0,
        )
        await tracker.record(c1)
        await tracker.record(c2)
        by_agent = tracker.cost_by_agent()
        assert by_agent["coder"] == pytest.approx(2.0)
        assert by_agent["reviewer"] == pytest.approx(4.0)

    async def test_reset(self) -> None:
        tracker = CostTracker()
        call = _llm_call(
            provider=LLMProvider.OPENROUTER,
            model="gpt-5.5",
            prompt_tokens=1_000_000,
            completion_tokens=0,
        )
        await tracker.record(call)
        tracker.reset()
        assert tracker.total_cost == 0.0


# ======================================================================
# Latency Histogram
# ======================================================================


class TestLatencyHistogram:
    def test_empty(self) -> None:
        h = LatencyHistogram()
        assert h.count == 0
        assert h.min_ms == 0.0
        assert h.max_ms == 0.0
        assert h.avg_ms == 0.0
        assert h.p95_ms == 0.0

    def test_single_value(self) -> None:
        h = LatencyHistogram()
        h.record(100.0)
        assert h.count == 1
        assert h.min_ms == 100.0
        assert h.max_ms == 100.0
        assert h.avg_ms == 100.0
        assert h.p95_ms == 100.0

    def test_multiple_values(self) -> None:
        h = LatencyHistogram()
        for v in [10.0, 20.0, 30.0, 40.0, 50.0]:
            h.record(v)
        assert h.count == 5
        assert h.min_ms == 10.0
        assert h.max_ms == 50.0
        assert h.avg_ms == 30.0
        assert h.p95_ms == 50.0

    def test_snapshot(self) -> None:
        h = LatencyHistogram()
        h.record(10.0)
        snap = h.snapshot()
        assert snap["count"] == 1
        assert snap["min_ms"] == 10.0

    def test_reset(self) -> None:
        h = LatencyHistogram()
        h.record(10.0)
        h.reset()
        assert h.count == 0


# ======================================================================
# Metrics Manager
# ======================================================================


class TestMetricsManager:
    async def test_record_execution(self) -> None:
        mgr = MetricsManager()
        ex = _execution(agent="coder")
        await mgr.record_execution(ex)
        snap = mgr.snapshot()
        assert snap["executions"] == 1
        assert snap["agents"]["coder"] == 1

    async def test_record_llm_call(self) -> None:
        mgr = MetricsManager()
        call = _llm_call(prompt_tokens=100, completion_tokens=50, latency_ms=200.0)
        await mgr.record_llm_call(call)
        snap = mgr.snapshot()
        assert snap["llm_calls"] == 1
        assert snap["tokens"] == 150
        assert snap["llm_latency"]["count"] == 1
        assert snap["llm_latency"]["min_ms"] == 200.0

    async def test_record_tool_call(self) -> None:
        mgr = MetricsManager()
        tc = _tool_call(latency_ms=30.0)
        await mgr.record_tool_call(tc)
        snap = mgr.snapshot()
        assert snap["tool_calls"] == 1
        assert snap["tool_latency"]["count"] == 1

    async def test_record_error(self) -> None:
        mgr = MetricsManager()
        await mgr.record_error(
            execution_id=str(uuid4()),
            agent="coder",
            error=ValueError("test"),
        )
        snap = mgr.snapshot()
        assert snap["errors"] == 1


# ======================================================================
# Tracing Manager
# ======================================================================


class TestTracingManager:
    async def test_start_and_get(self) -> None:
        mgr = TracingManager()
        ex = _execution()
        await mgr.start_execution(ex)
        found = mgr.get_execution(ex.execution_id)
        assert found is ex

    async def test_finish_removes(self) -> None:
        mgr = TracingManager()
        ex = _execution()
        await mgr.start_execution(ex)
        removed = await mgr.finish_execution(ex.execution_id)
        assert removed is ex
        assert mgr.get_execution(ex.execution_id) is None

    async def test_active_executions(self) -> None:
        mgr = TracingManager()
        e1 = _execution(agent="coder")
        e2 = _execution(agent="reviewer")
        await mgr.start_execution(e1)
        await mgr.start_execution(e2)
        active = mgr.active_executions()
        assert len(active) == 2


# ======================================================================
# Logging Manager
# ======================================================================


class TestLoggingManager:
    async def test_log_execution(self) -> None:
        mgr = LoggingManager()
        ex = _execution()
        await mgr.log_execution(ex)

    async def test_log_llm_call(self) -> None:
        mgr = LoggingManager()
        call = _llm_call()
        await mgr.log_llm_call(call)

    async def test_log_tool_call(self) -> None:
        mgr = LoggingManager()
        tc = _tool_call()
        await mgr.log_tool_call(tc)

    async def test_log_error(self) -> None:
        mgr = LoggingManager()
        await mgr.log_error(
            execution_id=uuid4(),
            agent="coder",
            error=ValueError("boom"),
        )
