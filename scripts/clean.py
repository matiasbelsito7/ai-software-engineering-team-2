```python
"""
scripts/clean.py

Cross-platform cleanup utility for the AI Software Engineering Team project.

Removes build artifacts, caches and temporary files generated during
development, testing and packaging.
"""

from __future__ import annotations

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DIRECTORIES_TO_REMOVE = [
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".hypothesis",
    ".coverage",
    "htmlcov",
    "build",
    "dist",
    ".tox",
]

FILES_TO_REMOVE = [
    ".coverage",
]

FILE_PATTERNS = [
    "*.pyc",
    "*.pyo",
]


def remove_directory(path: Path) -> None:
    """Remove a directory if it exists."""

    if not path.exists():
        return

    shutil.rmtree(path)
    print(f"✓ Removed directory: {path.relative_to(PROJECT_ROOT)}")


def remove_file(path: Path) -> None:
    """Remove a file if it exists."""

    if not path.exists():
        return

    path.unlink()
    print(f"✓ Removed file: {path.relative_to(PROJECT_ROOT)}")


def remove_named_directories() -> None:
    """Remove known cache/build directories recursively."""

    for directory_name in DIRECTORIES_TO_REMOVE:
        for directory in PROJECT_ROOT.rglob(directory_name):
            if directory.is_dir():
                remove_directory(directory)


def remove_named_files() -> None:
    """Remove known files."""

    for filename in FILES_TO_REMOVE:
        remove_file(PROJECT_ROOT / filename)


def remove_pattern_files() -> None:
    """Remove files matching known patterns."""

    for pattern in FILE_PATTERNS:
        for file in PROJECT_ROOT.rglob(pattern):
            if file.is_file():
                remove_file(file)


def main() -> None:
    """Run project cleanup."""

    print()
    print("Cleaning project...")
    print()

    remove_named_directories()
    remove_named_files()
    remove_pattern_files()

    print()
    print("Project successfully cleaned.")


if __name__ == "__main__":
    main()
```
