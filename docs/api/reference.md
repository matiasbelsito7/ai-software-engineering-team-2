# API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

Currently, no authentication is required. CORS is configured to allow all origins by default.

## Endpoints

### Health Check

```
GET /api/v1/health
```

**Response** `200 OK`

```json
{
  "status": "ok",
  "version": "0.1.0",
  "uptime_seconds": 123.45
}
```

---

### Create Task

```
POST /api/v1/tasks
```

Submit a task for execution. The task runs in the background. Use the returned `task_id` to poll status or subscribe via WebSocket.

**Request Body**

```json
{
  "task": "Build a REST API for user management",
  "system_prompt": "Use FastAPI and SQLAlchemy",
  "metadata": {"priority": "high"}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `task` | string | Yes | Natural-language task description (1–10,000 chars) |
| `system_prompt` | string | No | Optional system prompt override |
| `metadata` | object | No | Arbitrary metadata attached to the task |

**Response** `202 Accepted`

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

---

### Get Task

```
GET /api/v1/tasks/{task_id}
```

Retrieve the current status and results of a task.

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | string | The task UUID |

**Response** `200 OK`

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:05:00+00:00",
  "results": [
    {
      "agent": "backend",
      "success": true,
      "output": {"files": ["api/users.py", "models/user.py"]},
      "message": "Backend implementation completed",
      "next_agent": "frontend",
      "metadata": {}
    }
  ],
  "files": {
    "api/users.py": "from fastapi import APIRouter...",
    "models/user.py": "from pydantic import BaseModel..."
  },
  "error": null
}
```

**Task Status Values**

| Status | Description |
|--------|-------------|
| `pending` | Task created, waiting to start |
| `running` | Task is being executed |
| `completed` | Task finished successfully |
| `failed` | Task failed with an error |

---

### List Tasks

```
GET /api/v1/tasks
```

List tasks with optional filtering and pagination.

**Query Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `offset` | int | `0` | Pagination offset |
| `limit` | int | `50` | Maximum items to return |
| `status` | string | — | Filter by status |

**Response** `200 OK`

```json
{
  "tasks": [
    {
      "task_id": "...",
      "status": "completed",
      "created_at": "...",
      "updated_at": "..."
    }
  ],
  "total": 42,
  "offset": 0,
  "limit": 50
}
```

---

### Delete Task

```
DELETE /api/v1/tasks/{task_id}
```

Delete a task and its results.

**Response** `204 No Content`

---

### WebSocket: Task Progress

```
WS /ws/tasks/{task_id}
```

Connect for real-time task progress updates.

**Messages**

Progress update:
```json
{
  "type": "progress",
  "task_id": "...",
  "status": "running",
  "agent": "backend",
  "message": "Generating API endpoints",
  "progress": 0.4,
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

Task complete:
```json
{
  "type": "complete",
  "task_id": "...",
  "status": "completed",
  "results": [...],
  "files": {...},
  "timestamp": "2024-01-01T00:05:00+00:00"
}
```

Task failed:
```json
{
  "type": "error",
  "task_id": "...",
  "error": "LLM provider unavailable",
  "timestamp": "2024-01-01T00:01:00+00:00"
}
```

Ping (keepalive, every 30s):
```json
{"type": "ping"}
```

---

## Error Responses

All errors follow a standard format:

```json
{
  "detail": "Task 'abc' not found.",
  "error_code": "task_not_found"
}
```

| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 404 | `task_not_found` | Task does not exist |
| 409 | `task_conflict` | Task state conflict |
| 422 | `validation_error` | Request validation failed |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_error` | Unexpected server error |

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
