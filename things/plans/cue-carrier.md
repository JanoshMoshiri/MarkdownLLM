---
id: cue-carrier
type: plan
status: in-progress
version: 1.0
created: 2026-09-12
session: 2026-09-12
priority: high
tags: [change-reconciliation, cue, seat-protocol, floor, session-start, dispatcher]
linked_things:
  - id: unattended-cue-carrier-2026-09-12
    relation: implements
    notes: "The ruling this plan builds. Every phase below is that decision made operative; nothing here widens it."
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 3's F5 row is ruled; this plan delivers the carrier that row said did not exist. The queue's assembly stays with that plan."
  - id: change-reconciliation-specification
    relation: extends
    notes: "Phase 4 writes the carrier into the spec's Cue beat and Enforcement table."
  - id: inflection-candidates-are-computable
    relation: implements
    notes: "The pre-commit advisory asked the question at the boundary; this plan gives the question somewhere to wait."
---

# Plan: The Cue Carrier

**What this delivers.** A reasoned-from thing gets modified. Today the floor
asks *"inflection?"* once, at the commit boundary, to whoever is at the
terminal — and at 3am that is nobody. After this plan the question is a
thing that waits: computed from the commit stream, listed at every session
start until a human answers it, and answered with a recorded verdict and
reason that the floor checks for shape.

**What it does not deliver.** The verdict. No floor path, hook, or prompt
answers a cue. Automating the answer is the exact move
`change-reconciliation.md` refuses and the operator reaffirmed on ruling
this. The plan makes reconciliation *feel* automatic — nothing is forgotten
— without making it *be* automatic.

**Shape may change.** The operator ruled this as deploy-and-see. Phase 6
is the seeing.

## Phases

- [x] **Phase 0 — Record the ruling.** `unattended-cue-carrier-2026-09-12`:
      option 3 with option 2's net; the cue is a reserved thing; loud at
      session start; the verdict stays human. *Done 2026-09-12.*
- [ ] **Phase 1 — Two landings the review found and the record agrees
      with.** (a) The pre-commit hook's block message stops advertising
      `--no-verify` — the contract says never, and the hook said "run with"
      at the one moment the contract matters. (b) The trigger actions table
      marks which actions cross a seat: `notify` pushes through an output
      route, which is an external effect, and belongs to whoever holds that
      route's authority; the rest are agent-executable reads and status
      moves.
- [ ] **Phase 2 — The type in the floor.** `cue` joins `RESERVED_STATUSES`
      (`open` / `answered`, terminal `answered`); `subject` joins the
      structural reference registry (id-scalar, validated, reverse-indexed,
      not cue-relevant — a cue must not count toward its own subject's
      fan-in); `raised_at` joins the commit-pin registry (scalar, local,
      resolved by the structural-pin check). Validation: answered ⇒ verdict
      ∈ {inflection, not-inflection} and reason non-empty (Error); open ⇒
      no verdict (Warning). A `templates/cue.md.template` beside the
      conflict template. Tests pin each rule.
- [ ] **Phase 3 — The question, computed and emitted.** `mdllm cues`:
      the commit stream since the newest retrospective (30 days when none),
      modifications only, filtered to reasoned-from things by the same
      predicate `candidates` uses (definition-surface type or fan-in ≥ 3);
      a cue covers its subject's modifications at and before its `raised_at`
      commit; what is left is *unraised*. Open cue things are *unanswered*.
      Both under one heading in the session-start digest, every session,
      after the open-conflicts line. Exit 0 always — advisory, like
      `candidates`. Tests: unraised listed; a raised cue covers; an answered
      cue silences until the next modification; the digest carries the line.
- [ ] **Phase 4 — Specs, prompts, generated surfaces.**
      `change-reconciliation.md` gains the carrier (the Cue beat, the
      unattended rule, the Enforcement table rows); `thing.md` and
      `validate.thing.md` list the type where they list the others; the
      session-end brake reads open cues beside open conflicts (the prompt
      and its four command surfaces); `retrospective.md` scan 4 answers the
      accumulated open set; `dispatch-loop.md` step 6 names the cue as
      seat-shaped and says raise-never-answer; the orient bound-prompt line
      and `orchestration.md`'s digest enumeration name the new line; kernel
      and the entry file's generated block regenerated; `framework-map.md`
      and the README's template list updated in the prose walk.
- [ ] **Phase 5 — Reconcile the inflection this plan is.** Adding a reserved
      type and a digest line is an inflection by the spec's own test. Run
      `touchpoints` on the changed specs, walk the prose residue, update the
      closed-loop plan's Phase 3 row and the review artifact's F5 disposition,
      seal with a `reconcile:` commit. Answer the cues this work raises —
      the first real use of the carrier is on itself.
- [ ] **Phase 6 — See.** One session that starts with an open cue in the
      digest and ends with it answered; one dispatch run that raises a cue
      and files it. Record both as evidence, including what the shape got
      wrong. Then decide whether the cue stays a thing, becomes a computed
      view only, or grows an age finding like conflicts have.

## Done when

- [ ] A modification of a reasoned-from thing with no cue is named in the
      next session-start digest, and keeps being named until a cue covers it.
- [ ] An open cue is named in every session-start digest until answered, and
      an answered cue is silent until its subject moves again.
- [ ] The floor rejects an answered cue without a verdict and reason.
- [ ] The full suite is green, the kernel and generated blocks are current,
      and the change is reconciled on the record.
- [ ] Phase 6 has at least one real observation recorded.
