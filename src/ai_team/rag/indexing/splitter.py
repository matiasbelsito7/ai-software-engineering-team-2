"""
Document splitter.
"""

from __future__ import annotations


class DocumentSplitter:
    """
    Splits a document into logical sections.

    This component is intentionally simple.
    Future implementations may support:

        - Markdown
        - Python
        - JSON
        - HTML
        - PDF
    """

    def split(
        self,
        text: str,
    ) -> list[str]:
        """
        Split a document into logical sections.
        """

        sections = [section.strip() for section in text.split("\n\n") if section.strip()]

        return sections
