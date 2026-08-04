# Deployment Refinement

Before producing the final deployment plan, review every generated infrastructure artifact.

Your objective is to improve the quality and consistency of the deployment solution.

Do not modify the application implementation.

Refine only the deployment artifacts and deployment plan.

---

# Infrastructure Validation

Review every generated artifact.

Ensure that:

- deployment targets are correct
- configuration files are internally consistent
- generated files do not contradict each other
- paths are valid
- artifact descriptions match their contents

Remove unnecessary artifacts.

Do not generate duplicate infrastructure.

---

# Deployment Plan

Review the deployment plan.

Ensure that:

- prerequisites are complete
- deployment steps follow the correct order
- every step is actionable
- operational requirements are explicit

Avoid unnecessary complexity.

Prefer simple and reproducible deployment procedures.

---

# Best Practices

Verify that the deployment solution follows modern DevOps principles.

Ensure that the infrastructure is:

- reproducible
- deterministic
- maintainable
- portable
- secure

Prefer declarative configurations whenever possible.

Avoid hardcoded secrets, credentials or environment-specific values.

---

# Consistency

Verify consistency between:

- deployment target
- generated artifacts
- deployment plan
- infrastructure descriptions

Every artifact should support the same deployment strategy.

---

# Final Validation

Before returning the result, verify that:

- every required field is present
- deployment artifacts contain valid content
- artifact paths are valid
- deployment plan is complete
- the JSON conforms to the DevOpsResult schema

Return only the final DevOpsResult JSON document.

Do not include Markdown outside the generated artifact contents.

Do not include explanations outside the JSON response.