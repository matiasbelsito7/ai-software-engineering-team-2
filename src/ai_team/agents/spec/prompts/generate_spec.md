# Specification Generation Task

Your task is to transform the user's natural language description into a complete technical specification.

Carefully analyze the description before creating any specification components.

Do not rush to list features immediately.

Instead, follow this reasoning process.

---

## Step 1 — Understand the Application

Determine:

- The primary purpose of the application.
- Who the target users are.
- The core problem it solves.
- Any implicit requirements.

If information is missing, make reasonable assumptions instead of leaving gaps.

---

## Step 2 — Define Tech Stack

Choose appropriate technologies:

- Frontend framework and language
- Backend framework and language
- Database system
- CSS/styling framework
- Any additional services

Use the default stack unless the user specifies otherwise.

---

## Step 3 — Identify Components

List every UI component and page the application needs.

For each component, specify:

- A clear, PascalCase name
- The type (page, form, modal, card, layout, nav, table)
- What it does
- What fields it displays or collects
- What actions the user can take

Think about:

- Navigation (header, sidebar, footer)
- Authentication pages (login, register, forgot password)
- Main application pages
- Forms and modals
- Data display components (cards, tables, lists)

---

## Step 4 — Define Features

List every business feature the application supports.

For each feature, specify:

- A clear, snake_case name
- What it does
- Priority (critical, high, medium, low)
- Whether it requires authentication
- Which components are involved

Group related functionality into features.

---

## Step 5 — Design Database Schema

Design the database models needed.

For each model:

- Choose a singular, PascalCase name
- Describe what it represents
- List all fields with types
- Identify primary keys, unique fields, and indexed fields
- Describe relationships to other models

Include enums for status fields and categorical data.

Common patterns:

- User model (if auth is required)
- Core domain models
- Join tables for many-to-many relationships

---

## Step 6 — Specify API Endpoints

Define all API endpoints.

For each endpoint:

- HTTP method (GET, POST, PUT, PATCH, DELETE)
- Path (use RESTful conventions)
- Description
- Request body fields (for POST/PUT/PATCH)
- Response body fields
- Whether authentication is required

Follow RESTful conventions:

- GET /resource — list
- GET /resource/{id} — detail
- POST /resource — create
- PUT /resource/{id} — update
- PATCH /resource/{id} — partial update
- DELETE /resource/{id} — delete

---

## Step 7 — Determine Authentication

If the application requires authentication:

- Choose the auth method (JWT, session, OAuth2)
- Define user roles
- List auth features (registration, login, password reset, email verification)
- Identify which endpoints and components require auth

---

## Step 8 — Configure Deployment

Specify deployment requirements:

- Target platform
- Required environment variables
- External services needed

---

## Step 9 — Estimate Complexity

Based on the specification:

- Count the approximate number of files to generate
- Assess complexity: low (simple CRUD), medium (multi-feature), high (complex business logic)

---

## Step 10 — Validate the Specification

Before returning the result, verify:

- All fields in AppSpecification are populated.
- Components align with features.
- API endpoints cover all features.
- Database models support all endpoints.
- Authentication is consistent across endpoints.
- No orphaned components or features.
- The specification is realistic for a single generation session.

---

## Output

Return only a valid AppSpecification JSON document.

Do not include explanations.

Do not include Markdown.

Do not include comments.

Do not include any text outside the JSON.
