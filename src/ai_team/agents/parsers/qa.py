"""
QA agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.qa import QAOutput
from ai_team.agents.parsers.base import BaseParser


class QAParser(BaseParser[QAOutput]):
    """
    Parse QA Agent responses.
    """

    model = QAOutput