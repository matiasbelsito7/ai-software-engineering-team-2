# Database Refinement

Before producing the final result, review the entire database design.

Improve the schema whenever necessary while preserving the original business requirements.

---

# Consistency

Verify that:

- entity names are consistent
- column names follow the same convention
- data types are coherent
- identifiers are stable
- relationships are correctly represented

Remove duplicated or conflicting definitions.

---

# Integrity

Ensure that the schema preserves data integrity.

Review:

- primary keys
- foreign keys
- uniqueness constraints
- nullable fields
- default values

Avoid invalid or ambiguous designs.

---

# Relationships

Verify that every relationship:

- references existing entities
- references existing columns
- uses the correct cardinality
- contains an appropriate foreign key

Avoid circular dependencies unless they are explicitly required.

---

# Performance

Review the proposed indexes.

Ensure that:

- important queries are supported
- unnecessary indexes are removed
- duplicated indexes are avoided

Do not optimize prematurely.

---

# Normalization

Verify that the schema:

- minimizes duplicated information
- avoids update anomalies
- avoids insertion anomalies
- avoids deletion anomalies

Only introduce denormalization when it is clearly justified.

---

# Scalability

Review whether the schema can evolve without major redesign.

Prefer:

- stable identifiers
- extensible entities
- explicit relationships
- maintainable structures

---

# Final Validation

Before returning the result, verify that:

- every entity is valid
- every relationship is valid
- every foreign key references an existing entity
- every index references existing columns
- every required field is present
- the output conforms to the expected DatabaseResult schema

Return only the final JSON document.

Do not include explanations.

Do not include Markdown.

Do not include SQL.