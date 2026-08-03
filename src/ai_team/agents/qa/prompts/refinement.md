# Quality Assessment Refinement

Before producing the final result, review your entire quality assessment.

Ensure that the report is complete, objective and internally consistent.

Do not modify the implementation.

Refine only the assessment.

---

# Findings

Review every reported issue.

Ensure that:

- every issue is supported by evidence
- duplicated findings are removed
- recommendations are actionable
- severity matches the actual impact
- locations are correct whenever available

Do not report speculative problems.

---

# Suggested Test Cases

Review every proposed test case.

Ensure that each test:

- validates meaningful behavior
- has a clear objective
- contains realistic inputs
- defines an observable expected result

Remove redundant or low-value tests.

---

# Quality Evaluation

Verify that the overall quality score is consistent with the reported findings.

Avoid contradictions such as:

- very high score with many critical issues
- rejection without significant findings
- approval despite severe unresolved defects

The summary must accurately reflect the assessment.

---

# Consistency

Ensure consistency between:

- summary
- quality score
- review status
- findings
- suggested test cases

Every section should support the same overall conclusion.

---

# Final Validation

Before returning the result, verify that:

- every required field is present
- every enum contains a valid value
- the JSON conforms to the QAResult schema
- no Markdown is included
- no explanations are included outside the JSON

Return only the final QAResult JSON document.