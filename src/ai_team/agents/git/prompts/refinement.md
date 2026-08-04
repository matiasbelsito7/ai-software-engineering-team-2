# Version Control Refinement

Before producing the final version control plan, review every generated action.

Your objective is to improve the organization and consistency of the project history.

Do not modify the implementation.

Do not invent additional file changes.

Refine only the version control actions.

---

# File Changes

Review every reported file.

Ensure that:

- file paths are valid
- change types are correct
- descriptions accurately summarize the modification
- duplicated file changes are removed

Only include files supported by the provided artifacts.

---

# Commit Quality

Review every generated commit.

Ensure that:

- each commit represents a single logical change
- unrelated modifications are not grouped together
- commit messages are concise
- commit messages accurately describe the changes
- commit descriptions are consistent with the affected files

Prefer multiple small commits over one large mixed commit when appropriate.

---

# Version Control Operations

Review every proposed Git operation.

Ensure that:

- operations follow a logical order
- unnecessary operations are removed
- branch, merge and tagging operations are justified
- operations are internally consistent

Do not recommend operations that cannot be inferred from the provided context.

---

# Consistency

Verify consistency between:

- file changes
- commits
- Git operations
- code patches

Every file should belong to an appropriate commit.

Every commit should support the requested version control workflow.

---

# Final Validation

Before returning the result, verify that:

- every required field is present
- every enum contains a valid value
- commit messages are complete
- file paths are valid
- the JSON conforms to the GitResult schema

Return only the final GitResult JSON document.

Do not include Markdown.

Do not include explanations outside the JSON response.