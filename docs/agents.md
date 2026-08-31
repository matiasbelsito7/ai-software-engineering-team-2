# Agent Descriptions

## Overview

The AI Software Engineering Team consists of 10 specialized agents that collaborate through a structured LangGraph workflow. Each agent follows a consistent lifecycle and is responsible for a specific phase of software development.

---

## Agent Workflow

```
START → Spec → Planner → Architect → Backend → Frontend → Reviewer
                                                          │
                                           approved ──────┤
                                                          ├──→ QA
                                           not approved ──┤
                                                          │
                                                          └──→ Backend (loop)
                                                                 │
                                           QA passed ───────────┤
                                                                 ├──→ Documentation → DevOps → Git → END
                                           QA failed ───────────┤
                                                                 │
                                                                 └──→ Backend (loop)
```

---

## Agent Specifications

### 1. Spec Agent

| Property | Value |
|----------|-------|
| Capability | `SPEC` |
| Purpose | Generate technical specification from natural language requirements |
| Input | User's app description (natural language) |
| Output | `AppSpecification` (components, features, DB schema, endpoints) |
| Tools | search, documentation, rag, memory |
| Position in workflow | First (before Planner) |

**Responsibilities:**
- Parse user's natural language description
- Identify required UI components (pages, forms, modals)
- Define business features and logic
- Design database schema
- Specify API endpoints
- Determine authentication requirements
- Output technical specification for other agents

**Output Model:**
```python
class AppSpecification(BaseModel):
    app_name: str
    description: str
    tech_stack: dict  # frontend, backend, database
    components: list[AppComponent]
    features: list[Feature]
    database_schema: DatabaseSchema
    api_endpoints: list[Endpoint]
    authentication: AuthRequirements
    deployment: DeploymentConfig
```

---

### 2. Planner Agent

| Property | Value |
|----------|-------|
| Capability | `PLANNER` |
| Purpose | Decompose specification into ordered execution plan |
| Input | `AppSpecification` from Spec Agent |
| Output | `ExecutionPlan` (phases, tasks, dependencies) |
| Tools | search, documentation, rag, memory |
| Position in workflow | Second |

**Responsibilities:**
- Read specification from Spec Agent
- Break down into phases (setup, backend, frontend, testing)
- Define task dependencies and execution order
- Estimate tokens and cost per phase
- Create actionable plan for downstream agents

---

### 3. Architect Agent

| Property | Value |
|----------|-------|
| Capability | `ARCHITECT` |
| Purpose | Design system architecture and technology decisions |
| Input | `ExecutionPlan` from Planner |
| Output | `ArchitectureDesign` (patterns, tech choices, structure) |
| Tools | search, documentation, rag, memory |
| Position in workflow | Third |

**Responsibilities:**
- Design overall system architecture
- Choose frameworks and libraries
- Define project structure
- Specify integration patterns
- Create technical design document

---

### 4. Backend Agent

| Property | Value |
|----------|-------|
| Capability | `BACKEND` |
| Purpose | Implement backend code and API |
| Input | Architecture design + specification |
| Output | Source code files, dependency changes |
| Tools | repository, filesystem, search, documentation, rag, memory, code_formatter, dependency_manager, code_analyzer, complexity_analyzer, test_runner, linter, type_checker |
| Position in workflow | Fourth (can loop back from Reviewer/QA) |

**Responsibilities:**
- Implement API endpoints
- Create database models
- Write business logic
- Add authentication
- Write unit tests
- Format and lint code

---

### 5. Frontend Agent

| Property | Value |
|----------|-------|
| Capability | `FRONTEND` |
| Purpose | Implement frontend UI and components |
| Input | Architecture design + specification |
| Output | React/TypeScript components, styles |
| Tools | repository, filesystem, search, documentation, rag, memory, code_formatter, dependency_manager, code_analyzer, test_runner, linter, type_checker |
| Position in workflow | Fifth |

**Responsibilities:**
- Create React components
- Implement pages and routing
- Add state management
- Style with Tailwind CSS
- Write component tests
- Ensure responsive design

