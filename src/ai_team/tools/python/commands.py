"""
Python command builders.
"""

from __future__ import annotations

from shlex import quote


def run_script(
    script: str,
) -> str:
    """
    Execute a Python script.
    """

    return f"python {quote(script)}"


def run_module(
    module: str,
) -> str:
    """
    Execute a Python module.
    """

    return f"python -m {quote(module)}"


def run_code(
    code: str,
) -> str:
    """
    Execute inline Python code.
    """

    return f"python -c {quote(code)}"


def pip_install(
    package: str,
) -> str:
    """
    Install a package.
    """

    return f"pip install {quote(package)}"


def pip_uninstall(
    package: str,
) -> str:
    """
    Uninstall a package.
    """

    return f"pip uninstall -y {quote(package)}"


def format_script(
    script: str,
) -> str:
    """
    Format a Python file using Black.
    """

    return f"black {quote(script)}"


def lint_script(
    script: str,
) -> str:
    """
    Lint a Python file using Ruff.
    """

    return f"ruff check {quote(script)}"


def test(
    path: str = ".",
) -> str:
    """
    Run pytest.
    """

    return f"pytest {quote(path)}"
