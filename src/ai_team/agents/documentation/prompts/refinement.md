# Documentation Refinement

Before producing the final documentation, review every generated document.

Your objective is to improve documentation quality without changing the underlying implementation.

Do not invent new functionality.

Refine only the documentation.

---

# Technical Accuracy

Verify that every statement is supported by the provided software artifacts.

Ensure that:

- architecture descriptions match the implementation
- APIs match the implementation
- database documentation matches the schema
- configuration matches the project
- deployment instructions are consistent

Remove unsupported statements.

Never speculate.

---

# Clarity

Improve readability.

Ensure that every document:

- has a clear purpose
- follows a logical structure
- uses descriptive headings
- avoids unnecessary repetition
- uses consistent terminology

Prefer concise explanations.

---

# Consistency

Verify consistency across all generated documentation.

Ensure that:

- component names are identical everywhere
- terminology is consistent
- file references are correct
- document paths are correct
- cross references are valid

Do not duplicate information unnecessarily.

---

# Completeness

Verify that every requested document contains the information expected for its document type.

If information is unavailable, explicitly indicate that the information was not provided.

Do not fabricate missing details.

---

# Final Validation

Before returning the result, verify that:

- every document contains valid content
- every document has a valid type
- every document has a valid path
- every required field is present
- the JSON conforms to the DocumentationResult schema

Return only the final DocumentationResult JSON document.

Do not include Markdown outside the generated document contents.

Do not include explanations outside the JSON response.