---

### 6. Reviewer Agent

| Property | Value |
|----------|-------|
| Capability | `REVIEWER` |
| Purpose | Review code quality and approve/reject changes |
| Input | Code from Backend + Frontend |
| Output | Review result (approved: bool, issues, suggestions) |
| Tools | repository, filesystem, search, documentation, rag, memory, code_analyzer, complexity_analyzer, security_scanner, test_runner, linter, type_checker |
| Position in workflow | Sixth (can send back to Backend) |

**Responsibilities:**
- Analyze code quality
- Check for security vulnerabilities
- Verify best practices
- Approve or reject with detailed feedback
- Loop back to Backend if issues found

---

### 7. QA Agent

| Property | Value |
|----------|-------|
| Capability | `QA` |
| Purpose | Validate software quality through testing |
| Input | Code + Review results |
| Output | Test results (passed: bool, test cases, issues) |
| Tools | repository, filesystem, search, documentation, rag, memory, code_analyzer, security_scanner, test_runner, linter, type_checker |
| Position in workflow | Seventh (can send back to Backend) |

**Responsibilities:**
- Generate test cases
- Run automated tests
- Validate functionality
- Report failures
- Loop back to Backend if tests fail

---

### 8. Documentation Agent

| Property | Value |
|----------|-------|
| Capability | `DOCUMENTATION` |
| Purpose | Generate project documentation |
| Input | All previous agent outputs |
| Output | README, API docs, setup instructions |
| Tools | repository, filesystem, search, documentation, rag, memory |
| Position in workflow | Eighth |

**Responsibilities:**
- Generate README.md
- Create API documentation
- Write setup instructions
- Document environment variables
- Add code comments

---

### 9. DevOps Agent

| Property | Value |
|----------|-------|
| Capability | `DEVOPS` |
| Purpose | Generate deployment configuration |
| Input | Architecture + Documentation |
| Output | Docker, CI/CD, deployment configs |
| Tools | repository, filesystem, search, documentation, rag, memory, dependency_manager, code_analyzer, security_scanner, test_runner, linter, type_checker |
| Position in workflow | Ninth |

**Responsibilities:**
- Create Dockerfile
- Generate docker-compose.yml
- Set up CI/CD pipelines
- Configure environment variables
- Prepare deployment scripts

---

### 10. Git Agent

| Property | Value |
|----------|-------|
| Capability | `GIT` |
| Purpose | Manage version control operations |
| Input | All generated files |
| Output | Git repository with commits |
| Tools | repository, filesystem, git |
| Position in workflow | Last (before END) |

**Responsibilities:**
- Initialize git repository
- Create initial commit
- Set up .gitignore
- Tag release
- Package for download

---

## Agent Communication

### Via Graph State

All agents share `GraphState`:

```python
class GraphState(BaseModel):
    conversation: ConversationState  # user_request, history
    execution: ExecutionState        # iteration, max_iterations
    memory: MemoryContext | None     # shared memory
    rag: RAGContext | None           # shared RAG
    artifacts: ArtifactState         # results[], shared_files
    feedback: FeedbackState          # human-in-the-loop
```

Each agent:
1. Reads previous results from `state.artifacts.results`
2. Appends its own result to `state.artifacts.results`
3. Returns modified state for next agent

### Via Conditional Routing

- **Reviewer → Backend**: If `approved == False`, loop back for revisions
- **QA → Backend**: If `passed == False`, loop back for fixes
- **Budget check**: Before each agent, verify remaining tokens > 0

---

## BaseAgent Lifecycle

```
execute(execution)
  ├── validate()         → Check preconditions
  ├── before_execution() → Start observability tracking
  ├── prepare()          → RAG retrieval, memory, context window
  ├── run()              → Generate LLM response, parse output
  └── after_execution()  → Store result, record metrics
```

Each agent implements:
- `AgentInfo` — metadata (name, capability, version)
- `BaseParser[T]` — parse LLM output into Pydantic model
- `BasePromptBuilder` — build system + task prompts
- Output model `T` — structured result type
