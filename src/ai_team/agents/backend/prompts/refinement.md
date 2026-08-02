# Backend Refinement Task

You are given an existing backend implementation.

Your task is to improve the implementation while preserving the intended functionality and approved architecture.

Do not redesign the system.

Modify only what is necessary.

---

## Refinement Goals

Improve the implementation by:

- increasing readability
- improving maintainability
- improving modularity
- improving type safety
- improving testability
- reducing code duplication
- simplifying complex logic
- improving consistency
- removing dead code

Preserve the existing behavior.

---

## Review Existing Code

Before making changes:

- understand the existing implementation
- identify unnecessary complexity
- identify duplicated logic
- identify inconsistent patterns
- identify potential bugs

Avoid unnecessary rewrites.

---

## Validate Architecture

Verify that the implementation:

- follows the approved architecture
- respects module boundaries
- preserves public APIs
- maintains dependency direction
- follows project conventions

Do not introduce architectural changes.

---

## Improve Code Quality

Ensure the implementation:

- follows SOLID principles
- follows DRY
- follows KISS
- uses clear naming
- has appropriate error handling
- avoids unnecessary abstractions

Prefer small, focused improvements.

---

## Validate Dependencies

Before introducing or modifying dependencies:

- verify they are necessary
- reuse existing libraries whenever possible
- avoid redundant dependencies

---

## Validate the Result

Before returning the response verify:

- functionality is preserved
- no unrelated files were modified
- imports are correct
- type consistency is maintained
- no dead code remains
- no duplicated logic remains

---

## Produce Code Patches

Represent every modification as a CodePatch.

Each patch must include:

- target file
- operation
- content (when applicable)
- reason

Return only the patches required to perform the refinement.

---

## Output

Return only a valid BackendResult JSON document.

Do not return Markdown.

Do not return explanations.

Do not include comments outside the JSON document.