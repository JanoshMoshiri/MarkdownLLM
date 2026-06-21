---
id: modeling-cognition-yields-a-learning-loop-not-a-coherence-loop
type: insight
status: active
version: 1.0
created: 2026-06-21
session: 2026-06-21
source: both
confidence: medium
origin: synthesised
tags: [loops, learning, cognition, harness, context-engineering, memory, insights, retrospective, manifesto-thesis]
linked_things:
  - id: llm-driven-systems-manifesto
    relation: informs
  - id: retrospective-specification
    relation: informs
  - id: session-memory-specification
    relation: informs
  - id: the-notation-changed-not-the-primitives
    relation: supports
  - id: consequence-is-recoverable-only-in-retrospect
    relation: complements
---

# Modeling Cognition Yields a Learning Loop, Not a Coherence Loop

## The Insight

There are two ways to arrive at an agent loop, and they carry different cargo.

**Engineering-first (the harness path).** Start from the `while` loop — *gather context → take action → verify → repeat* — and then engineer carry-forward so the loop survives the context window. This is what Anthropic's published harness work optimises: compaction ("summarising its contents, and reinitiating a new context window with the summary"), structured note-taking (`NOTES.md`, to-do lists, `claude-progress.txt`, `feature_list.json`), sub-agent distillation, the file-based memory tool, and git history. All of it is real memory — the loop is *not* hollow — but every piece carries **task state**, and the optimisation target is *coherence within a run*: "find the smallest set of high-signal tokens that maximise the likelihood of your desired outcome." Asked directly about learned lessons, the docs are blunt: these artifacts "serve immediate task completion **rather than cross-session learning accumulation**," with "no explicit mechanism for extracting generalizable lessons."

**Cognition-first (this framework's path).** Don't start from a loop at all. Model how a mind accumulates understanding — *encode → consolidate → retrieve → apply* — and the loop falls out as a side effect. Session produces an **insight** (encode), the **retrospective** consolidates and triages it (consolidate), the **continuity brief** carries the live ones forward (retrieve), and the next session reasons within them (apply). The cargo here is not task state but **graded, typed, promotable insight** (`confidence`, `origin`, `promoted_to`, a lifecycle, a retrospective that asks ["is our reasoning working?"](../../retrospective.md)). The optimisation target is *learning across runs*.

Same topology — both are loops. The difference is entirely **what survives the turn**, and that traces directly to which system you imitated. The harness path imitates a *task executor*, so it keeps what the task needs and the learning row is the thing it leaves on the floor. The cognition path imitates a *learner*, so cross-run accumulation isn't a feature that was added — it's the whole point of the thing being copied, and it comes for free.

## Why It Matters

This supplies a **cleaner cause** for the manifesto thesis than "we added insights and retrospectives." The framework accumulates understanding not because of any one primitive, but because its loop was modelled on cognition rather than engineered as a harness — and the engineering-first path *structurally* omits that row. It is the same razor as [the-notation-changed-not-the-primitives](the-notation-changed-not-the-primitives.md): the learning loop was not invented here; an existing pattern (how a mind learns) was reproduced in a new notation. Arriving at it unintentionally — "because that was the way to make it work" — is evidence *for* the framing, not against it: imitate the right system and its properties come along whether you designed for them or not.

It also guards against a false equivalence. When a reader points at Anthropic's note-taking, compaction, or memory tool and says "they already do this," the answer is precise: those are **coherence** mechanisms (survive the window, complete *this* task), not **learning** mechanisms (typed, confidence-graded, promotion-gated, retrospective-triaged knowledge that compounds across tasks and domains). The memory tool — "build up knowledge bases over time" — is the one place the harness path is *reaching toward* this row; the difference is it offers a filesystem to write blobs into, whereas the framework offers a *theory of what earns the right to be remembered*. That convergence is worth watching, not dismissing.

The razor it carries: when admitting a new mechanism, ask whether it serves **coherence** (keep the run from losing what it figured out) or **learning** (let the system compound what it figured out). They look alike — both write things down and read them back — but they are different loops, and only the second is the framework's reason to exist.

## Context

Synthesised 2026-06-21 from a human-led exploration. The operator opened on loops as "a brute-force way to create determinism with a non-deterministic executor," and felt "an element of learned insight missing" from the *do → check → refine → repeat* pattern. Walking it through surfaced two things: (1) the naive loop chases determinism, which the [thesis](../../llm-driven-systems.manifesto.md) explicitly disclaims — convergence, not determinism, is the right target; and (2) mid-conversation the operator realised the framework *already is* a loop, arrived at not by designing one but by modelling how the mind works — "insights, understanding, retrospective, putting that into your workflow next time."

A check of Anthropic's harness writing confirmed the distinction rather than collapsing it: their loop genuinely passes information back (compaction, note-taking, sub-agents, memory tool, git), but the carried cargo is task-state optimised for within-run coherence, and the docs explicitly disclaim a cross-session learned-lesson mechanism. The framework's session→insight→retrospective→continuity cycle is the same loop with different cargo — learning, not coherence — because it was copied from cognition, not engineered from a `while` loop.

Sources: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents); [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

**Related open thread:** the *loop-scoped insight* — a cheap, low-confidence, born-inside-one-loop note with a promotion gate to the durable backlog — is the per-iteration cadence this same pattern would take if pushed below session granularity. Capture as its own insight or spec if it recurs; it is the unbuilt sibling of this one.
