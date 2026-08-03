# Database Design Task

Design the persistence layer for the software system.

Use the implementation plan and the approved architecture to produce a production-ready database design.

---

# Goals

Produce a normalized, maintainable and scalable schema.

The design should:

- represent business concepts accurately
- minimize duplicated information
- preserve data integrity
- support future evolution
- remain easy to understand

---

# Entities

For every entity:

- choose an appropriate name
- define its purpose
- define all columns
- choose suitable data types
- define nullable fields
- define default values when appropriate
- define primary keys
- define unique constraints

Avoid unnecessary columns.

---

# Relationships

Identify every relationship.

For each relationship define:

- source entity
- target entity
- relationship type
- foreign key

Relationship types should be one of:

- one_to_one
- one_to_many
- many_to_one
- many_to_many

---

# Constraints

Define constraints that preserve consistency.

Examples include:

- primary keys
- foreign keys
- uniqueness
- nullability

Do not introduce constraints that conflict with the business requirements.

---

# Indexes

Create indexes only when justified.

Typical reasons include:

- frequent lookups
- foreign keys
- uniqueness
- filtering
- sorting

Avoid unnecessary indexes.

---

# Normalization

Prefer a normalized schema.

Avoid:

- duplicated data
- repeated attributes
- inconsistent naming
- unnecessary denormalization

Introduce denormalization only when there is a clear performance benefit.

---

# Scalability

Design for future growth.

Prefer:

- stable identifiers
- explicit relationships
- extensible entities
- consistent naming

Avoid premature optimization.

---

# Output

Return only a valid DatabaseResult JSON document.

Do not return SQL.

Do not return ORM models.

Do not return Markdown.

Do not include explanations outside the JSON document.