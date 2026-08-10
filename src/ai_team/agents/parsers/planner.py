"""
Planner agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.planner import PlannerOutput
from ai_team.agents.parsers.base import BaseParser


class PlannerParser(BaseParser[PlannerOutput]):
    """
    Parse Planner Agent responses.
    """

    model = PlannerOutput