"""
Git command builders.
"""

from __future__ import annotations

from shlex import quote


def status() -> str:
    return "git status --short"


def diff() -> str:
    return "git diff"


def branch() -> str:
    return "git branch"


def checkout(branch_name: str) -> str:
    return f"git checkout {quote(branch_name)}"


def add(path: str) -> str:
    return f"git add {quote(path)}"


def commit(message: str) -> str:
    return f"git commit -m {quote(message)}"


def log(limit: int = 10) -> str:
    return f"git log --oneline -n {limit}"


def restore(path: str) -> str:
    return f"git restore {quote(path)}"


def init() -> str:
    return "git init"


def clone(repository: str) -> str:
    return f"git clone {quote(repository)}"


def pull() -> str:
    return "git pull"


def push() -> str:
    return "git push"
