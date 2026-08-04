# Frontend Refinement

Before producing the final frontend implementation, review every generated UI artifact.

Your objective is to improve the quality, consistency and usability of the interface.

Do not modify backend logic.

Do not redesign the software architecture.

Refine only the frontend implementation.

---

# UI Components

Review every generated component.

Ensure that:

- each component has a single responsibility
- reusable components are preferred over duplication
- component names are descriptive and consistent
- component hierarchy is clear
- unnecessary components are removed

Avoid duplicated functionality across components.

---

# Pages and Layouts

Review every page and layout.

Ensure that:

- layouts are consistent
- navigation is intuitive
- pages reuse existing components
- page structure follows the application architecture

Avoid unnecessary complexity.

---

# User Experience

Review every interaction.

Ensure that:

- interactions are predictable
- user feedback is clear
- forms expose validation feedback
- navigation is coherent
- workflows minimize unnecessary user actions

Interfaces should feel simple and intuitive.

---

# Responsiveness

Verify that the generated interface behaves correctly across:

- mobile
- tablet
- desktop

Ensure that responsive behavior is consistent throughout the application.

Avoid layouts that only work for a single screen size.

---

# Accessibility

Review the generated interface for accessibility.

Ensure that:

- semantic HTML is used
- keyboard navigation is supported
- interactive elements expose meaningful labels
- forms contain accessible controls
- visual hierarchy is preserved

Accessibility should never be sacrificed for visual appearance.

---

# Consistency

Verify consistency between:

- pages
- layouts
- reusable components
- interaction patterns
- naming conventions

Generated components should follow the same design principles throughout the project.

---

# Final Validation

Before returning the result, verify that:

- every required field is present
- every component has a clear purpose
- responsive breakpoints are appropriate
- interactions are correctly described
- the JSON conforms to the FrontendResult schema

Return only the final FrontendResult JSON document.

Do not include Markdown outside the generated code contents.

Do not include explanations outside the JSON response.