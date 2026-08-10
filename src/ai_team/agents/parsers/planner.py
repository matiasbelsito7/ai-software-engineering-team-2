"""
Parser for Planner agent outputs.
"""

from __future__ import annotations

from ai_team.agents.parsers.base import BaseParser
from ai_team.agents.planner.models import ExecutionPlan


class PlannerParser(BaseParser[ExecutionPlan]):
    """
    Parser for Planner agent responses.
    """

    model = ExecutionPlan