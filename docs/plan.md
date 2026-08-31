# Implementation Plan

## Overview

This plan details the implementation of the AI Software Engineering Team's new features:
- User authentication system
- Tier-based monetization
- Spec Agent for technical specification generation
- Non-technical user experience (wizard, preview, download)
- Admin dashboard

---

## Phase 1: Authentication System

**Goal:** Enable user registration, login, and JWT-based authentication.

**Estimated time:** 2-3 hours

### Files to Create

| File | Purpose |
|------|---------|
| `src/ai_team/domain/models/user.py` | ORM User model |
| `src/ai_team/domain/schemas/auth.py` | Pydantic schemas for auth |
| `src/ai_team/domain/services/auth_service.py` | Auth business logic |
| `src/ai_team/app/api/routers/auth.py` | Auth API endpoints |
| `src/ai_team/app/api/dependencies.py` | `get_current_user` dependency |

### Files to Modify

| File | Changes |
|------|---------|
| `src/ai_team/infrastructure/config/security.py` | Add JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION |
| `pyproject.toml` | Add python-jose, passlib, python-multipart |

### User Model

```python
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")  # "user" | "admin"
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
```

### API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | None | Create account |
| POST | `/api/v1/auth/login` | None | Get JWT tokens |
| POST | `/api/v1/auth/refresh` | Refresh token | Refresh access token |
| GET | `/api/v1/auth/me` | Bearer | Get profile |
| PUT | `/api/v1/auth/me` | Bearer | Update profile |
| POST | `/api/v1/auth/forgot-password` | None | Request reset |
| POST | `/api/v1/auth/reset-password` | Reset token | Set new password |

### Dependencies

```
python-jose[cryptography]  # JWT
passlib[bcrypt]            # Password hashing
python-multipart           # Form data
```

---

## Phase 2: Tier System

**Goal:** Define tiers, create Project model, enforce limits.

**Estimated time:** 1-2 hours

### Files to Create

| File | Purpose |
|------|---------|
| `src/ai_team/domain/models/project.py` | ORM Project model |
| `src/ai_team/domain/models/tier.py` | Tier configuration |
| `src/ai_team/domain/schemas/project.py` | Project schemas |
| `src/ai_team/domain/services/project_service.py` | Project business logic |
| `src/ai_team/app/api/routers/projects.py` | Project API endpoints |

### Tier Configuration

```python
class TierConfig:
    FREE = {
        "name": "Empieza Gratis",
        "price": 0,
        "tokens_per_project": 50_000,
        "max_iterations": 2,
        "max_projects": 3,
        "retention_days": 30,
        "can_download_code": False,
    }
    STARTER = {
        "name": "App Personal",
        "price": 9.99,
        "tokens_per_project": 200_000,
        "max_iterations": 5,
        "max_projects": 10,
        "retention_days": 180,
        "can_download_code": True,
    }
    PRO = {
        "name": "App Profesional",
        "price": 29.99,
        "tokens_per_project": 1_000_000,
        "max_iterations": 15,
        "max_projects": 50,
        "retention_days": 365,
        "can_download_code": True,
    }
    BUSINESS = {
        "name": "App de Negocio",
        "price": 79.99,
        "tokens_per_project": 3_000_000,
        "max_iterations": 30,
        "max_projects": -1,  # unlimited
        "retention_days": 730,
        "can_download_code": True,
    }
```

### Project Model

```python
class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    description: Mapped[str]  # user's natural language description
    tier: Mapped[str] = mapped_column(default="free")
    tokens_used: Mapped[int] = mapped_column(default=0)
    iterations_used: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(default="pending")  # pending|running|completed|failed
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    expires_at: Mapped[datetime]  # based on tier retention
    files_path: Mapped[str | None]  # path to generated files
```

---

## Phase 3: Cost Tracking Integration

**Goal:** Connect cost tracking to workflow, enforce budget limits.

**Estimated time:** 1-2 hours

### Files to Modify

| File | Changes |
|------|---------|
| `src/ai_team/observability/costs.py` | Add budget enforcement |
| `src/ai_team/observability/manager.py` | Connect with tier limits |
| `src/ai_team/agents/base.py` | Call `record_llm_call()` after each LLM call |
| `src/ai_team/graph/builder.py` | Check budget before each node |

### Budget Flow

```
Before each agent node:
  1. Check remaining_tokens = tier_budget - tokens_used
  2. If remaining_tokens <= 0:
     - Stop workflow
     - Set status = "budget_exceeded"
     - Notify user
  3. Execute agent
  4. Record tokens used
  5. Update project.tokens_used
```

### Cost Recording Fix

In `BaseAgent.generate()` (line ~216), after `self.llm.generate()`:

