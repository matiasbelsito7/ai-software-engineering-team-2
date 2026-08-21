"""Validate project architecture structure."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_DIRS = [
    "src/ai_team/agents",
    "src/ai_team/app",
    "src/ai_team/context",
    "src/ai_team/evals",
    "src/ai_team/graph",
    "src/ai_team/infrastructure",
    "src/ai_team/memory",
    "src/ai_team/observability",
    "src/ai_team/rag",
    "src/ai_team/shared",
    "src/ai_team/tools",
]

REQUIRED_FILES = [
    "src/ai_team/agents/__init__.py",
    "src/ai_team/agents/base.py",
    "src/ai_team/graph/builder.py",
    "src/ai_team/graph/state.py",
    "pyproject.toml",
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []

    errors.extend(f"Missing directory: {d}" for d in REQUIRED_DIRS if not (root / d).is_dir())

    errors.extend(f"Missing file: {f}" for f in REQUIRED_FILES if not (root / f).is_file())

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("Architecture validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
