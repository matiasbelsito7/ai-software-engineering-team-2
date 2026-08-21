"""
Repository loader.
"""

from __future__ import annotations

import logging
from pathlib import Path

from ai_team.rag.loaders.base import BaseDocumentLoader
from ai_team.rag.models import (
    Document,
    DocumentMetadata,
    DocumentSource,
)

logger = logging.getLogger(__name__)

_SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".eggs",
    ".tox",
    ".nox",
    ".idea",
    ".vscode",
}

_MAX_FILES = 200


class RepositoryLoader(BaseDocumentLoader):
    """
    Loads an entire software repository as a single document.

    Aggregates file paths and content from the source directory.
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:
        root = Path(source.uri)

        files: list[str] = []
        contents: list[str] = []

        self._walk(root, root, files, contents, depth=0)

        header = f"Repository: {root.name}\nFiles: {len(files)}\n"
        file_listing = "\n".join(f"- {f}" for f in files)
        file_contents = "\n\n---\n\n".join(contents)

        content = f"{header}\n## Files\n\n{file_listing}\n\n## Content\n\n{file_contents}"

        metadata = DocumentMetadata(
            title=source.title or root.name,
        )

        return Document(
            source=source,
            content=content,
            metadata=metadata,
        )

    def _walk(
        self,
        root: Path,
        current: Path,
        files: list[str],
        contents: list[str],
        depth: int,
    ) -> None:
        if depth > 10 or len(files) >= _MAX_FILES:
            return

        try:
            entries = sorted(current.iterdir())
        except PermissionError:
            return

        for entry in entries:
            if entry.name in _SKIP_DIRS:
                continue

            if entry.is_dir():
                self._walk(root, entry, files, contents, depth + 1)
            elif entry.is_file():
                rel = str(entry.relative_to(root))
                files.append(rel)

                try:
                    text = entry.read_text(encoding="utf-8", errors="ignore")
                    contents.append(f"### {rel}\n\n{text[:5000]}")
                except Exception:
                    contents.append(f"### {rel}\n\n[unreadable]")
