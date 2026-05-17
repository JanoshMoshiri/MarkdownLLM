# Compliance Patterns Library

## What This Domain Is

A collection of example things demonstrating compliance patterns, multi-lens reasoning, and regulatory best practices for domains operating under constraints (GDPR, HIPAA, financial regulations, etc.).

This is **not** a compliance domain itself. It's a reference library for domain builders creating regulated systems.

## How to Use This

### For Domain Builders

When building a regulated domain (law, finance, healthcare), you can:

1. **Study the examples** — Understand how multi-lens reasoning applies to your domain
2. **Copy the reasoning patterns** — See how compliance, domain logic, and audit logic interact
3. **Create your own examples** — Add domain-specific compliance examples to your domain

### For LLMs Working Within Regulated Domains

When you encounter `type: example` things in compliance-patterns:

1. **Learn the pattern** — Understand what good compliance looks like in that context
2. **Apply to your domain** — Use the reasoning pattern when making similar decisions
3. **Reference when uncertain** — If unsure how to handle a compliance question, load examples and reason by pattern

## Example Patterns Included

### GDPR Data Handling
How to structure and operate on personal data compliantly.

- Metadata requirements
- Access logging
- Data minimization
- Residency constraints

### Multi-Lens Reasoning Alignment
Example of a decision where all reasoning lenses agree.

- Domain logic: What we want to accomplish
- Compliance logic: Regulatory constraints
- Audit logic: Traceability and defensibility

### Multi-Lens Reasoning Conflict
Example of a decision where lenses conflict, and how to handle it.

- When domain goals clash with compliance
- How to surface the conflict
- How to let humans decide

## Philosophy

Compliance doesn't have to be a burden. When you encode it as reasoning patterns and examples, it becomes part of how the system thinks. LLMs naturally learn from examples, so compliance becomes reinforced through every decision, not imposed as external constraints.

The examples here are starting points. Your domain will grow its own library as you discover patterns specific to your context and constraints.

## For Regulators

If you're auditing a system built on this framework:

- Example things serve as documentation of compliance intent
- Reasoning lenses document how compliance decisions are made
- Git history shows all changes and decisions
- The framework is *designed* for auditability, not retrofitted

---

See the example things in this domain for concrete patterns you can learn from.
