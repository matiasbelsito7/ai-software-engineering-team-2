# Backend Implementation Task

Implement the requested backend functionality.

Follow the approved execution plan and software architecture.

Do not redesign the system.

Implement only the requested functionality.

---

## Step 1 — Understand the Task

Before writing code:

- identify the requested functionality
- identify affected modules
- identify affected files
- identify required dependencies

Do not assume missing requirements.

---

## Step 2 — Analyze Existing Code

Before modifying the project:

- inspect existing implementations
- reuse existing abstractions
- preserve project conventions
- avoid duplicate implementations

Prefer extending existing code over creating new code.

---

## Step 3 — Plan the Changes

Determine the minimal set of changes required.

Possible operations include:

- creating files
- modifying files
- deleting obsolete files

Every change must have a clear purpose.

---

## Step 4 — Implement

Generate production-ready code.

The implementation must be:

- correct
- readable
- maintainable
- type-safe
- modular

Follow the project's architecture and coding conventions.

---

## Step 5 — Validate

Before returning the result verify:

- imports are correct
- dependencies are satisfied
- naming is consistent
- no duplicated logic exists
- no dead code exists
- no unrelated files were modified

---

## Step 6 — Produce Code Patches

Represent every modification as a CodePatch.

Each patch must include:

- target file
- operation
- content (when applicable)
- reason

Only include files that actually changed.

---

## Output

Return only a valid BackendResult JSON document.

Do not return Markdown.

Do not include explanations.

Do not include comments outside the JSON document.