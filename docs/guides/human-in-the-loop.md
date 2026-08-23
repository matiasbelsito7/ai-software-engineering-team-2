# Human-in-the-Loop

The AI Software Engineering Team supports human-in-the-loop approval for sensitive commands. When enabled, certain commands require explicit user approval before execution.

## Overview

Some terminal commands are potentially destructive or have significant side effects. The human-in-the-loop system ensures that commands like `git push`, `git commit`, `docker run`, etc. require explicit approval from the user before they are executed.

## How It Works

1. **Agent attempts to execute a command** — When an agent tries to run a command that requires approval (e.g., `git push`), the `TerminalTool` detects this via `CommandPolicy`.

2. **Approval request is created** — The system stores the pending approval and notifies the frontend via WebSocket with an `approval_request` event.

3. **User reviews the request** — The frontend displays the command details, including which agent requested it and what the command does.

4. **User approves or rejects** — The user clicks "Approve" or "Reject" in the UI.

5. **Command executes or is blocked** — If approved, the command executes. If rejected, the agent receives an error and can adjust its approach.

## Commands Requiring Approval

The following commands require human approval by default:

| Command | Description |
|---------|-------------|
| `git push` | Push commits to remote |
| `git push --force` | Force push to remote |
| `git clone` | Clone a repository |
| `git commit` | Create a commit |
| `git reset --hard` | Hard reset to a commit |
| `git clean` | Remove untracked files |
| `gh pr merge` | Merge a pull request |
| `gh pr create` | Create a pull request |
| `docker run` | Run a container |
| `docker compose up` | Start containers |

## Configuration

### Customizing Approval Commands

You can customize which commands require approval by modifying the `CommandPolicy`:

```python
from ai_team.tools.terminal.policy import CommandPolicy

# Create a custom policy
policy = CommandPolicy(
    approval_commands={
        "git push",
        "git commit",
        "npm publish",  # Add custom commands
    }
)
```

### Disabling Approval (Not Recommended)

To disable approval for all commands, set an empty set:

```python
policy = CommandPolicy(approval_commands=set())
```

## API Endpoints

### Get Pending Approvals

```bash
GET /api/v1/tasks/{task_id}/approvals
```

Returns all pending approval requests for a task.

**Response:**
```json
[
  {
    "approval_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": "abc-123",
    "command": "git push origin main",
    "agent": "Git",
    "description": "The agent wants to execute: git push origin main",
    "status": "pending"
  }
]
```

### Approve or Reject

```bash
POST /api/v1/tasks/{task_id}/approvals/{approval_id}
```

**Request body:**
```json
{
  "approved": true
}
```

**Response:**
```json
{
  "approval_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_id": "abc-123",
  "command": "git push origin main",
  "agent": "Git",
  "description": "The agent wants to execute: git push origin main",
  "status": "approved"
}
```

## WebSocket Events

When an approval is requested, the frontend receives an `approval_request` event:

```json
{
  "type": "approval_request",
  "task_id": "abc-123",
  "approval_id": "550e8400-e29b-41d4-a716-446655440000",
  "command": "git push origin main",
  "agent": "Git",
  "description": "The agent wants to execute: git push origin main"
}
```

When the user responds, an `approval_response` event is sent:

```json
{
  "type": "approval_response",
  "task_id": "abc-123",
  "approval_id": "550e8400-e29b-41d4-a716-446655440000",
  "approved": true,
  "command": "git push origin main"
}
```

## Frontend Integration

The frontend automatically displays approval requests in the task detail page:

- **Pending Approvals Panel** — Shows all commands waiting for approval
- **Approve Button** — Green button to approve the command
- **Reject Button** — Red button to reject the command
- **Real-time Updates** — WebSocket updates show new approvals instantly

## Implementation Details

### CommandPolicy

Located in `src/ai_team/tools/terminal/policy.py`:

- `REQUIRES_APPROVAL_COMMANDS` — Set of commands that need approval
- `requires_approval(command)` — Returns True if command needs approval

### TerminalTool

Located in `src/ai_team/tools/terminal/terminal.py`:

- `set_approval_context()` — Sets the TaskStore and task_id for approval
- `_request_approval()` — Creates approval request and waits for response

### TaskStore

Located in `src/ai_team/app/api/task_store.py`:

- `request_approval()` — Stores approval and notifies subscribers
- `wait_approval()` — Blocks until approval is resolved
- `resolve_approval()` — Resolves approval and unblocks the agent

### Approvals Router

Located in `src/ai_team/app/api/routers/approvals.py`:

- `GET /tasks/{task_id}/approvals` — List pending approvals
- `POST /tasks/{task_id}/approvals/{approval_id}` — Resolve approval
