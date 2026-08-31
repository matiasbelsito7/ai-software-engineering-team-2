"""
Workflow definition for the AI Software Engineering Team.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_team.graph.state import GraphState


class WorkflowNode(StrEnum):
    """
    Workflow node names.
    """

    SPEC = "spec"

    PLANNER = "planner"

    ARCHITECT = "architect"

    BACKEND = "backend"

    FRONTEND = "frontend"

    REVIEWER = "reviewer"

    QA = "qa"

    DOCUMENTATION = "documentation"

    DEVOPS = "devops"

    GIT = "git"

    END = "__end__"


class Workflow:
    """
    Defines the execution flow of the multi-agent system.
    """

    @staticmethod
    def start() -> str:
        """
        Entry point of the workflow.
        """

        return WorkflowNode.SPEC

    # ---------------------------------------------------------
    # Sequential transitions
    # ---------------------------------------------------------

    @staticmethod
    def spec(
        state: GraphState,
    ) -> str:

        return WorkflowNode.PLANNER

    @staticmethod
    def planner(
        state: GraphState,
    ) -> str:

        return WorkflowNode.ARCHITECT

    @staticmethod
    def architect(
        state: GraphState,
    ) -> str:

        return WorkflowNode.BACKEND

    @staticmethod
    def backend(
        state: GraphState,
    ) -> str:

        return WorkflowNode.FRONTEND

    @staticmethod
    def frontend(
        state: GraphState,
    ) -> str:

        return WorkflowNode.REVIEWER

    @staticmethod
    def documentation(
        state: GraphState,
    ) -> str:

        return WorkflowNode.DEVOPS

    @staticmethod
    def devops(
        state: GraphState,
    ) -> str:

        return WorkflowNode.GIT

    @staticmethod
    def git(
        state: GraphState,
    ) -> str:

        return WorkflowNode.END

    # ---------------------------------------------------------
    # Conditional transitions
    # ---------------------------------------------------------

    @staticmethod
    def reviewer(
        state: GraphState,
    ) -> str:
        """
        Reviewer decides whether the implementation
        must be reworked or can continue.

        Checks the last reviewer result for approval status.
        """

        last_result = state.artifacts.results[-1] if state.artifacts.results else None

        if (
            last_result is not None
            and hasattr(last_result, "approved")
            and not last_result.approved
        ):
            return WorkflowNode.BACKEND

        return WorkflowNode.QA

    @staticmethod
    def qa(
        state: GraphState,
    ) -> str:
        """
        QA decides whether testing passed.

        Checks the last QA result for pass/fail status.
        """

        last_result = state.artifacts.results[-1] if state.artifacts.results else None

        if last_result is not None and hasattr(last_result, "passed") and not last_result.passed:
            return WorkflowNode.BACKEND

        return WorkflowNode.DOCUMENTATION
