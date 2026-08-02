"""
Parser for Planner agent responses.
"""

from __future__ import annotations

import json

from pydantic import ValidationError

from ai_team.agents.exceptions import AgentExecutionError
from ai_team.agents.planner.models import ExecutionPlan
from ai_team.infrastructure.llm.responses import LLMResponse


class PlannerParser:
    """
    Parses LLM responses into execution plans.
    """

    @staticmethod
    def parse(
        response: LLMResponse,
    ) -> ExecutionPlan:
        """
        Parse an LLM response into an ExecutionPlan.
        """

        try:
            data = json.loads(response.content)

        except json.JSONDecodeError as exc:
            raise AgentExecutionError(
                "Planner returned invalid JSON."
            ) from exc

        try:
            return ExecutionPlan.model_validate(data)

        except ValidationError as exc:
            raise AgentExecutionError(
                "Planner returned an invalid execution plan."
            ) from exc

    @staticmethod
    def parse_json(
        content: str,
    ) -> ExecutionPlan:
        """
        Parse a raw JSON string into an ExecutionPlan.
        """

        try:
            data = json.loads(content)

        except json.JSONDecodeError as exc:
            raise AgentExecutionError(
                "Invalid planner JSON."
            ) from exc

        try:
            return ExecutionPlan.model_validate(data)

        except ValidationError as exc:
            raise AgentExecutionError(
                "Invalid execution plan."
            ) from exc