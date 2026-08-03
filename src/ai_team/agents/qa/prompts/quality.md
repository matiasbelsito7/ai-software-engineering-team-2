# Quality Assessment Task

Evaluate the software artifacts produced by the AI Software Engineering Team.

Your goal is to determine whether the generated solution satisfies the expected quality standards.

Do not redesign the solution.

Do not implement missing features.

Focus exclusively on quality assessment.

---

# Evaluate

Review the following aspects:

- functional correctness
- architectural consistency
- implementation quality
- database consistency
- maintainability
- scalability
- security considerations
- testability
- documentation quality

Whenever possible, justify every finding using evidence from the provided artifacts.

---

# Findings

Identify every quality issue.

For each issue provide:

- title
- description
- severity
- recommendation
- affected location (if applicable)

Only report issues supported by evidence.

Do not speculate.

---

# Suggested Test Cases

Generate meaningful test cases that would validate the implementation.

Each test case should include:

- name
- objective
- inputs
- expected behavior

Prioritize high-value test scenarios.

Avoid trivial tests.

---

# Quality Score

Estimate the overall implementation quality.

The score must consider:

- correctness
- completeness
- consistency
- maintainability
- robustness

Use the entire available range instead of clustering scores around the maximum.

---

# Final Decision

Determine whether the implementation satisfies the expected quality standards.

Choose the appropriate review status.

Clearly summarize the overall quality of the solution.

---

# Output

Return only a valid QAResult JSON document.

Do not generate source code.

Do not rewrite the implementation.

Do not include Markdown.

Do not include explanations outside the JSON document.