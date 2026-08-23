# API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

API key authentication is available via the `X-API-Key` header. Rate limiting is applied per IP address.

## Endpoints

### Core

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/tasks` | Submit a task (202 Accepted) |
| `GET` | `/tasks` | List tasks with pagination |
| `GET` | `/tasks/{task_id}` | Get task status and results |
| `DELETE` | `/tasks/{task_id}` | Delete a task |
| `GET` | `/tasks/{task_id}/stream` | SSE streaming |
| `GET` | `/tasks/{task_id}/feedback` | Get feedback |
| `POST` | `/tasks/{task_id}/feedback/{id}` | Submit feedback |
| `WS` | `/ws/tasks/{task_id}` | WebSocket progress |

### Approvals (Human-in-the-Loop)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/tasks/{task_id}/approvals` | Get pending approvals for a task |
| `POST` | `/tasks/{task_id}/approvals/{approval_id}` | Approve or reject a command |

See [Human-in-the-Loop Guide](../guides/human-in-the-loop.md) for details.

### Templates

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/templates` | List all templates |
| `GET` | `/templates/{template_id}` | Get template details |
| `POST` | `/templates/{template_id}/render` | Render template |
| `POST` | `/templates/{template_id}/create-task` | Create task from template |

### Code Review

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/review` | Run automated code review |

### Testing

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/tests/generate` | Generate test files |

### Deployment

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/deployment/generate` | Generate CI/CD pipelines |

### Knowledge Base

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/knowledge` | Add knowledge entry |
| `GET` | `/knowledge` | List entries |
| `GET` | `/knowledge/search` | Search knowledge |
| `GET` | `/knowledge/{entry_id}` | Get entry |
| `DELETE` | `/knowledge/{entry_id}` | Delete entry |
| `GET` | `/knowledge/stats` | Knowledge statistics |

### Orchestration

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/orchestration/plans` | Create orchestration plan |
| `GET` | `/orchestration/plans` | List plans |
| `GET` | `/orchestration/plans/{plan_id}` | Get plan |
| `GET` | `/orchestration/plans/{plan_id}/result` | Get result |
| `GET` | `/orchestration/plans/{plan_id}/execution-order` | Get execution stages |
| `GET` | `/orchestration/plans/{plan_id}/runnable` | Get runnable tasks |
| `DELETE` | `/orchestration/plans/{plan_id}` | Delete plan |

### Cost Tracking

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/cost-tracking/records` | Record LLM usage |
| `GET` | `/cost-tracking/summary` | Cost summary |
| `GET` | `/cost-tracking/records` | List cost records |
| `GET` | `/cost-tracking/stats` | Cost statistics |
| `POST` | `/cost-tracking/alerts` | Create alert |
| `GET` | `/cost-tracking/alerts` | List alerts |
| `DELETE` | `/cost-tracking/alerts/{alert_id}` | Delete alert |
| `POST` | `/cost-tracking/budgets` | Create budget |
| `GET` | `/cost-tracking/budgets` | List budgets |
| `DELETE` | `/cost-tracking/budgets/{budget_id}` | Delete budget |

## Detailed Examples

### Create Task

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"task": "Build a REST API for user management"}'
```

Response `202 Accepted`:

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

### SSE Streaming

```bash
curl -N http://localhost:8000/api/v1/tasks/{task_id}/stream
```

Events: `task_start`, `agent_progress`, `task_complete`, `error`, `ping`

### Code Review

```bash
curl -X POST http://localhost:8000/api/v1/review \
  -H "Content-Type: application/json" \
  -d '{"task_id": "...", "files": [{"file_path": "app.py", "content": "..."}]}'
```

### Knowledge Base

```bash
# Add entry
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{"entry_id": "auth", "title": "Authentication", "content": "...", "knowledge_type": "procedure", "tags": ["auth"]}'

# Search
curl "http://localhost:8000/api/v1/knowledge/search?q=authentication"
```

### Orchestration

```bash
# Create plan with dependencies
curl -X POST http://localhost:8000/api/v1/orchestration/plans \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": "stack",
    "name": "Full Stack",
    "tasks": [
      {"task_id": "api", "name": "API", "task_prompt": "Build API"},
      {"task_id": "ui", "name": "UI", "task_prompt": "Build UI", "dependencies": ["api"]}
    ]
  }'

# Get execution order
curl http://localhost:8000/api/v1/orchestration/plans/stack/execution-order
```

### Cost Tracking

```bash
# Record usage
curl -X POST http://localhost:8000/api/v1/cost-tracking/records \
  -H "Content-Type: application/json" \
  -d '{"record_id": "r1", "provider": "openai", "model": "gpt-4o", "input_tokens": 1000, "output_tokens": 500}'

# Get summary
curl "http://localhost:8000/api/v1/cost-tracking/summary"

# Create budget
curl -X POST http://localhost:8000/api/v1/cost-tracking/budgets \
  -H "Content-Type: application/json" \
  -d '{"budget_id": "monthly", "name": "Monthly", "limit": 100.0}'
```

## Error Responses

```json
{
  "detail": "Task 'abc' not found.",
  "error_code": "task_not_found"
}
```

| Status | Error Code | Description |
|--------|------------|-------------|
| 404 | `task_not_found` | Resource not found |
| 409 | `task_conflict` | State conflict |
| 422 | `validation_error` | Validation failed |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_error` | Server error |

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