```python
# Add after LLM call
if self.observations and response.token_usage:
    call = LLMCall(
        execution_id=execution.execution_id,
        agent=execution.capability.value,
        provider=response.provider,
        model=response.model,
        prompt_tokens=response.token_usage.prompt_tokens,
        completion_tokens=response.token_usage.completion_tokens,
        latency_ms=response.latency_ms,
    )
    await self.observations.record_llm_call(call)
```

---

## Phase 4: Spec Agent

**Goal:** Create agent that generates technical specification from natural language.

**Estimated time:** 2-3 hours

### Files to Create

| File | Purpose |
|------|---------|
| `src/ai_team/agents/spec/__init__.py` | Module export |
| `src/ai_team/agents/spec/agent.py` | SpecAgent class |
| `src/ai_team/agents/spec/models.py` | Output models |
| `src/ai_team/agents/spec/prompt_builder.py` | Prompt construction |
| `src/ai_team/agents/spec/prompts/system.md` | System prompt |
| `src/ai_team/agents/spec/prompts/generate_spec.md` | Spec generation template |

### Output Model

```python
class AppSpecification(BaseModel):
    app_name: str
    description: str
    tech_stack: TechStack
    components: list[AppComponent]
    features: list[Feature]
    database_schema: DatabaseSchema
    api_endpoints: list[Endpoint]
    authentication: AuthRequirements
    deployment: DeploymentConfig

class TechStack(BaseModel):
    frontend: str  # "React + TypeScript"
    backend: str   # "FastAPI + Python"
    database: str  # "PostgreSQL"

class AppComponent(BaseModel):
    name: str
    type: str  # "page" | "form" | "modal" | "component"
    description: str
    fields: list[Field] | None

class Feature(BaseModel):
    name: str
    description: str
    requires_auth: bool
    endpoints: list[str]

class DatabaseSchema(BaseModel):
    tables: list[Table]

class Table(BaseModel):
    name: str
    columns: list[Column]
    relationships: list[Relationship]

class Endpoint(BaseModel):
    method: str
    path: str
    description: str
    requires_auth: bool
    request_body: dict | None
    response_body: dict | None
```

---

## Phase 5: Workflow Integration

**Goal:** Add Spec Agent to workflow, connect tier config to state.

**Estimated time:** 1 hour

### Files to Modify

| File | Changes |
|------|---------|
| `src/ai_team/graph/builder.py` | Add Spec node before Planner |
| `src/ai_team/graph/state.py` | Add specification, project_id, tier_config |
| `src/ai_team/graph/workflow.py` | Update routing logic |

### Updated Workflow

```
START → spec → planner → architect → backend → frontend → reviewer
                                                            │
                                             approved ──────┤
                                                            ├──→ qa
                                             not approved ──┤
                                                            │
                                                            └──→ backend (loop)
                                                                   │
                                             qa passed ───────────┤
                                                                   ├──→ documentation → devops → git → END
                                             qa failed ───────────┤
                                                                   │
                                                                   └──→ backend (loop)
```

### State Additions

```python
class GraphState(BaseModel):
    # ... existing fields ...
    specification: AppSpecification | None = None
    project_id: str | None = None
    tier_config: dict | None = None
    tokens_used: int = 0
    tokens_budget: int = 0
```

---

## Phase 6: App Generator Service

**Goal:** Orchestrate spec generation → workflow → final output.

**Estimated time:** 2 hours

### Files to Create

| File | Purpose |
|------|---------|
| `src/ai_team/domain/services/app_generator.py` | Main orchestration |
| `src/ai_team/domain/services/app_preview.py` | Generate preview HTML |
| `src/ai_team/domain/services/app_packager.py` | Create ZIP package |

### AppGenerator Flow

```python
class AppGenerator:
    async def generate(self, project_id: str, user_description: str) -> GenerationResult:
        # 1. Load project and tier config
        project = await self.project_service.get(project_id)
        tier = TierConfig.get(project.tier)
        
        # 2. Execute workflow
        initial_state = {
            "conversation": {"user_request": user_description},
            "project_id": project_id,
            "tier_config": tier,
            "tokens_budget": tier["tokens_per_project"],
        }
        
        final_state = await self.graph.ainvoke(initial_state)
        
        # 3. Extract generated files
        files = final_state["artifacts"]["shared_files"]
        
        # 4. Save to disk
        await self.save_files(project_id, files)
        
        # 5. Generate preview
        preview_html = await self.preview_generator.generate(files)
        
        # 6. Return result
        return GenerationResult(
            project_id=project_id,
            files_count=len(files),
            tokens_used=final_state["tokens_used"],
            preview_html=preview_html,
        )
```

---

## Phase 7: Frontend Auth

**Goal:** Login, Register, and Protected Routes.

**Estimated time:** 2 hours

### Files to Create

