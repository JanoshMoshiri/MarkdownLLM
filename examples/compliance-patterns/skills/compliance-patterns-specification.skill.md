---
id: compliance-patterns-specification
name: Compliance Patterns Specification
type: specification
status: stable
version: 2.1
created: 2026-05-18
linked_things:
  - id: compliance-patterns-read-thing-skill
    relation: informs
  - id: compliance-patterns-write-thing-skill
    relation: informs
  - id: compliance-patterns-workflow-skill
    relation: informs
description: Philosophy and approach to encoding compliance as verifiable reasoning
applies_to: "**/*.md"
---

# Compliance Patterns Specification

## What This Domain Is

A collection of example things demonstrating compliance patterns, multi-lens reasoning, and regulatory best practices for domains operating under constraints (GDPR, HIPAA, financial regulations, etc.).

This is **not** a compliance domain itself. It's a reference library for domain builders creating regulated systems.

## Philosophy: Why Examples Work for Compliance

Traditional compliance approaches:
- Write rules and hope the system follows them
- Rely on checklists to prevent violations
- Separate "compliance team" from "engineering team"
- End up with technical debt and audit friction

**Better approach: Make compliance verifiable through examples.**

LLMs excel at **verifiable** reasoning—tasks with clear right/wrong answers. Compliance is inherently verifiable:

- ✓ Data classified or not classified
- ✓ Access logged or not logged
- ✓ Data residency UK or non-UK
- ✓ Retention policy followed or violated

By providing both **positive examples** (compliant patterns) and **negative examples** (violations with explanations), we transform compliance from abstract rules into verifiable patterns. The LLM learns not just "what to do" but "why this is right and that is wrong."

### Contrast Creates Clarity

Showing both the correct pattern AND the violation pattern (with consequences) gives the LLM two concrete reference points. This is why anti-patterns paired with remediation are more effective than rules alone—the LLM can verify its reasoning against both.

## Core Principles

**Verifiable Compliance:** Every compliance decision should be reducible to verifiable facts, not subjective interpretation.

**Multi-Lens Reasoning:** Every significant decision should be evaluated through domain logic, compliance logic, and audit logic.

**Explicit Conflicts:** When lenses conflict, surface the conflict for human resolution rather than hiding it in logic.

**Pattern-Based Learning:** LLMs learn from examples; compliance becomes reinforced through every decision, not imposed as external constraints.

**Auditability by Design:** Git history + clear reasoning patterns + explicit examples = natural audit trail.

## The Multi-Lens Framework

### Lens 1: Domain Logic
"What does this accomplish in the domain's terms?"
- What is the business or operational outcome?
- Does this decision serve the domain's goals?
- Is the tradeoff acceptable?

### Lens 2: Compliance Logic
"Would this violate regulatory constraints?"
- Does this respect GDPR, HIPAA, financial regulations, etc.?
- Are there data residency requirements?
- What audit requirements exist?
- How could risks be mitigated?

### Lens 3: Audit Logic
"Can we trace and explain this decision?"
- Is the decision traceable in logs/git?
- Can we justify it to a regulator?
- Is there sufficient documentation?
- Would an auditor accept our reasoning?

**All three lenses must align before proceeding. If they conflict, the conflict is explicit.**

## Thing Types in This Domain

**type: pattern**
- A verified, compliant behavior or process
- Shows what to do and why it's compliant
- May include positive examples

**type: anti-pattern**
- A violation of regulatory requirements
- Shows what NOT to do and why it's wrong
- Includes consequences or remediation

**type: example**
- A concrete scenario with all three lenses
- Shows domain logic, compliance logic, audit logic
- Demonstrates how to reason through a decision

**type: decision-tree**
- A framework for evaluating recurring decisions
- Shows questions to ask at each step
- Helps apply reasoning lenses systematically

## How to Use This

### For Domain Builders

When building a regulated domain (law, finance, healthcare):

1. **Study the examples** — Understand how multi-lens reasoning applies
2. **Copy the reasoning patterns** — See how domain, compliance, and audit logic interact
3. **Create your own examples** — Add domain-specific compliance examples to your domain

### For LLMs Working Within Regulated Domains

When you encounter `type: example` things:

1. **Learn the pattern** — Understand what good compliance looks like
2. **Apply to your domain** — Use the reasoning when making similar decisions
3. **Reference when uncertain** — If unsure how to handle a compliance question, load examples and reason by pattern

### For Regulators/Auditors

If you're auditing a system built on this framework:

- Example things serve as documentation of compliance intent
- Reasoning lenses document how compliance decisions are made
- Git history shows all changes and decisions
- The framework is *designed* for auditability, not retrofitted

## Growing Your Pattern Library

The examples here are starting points. Your domain will grow its own library as you discover patterns specific to your context and constraints. Each new example you add teaches the system what compliance looks like in your specific context.

When you encounter a compliance decision in your domain:

1. **Document it as a thing**
2. **Reason through all three lenses**
3. **If aligned: Add as a pattern (positive example)**
4. **If conflicts: Document conflict, resolution, reasoning**
5. **Store in git: Build your library**

## What This IS / IS NOT

**Is:**
- Educational reference material
- Examples you can adapt for your domain
- Documentation of reasoning approaches
- A starting point, not a complete solution

**Is NOT:**
- Legal or regulatory advice
- A complete compliance solution (domain-specific)
- A substitute for expert legal/compliance review
- Production code

## Domain-Specific Validation Rules

Beyond the universal structural checks (id, type, status, created present):

- Things of `type: pattern` must document all three lenses (domain, compliance, audit)
- Things of `type: anti-pattern` must have a `linked_things` entry with relation `remediated-by`
- Things of `type: example` must include a concrete scenario (not just abstract rules)
- Things of `type: decision-tree` must show branching logic with clear outcomes at each node

## Triggers

### Dependency
- **Orphaned anti-pattern** — Anti-pattern without a remediation link → flag for completion
- **Stale regulation reference** — If a pattern references a regulation version, flag when newer versions are known

### Relationship
- **Pattern consistency** — When a pattern is updated, verify all anti-patterns that contrast with it still make sense

## Integration with Reasoning Lenses

Compliance doesn't have to be a burden. When you encode it as reasoning patterns and examples, it becomes part of how the system thinks. The multi-lens approach makes compliance reasoning explicit and verifiable at every decision point.

LLMs naturally learn from examples, so compliance becomes reinforced through every decision, not imposed as external constraints.

## Example Domains

See the thing files in `./things/` for concrete patterns:

- GDPR Data Handling — How to structure personal data compliantly
- Multi-Lens Alignment — Example where domain, compliance, and audit lenses agree
- Multi-Lens Conflict — Example where lenses conflict and how to resolve
- Compliance Checklist — A decision-tree for systematic compliance evaluation
