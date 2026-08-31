# Task List

## Overview

Implementation tasks for the AI Software Engineering Team new features. Each task is numbered and includes description, files to create/modify, acceptance criteria, and dependencies.

---

## Task 1: Authentication System — User Model & JWT

**Status:** Completed
**Priority:** High
**Estimated time:** 2-3 hours
**Dependencies:** None

### Description

Implement the complete authentication system including User ORM model, JWT token handling, password hashing, and auth API endpoints.

### Files to Create

- `src/ai_team/domain/models/user.py`
- `src/ai_team/domain/schemas/auth.py`
- `src/ai_team/domain/services/auth_service.py`
- `src/ai_team/app/api/routers/auth.py`

### Files to Modify

- `src/ai_team/infrastructure/config/security.py` (add JWT config)
- `src/ai_team/app/api/dependencies.py` (add get_current_user)
- `pyproject.toml` (add dependencies)

### Acceptance Criteria

- [ ] User can register with email and password
- [ ] Password is hashed with bcrypt
- [ ] User can login and receive JWT access + refresh tokens
- [ ] Access token expires in 30 minutes
- [ ] Refresh token expires in 7 days
- [ ] User can get profile with GET /auth/me
- [ ] Invalid credentials return 401
- [ ] Expired tokens return 401
- [ ] Password reset flow works (forgot-password → email → reset-password)

---

## Task 2: Tier System — Configuration & Project Model

**Status:** Completed
**Priority:** High
**Estimated time:** 1-2 hours
**Dependencies:** Task 1

### Description

Define tier configurations (Free, Starter, Pro, Business) and create Project ORM model with tier-aware limits.

### Files to Create

- `src/ai_team/domain/models/project.py`
- `src/ai_team/domain/models/tier.py`
- `src/ai_team/domain/schemas/project.py`
- `src/ai_team/domain/services/project_service.py`
- `src/ai_team/app/api/routers/projects.py`

### Acceptance Criteria

- [ ] Tier configurations defined with all parameters
- [ ] Project model stores user_id, tier, tokens_used, status
- [ ] User can create project via POST /projects
- [ ] User can list their projects via GET /projects
- [ ] Free tier limited to 3 projects
- [ ] Token budget per project enforced by tier
- [ ] Iteration limit per project enforced by tier
- [ ] Project expires based on tier retention period

---

## Task 3: Cost Tracking Integration

**Status:** Completed
**Priority:** High
**Estimated time:** 1-2 hours
**Dependencies:** Task 2

### Description

Connect the observability cost tracking to the agent workflow and enforce budget limits based on tier configuration.

### Files to Modify

- `src/ai_team/observability/costs.py`
- `src/ai_team/observability/manager.py`
- `src/ai_team/agents/base.py`
- `src/ai_team/graph/builder.py`

### Acceptance Criteria

- [ ] LLM calls are recorded in cost tracker automatically
- [ ] Token usage is tracked per agent
- [ ] Budget is checked before each agent execution
- [ ] Workflow stops when budget is exhausted
- [ ] User receives clear message when budget exceeded
- [ ] Partial progress is saved on budget exhaustion

---

## Task 4: Spec Agent

**Status:** Completed
**Priority:** High
**Estimated time:** 2-3 hours
**Dependencies:** None (can run in parallel with Tasks 1-3)

### Description

Create the Spec Agent that generates technical specifications from natural language user descriptions.

### Files to Create

- `src/ai_team/agents/spec/__init__.py`
- `src/ai_team/agents/spec/agent.py`
- `src/ai_team/agents/spec/models.py`
- `src/ai_team/agents/spec/prompt_builder.py`
- `src/ai_team/agents/spec/prompts/system.md`
- `src/ai_team/agents/spec/prompts/generate_spec.md`

### Acceptance Criteria

