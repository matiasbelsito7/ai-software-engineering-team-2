# Deployment Preparation Task

Prepare the software project for deployment and operational execution.

Generate the infrastructure artifacts required to deploy the current implementation.

Do not modify the application logic.

Do not redesign the software architecture.

Focus exclusively on deployment and operational infrastructure.

---

# Objectives

Prepare a deployment solution that is:

- reproducible
- automated
- maintainable
- secure
- scalable

Prefer infrastructure-as-code whenever possible.

Avoid manual deployment procedures.

---

# Infrastructure

Generate only the infrastructure artifacts that are appropriate for the requested deployment target.

Examples include:

- Dockerfile
- docker-compose.yml
- Kubernetes manifests
- GitHub Actions workflows
- Terraform configurations
- deployment scripts
- configuration files

Do not generate unnecessary artifacts.

---

# Deployment Plan

Describe the deployment process.

Include:

- deployment sequence
- required prerequisites
- execution order
- operational considerations

Keep deployment steps concise and actionable.

---

# Best Practices

Follow current DevOps best practices.

Ensure that generated infrastructure is:

- reproducible
- deterministic
- portable
- maintainable

Prefer declarative configurations.

Avoid hardcoded values whenever possible.

---

# Validation

Verify that:

- deployment artifacts are internally consistent
- generated files match the project structure
- deployment targets match the requested environment
- configuration files do not contradict one another

Do not invent infrastructure requirements.

If deployment information is missing, explicitly state the limitation.

---

# Output

Return a valid DevOpsResult JSON document.

Include:

- deployment plan
- generated deployment artifacts
- code patches (if required)

Do not include Markdown outside the generated artifact contents.

Do not include explanations outside the JSON response.