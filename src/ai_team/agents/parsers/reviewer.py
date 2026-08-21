"""
Parser for Reviewer agent outputs.
"""

from __future__ import annotations

from ai_team.agents.parsers.base import BaseParser
from ai_team.agents.reviewer.models import ReviewerResult


class ReviewerParser(BaseParser[ReviewerResult]):
    """
    Parser for Reviewer agent responses.
    """

    model = ReviewerResult