- [ ] SpecAgent extends BaseAgent correctly
- [ ] Output model includes all required fields (components, features, schema, endpoints)
- [ ] Agent parses natural language description into structured spec
- [ ] System prompt guides LLM to produce accurate specs
- [ ] Agent works with existing agent infrastructure (RAG, memory, observability)
- [ ] Unit tests pass for model validation

---

## Task 5: Workflow Integration — Add Spec Agent

**Status:** Completed
**Priority:** High
**Estimated time:** 1 hour
**Dependencies:** Tasks 2, 4

### Description

Integrate the Spec Agent into the LangGraph workflow as the first node, before the Planner Agent.

### Files to Modify

- `src/ai_team/graph/builder.py`
- `src/ai_team/graph/state.py`
- `src/ai_team/graph/workflow.py`

### Acceptance Criteria

- [ ] Spec Agent node added before Planner in graph
- [ ] GraphState includes specification field
- [ ] Spec output is available to all subsequent agents
- [ ] Workflow executes: Spec → Planner → Architect → ...
- [ ] No regression in existing agent functionality

---

## Task 6: App Generator Service

**Status:** Pending
**Priority:** High
**Estimated time:** 2 hours
**Dependencies:** Tasks 2, 3, 5

### Description

Create the service that orchestrates the full generation pipeline: spec → workflow → file output → preview → ZIP.

### Files to Create

- `src/ai_team/domain/services/app_generator.py`
- `src/ai_team/domain/services/app_preview.py`
- `src/ai_team/domain/services/app_packager.py`

### Acceptance Criteria

- [ ] Generator creates project, runs workflow, saves files
- [ ] Preview HTML is generated from output files
- [ ] ZIP package includes complete project structure
- [ ] ZIP includes README with setup instructions
- [ ] Generator respects tier token budget
- [ ] Generator updates project.tokens_used in real-time
- [ ] Generator handles workflow failures gracefully

---

## Task 7: Frontend Authentication

**Status:** Pending
**Priority:** High
**Estimated time:** 2 hours
**Dependencies:** Task 1

### Description

Implement login, registration, and protected route components in the React frontend.

### Files to Create

- `frontend/src/pages/Login.tsx`
- `frontend/src/pages/Register.tsx`
- `frontend/src/contexts/AuthContext.tsx`
- `frontend/src/components/ProtectedRoute.tsx`
- `frontend/src/services/api.ts`

### Acceptance Criteria

- [ ] Login form with email and password
- [ ] Registration form with email, password, confirm password
- [ ] JWT tokens stored securely (HTTP-only cookies)
- [ ] Protected routes redirect to login if unauthenticated
- [ ] Auth context provides user state to all components
- [ ] Logout clears tokens and redirects to login
- [ ] Form validation (email format, password strength)
- [ ] Error messages displayed for failed attempts

---

## Task 8: Frontend Wizard + Dashboard

**Status:** Pending
**Priority:** High
**Estimated time:** 2-3 hours
**Dependencies:** Tasks 2, 7

### Description

Create the 3-step project creation wizard and the user dashboard showing all projects.

### Files to Create

- `frontend/src/pages/Dashboard.tsx`
- `frontend/src/pages/Wizard.tsx`
- `frontend/src/components/AppCard.tsx`
- `frontend/src/components/TierSelector.tsx`

### Acceptance Criteria

- [ ] Dashboard shows all user projects with status
- [ ] "Create New App" button opens wizard
- [ ] Step 1: Textarea for app description (max 2000 chars)
- [ ] Step 2: Tier selector with pricing and features
- [ ] Step 3: Summary with estimated time and tokens
- [ ] Generation starts on confirm
- [ ] Loading state shows real-time progress
- [ ] Project card shows status, tier, creation date
- [ ] Free tier shows "Max 3 projects" limit

---

## Task 9: Frontend Preview + Download

**Status:** Pending
**Priority:** High
**Estimated time:** 2 hours
**Dependencies:** Tasks 6, 8

### Description

Implement the app preview page with iframe and ZIP download functionality.

### Files to Create

- `frontend/src/pages/Preview.tsx`
- `frontend/src/components/AppPreviewFrame.tsx`

