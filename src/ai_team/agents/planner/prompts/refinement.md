# Plan Refinement Task

You are given an existing ExecutionPlan.

Your task is to improve it without changing its objective.

Preserve every valid part of the plan and modify only what is necessary.

---

## Refinement Goals

Improve the execution plan by:

- fixing missing tasks
- removing duplicated work
- correcting invalid dependencies
- improving task decomposition
- increasing parallel execution
- reducing execution cost
- reducing estimated token usage
- improving execution order
- improving task descriptions
- improving ownership assignment

Do not redesign the plan unless it is clearly incorrect.

---

## Preserve

Keep unchanged whenever possible:

- the original objective
- valid tasks
- correct dependencies
- correct execution phases
- existing engineering decisions

Avoid unnecessary modifications.

---

## Validate

Before producing the refined plan verify:

- every task has exactly one owner
- every dependency exists
- there are no circular dependencies
- no duplicated tasks exist
- every phase is executable
- every task belongs to a valid capability
- the plan is complete
- the execution order is coherent

---

## Optimize

Optimize for:

- minimal execution time
- maximum safe parallelism
- minimal LLM cost
- minimal token consumption
- deterministic execution
- maintainability

Never sacrifice correctness for optimization.

---

## Constraints

Never invent capabilities.

Use only the capabilities supported by the system.

Do not remove tasks that are required to satisfy the user's objective.

Do not merge unrelated tasks.

Do not introduce ambiguity.

---

## Output

Return a complete ExecutionPlan.

Return only valid JSON.

Do not include Markdown.

Do not include explanations.

Do not include comments.

Do not include text outside the JSON document.