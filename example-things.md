---
id: example-things-specification
type: specification
status: stable
version: 1.0
created: 2026-05-29
linked_things:
  - id: thing-specification
    relation: extends
  - id: domain-specification-guide
    relation: complements
---

# Example Things

## What This Specifies

This document defines `type: example` — the framework mechanism for building pattern libraries and teaching LLMs domain-specific reasoning inductively. All other framework-reserved types (`insight`, `continuity-brief`, `conflict`, `retrospective`) have their own dedicated specs; this spec gives `type: example` the same treatment.

## Structure of an Example Thing

```yaml
---
id: example-[pattern-name]
type: example
pattern_type: [what kind of pattern]
demonstrates: [compliance/good-practice/anti-pattern/edge-case]
applies_to: [which domains or thing-types this pattern applies to]
created: 2026-05-18
---

# [Pattern Name]

## The Pattern
[Clear description of what this example demonstrates]

## Why It Matters
[The reasoning: why is this pattern important to follow?]

## Structure/Code Example
[Show the correct structure or code pattern]

## Anti-Patterns (What NOT to Do)
[Common mistakes or violations of this pattern]

## How to Adapt
[How to apply this pattern to your specific domain]
```

## When To Use Example Things

Example things are a teaching mechanism for LLMs. They serve as inductive learning — showing rather than telling how patterns should work.

Create an example thing when:
- A domain pattern is difficult to express as a rule alone
- You want to teach positive and negative contrast (what good looks like vs. what breaks)
- You have a recurring decision type that should be made consistently
- You want future sessions to inherit reasoning patterns from previous ones

## Why Examples Work Better Than Rules

LLMs excel at **verifiable reasoning** — tasks where patterns can be checked against clear criteria — and struggle with non-verifiable tasks. Compliance patterns are inherently verifiable (data classified or not, access logged or not, etc.). A single rule ("classify personal data") is abstract; positive + negative examples create verifiability:

- **Positive example**: Shows what good classification looks like (verifiable)
- **Negative example**: Shows violations and consequences (verifiable contrast)
- **Together**: LLM learns the pattern boundary, not just a rule

This mirrors how humans learn — contrast creates clarity that rules alone don't provide.

## Common Use Cases

- Compliance patterns (GDPR, audit trails, data handling) — *especially useful for verifiable decisions*
- Architectural patterns (how to structure complex domains)
- Naming conventions (what field names mean what)
- Edge cases (showing how to handle ambiguous situations)
- Anti-patterns (showing what breaks and why) — *pairs negative examples with remediation*

## Examples Are Discoverable

When an LLM encounters a domain with example things, it naturally learns from them. You don't need to explicitly reference them; they guide reasoning through pattern recognition.

## Scaling Through Examples

As your system grows, your library of example things becomes organisational knowledge — versioned, auditable, and automatically referenced by any LLM working within your domains. See `scalability-guide.md` for how example things complement the broader scaling strategy.
