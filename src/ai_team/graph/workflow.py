"""
Workflow definition for the AI Software Engineering Team.
"""

from __future__ import annotations

from enum import StrEnum

from ai_team.graph.state import GraphState


class WorkflowNode(StrEnum):
    """
    Workflow node names.
    """

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

        return WorkflowNode.PLANNER

    # ---------------------------------------------------------
    # Sequential transitions
    # ---------------------------------------------------------

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
        """

        #
        # Placeholder.
        # Later this decision will depend on ReviewerAgent.
        #

        approved = True

        if approved:
            return WorkflowNode.QA

        return WorkflowNode.BACKEND

    @staticmethod
    def qa(
        state: GraphState,
    ) -> str:
        """
        QA decides whether testing passed.
        """

        #
        # Placeholder.
        #

        passed = True

        if passed:
            return WorkflowNode.DOCUMENTATION

        return WorkflowNode.BACKEND