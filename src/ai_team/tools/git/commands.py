"""
Git command builders.
"""

from __future__ import annotations

from shlex import quote


def status() -> str:
    return "git status --short"


def diff() -> str:
    return "git diff"


def diff_staged() -> str:
    return "git diff --staged"


def diff_name_only() -> str:
    return "git diff --name-only"


def branch() -> str:
    return "git branch"


def checkout(branch_name: str) -> str:
    return f"git checkout {quote(branch_name)}"


def checkout_new(branch_name: str) -> str:
    return f"git checkout -b {quote(branch_name)}"


def add(path: str) -> str:
    return f"git add {quote(path)}"


def commit(message: str) -> str:
    return f"git commit -m {quote(message)}"


def log(limit: int = 10) -> str:
    return f"git log --oneline -n {limit}"


def log_detailed(limit: int = 5) -> str:
    return f"git log --pretty=format:'%h %s' -n {limit}"


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


def push_upstream(branch_name: str) -> str:
    return f"git push -u origin {quote(branch_name)}"


# =====================================================================
# Branch Management
# =====================================================================


def create_branch(branch_name: str) -> str:
    return f"git branch {quote(branch_name)}"


def create_and_checkout(branch_name: str) -> str:
    return f"git checkout -b {quote(branch_name)}"


def delete_branch(branch_name: str, force: bool = False) -> str:
    flag = "-D" if force else "-d"
    return f"git branch {flag} {quote(branch_name)}"


def rename_branch(old_name: str, new_name: str) -> str:
    return f"git branch -m {quote(old_name)} {quote(new_name)}"


def merge_branch(branch_name: str) -> str:
    return f"git merge {quote(branch_name)}"


def list_branches_remote() -> str:
    return "git branch -r"


def fetch() -> str:
    return "git fetch --all"


# =====================================================================
# Tag Operations
# =====================================================================


def create_tag(tag_name: str, message: str | None = None) -> str:
    if message:
        return f"git tag -a {quote(tag_name)} -m {quote(message)}"
    return f"git tag {quote(tag_name)}"


def list_tags() -> str:
    return "git tag -l"


def delete_tag(tag_name: str) -> str:
    return f"git tag -d {quote(tag_name)}"


# =====================================================================
# Stash Operations
# =====================================================================


def stash(message: str | None = None) -> str:
    if message:
        return f"git stash push -m {quote(message)}"
    return "git stash push"


def stash_pop() -> str:
    return "git stash pop"


def stash_list() -> str:
    return "git stash list"


def stash_drop() -> str:
    return "git stash drop"


# =====================================================================
# Remote Operations
# =====================================================================


def add_remote(name: str, url: str) -> str:
    return f"git remote add {quote(name)} {quote(url)}"


def list_remotes() -> str:
    return "git remote -v"


def remove_remote(name: str) -> str:
    return f"git remote remove {quote(name)}"


# =====================================================================
# PR Operations (via gh CLI)
# =====================================================================


def create_pr(title: str, body: str, base: str = "main", head: str | None = None) -> str:
    cmd = f"gh pr create --title {quote(title)} --body {quote(body)} --base {quote(base)}"
    if head:
        cmd += f" --head {quote(head)}"
    return cmd


def list_prs(state: str = "open") -> str:
    return f"gh pr list --state {quote(state)}"


def view_pr(pr_number: int | None = None) -> str:
    if pr_number:
        return f"gh pr view {pr_number}"
    return "gh pr view"


def checkout_pr(pr_number: int) -> str:
    return f"gh pr checkout {pr_number}"


def merge_pr(pr_number: int) -> str:
    return f"gh pr merge {pr_number} --merge"


def close_pr(pr_number: int) -> str:
    return f"gh pr close {pr_number}"


# =====================================================================
# Repository Info
# =====================================================================


def repo_url() -> str:
    return "git remote get-url origin"


def current_branch() -> str:
    return "git rev-parse --abbrev-ref HEAD"


def commit_count() -> str:
    return "git rev-list --count HEAD"


def last_commit() -> str:
    return "git log -1 --pretty=format:'%h %s'"
