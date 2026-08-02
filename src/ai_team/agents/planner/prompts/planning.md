# Planning Task

Your task is to transform the user's request into a complete execution plan.

Carefully analyze the request before creating any tasks.

Do not start by decomposing the problem immediately.

Instead, follow this reasoning process.

---

## Step 1 — Understand the Objective

Determine:

- The primary goal.
- The expected final outcome.
- Any implicit requirements.
- Any engineering assumptions that must be made.

If information is missing, make reasonable assumptions instead of leaving gaps.

---

## Step 2 — Identify Work

Identify every major engineering activity required.

Examples include:

- Architecture
- Backend development
- Frontend development
- Database design
- Testing
- Documentation
- DevOps
- Repository management

Do not omit supporting work.

---

## Step 3 — Decompose Work

Break every activity into small executable tasks.

Each task must:

- Have one clear objective.
- Be executable by exactly one agent.
- Produce a concrete deliverable.
- Avoid combining unrelated work.

---

## Step 4 — Assign Ownership

Assign each task to exactly one capability.

Allowed capabilities are:

- ARCHITECTURE
- BACKEND
- FRONTEND
- DATABASE
- REVIEW
- QA
- DOCUMENTATION
- DEVOPS
- GIT

Never assign multiple owners.

---

## Step 5 — Determine Dependencies

Identify which tasks depend on previous work.

Only create dependencies when they are technically necessary.

Avoid unnecessary sequential execution.

Prefer parallel work whenever possible.

---

## Step 6 — Organize into Phases

Group tasks into execution phases.

Tasks within the same phase should be executable concurrently.

Different phases should represent dependency boundaries.

---

## Step 7 — Estimate

For each task estimate:

- approximate token usage
- approximate execution cost (if possible)

Provide conservative estimates.

---

## Step 8 — Validate the Plan

Before returning the result verify:

- Every task has an owner.
- Every dependency is valid.
- No dependency cycles exist.
- No duplicated tasks exist.
- The plan is complete.
- The execution order is coherent.
- Parallel execution has been maximized.

---

## Step 9 — Optimize

Review the execution plan one final time.

Reduce unnecessary tasks.

Merge tasks only when they belong to the same capability and objective.

Increase parallelism whenever possible.

Reduce estimated execution cost without sacrificing quality.

Prefer deterministic execution over overly complex workflows.

---


## Output

Return only a valid ExecutionPlan JSON document.

Do not include explanations.

Do not include Markdown.

Do not include comments.

Do not include any text outside the JSON.