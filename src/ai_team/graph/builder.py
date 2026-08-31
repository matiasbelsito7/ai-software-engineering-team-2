"""
LangGraph builder.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from langgraph.graph import END, START, StateGraph

from ai_team.graph.state import GraphState
from ai_team.graph.workflow import Workflow, WorkflowNode

if TYPE_CHECKING:
    from ai_team.agents.architect.agent import ArchitectAgent
    from ai_team.agents.backend.agent import BackendAgent
    from ai_team.agents.devops.agent import DevOpsAgent
    from ai_team.agents.documentation.agent import DocumentationAgent
    from ai_team.agents.frontend.agent import FrontendAgent
    from ai_team.agents.git.agent import GitAgent
    from ai_team.agents.planner.agent import PlannerAgent
    from ai_team.agents.qa.agent import QAAgent
    from ai_team.agents.reviewer.agent import ReviewerAgent

logger = logging.getLogger(__name__)


def _make_agent_node(
    agent: Any,
) -> Any:
    """
    Wrap a BaseAgent so it can be used as a LangGraph node.

    LangGraph nodes receive and return GraphState.
    BaseAgent.execute() expects AgentExecution and returns AgentExecution.

    Includes budget checking before execution.
    """

    async def _node(state: GraphState) -> GraphState:
        from ai_team.agents.execution import (
            AgentExecution,
            AgentRequest,
        )

        # Check budget before executing
        if state.budget.budget_exhausted:
            logger.warning(
                "Budget exhausted for project %s. Skipping agent %s.",
                state.budget.project_id,
                agent.info.name,
            )
            # Create a skipped result
            from ai_team.agents.result import AgentResult

            skipped_result = AgentResult(
                success=False,
                output=None,
                message=f"Budget exhausted. Used {state.budget.tokens_used}/{state.budget.tokens_budget} tokens.",
                next_agent=None,
                metadata={
                    "agent": agent.info.name,
                    "skipped": True,
                    "reason": "budget_exhausted",
                },
            )
            state.artifacts.results.append(skipped_result)
            state.execution.current_agent = agent.info.name
            state.execution.previous_agent = agent.info.name
            return state

        # Check iteration limit
        if state.budget.iterations_exhausted:
            logger.warning(
                "Iteration limit reached for project %s. Skipping agent %s.",
                state.budget.project_id,
                agent.info.name,
            )
            from ai_team.agents.result import AgentResult

            skipped_result = AgentResult(
                success=False,
                output=None,
                message=f"Iteration limit reached. Used {state.budget.iterations_used}/{state.budget.max_iterations} iterations.",
                next_agent=None,
                metadata={
                    "agent": agent.info.name,
                    "skipped": True,
                    "reason": "iterations_exhausted",
                },
            )
            state.artifacts.results.append(skipped_result)
            state.execution.current_agent = agent.info.name
            state.execution.previous_agent = agent.info.name
            return state

        execution = AgentExecution(
            capability=agent.capability,
            request=AgentRequest(
                task=state.conversation.user_request,
            ),
            graph_state=state,
        )

        execution = await agent.execute(execution)

        # Update budget tracking from LLM response
        if execution.llm_response is not None and execution.llm_response.usage is not None:
            tokens = execution.llm_response.usage.total_tokens
            state.budget.tokens_used += tokens

        state.artifacts.results.append(
            execution.result,
        )

        state.execution.current_agent = agent.info.name
        state.execution.previous_agent = state.execution.current_agent

        return state

    return _node


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

    def build(self) -> Any:
        """
        Build and compile the workflow graph.
        """

        graph = StateGraph(GraphState)

        # -----------------------------------------------------
        # Nodes
        # -----------------------------------------------------

        graph.add_node(
            WorkflowNode.PLANNER,
            _make_agent_node(self._planner),
        )

        graph.add_node(
            WorkflowNode.ARCHITECT,
            _make_agent_node(self._architect),
        )

        graph.add_node(
            WorkflowNode.BACKEND,
            _make_agent_node(self._backend),
        )

        graph.add_node(
            WorkflowNode.FRONTEND,
            _make_agent_node(self._frontend),
        )

        graph.add_node(
            WorkflowNode.REVIEWER,
            _make_agent_node(self._reviewer),
        )

        graph.add_node(
            WorkflowNode.QA,
            _make_agent_node(self._qa),
        )

        graph.add_node(
            WorkflowNode.DOCUMENTATION,
            _make_agent_node(self._documentation),
        )

        graph.add_node(
            WorkflowNode.DEVOPS,
            _make_agent_node(self._devops),
        )

        graph.add_node(
            WorkflowNode.GIT,
            _make_agent_node(self._git),
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
            WorkflowNode.FRONTEND,
            WorkflowNode.REVIEWER,
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
