"""
LangGraph builder.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from ai_team.agents.architect.agent import ArchitectAgent
from ai_team.agents.backend.agent import BackendAgent
from ai_team.agents.devops.agent import DevOpsAgent
from ai_team.agents.documentation.agent import DocumentationAgent
from ai_team.agents.frontend.agent import FrontendAgent
from ai_team.agents.git.agent import GitAgent
from ai_team.agents.planner.agent import PlannerAgent
from ai_team.agents.qa.agent import QAAgent
from ai_team.agents.reviewer.agent import ReviewerAgent

from ai_team.graph.state import GraphState
from ai_team.graph.workflow import Workflow, WorkflowNode


class GraphBuilder:
    """
    Builds the LangGraph workflow.
    """

    def __init__(
        self,
        *,
        planner: PlannerAgent,
        architect: ArchitectAgent,
        backend: BackendAgent,
        frontend: FrontendAgent,
        reviewer: ReviewerAgent,
        qa: QAAgent,
        documentation: DocumentationAgent,
        devops: DevOpsAgent,
        git: GitAgent,
    ) -> None:

        self._planner = planner
        self._architect = architect
        self._backend = backend
        self._frontend = frontend
        self._reviewer = reviewer
        self._qa = qa
        self._documentation = documentation
        self._devops = devops
        self._git = git

    def build(self):
        """
        Build and compile the workflow graph.
        """

        graph = StateGraph(GraphState)

        # -----------------------------------------------------
        # Nodes
        # -----------------------------------------------------

        graph.add_node(
            WorkflowNode.PLANNER,
            self._planner.run,
        )

        graph.add_node(
            WorkflowNode.ARCHITECT,
            self._architect.run,
        )

        graph.add_node(
            WorkflowNode.BACKEND,
            self._backend.run,
        )

        graph.add_node(
            WorkflowNode.FRONTEND,
            self._frontend.run,
        )

        graph.add_node(
            WorkflowNode.REVIEWER,
            self._reviewer.run,
        )

        graph.add_node(
            WorkflowNode.QA,
            self._qa.run,
        )

        graph.add_node(
            WorkflowNode.DOCUMENTATION,
            self._documentation.run,
        )

        graph.add_node(
            WorkflowNode.DEVOPS,
            self._devops.run,
        )

        graph.add_node(
            WorkflowNode.GIT,
            self._git.run,
        )

        # -----------------------------------------------------
        # Entry point
        # -----------------------------------------------------

        graph.add_edge(
            START,
            Workflow.start(),
        )

        # -----------------------------------------------------
        # Sequential edges
        # -----------------------------------------------------

        graph.add_edge(
            WorkflowNode.PLANNER,
            WorkflowNode.ARCHITECT,
        )

        graph.add_edge(
            WorkflowNode.ARCHITECT,
            WorkflowNode.BACKEND,
        )

        graph.add_edge(
            WorkflowNode.BACKEND,
            WorkflowNode.FRONTEND,
        )

        graph.add_edge(
            WorkflowNode.DOCUMENTATION,
            WorkflowNode.DEVOPS,
        )

        graph.add_edge(
            WorkflowNode.DEVOPS,
            WorkflowNode.GIT,
        )

        graph.add_edge(
            WorkflowNode.GIT,
            END,
        )

        # -----------------------------------------------------
        # Conditional edges
        # -----------------------------------------------------

        graph.add_conditional_edges(
            WorkflowNode.REVIEWER,
            Workflow.reviewer,
            {
                WorkflowNode.BACKEND: WorkflowNode.BACKEND,
                WorkflowNode.QA: WorkflowNode.QA,
            },
        )

        graph.add_conditional_edges(
            WorkflowNode.QA,
            Workflow.qa,
            {
                WorkflowNode.BACKEND: WorkflowNode.BACKEND,
                WorkflowNode.DOCUMENTATION: WorkflowNode.DOCUMENTATION,
            },
        )

        return graph.compile()