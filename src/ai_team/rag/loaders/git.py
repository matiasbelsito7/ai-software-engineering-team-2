"""
Git repository loader.
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


class GitLoader(BaseDocumentLoader):
    """
    Loads Git repository metadata as a document.

    Extracts recent commit history, branch info, and file listing.
    """

    async def load(
        self,
        source: DocumentSource,
    ) -> Document:
        path = Path(source.uri)

        sections: list[str] = []

        sections.append(self._git_log(path))
        sections.append(self._git_branches(path))
        sections.append(self._git_files(path))

        content = "\n\n".join(s for s in sections if s)

        metadata = DocumentMetadata(
            title=source.title or path.name,
            language="git",
        )

        return Document(
            source=source,
            content=content,
            metadata=metadata,
        )

    def _git_log(self, path: Path) -> str:
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(path),
                    "log",
                    "--oneline",
                    "-20",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                return f"## Recent Commits\n\n```\n{result.stdout.strip()}\n```"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.debug("git log failed for %s", path)
        return ""

    def _git_branches(self, path: Path) -> str:
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(path),
                    "branch",
                    "-a",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                return f"## Branches\n\n```\n{result.stdout.strip()}\n```"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.debug("git branch failed for %s", path)
        return ""

    def _git_files(self, path: Path) -> str:
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(path),
                    "ls-files",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                files = result.stdout.strip().split("\n")
                listing = "\n".join(f"- {f}" for f in files[:100])
                return f"## Tracked Files ({len(files)} total)\n\n{listing}"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.debug("git ls-files failed for %s", path)
        return ""
