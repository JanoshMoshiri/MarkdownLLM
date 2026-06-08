---
id: the-notation-changed-not-the-primitives
type: insight
status: active
version: 1.0
created: 2026-06-08
confidence: high
origin: synthesised
source: session — philosophical discussion on the programming paradigm shift
session: 2026-06-08
tags: [paradigm, philosophy, foundational, manifesto, identity]
linked_things:
  - id: llm-driven-systems-manifesto
    relation: extends
  - id: thing-specification
    relation: references
  - id: orchestration-specification
    relation: references
  - id: git-workflow-specification
    relation: references
---

# The Notation Changed, Not The Primitives

## The Insight

A program has only ever been two things: **data structures** — what exists and how it is shaped — and **instructions** — what to do, in what order, under what conditions. Every language that ever compiled, from assembly to C++ to Python, was just a notation for expressing those two invariants. The syntax differed; the primitives never did.

MarkdownLLM is not an exception to this. It is the same two things in a different notation:

- `thing.md` defines the **data structure**.
- The prompts in `templates/prompts/` are the **instructions**.
- The hooks in `orchestration.md` are the **control flow**.
- Git is the **state machine** — the commit is the moment state becomes real.

What changed is the notation, and with it the thing that reads the notation. A compiler-parsable grammar gave way to natural language; a deterministic compiler gave way to a reasoning model. The artifact did not become something new. The program is still a program. It is simply written in a notation a model can reason over rather than one a compiler can parse — and so the reader can now hold ambiguity, weigh context, and revise its own understanding, which no compiler could ever do.

This reframes what the framework *is*. It is not a new category of software invented for the LLM era. It is the oldest category of software — data and instructions over it — finally freed from the demand that its notation be mechanically parsable. The leverage moved from making the syntax precise enough for a machine to compile, to making the definition clear enough for a mind to reason within.

## Why It Matters

This is the framework's claim to legitimacy, and its defence against being dismissed as prompt-stuffing. Because the primitives are unchanged, every hard-won lesson of software architecture still applies — separation of concerns, single responsibility, versioned state, dependency inversion. The manifesto already names Clean Architecture and SOLID as ancestors; this insight says *why* they remain ancestors rather than analogies: it is literally the same kind of artifact, so the same discipline governs it.

It also sets the bar for what belongs in the framework. If a proposed mechanism has no analogue in "data structures and instructions over them," it is probably accidental complexity, not a primitive. The question to ask of any new feature is: is this a data structure, an instruction, control flow, or state? If it is none of those, it is suspect.

## Context

Surfaced in a philosophical discussion where Janosh observed that his original vision — "before, my code was written in C#, C++; now I write in English; we still hold the same things, sets and instructions that come together to create the system" — had quietly succeeded. The insight is the formal statement of that observation: the vision was not to build a new kind of program, but to write the same kind of program in a notation a model could read. Recorded here as the canonical articulation; the manifesto's *Paradigm Shift* section now opens on it.
