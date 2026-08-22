# Architecture Overview

## System Architecture

The AI Software Engineering Team is a multi-agent system where 9 specialized AI agents collaborate through a structured workflow to deliver complete software projects.

## Agent Workflow

```
                    ┌─────────────────────────────────────────────────┐
                    │                                                 │
                    ▼                                                 │
              ┌──────────┐    ┌───────────┐    ┌──────────┐          │
              │ Planner  │───▶│ Architect │───▶│ Backend  │──┐       │
              └──────────┘    └───────────┘    └──────────┘  │       │
                                                         │    │       │
                                                         ▼    │       │
                                                   ┌──────────┐│      │
                                                   │ Frontend ││      │
                                                   └──────────┘│      │
                                                         │     │      │
                                                         ▼     │      │
                                                   ┌──────────┐│      │
                                                   │ Reviewer ││      │
                                                   └──────────┘│      │
                                                         │     │      │
                                                    not  │     │      │
                                                    approved    │      │
                                                         │     │      │
                                                         └─────┘      │
                                                                      │
                                                         approved     │
                                                         │            │
                                                         ▼            │
                                                   ┌──────────┐      │
                                                   │    QA    │──┐   │
                                                   └──────────┘  │   │
                                                         │       │   │
                                                    fail  │       │   │
                                                         │       │   │
                                                         └───────┘   │
                                                                     │
                                                    pass            │
                                                         │          │
                                                         ▼          │
                                              ┌─────────────────┐   │
                                              │  Documentation  │   │
                                              └────────┬────────┘   │
                                                       │            │
                                                       ▼            │
                                                 ┌──────────┐       │
                                                 │  DevOps  │       │
                                                 └────────┬┘       │
                                                          │        │
                                                          ▼        │
                                                    ┌──────────┐   │
                                                    │   Git    │───┘
                                                    └──────────┘
```

### Conditional Routing

- **Reviewer → Backend**: If code review is not approved, tasks loop back to Backend for revisions (max 3 iterations)
- **QA → Backend**: If tests fail, tasks loop back to Backend for fixes (max 2 iterations)
- **QA → Documentation**: If tests pass, the workflow continues

## Component Architecture

### Agents

Each agent follows a consistent lifecycle:

1. **`prepare()`** — Build context from RAG, memory, and conversation history
2. **`validate()`** — Check preconditions (task, capability, inputs)
3. **`run()`** — Execute the agent's core logic (generate → parse → result)
4. **`after_execution()`** — Store results in memory, emit observability events

Agents are composed of:
- **`AgentInfo`** — Name, capability, version, description
- **`PromptBuilder`** — Builds system + task prompts from templates
- **`Parser`** — Parses LLM output into structured models
- **Output Model** — Pydantic model for the agent's result

### Tools

25+ tools organized by category:

| Category | Tools |
|----------|-------|
| Core | Filesystem, Terminal, Git, Python |
| Information | Search, Documentation, Repository, RAG, Memory |
| Code Quality | CodeFormatter, Linter, TypeChecker, ComplexityAnalyzer |
| Security | SecurityScanner, DependencyManager |
| Containers | Docker |
| Network | HTTP, Browser |

Tools are registered via `build_tools()` and injected into agents through `AgentDependencies`.

### Graph (LangGraph)

The workflow is defined as a LangGraph `StateGraph` with:

- **Nodes**: Agent execution wrappers
- **Edges**: Sequential and conditional routing
- **State**: `GraphState` (conversation, execution, memory, RAG, artifacts)
- **Checkpoints**: Optional Redis-backed state persistence

### Infrastructure

- **Container**: Dependency injection composition root
- **Config**: Pydantic Settings with environment variable support
- **LLM**: OpenRouter (SSE streaming) and Ollama providers
- **Observability**: OpenTelemetry tracing, structured logging, cost tracking

## Data Flow

```
User Request
    │
    ▼
FastAPI Router ──▶ TaskStore (in-memory)
    │                    │
    │                    ▼
    │            Background Task
    │                    │
    │                    ▼
    │            LangGraph Workflow
    │                    │
    │    ┌───────────────┼───────────────┐
    │    ▼               ▼               ▼
    │  RAG           Memory          Context
    │  (retrieve      (retrieve       (select,
    │   relevant       past            compress,
    │   docs)          decisions)      summarize)
    │    │               │               │
    │    └───────────────┼───────────────┘
    │                    ▼
    │            Agent Execution
    │            (LLM + Tools)
    │                    │
    │                    ▼
    │            Artifacts (results, files)
    │                    │
    │                    ▼
    └──────────────▶ TaskStore
                         │
                         ▼
                   WebSocket / REST Response
```

## Design Principles

1. **Separation of Concerns**: Each module handles one responsibility
2. **Dependency Injection**: All services composed via the Container
3. **Optional Dependencies**: Docker, HTTP, Browser tools are conditionally registered
4. **Fail-Safe**: Docker failures don't crash the application
5. **Observability First**: Every agent call is traced, logged, and cost-tracked
6. **Type Safety**: Strict mypy with Pydantic models throughout
