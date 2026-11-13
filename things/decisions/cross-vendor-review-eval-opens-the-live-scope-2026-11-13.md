---
id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
type: decision
status: made
version: 1.0
created: 2026-11-13
session: 2026-11-11/13
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [evals, scope, cross-vendor, review, codex, reviewer-independence, peer-review]
informed_by:
  - id: live-eval-scope-bounded-to-claude
    commit: 83ad75d008fdc7ad2f96a3f799c9c4327ca01b26
  - id: review-agent-coordination-leaders-2026-11-13-workspace-2
    commit: 83ad75d008fdc7ad2f96a3f799c9c4327ca01b26
  - id: eval-cycle
    commit: 83ad75d008fdc7ad2f96a3f799c9c4327ca01b26
linked_things:
  - id: live-eval-scope-bounded-to-claude
    relation: extends
    notes: "That decision said another harness enters the live evals only on an explicit decision made for its own sake, with its own eval set. This is that decision, for one programme. Its boundary stands for everything else, so it is extended and not superseded."
  - id: review-agent-coordination-leaders-2026-11-13-workspace-2
    relation: derived-from
    notes: "The reading of the field that found no published catch rate for review by a different vendor against review by the same model, with the reviewer kept from the author's verdict."
  - id: eval-cycle
    relation: references
    notes: "The method is used unchanged. The surfaces this programme moves are its own: the reviewer's vendor, and whether the reviewer sees the author's account."
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "A second eval programme beside the work-continuity ablation, with its own set, runner and record. It takes nothing from that programme's cells and adds nothing to them."
  - id: peer-loops
    relation: informs
    notes: "Whether the hub should review at all, who reviews whom, and whether a review starts blind are design questions that plan now waits on. This programme is how they get an answer from the record."
---

# The Cross-Vendor Review Eval Opens The Live Scope, For One Programme

## Context

On 2026-08-18 the operator bounded the live evals to the Claude harness and
Claude models, and ruled that any other harness arrives only on an explicit
decision made for its own sake, with its own eval set
(`live-eval-scope-bounded-to-claude`).

On 2026-11-13 a reading of the field
(`review-agent-coordination-leaders-2026-11-13-workspace-2`) found that
products now offer review by a different model, and that none has published
whether it catches more than review by the same model, nor whether the
reviewer is kept from the author's own verdict. The operator runs
cross-vendor loops for the reason science runs peer review, and said of the
gap:

> Anytime there's an opening of things that are not explored, the first
> person to explore them is always going to be a little bit ahead. So I'm
> quite keen to look into that.

## Decision

Ruled by the operator on 2026-11-13, on reading the six points below as
drafted, the run that follows from them and its predictions:

> Yeah let's go. I agree with all of this.

1. **The live eval scope opens to one added surface, for one programme.**
   A Codex reviewer, run headless and read-only, joins the live evals in
   the review-catch programme and nowhere else.
2. **It has its own eval set and structures**, as the 2026-08-18 decision
   required: its own review set, instructions, runner and scorer, under
   `evals/review-catch/`. `mdllm eval --run` and the polar-station
   programme are untouched and stay Claude-scoped.
3. **The question is one question.** Does review by a different vendor,
   started without the author's verdict, catch more real defects than
   review by the same model? The reviewer's vendor and the author's verdict
   are the two surfaces the programme moves, one per cycle.
4. **The method is `eval-cycle`, unchanged.** Freeze, baseline, move one
   surface, predict before the run, log either way.
5. **The 2026-08-18 boundary stands for everything else.** Any further
   harness, or this harness in any other eval, is again its own decision.
6. **No claim expands and nothing is concluded.** The standing direction of
   2026-10-05, no write-up until much more testing, covers this programme.
   A result here is about one operator's repository and says so.

## Consequences

- The first cycle is `run-eval-cycle-0-review-catch-baseline-2026-11`, with
  its hypothesis committed before any review runs.
- Runs start from the operator's terminal, on the operator's own accounts
  with each vendor. No agent launches a reviewer.
- If the programme is kept, `eval-cycle`'s table of moving surfaces is owed
  a line saying a programme may name surfaces of its own. That is a change
  to a definition and is not made here.
- The runner for this programme lives beside its set and not in the tool,
  because it holds two vendors' command lines. Lifting any shared part into
  the tool waits until a second programme needs it, as the 2026-08-18
  decision said.

## Rationale

The claim the operator makes for cross-vendor work is validation, and no
one has measured it. The repository already holds the instrument: its own
fix commits mark real defects in earlier commits, so the answer key is in
git and was written by people who were not thinking about an eval. Opening
the scope for exactly this, and for nothing else, keeps the 2026-08-18
discipline and still lets the question be asked.