| File | Purpose |
|------|---------|
| `frontend/src/pages/Login.tsx` | Login page |
| `frontend/src/pages/Register.tsx` | Registration page |
| `frontend/src/contexts/AuthContext.tsx` | Auth state management |
| `frontend/src/components/ProtectedRoute.tsx` | Route guard |
| `frontend/src/services/api.ts` | API client with JWT |

### Auth Flow

```
1. User opens app → check localStorage for token
2. If no token → redirect to /login
3. User submits credentials → POST /auth/login
4. Store tokens in HTTP-only cookies
5. All API requests include Authorization: Bearer <token>
6. On 401 → redirect to /login
```

---

## Phase 8: Frontend Wizard + Dashboard

**Goal:** 3-step wizard and project dashboard.

**Estimated time:** 2-3 hours

### Files to Create

| File | Purpose |
|------|---------|
| `frontend/src/pages/Dashboard.tsx` | Project list |
| `frontend/src/pages/Wizard.tsx` | 3-step creation wizard |
| `frontend/src/components/AppCard.tsx` | Project card |
| `frontend/src/components/TierSelector.tsx` | Tier selection |

### Wizard Steps

```
Step 1: Describe Your App
  - Textarea: "Describe tu app en palabras simples"
  - Character limit: 2000
  - Example: "Quiero una app de tareas con login..."

Step 2: Choose Your Plan
  - Tier cards: Free | Starter | Pro | Business
  - Show: price, tokens, iterations, features
  - Highlight recommended tier

Step 3: Confirm & Generate
  - Summary: description, tier, estimated time
  - "Tu app tomará ~3 minutos y usará ~180K tokens"
  - [Generar] button
```

---

## Phase 9: Frontend Preview + Download

**Goal:** Preview generated app and download as ZIP.

**Estimated time:** 2 hours

### Files to Create

| File | Purpose |
|------|---------|
| `frontend/src/pages/Preview.tsx` | App preview page |
| `frontend/src/components/AppPreviewFrame.tsx` | iframe wrapper |

### Preview Page

```
┌─────────────────────────────────────────────────┐
│  Tu App: [App Name]                             │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │                                           │  │
│  │         Generated App Preview             │  │
│  │            (iframe)                       │  │
│  │                                           │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  [Descargar Código] [Crear Otra App] [Eliminar] │
│                                                 │
│  Tier: Free                                     │
│  Para descargar, actualiza a Starter ($9.99)    │
└─────────────────────────────────────────────────┘
```

---

## Phase 10: Admin Dashboard

**Goal:** Admin metrics and user management.

**Estimated time:** 2 hours

### Files to Create

| File | Purpose |
|------|---------|
| `frontend/src/pages/admin/AdminDashboard.tsx` | Metrics overview |
| `frontend/src/pages/admin/UserManagement.tsx` | User list |
| `frontend/src/pages/admin/ProjectMonitoring.tsx` | Project list |
| `src/ai_team/app/api/routers/admin.py` | Admin API endpoints |

### Admin Dashboard

```
┌─────────────────────────────────────────────────┐
│  Admin Dashboard                                │
│                                                 │
│  Users: 150  |  Projects: 320  |  Revenue: $1,670│
│                                                 │
│  Tokens Usage by Tier:                          │
│  ████ Free: 2.1M                                │
│  ████████ Starter: 5.8M                         │
│  ██████████ Pro: 3.2M                           │
│  ██ Business: 0.4M                              │
│                                                 │
│  Recent Projects:                               │
│  - "Task App" by user@email.com (completed)     │
│  - "E-commerce" by admin@test.com (running)     │
└─────────────────────────────────────────────────┘
```

---

## Phase 11: Testing & Polish

**Goal:** End-to-end testing, bug fixes, documentation.

**Estimated time:** 2-3 hours

### Checklist

- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test password reset
- [ ] Test project creation wizard
- [ ] Test tier selection
- [ ] Test app generation
- [ ] Test preview display
- [ ] Test ZIP download
- [ ] Test admin login
- [ ] Test admin metrics
- [ ] Test budget enforcement
- [ ] Test project retention cleanup
- [ ] Update README.md
- [ ] Update API documentation

---

## Summary

| Phase | Description | Est. Time |
|-------|-------------|-----------|
| 1 | Auth System | 2-3h |
| 2 | Tier System | 1-2h |
| 3 | Cost Tracking Integration | 1-2h |
| 4 | Spec Agent | 2-3h |
| 5 | Workflow Integration | 1h |
| 6 | App Generator Service | 2h |
| 7 | Frontend Auth | 2h |
| 8 | Frontend Wizard + Dashboard | 2-3h |
| 9 | Frontend Preview + Download | 2h |
| 10 | Admin Dashboard | 2h |
| 11 | Testing & Polish | 2-3h |
| **Total** | | **20-25h** |
