# Architecture Design Task

Your task is to design a complete technical architecture for the given software project.

Analyze the requirements carefully before making any architectural decisions.

Do not start by selecting technologies.

Start by understanding the problem.

---

## Step 1 — Analyze Requirements

Identify:

- Functional requirements
- Non-functional requirements
- Constraints
- Scalability expectations
- Security requirements
- Performance requirements
- Integration requirements

Separate confirmed requirements from assumptions.

---

## Step 2 — Define the Architecture

Select the most appropriate architecture style.

Examples include:

- Clean Architecture
- Hexagonal Architecture
- Layered Architecture
- Event-Driven Architecture
- Microservices
- Modular Monolith

Choose the simplest architecture capable of satisfying the requirements.

Avoid unnecessary complexity.

---

## Step 3 — Identify Modules

Define every major software module.

For each module specify:

- name
- responsibilities
- dependencies

Modules should have:

- high cohesion
- low coupling
- explicit responsibilities

Avoid overlapping responsibilities.

---

## Step 4 — Define Interfaces

Identify the public interfaces between modules.

Every interface should have:

- owner
- purpose
- responsibilities

Keep interfaces minimal and stable.

---

## Step 5 — Evaluate Alternatives

Before making important architectural decisions:

- identify reasonable alternatives
- compare their advantages
- compare their disadvantages
- justify the selected solution

Do not choose technologies arbitrarily.

---

## Step 6 — Record Architectural Decisions

For every important decision provide:

- decision
- rationale
- consequences

Architectural decisions must be technically justified.

---

## Step 7 — Identify Risks

Identify:

- technical risks
- scalability risks
- operational risks
- maintenance risks

Suggest mitigations whenever appropriate.

---

## Step 8 — Validate the Architecture

Before returning the result verify:

- every module has a clear responsibility
- dependencies are coherent
- interfaces are consistent
- responsibilities do not overlap
- the architecture satisfies the requirements
- unnecessary complexity has been avoided

---

## Output

Return only a valid ArchitectureDesign JSON document.

Do not include Markdown.

Do not include explanations.

Do not include comments.

Do not include text outside the JSON document.