# Documentation Generation Task

Generate technical documentation for the provided software artifacts.

Your objective is to produce documentation that accurately describes the current implementation.

Do not modify the implementation.

Do not invent missing functionality.

Document only what can be supported by the provided information.

---

# Documentation Goals

Generate documentation that is:

- technically accurate
- complete
- concise
- well structured
- internally consistent
- easy to maintain

The documentation should help engineers understand the project without reading the entire source code.

---

# Content

Depending on the requested document type, include the appropriate sections.

Examples include:

- project overview
- architecture
- design decisions
- API documentation
- database schema
- deployment
- configuration
- usage examples
- limitations
- future improvements

Avoid including irrelevant sections.

Generate only the sections appropriate for the requested document.

---

# Style

Use professional technical language.

Prefer short paragraphs.

Use descriptive headings.

Avoid repetition.

Avoid marketing language.

Do not speculate.

If information is unavailable, explicitly state that the information is not available.

---

# Consistency

Ensure that:

- terminology is consistent
- component names match the implementation
- APIs match the implementation
- database entities match the schema
- architectural descriptions match the architecture

Never contradict the provided artifacts.

---

# Output

Generate one or more documentation files.

Each generated file should contain:

- document type
- path
- description
- content

Return only a valid DocumentationResult JSON document.

Do not include Markdown outside the generated document contents.

Do not include explanations outside the JSON response.