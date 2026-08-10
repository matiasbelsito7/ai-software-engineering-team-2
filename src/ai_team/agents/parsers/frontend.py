"""
Frontend agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.frontend import FrontendOutput
from ai_team.agents.parsers.base import BaseParser


class FrontendParser(
    BaseParser[FrontendOutput],
):
    """
    Parse Frontend Agent responses.
    """

    model = FrontendOutput