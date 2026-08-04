"""
Document cleaning utilities.
"""

from __future__ import annotations

import re


class DocumentCleaner:
    """
    Cleans raw documents before indexing.
    """

    _MULTIPLE_SPACES = re.compile(r"[ \t]+")
    _MULTIPLE_NEWLINES = re.compile(r"\n{3,}")

    def clean(
        self,
        text: str,
    ) -> str:
        """
        Normalize whitespace while preserving paragraphs.
        """

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        text = self._MULTIPLE_SPACES.sub(
            " ",
            text,
        )

        text = self._MULTIPLE_NEWLINES.sub(
            "\n\n",
            text,
        )

        return text.strip()