"""
Workspace management.
"""

from __future__ import annotations

from pathlib import Path


class Workspace:
    """
    Represents the application workspace.

    Every tool operates relative to this directory.
    """

    def __init__(
        self,
        root: Path | str,
    ) -> None:

        self._root = Path(root).resolve()

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @property
    def root(
        self,
    ) -> Path:
        """
        Workspace root directory.
        """

        return self._root

    @property
    def cwd(self) -> Path:
        return self._root

    def resolve(
        self,
        relative_path: str | Path,
    ) -> Path:
        """
        Resolve a path inside the workspace.

        Prevents escaping outside the workspace.
        """

        path = (
            self._root
            / Path(relative_path)
        ).resolve()

        if not str(path).startswith(
            str(self._root),
        ):
            raise PermissionError(
                "Path escapes workspace."
            )

        return path

    def exists(
        self,
        relative_path: str | Path,
    ) -> bool:

        return self.resolve(
            relative_path,
        ).exists()

    def mkdir(
        self,
        relative_path: str | Path,
    ) -> Path:

        path = self.resolve(
            relative_path,
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    def delete(
        self,
        relative_path: str | Path,
    ) -> None:

        path = self.resolve(
            relative_path,
        )

        if path.exists():
            path.unlink()