### Acceptance Criteria

- [ ] Preview page shows generated app in iframe
- [ ] Download button generates and downloads ZIP
- [ ] Free tier shows upgrade prompt instead of download
- [ ] Preview page shows project metadata (name, tier, tokens used)
- [ ] "Create Another App" button returns to wizard
- [ ] "Delete Project" button with confirmation dialog
- [ ] Loading state during ZIP generation

---

## Task 10: Admin Dashboard

**Status:** Pending
**Priority:** Medium
**Estimated time:** 2 hours
**Dependencies:** Tasks 1, 2

### Description

Create admin dashboard with user management and platform metrics. Admin can only see metrics, not generated code.

### Files to Create

- `frontend/src/pages/admin/AdminDashboard.tsx`
- `frontend/src/pages/admin/UserManagement.tsx`
- `frontend/src/pages/admin/ProjectMonitoring.tsx`
- `src/ai_team/app/api/routers/admin.py`

### Acceptance Criteria

- [ ] Admin dashboard shows total users, projects, revenue
- [ ] Token usage breakdown by tier displayed
- [ ] User list with search and pagination
- [ ] User detail view (email, role, projects count)
- [ ] Can change user role (user ↔ admin)
- [ ] Can deactivate user accounts
- [ ] Project list shows all projects across users
- [ ] Admin CANNOT view generated code files
- [ ] Admin endpoints require admin role
- [ ] Regular users cannot access admin routes

---

## Task 11: Testing & Polish

**Status:** Pending
**Priority:** Medium
**Estimated time:** 2-3 hours
**Dependencies:** All previous tasks

### Description

End-to-end testing, bug fixes, documentation updates, and final polish.

### Checklist

- [ ] Test complete registration flow
- [ ] Test complete login flow
- [ ] Test password reset flow
- [ ] Test project creation wizard (all 3 steps)
- [ ] Test tier selection and enforcement
- [ ] Test app generation (Free tier)
- [ ] Test app generation (paid tier)
- [ ] Test preview display
- [ ] Test ZIP download
- [ ] Test admin login
- [ ] Test admin metrics display
- [ ] Test budget exhaustion scenario
- [ ] Test project retention cleanup
- [ ] Test concurrent user limit (Free tier)
- [ ] Run full test suite (pytest)
- [ ] Run linting (ruff)
- [ ] Run type checking (mypy)
- [ ] Update README.md
- [ ] Update API documentation
- [ ] Test on fresh database (Alembic migration)

---

## Task Dependency Graph

```
Task 1 (Auth) ──────────────┬──→ Task 7 (Frontend Auth) ──→ Task 8 (Wizard) ──→ Task 9 (Preview)
                             │
Task 2 (Tiers) ──────┬──────┤
                      │      │
Task 4 (Spec Agent) ─┤      └──→ Task 10 (Admin)
                      │
                      └──→ Task 5 (Workflow) ──→ Task 6 (Generator) ──→ Task 9 (Preview)
                      
Task 3 (Cost Tracking) ──→ Task 6 (Generator)

Task 11 (Testing) ←── All tasks
```

---

## Progress Summary

| Task | Status | Assignee | Started | Completed |
|------|--------|----------|---------|-----------|
| 1. Auth System | Completed | - | - | 2026-08-31 |
| 2. Tier System | Completed | - | - | 2026-08-31 |
| 3. Cost Tracking | Completed | - | - | 2026-08-31 |
| 4. Spec Agent | Completed | - | - | 2026-08-31 |
| 5. Workflow Integration | Completed | - | - | 2026-08-31 |
| 6. App Generator | Pending | - | - | - |
| 7. Frontend Auth | Pending | - | - | - |
| 8. Frontend Wizard | Pending | - | - | - |
| 9. Frontend Preview | Pending | - | - | - |
| 10. Admin Dashboard | Pending | - | - | - |
| 11. Testing & Polish | Pending | - | - | - |
