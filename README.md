# AI Software Engineering Team

Production-ready multi-agent AI software engineering platform built with LangGraph.

A team of 9 specialized AI agents that collaborate to plan, design, build, review, test, document, and deploy software projects through a structured workflow.

## Architecture

```
Planner → Architect → Backend → Frontend → Reviewer → QA → Documentation → DevOps → Git
    ↑                         ↑                                    │
    │                         └────────────────────────────────────┘
    │                                    (review loop)
    └─────────────────────────────────────────────────────────────────────
```

Each agent is powered by an LLM and has access to specialized tools (filesystem, terminal, git, code analysis, Docker, RAG, memory). The workflow is orchestrated via LangGraph with conditional routing — the Reviewer can send tasks back to Backend for revisions, and QA can trigger rework if tests fail.

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
- Docker & Docker Compose (optional, for containerized deployment)

### Installation

```bash
git clone https://github.com/matiasbelsito7/ai-software-engineering-team-2.git
cd ai-software-engineering-team-2
make install
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your settings (LLM provider API keys, etc.)
```

### Run Locally

```bash
make run
# API available at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

### Run with Docker

```bash
make docker-build
make docker-up
# API available at http://localhost:8000
```

## API

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/tasks` | Submit a task (runs in background) |
| `GET` | `/api/v1/tasks` | List tasks with pagination |
| `GET` | `/api/v1/tasks/{id}` | Get task status and results |
| `DELETE` | `/api/v1/tasks/{id}` | Delete a task |
| `GET` | `/api/v1/tasks/{id}/stream` | SSE streaming of task events |
| `GET` | `/api/v1/tasks/{id}/feedback` | Get task feedback |
| `POST` | `/api/v1/tasks/{id}/feedback/{id}` | Submit feedback response |
| `WS` | `/ws/tasks/{id}` | Real-time task progress |
| `GET` | `/api/v1/templates` | List task templates |
| `GET` | `/api/v1/templates/{id}` | Get template details |
| `POST` | `/api/v1/templates/{id}/render` | Render template with parameters |
| `POST` | `/api/v1/templates/{id}/create-task` | Create task from template |
| `POST` | `/api/v1/review` | Run automated code review |
| `POST` | `/api/v1/tests/generate` | Generate test files |
| `POST` | `/api/v1/deployment/generate` | Generate CI/CD pipelines |
| `POST/GET/DELETE` | `/api/v1/knowledge` | Knowledge base CRUD |
| `GET` | `/api/v1/knowledge/search` | Search knowledge base |
| `GET` | `/api/v1/knowledge/stats` | Knowledge base statistics |
| `POST/GET/DELETE` | `/api/v1/orchestration/plans` | Multi-task orchestration |
| `GET` | `/api/v1/orchestration/plans/{id}/execution-order` | Get execution stages |
| `GET` | `/api/v1/orchestration/plans/{id}/runnable` | Get runnable tasks |
| `POST/GET/DELETE` | `/api/v1/cost-tracking/records` | LLM cost tracking |
| `GET` | `/api/v1/cost-tracking/summary` | Cost summary with filters |
| `GET` | `/api/v1/cost-tracking/stats` | Overall cost statistics |
| `POST/GET/DELETE` | `/api/v1/cost-tracking/alerts` | Cost alerts |
| `POST/GET/DELETE` | `/api/v1/cost-tracking/budgets` | Cost budgets |

### Example

```bash
# Submit a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Build a REST API for user management with CRUD operations"}'

# Check status
curl http://localhost:8000/api/v1/tasks/{task_id}
```

### WebSocket

Connect to `ws://localhost:8000/ws/tasks/{task_id}` for real-time progress:

```json
{"type": "progress", "task_id": "...", "status": "running", "agent": "backend", "progress": 0.4}
{"type": "complete", "task_id": "...", "status": "completed", "results": [...]}
```

### SSE Streaming

Connect to `GET /api/v1/tasks/{id}/stream` for Server-Sent Events:

```
event: task_start
data: {"task_id": "...", "status": "running"}

event: agent_progress
data: {"task_id": "...", "agent": "backend", "message": "Generating code"}

event: task_complete
data: {"task_id": "...", "status": "completed", "results": [...]}

event: ping
data: {}
```

## Features

### Task Templates
Pre-built templates for common tasks: REST API, CLI tool, documentation, refactoring, testing, database schema.

```bash
# List templates
curl http://localhost:8000/api/v1/templates

# Create task from template
curl -X POST http://localhost:8000/api/v1/templates/rest-api/create-task \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"project_name": "my-api", "entities": ["User", "Post"]}}'
```

### Automated Code Review
Pattern-based code analysis with inline comments, severity levels, and scoring.

```bash
curl -X POST http://localhost:8000/api/v1/review \
  -H "Content-Type: application/json" \
  -d '{"task_id": "...", "files": [{"file_path": "app.py", "content": "..."}]}'
```

### Test Generation
Automated test file generation from source code analysis.

```bash
curl -X POST http://localhost:8000/api/v1/tests/generate \
  -H "Content-Type: application/json" \
  -d '{"source_files": [{"file_path": "app.py", "content": "..."}], "framework": "pytest"}'
```

