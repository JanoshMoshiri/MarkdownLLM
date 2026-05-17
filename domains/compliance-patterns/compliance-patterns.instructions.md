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

### Why Examples Matter (Verifiability)

LLMs excel at **verifiable** reasoning—tasks with clear right/wrong answers—and struggle with **non-verifiable** tasks (pure opinion, abstract preference). Compliance is inherently verifiable:

- ✓ Data classified or not classified
- ✓ Access logged or not logged  
- ✓ Data residency UK or non-UK
- ✓ Retention policy followed or violated

By providing both **positive examples** (compliant patterns) and **negative examples** (violations with explanations), we create verifiability. The LLM learns not just "what to do" but "why this is right and that is wrong"—transforming compliance from an abstract requirement into a verifiable pattern.

**Contrast creates clarity.** Showing both the correct GDPR data handling pattern AND the violation pattern (with consequences) gives the LLM two concrete reference points. This is why anti-patterns paired with their remediation are more effective than rules alone—the LLM can verify its reasoning against both.

### Integration with Reasoning Lenses

Compliance doesn't have to be a burden. When you encode it as reasoning patterns and examples, it becomes part of how the system thinks. The multi-lens approach (domain logic, compliance logic, audit logic) makes compliance reasoning explicit and verifiable at every decision point.

LLMs naturally learn from examples, so compliance becomes reinforced through every decision, not imposed as external constraints.

### Growing Your Pattern Library

The examples here are starting points. Your domain will grow its own library as you discover patterns specific to your context and constraints. Each new example you add teaches the system what compliance looks like in your specific context.

## For Regulators

If you're auditing a system built on this framework:

- Example things serve as documentation of compliance intent
- Reasoning lenses document how compliance decisions are made
- Git history shows all changes and decisions
- The framework is *designed* for auditability, not retrofitted

---

See the example things in this domain for concrete patterns you can learn from.
