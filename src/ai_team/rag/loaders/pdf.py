"""
PDF document loader.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from ai_team.rag.loaders.base import BaseDocumentLoader
from ai_team.rag.models import (
    Document,
    DocumentMetadata,
    DocumentSource,
)

logger = logging.getLogger(__name__)


class PDFLoader(BaseDocumentLoader):
    """
    Loads PDF documents by extracting text with pdftotext (poppler).

    Falls back to reading raw bytes if pdftotext is unavailable.
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:
        path = Path(source.uri)

        content = self._extract_with_pdftotext(path)

        if not content:
            content = self._extract_raw(path)

        metadata = DocumentMetadata(
            title=source.title or path.stem,
        )

        return Document(
            source=source,
            content=content,
            metadata=metadata,
        )

    def _extract_with_pdftotext(self, path: Path) -> str:
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.debug("pdftotext not available for %s", path)
        return ""

    def _extract_raw(self, path: Path) -> str:
        try:
            data = path.read_bytes()
            text_parts: list[str] = []
            for line in data.split(b"\n"):
                try:
                    decoded = line.decode("utf-8", errors="ignore")
                    if any(c.isalpha() for c in decoded):
                        text_parts.append(decoded)
                except Exception:
                    continue
            return "\n".join(text_parts[:500])
        except Exception:
            logger.warning("Failed to read PDF bytes from %s", path)
            return f"[PDF content could not be extracted: {path.name}]"
