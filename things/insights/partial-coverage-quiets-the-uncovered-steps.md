---
id: partial-coverage-quiets-the-uncovered-steps
type: insight
status: active
version: 1.1
created: 2026-08-19
session: 2026-08-19
source: both
confidence: high
origin: inferred
tags: [adapters, session-start, coverage, masking, hardening, salience]
linked_things:
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: extends
    notes: "The delivery law's corollary: emission determines what is consumed; coverage determines how loudly the remainder asks to be done."
  - id: session-start-loses-to-the-first-request
    relation: complements
    notes: "Pull-collision explains why un-pulled duties lose; this adds that partial mechanisation lowers their salience further — the session feels started."
  - id: review-independent-seams-verification-2026-08-26-claude
    relation: references
    notes: "Second surface, 2026-08-26: an explicit reading list in a handover prompt quieted the routing table the same prompt invoked. The two specs the list omitted are exactly the two whose rules the builder then reconstructed from concept."
---

# Partial coverage quiets the uncovered steps

## The Insight

When an adapter mechanises part of a ritual, the uncovered remainder does
not stay equally visible — it gets quieter. The mechanical steps complete,
the session feels started, and the unmechanised steps lose the salience an
entirely manual ritual would have forced on them. Articulated from inside
the failure by the strongest Claude run in the five-run baseline (Fable,
Claude Code, xhigh, 2026-08-19), diagnosing its own kernel skip unprompted:
"the adapter ran the sync and orient steps mechanically, which made the
session feel started, and the unmechanized kernel-load step fell through
the gap... the adapter's partial coverage makes the uncovered steps
quieter, not louder."

## Why It Matters

- It is the standing argument for [[session-start-hardening]] Phase 4:
  Phases 2–3 move more of the ritual into the floor, which by this
  mechanism deepens the quiet over the judgement residue. The residue
  therefore needs a named invocation — it cannot rely on leftover pull,
  because each hardening pass leaves less of it.
- It bounds the emission strategy: emission is not monotonically safe.
  Every step mechanised makes its unmechanised neighbours easier to skip
  silently. The honest countermeasure is making the seam loud — the digest
  naming what it did *not* do — rather than assuming visibility is
  conserved.
- Confidence is deliberately medium: the masking claim goes beyond
  pull-collision, which alone explains the observed skips, and the
  five-run baseline contains no no-adapter control. The discriminating
  test is named: a bare-harness run with no adapter coverage. If ritual
  compliance there is no better, masking reduces to plain pull and this
  insight falls.

## Context

Surfaced at the close of the five-run baseline (2026-08-18/19, two vendors,
three harnesses, four models, one live compliance domain). The diagnosing
quote came from the run under test: the agent that skipped the kernel
explained why, unprompted, in the framework's own anchor vocabulary — and
proposed its own mitigation (a session-gate line), which Phase 2's
emission-plus-integrity-trailer supersedes.

Dismissal condition: dismissed if the no-adapter control shows
equal-or-worse compliance without coverage (masking not evidenced beyond
pull); promoted if a "name the uncovered steps loudly" rule lands in
orchestration.md's adapter doctrine or the session-start projection.

## Second surface — prompts, 2026-08-26 (confidence medium → high)

The same shape appeared where no adapter was involved, and it is the
cleaner instance because the original confound does not fit it.

A handover prompt directed a builder to run session start, read
`AGENTS.md` **end to end**, then named five specs explicitly and added
"the other specifications relevant to the framework". The routing table
in that very file has rows for both specs the list omitted. Both omitted
rules were then reconstructed from concept rather than read: the atom's
canonical stage ids became a third invented vocabulary, and a
`type: example` thing was minted at `status: stable` with new schema
vocabulary, without its governing spec.

Why this discriminates: pull-collision cannot explain it. There was no
competing live request stealing salience — the reading *was* the task,
and the file containing the table was read as instructed. What quieted
the two rows was the presence of a partial list beside them. **An
explicit enumeration reads as the set, not as a floor the table
extends** — coverage of five made the remainder quieter, exactly as
mechanising four steps quiets the fifth.

The named discriminating test for the *adapter* form (a bare-harness,
no-adapter control) remains owed and unchanged; this instance raises
confidence in the general claim, not in that untested one. Evidence:
`review-independent-seams-verification-2026-08-26-claude`.

**Practical corollary, now earned twice:** a partial list must say it is
partial. A handover that names specs should name the routing table as
the authority above them — "these, plus whatever the table routes you
to" — or name nothing and let the table do its job.
