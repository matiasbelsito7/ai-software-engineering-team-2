"""
Document chunker.
"""

from __future__ import annotations


class DocumentChunker:
    """
    Splits sections into chunks of approximately equal size.
    """

    def __init__(
        self,
        *,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> None:
        self._chunk_size = chunk_size
        self._overlap = overlap

    def chunk(
        self,
        sections: list[str],
    ) -> list[str]:
        """
        Chunk document sections.
        """

        chunks: list[str] = []

        for section in sections:

            start = 0

            while start < len(section):

                end = start + self._chunk_size

                chunks.append(
                    section[start:end],
                )

                start += (
                    self._chunk_size
                    - self._overlap
                )

        return chunks