### Deployment Automation
Generate CI/CD pipelines for GitHub Actions, GitLab CI, and Docker.

```bash
curl -X POST http://localhost:8000/api/v1/deployment/generate \
  -H "Content-Type: application/json" \
  -d '{"project_name": "my-app", "platforms": ["github-actions", "docker"]}'
```

### Knowledge Base
Persistent knowledge storage with full-text search and relevance scoring.

```bash
# Add knowledge
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{"entry_id": "fastapi-auth", "title": "FastAPI Authentication", "content": "...", "knowledge_type": "procedure", "tags": ["fastapi", "auth"]}'

# Search
curl "http://localhost:8000/api/v1/knowledge/search?q=authentication&tags=fastapi"
```

### Multi-task Orchestration
Execute multiple tasks with dependency resolution and parallel stages.

```bash
# Create plan
curl -X POST http://localhost:8000/api/v1/orchestration/plans \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": "full-stack",
    "name": "Full Stack App",
    "tasks": [
      {"task_id": "backend", "name": "Build Backend", "task_prompt": "..."},
      {"task_id": "frontend", "name": "Build Frontend", "task_prompt": "...", "dependencies": ["backend"]}
    ]
  }'

# Get execution order
curl http://localhost:8000/api/v1/orchestration/plans/full-stack/execution-order
```

### Cost Tracking
Track LLM usage costs by provider, model, agent, and task with alerts and budgets.

```bash
# Record usage
curl -X POST http://localhost:8000/api/v1/cost-tracking/records \
  -H "Content-Type: application/json" \
  -d '{"record_id": "r1", "provider": "openai", "model": "gpt-4o", "input_tokens": 1000, "output_tokens": 500}'

# Get summary
curl "http://localhost:8000/api/v1/cost-tracking/summary?provider=openai"

# Create budget
curl -X POST http://localhost:8000/api/v1/cost-tracking/budgets \
  -H "Content-Type: application/json" \
  -d '{"budget_id": "monthly", "name": "Monthly Budget", "limit": 100.0, "period": "monthly"}'
```

## Project Structure

```
src/ai_team/
├── agents/              # 9 specialized AI agents
│   ├── planner/         # Task decomposition
│   ├── architect/       # System design
│   ├── backend/         # Backend implementation
│   ├── frontend/        # Frontend implementation
│   ├── reviewer/        # Code review
│   ├── qa/              # Quality assurance
│   ├── documentation/   # Documentation generation
│   ├── devops/          # Deployment & infrastructure
│   └── git/             # Version control
├── app/api/             # FastAPI application
│   ├── routers/         # API endpoints (12 routers)
│   ├── schemas/         # Request/response models
│   ├── middleware/       # Auth, rate limit, logging, security headers
│   └── exceptions/      # Custom error types
├── graph/               # LangGraph workflow orchestration
├── tools/               # 30+ tools (filesystem, git, Docker, RAG, etc.)
│   ├── git/             # Git operations (branch, tag, stash, PR)
│   ├── docker/          # Docker container management
│   └── test_runner/     # Test execution
├── rag/                 # Retrieval-Augmented Generation
├── memory/              # Agent memory (short-term, project, semantic)
├── context/             # Context management (selection, compression, summarization)
├── templates/           # Task templates (REST API, CLI, docs, etc.)
├── review/              # Automated code review engine
├── testing/             # Test generation pipeline
├── deployment/          # CI/CD pipeline generation
├── knowledge/           # Knowledge base with search
├── orchestration/       # Multi-task orchestration engine
├── cost_tracking/       # LLM cost tracking and budgets
├── observability/       # Tracing, metrics, logging, cost tracking
├── evals/               # Evaluation framework with 5 heuristic metrics
└── infrastructure/      # Config, container, LLM providers, workspace
```

## Available Commands

```bash
make help           # Show all commands
make install        # Install dependencies
make run            # Start API server
make test           # Run all tests
make test-unit      # Run unit tests only
make lint           # Run linter
make typecheck      # Run type checker
make format         # Format code
make check          # Run all quality checks
make docker-up      # Start Docker services
make docker-down    # Stop Docker services
```

## Development

### Code Quality

- **Linting**: Ruff (configured in `pyproject.toml`)
- **Formatting**: Black
- **Type Checking**: mypy (strict mode)
- **Testing**: pytest with coverage

```bash
make check   # Runs format-check + lint + typecheck + test
```

### Architecture

The project follows a layered architecture:

- **Agents** → depend on tools, memory, RAG, context, observability
- **Tools** → depend on infrastructure (workspace, Docker, HTTP)
- **Graph** → orchestrates agents via LangGraph
- **API** → exposes agents via FastAPI
- **Infrastructure** → config, container, LLM providers

Run architecture validation:

```bash
make validate
```

## Tech Stack

- **Orchestration**: LangGraph, LangChain
- **LLM Providers**: OpenRouter, Ollama (OpenAI-compatible)
- **API**: FastAPI, uvicorn
- **Vector Store**: Qdrant (in-memory fallback)
- **Cache**: Redis
- **Observability**: OpenTelemetry, structlog
- **Evaluation**: Custom heuristic metrics
- **Containerization**: Docker, Docker Compose

## License

MIT License. See [LICENSE](LICENSE) for details.
