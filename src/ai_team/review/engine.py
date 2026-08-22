"""
Code review engine - analyzes code and generates inline comments.
"""

from __future__ import annotations

import logging
import re
from typing import ClassVar

from ai_team.review.models import (
    FileReview,
    InlineComment,
    ReviewCategory,
    ReviewRequest,
    ReviewResult,
    ReviewSeverity,
)

logger = logging.getLogger(__name__)


class ReviewEngine:
    """Engine for performing automated code reviews."""

    # Common security patterns
    SECURITY_PATTERNS: ClassVar[list[tuple[str, str, ReviewSeverity]]] = [
        (r"eval\(", "Use of eval() is dangerous", ReviewSeverity.CRITICAL),
        (r"exec\(", "Use of exec() is dangerous", ReviewSeverity.CRITICAL),
        (r"__import__\(", "Dynamic import can be unsafe", ReviewSeverity.WARNING),
        (r"subprocess\.call.*shell=True", "Shell injection risk", ReviewSeverity.CRITICAL),
        (r"os\.system\(", "Shell injection risk", ReviewSeverity.CRITICAL),
        (r"pickle\.loads?", "Pickle deserialization is unsafe", ReviewSeverity.WARNING),
        (r"yaml\.load\(", "Use yaml.safe_load() instead", ReviewSeverity.WARNING),
        (r"password\s*=\s*['\"]", "Hardcoded password detected", ReviewSeverity.CRITICAL),
        (r"api_key\s*=\s*['\"]", "Hardcoded API key detected", ReviewSeverity.CRITICAL),
        (r"secret\s*=\s*['\"]", "Hardcoded secret detected", ReviewSeverity.CRITICAL),
    ]

    # Performance patterns
    PERFORMANCE_PATTERNS: ClassVar[list[tuple[str, str, ReviewSeverity]]] = [
        (r"for\s+.*\s+in\s+range\(len\(", "Use enumerate() instead", ReviewSeverity.WARNING),
        (r"\.append\(", "Consider list comprehension for better performance", ReviewSeverity.INFO),
        (r"import\s+\*", "Wildcard imports are discouraged", ReviewSeverity.WARNING),
    ]

    # Style patterns
    STYLE_PATTERNS: ClassVar[list[tuple[str, str, ReviewSeverity]]] = [
        (
            r"def\s+\w+\(.*\)\s*->\s*None\s*:",
            "Return type annotation is redundant for None",
            ReviewSeverity.INFO,
        ),
        (r"print\(", "Consider using logging instead of print", ReviewSeverity.INFO),
        (r"TODO|FIXME|HACK|XXX", "Unresolved TODO/FIXME comment", ReviewSeverity.WARNING),
    ]

    def __init__(self) -> None:
        self._custom_rules: list[tuple[str, str, ReviewSeverity, ReviewCategory]] = []

    def add_rule(
        self,
        pattern: str,
        message: str,
        severity: ReviewSeverity,
        category: ReviewCategory,
    ) -> None:
        """Add a custom review rule."""
        self._custom_rules.append((pattern, message, severity, category))

    async def review(self, request: ReviewRequest) -> ReviewResult:
        """Perform code review on the provided files."""
        result = ReviewResult(task_id=request.task_id)

        for file_path, content in request.files.items():
            file_review = await self._review_file(file_path, content, request)
            result.files.append(file_review)

        result.calculate_score()

        if result.files:
            summaries = [f"{f.file_path}: {f.summary}" for f in result.files if f.summary]
            result.summary = "\n".join(summaries) if summaries else "No issues found"

        logger.info(
            "Review complete for task %s: score=%.2f, issues=%d",
            request.task_id,
            result.overall_score,
            result.total_comments,
        )

        return result

    async def _review_file(
        self,
        file_path: str,
        content: str,
        request: ReviewRequest,
    ) -> FileReview:
        """Review a single file."""
        review = FileReview(file_path=file_path)
        lines = content.split("\n")

        for i, line in enumerate(lines, start=1):
            # Check security patterns
            for pattern, message, severity in self.SECURITY_PATTERNS:
                if re.search(pattern, line):
                    review.comments.append(
                        InlineComment(
                            file_path=file_path,
                            line_number=i,
                            severity=severity,
                            category=ReviewCategory.SECURITY,
                            message=message,
                            code_snippet=line.strip(),
                        )
                    )

            # Check performance patterns
            for pattern, message, severity in self.PERFORMANCE_PATTERNS:
                if re.search(pattern, line):
                    review.comments.append(
                        InlineComment(
                            file_path=file_path,
                            line_number=i,
                            severity=severity,
                            category=ReviewCategory.PERFORMANCE,
                            message=message,
                            code_snippet=line.strip(),
                        )
                    )

            # Check style patterns
            for pattern, message, severity in self.STYLE_PATTERNS:
                if re.search(pattern, line):
                    review.comments.append(
                        InlineComment(
                            file_path=file_path,
                            line_number=i,
                            severity=severity,
                            category=ReviewCategory.STYLE,
                            message=message,
                            code_snippet=line.strip(),
                        )
                    )

            # Check custom rules
            for pattern, message, severity, category in self._custom_rules:
                if re.search(pattern, line):
                    review.comments.append(
                        InlineComment(
                            file_path=file_path,
                            line_number=i,
                            severity=severity,
                            category=category,
                            message=message,
                            code_snippet=line.strip(),
                        )
                    )

        # Calculate file score
        if review.comments:
            penalty = sum(
                {
                    ReviewSeverity.INFO: 0.01,
                    ReviewSeverity.WARNING: 0.05,
                    ReviewSeverity.ERROR: 0.15,
                    ReviewSeverity.CRITICAL: 0.5,
                }.get(c.severity, 0.1)
                for c in review.comments
            )
            review.score = max(0.0, 1.0 - min(penalty, 1.0))
        else:
            review.score = 1.0

        return review
