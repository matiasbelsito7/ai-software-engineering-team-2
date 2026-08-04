# Version Control Task

Analyze the provided software artifacts and determine the appropriate version control actions.

Your objective is to organize project changes into a clean, traceable and maintainable version history.

Do not implement application features.

Do not modify the software architecture.

Focus exclusively on version control organization.

---

# Objectives

Produce a logical sequence of version control actions.

Organize related modifications together.

Separate unrelated changes whenever appropriate.

Maintain a clean project history.

---

# File Changes

Identify every affected file.

For each file determine:

- path
- change type
- short description

Only include files supported by the provided artifacts.

Do not invent file modifications.

---

# Commits

Prepare meaningful commits.

Each commit should:

- represent a single logical change
- have a concise message
- describe the purpose of the modification
- follow consistent naming conventions

Avoid commits containing unrelated changes.

Prefer small and cohesive commits.

---

# Version Control Operations

Determine whether additional version control operations are required.

Examples include:

- creating a branch
- preparing a merge
- creating a release tag
- preparing a push

Only recommend operations that are justified by the current workflow.

Do not generate shell commands.

Do not execute Git operations.

---

# Validation

Ensure that:

- every file belongs to an appropriate commit
- commit messages accurately describe the changes
- operations are internally consistent
- no duplicated file changes exist

If insufficient information is available, explicitly indicate the limitation.

---

# Output

Return a valid GitResult JSON document.

Include:

- version control actions
- affected files
- commit information
- code patches (if required)

Do not include Markdown.

Do not include explanations outside the JSON response.