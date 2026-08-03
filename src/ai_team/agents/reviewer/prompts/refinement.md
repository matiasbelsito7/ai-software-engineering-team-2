# Review Refinement Task

You are given an existing code review.

Your task is to improve the quality of the review without changing its intent.

Do not review the code again from scratch.

Instead, refine the existing review.

---

# Refinement Goals

Improve the review by:

- removing duplicated findings
- removing unsupported findings
- improving technical accuracy
- improving clarity
- improving consistency
- improving actionability
- improving severity classification

Preserve valid findings.

---

# Validate Findings

For every finding verify:

- the issue actually exists
- the description is technically correct
- the severity is appropriate
- the suggested improvement is actionable
- the issue is not duplicated

Remove findings that cannot be justified.

---

# Validate Severity

Ensure that:

- INFO is used for observations
- LOW is used for minor improvements
- MEDIUM is used for maintainability issues
- HIGH is used for significant correctness or security issues
- CRITICAL is reserved for severe defects

Avoid exaggerated severity.

---

# Validate Suggestions

Every suggestion should:

- be technically correct
- be specific
- be practical
- preserve the approved architecture
- avoid unnecessary refactoring

Do not recommend speculative improvements.

---

# Final Review

Before returning the result verify:

- no duplicated findings remain
- no unsupported findings remain
- all findings are technically justified
- approval status is consistent with the findings
- review score matches the review quality

---

# Output

Return only a valid ReviewerResult JSON document.

Do not return Markdown.

Do not return explanations.

Do not include comments outside the JSON document.