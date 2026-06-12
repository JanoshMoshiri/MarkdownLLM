---
id: review-schema-coherence
type: prompt
status: stable
version: 1.0
created: 2026-06-08
inputs:
  - name: schema-index
    description: "The domain's schema registry (things/_index/schema.md) — fields in use with counts and example values"
  - name: thing-md
    description: "thing.md — to distinguish universal core fields from emergent domain schema"
outputs:
  - name: overlap-findings
    description: "Pairs or clusters of field names that appear to mean the same thing"
  - name: normalisation-proposals
    description: "For each overlap, a proposed canonical field and the migration it implies"
bound_to:
  - hook: retrospective
linked_things:
  - id: orchestration-specification
    relation: implements
  - id: derived-index-specification
    relation: references
  - id: retrospective-specification
    relation: complements
  - id: thing-specification
    relation: references
---

# Review Schema Coherence

## Purpose

Emergent schema is a strength early — fields are added as the domain needs them,
never over-defined upfront (`thing.md`). But over time emergence produces *drift*:
three things use `effort`, two use `energy_cost`, one uses `complexity`, and all
three fields mean the same ordinal thing. Nothing in ordinary operation catches this,
because each field was reasonable when introduced. This prompt steps back at
retrospective cadence and audits the *vocabulary* of the domain's frontmatter.

It reviews the schema registry, not the things themselves — an O(registry) read, not
O(all things) (see `derived-index.md`).

## Reasoning Template

### 1. Separate emergent from core

Using `thing.md`, set aside the universal core fields. They are fixed and not subject
to drift. The review is only over emergent, domain-specific fields.

### 2. Cluster by meaning, not by name

For each emergent field, infer its meaning from its name, its example values, and the
types that use it. Group fields whose meaning converges:

- **Same value space + same role** → strong overlap (e.g. `effort` and `energy_cost`,
  both `low|medium|high` on task-like things).
- **Synonym names** → likely overlap (e.g. `owner` and `assigned_to`).
- **Same concept, different granularity** → possible overlap worth noting, not
  necessarily merging (e.g. `due_date` vs `target_quarter`).

### 3. Distinguish overlap from healthy emergence

A field used by one or two things is not a problem — it may be genuinely specific.
The signal worth acting on is **two names for one meaning**, not low usage. Do not
propose consolidating fields that merely happen to be rare.

### 4. Propose normalisation

For each genuine overlap:
- Name the **canonical** field — usually the more widely used, or the clearer name.
- State the **migration**: which things carry the deprecated field and must be updated.
- Note any **information loss**: if the fields are not exactly synonymous, say what
  nuance consolidation would drop, so the human can decide.

## Output Format

```
Schema coherence review (as of [index.generated]):
- Emergent fields reviewed: [count]
- Overlaps found: [count]
  - [field-a] ([n]) ↔ [field-b] ([m]): [why they overlap]
    → Propose canonical: [field], migrate [n or m] things, loss: [none | description]
- No action needed: [fields that are fine]
```

Findings feed the retrospective's "What Should Change" section. Acting on a proposal
is a normal write operation (update the affected things, rebuild the schema registry);
it is never applied silently.
