---
id: the-eval-question-is-which-surfaces-carry-the-weight-2026-11-08
type: decision
status: made
version: 1.0
created: 2026-11-08
session: 2026-11-09
decided_by: Janosh Moshiri
confidence: high
origin: stated
exposed: false
tags: [evals, direction, hypothesis, structure, ablation, continuity, memory-systems]
informed_by:
  - id: llm-driven-systems-manifesto
    commit: b9bb9a716e928f446d8b9a99ae16b5b52ba605e8
  - id: evidence-and-eval-backlog
    commit: b9bb9a716e928f446d8b9a99ae16b5b52ba605e8
  - id: run-eval-cycle-0-polar-baseline-2026-10
    commit: b9bb9a716e928f446d8b9a99ae16b5b52ba605e8
linked_things:
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "The backlog's purpose — evidence for the model-tier claim — is withdrawn by this ruling; its purpose line is owed a rewrite to 'which surfaces carry the weight'."
  - id: eval-cycle
    relation: informs
    notes: "The loop stands unchanged; what changes is what its arms are — variants of the structure against each other, not structure against bare."
  - id: flagship-models-look-around-the-edges
    relation: informs
    notes: "The pre-registered haiku-framework vs opus-bare prediction is no longer the deciding cell; it stays on record as a prediction, demoted with the claim it served."
  - id: run-eval-cycle-0-polar-baseline-2026-10
    relation: informs
    notes: "Cycle 0's baseline cell (haiku × framework) still serves — every ablation departs from it; cycles 1–2 as written (→ bare, → opus) do not follow from this ruling and are to be re-planned."
  - id: llm-driven-systems-manifesto
    relation: references
    notes: "The corollary section already names model-tier superiority 'a secondary, still-open hypothesis… re-proving it adds little'; this ruling takes the manifesto at its word and stops testing it. A rewrite of AGENTS.md principle 9 to match is a definition-surface change the operator has not yet asked for."
  - id: review-memory-systems-reread-2026-11-09-workspace-1
    relation: references
    notes: "The reading of the field made the same day, which supplies the first surface worth moving under this question."
---

# The Eval Question Is Which Surfaces Carry The Weight

## Context

Since 2026-06-11 the eval programme has been pointed at one claim: that a
smaller model inside the framework's structure matches or beats a larger model
working bare (`AGENTS.md` principle 9; the manifesto's efficiency corollary).
Every fixture, the 2×2 design, the polar-station seed and the pre-registered
cell-by-cell prediction of 2026-10-30 served that claim. Three things then
happened in a week. The operator objected (2026-11-01) that a bare arm with no
session-to-session memory loses for lacking *memory*, not for lacking
*structure*, so a win there proves the wrong thing. The operator spent a week
working in a harness with no MarkdownLLM record beneath it and found it
"difficult, to say the least" — a capable model that had to be re-told every
morning where yesterday ended. And on re-reading, the manifesto turned out to
have already demoted the claim: "a secondary, still-open hypothesis… its
general form is already well-supported in the broader literature, so re-proving
it adds little."

## Decision

In the operator's words, 2026-11-08:

> It's obvious that the structure is going to give you a better result. And I
> think I just need to take that claim altogether. I think the question I need
> to ask myself is, what am I trying to prove with this setup? And now I don't
> need to just prove it in a way, really, because I've experienced it. I know
> that when I use agents that don't run in their substrate, it's difficult.
> That context layer system and retrieval is really important. So I think I'm
> asking myself the wrong question.

And, to the agent's restatement — *not whether the structure works, but what
in it does the work* — "Yeah, that is pretty much the question."

So ruled:

1. **Model-tier superiority is no longer the claim the eval programme exists
   to test.** It stays in the record as what the manifesto already calls it —
   a secondary hypothesis, supported in general by the literature — and is not
   re-proved here.
2. **The question is which surfaces of the structure carry the weight.** The
   framework has a kernel, typed records, relations, status, triggers, cues, a
   computed session-start digest, a reckoning. Which of those does the work
   and which is ceremony is unknown, and it is the question whose answer makes
   the framework *better* rather than *defended*.
3. **The method stands; the arms change.** `eval-cycle` — freeze, baseline,
   move one surface, predict first, log either way — is the instrument. Its
   arms become variants of the structure against each other, every arm holding
   the same facts and the same knowledge layer. That dissolves the fairness
   objection of 2026-11-01 at the root: no arm is punished for lacking
   memory when every arm has it.
4. **The operator's aim is the problem statement.** "A tool that enhanced
   one's ability to work over multiple sessions, over multiple days, weeks,
   months, years, on a specific set thing, or on many things within a specific
   set domain — and that this knowledge graph that builds itself through use
   as a fractal piece would become a domain graph." This is the manifesto's
   Accumulation section in his voice, and it is continuity of *work*, not
   persistence of *facts*. What the eval measures should be what he felt the
   absence of: re-establishment cost, wrong turns against a stale record, and
   whether a session acts on the open loop the record names without being
   told.

## Consequences

- The backlog's purpose line, cycles 1–2 of `run-eval-cycle-0` (→ bare,
  → opus), and `AGENTS.md` principle 9 each now disagree with this ruling and
  are owed a revision. None is made in this commit: the backlog and the
  cycle plan are the agent's to revise on the operator's go-ahead; principle 9
  is a definition surface and its rewrite is the operator's to ask for.
- The reading of the field made the same day
  (`review-memory-systems-reread-2026-11-09-workspace-1`) supplies the first
  surface worth moving: the work-continuity layer — status, stage cursors,
  dated triggers, the computed digest — which no surveyed system has and the
  operator's Copilot week lacked. Its pre-registered prediction is written
  there, before any run.
- The `bare-journal` control arm proposed on 2026-11-01 is subsumed: under
  this ruling every arm is a journalled arm, and the variable is the shape.
- Nothing is concluded. The standing direction of 2026-10-05 — no write-ups
  until much more testing — holds across the new question as it did the old.

## Rationale

The claim being dropped was never the one the operator believed in; it was
inherited from an economic framing (cheaper model, same work) and survived
because it was the easiest thing to put a number on. The claim being kept is
the one the operator has lived and the one the record already names as the
reason the framework exists. An eval pointed at the first produces a defence;
pointed at the second it produces a design input — which surface to keep,
which to simplify — and that is what the one-surface-at-a-time method was
built to yield.
