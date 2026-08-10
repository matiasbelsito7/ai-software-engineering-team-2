"""
Reviewer agent response parser.
"""

from __future__ import annotations

from ai_team.agents.outputs.reviewer import ReviewerOutput
from ai_team.agents.parsers.base import BaseParser


class ReviewerParser(BaseParser[ReviewerOutput]):
    """
    Parse Reviewer Agent responses.
    """

    model = ReviewerOutput