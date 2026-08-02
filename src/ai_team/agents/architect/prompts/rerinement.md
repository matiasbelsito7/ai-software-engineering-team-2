# Architecture Refinement Task

You are given an existing ArchitectureDesign.

Your task is to improve the architecture without changing the project's objectives or introducing unnecessary redesign.

Preserve valid architectural decisions whenever possible.

Modify only what is necessary.

---

## Refinement Goals

Improve the architecture by:

- clarifying module responsibilities
- reducing coupling
- increasing cohesion
- improving scalability
- improving maintainability
- improving testability
- improving observability
- improving extensibility
- reducing unnecessary complexity
- improving architectural consistency

---

## Preserve

Keep unchanged whenever possible:

- valid architectural decisions
- correct module boundaries
- well-defined interfaces
- justified technology choices
- proven design patterns

Avoid unnecessary redesign.

---

## Review Module Design

Verify that:

- every module has a single responsibility
- responsibilities do not overlap
- dependencies are explicit
- coupling is minimized
- cohesion is maximized

Refactor module boundaries only when justified.

---

## Review Interfaces

Verify that:

- interfaces are minimal
- interfaces are stable
- ownership is clear
- responsibilities are explicit

Avoid unnecessary public APIs.

---

## Review Architectural Decisions

For every architectural decision:

- verify it is still justified
- verify it satisfies the project requirements
- verify the rationale remains valid

Update decisions only when there is a clear technical benefit.

---

## Review Quality Attributes

Evaluate whether the architecture satisfies:

- Maintainability
- Scalability
- Performance
- Reliability
- Availability
- Security
- Testability
- Observability
- Extensibility

Identify trade-offs where appropriate.

---

## Identify Risks

Review:

- technical risks
- scalability risks
- operational risks
- maintenance risks

Suggest mitigations whenever appropriate.

---

## Validate

Before returning the refined architecture verify:

- every module has a clear responsibility
- interfaces are consistent
- dependencies are coherent
- architectural decisions remain justified
- unnecessary complexity has been removed
- the architecture satisfies all known requirements

---

## Output

Return only a valid ArchitectureDesign JSON document.

Do not include Markdown.

Do not include explanations.

Do not include comments.

Do not include text outside the JSON document.