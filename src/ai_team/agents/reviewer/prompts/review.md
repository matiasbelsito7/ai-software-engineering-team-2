# Review Task

Review the provided software artifacts.

Evaluate them against the approved architecture, engineering principles and project conventions.

Do not redesign the implementation.

Do not implement code.

Only identify issues supported by technical evidence.

---

# Step 1 — Understand the Context

Before reviewing:

- understand the requested functionality
- understand the approved architecture
- understand the implementation
- identify the affected files

Do not assume missing context.

---

# Step 2 — Validate Correctness

Verify:

- requirements are implemented
- implementation is logically correct
- edge cases are handled
- exceptions are handled
- APIs are used correctly
- types are consistent

---

# Step 3 — Review Architecture

Verify that the implementation:

- follows the approved architecture
- respects module boundaries
- follows dependency direction
- preserves separation of concerns

Only report architectural issues when technically justified.

---

# Step 4 — Review Code Quality

Inspect:

- readability
- naming
- duplication
- complexity
- maintainability
- modularity
- dead code
- unnecessary abstractions
- consistency

---

# Step 5 — Review Security

Inspect for:

- input validation
- secret exposure
- injection vulnerabilities
- insecure defaults
- authorization issues
- authentication issues

Only report realistic security issues.

---

# Step 6 — Review Performance

Inspect for:

- inefficient algorithms
- unnecessary allocations
- repeated work
- unnecessary I/O
- redundant database queries
- scalability concerns

Avoid premature optimization recommendations.

---

# Step 7 — Review Dependencies

Verify:

- unnecessary dependencies
- duplicated dependencies
- outdated usage patterns
- dependency misuse

---

# Step 8 — Produce Findings

For every issue:

- describe the problem
- explain why it is a problem
- assign an appropriate severity
- identify the affected file
- provide a concrete suggestion

Never report duplicate findings.

Do not invent problems.

---

# Final Evaluation

Determine whether the implementation should be approved.

Approval should consider:

- correctness
- maintainability
- security
- architecture
- overall software quality

---

# Output

Return only a valid ReviewerResult JSON document.

Represent every issue as a ReviewIssue.

Do not return Markdown.

Do not return explanations outside the JSON document.