---
id: holistic-review-rulings-2026-10-21
type: decision
status: made
version: 1.0
created: 2026-10-21
session: 2026-10-21
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [ruling, review, reconciliation-gate, wording, discovery, evals, disposition]
informed_by:
  - id: review-holistic-substrate-2026-10-21-codex
    commit: f3ccc9b4efcc2d9fd3b9cc2744c2f02ae1e3c5aa
linked_things:
  - id: review-holistic-substrate-2026-10-21-codex
    relation: derived-from
    notes: "The six findings and the discovery proposal; the four questions the record could not settle, answered here through the native prompt."
  - id: limitations-guide
    relation: informs
    notes: "F1 lands as wording: the guide and the README now say what the gate enforces."
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "Its readiness line corrected by citation to the eval record — settled by the record, no ruling asked."
  - id: public-docs-face-build
    relation: informs
    notes: "Carries the F5 note: an evidence view over the framework map, noted and not built."
  - id: workflows-emerge-from-use
    relation: references
    notes: "F6: the multi-day filter is deliberate and documented; kept, moved only on evidence of real short workflows."
  - id: cold-read-of-the-seams-release
    relation: references
    notes: "Its cancellation reasoned that the 2026-10-17 comparison performed the cold read; the review names that comparison's memory-system brief as a category confound, so the next cold read excludes both reviews from its first pass."
---

# Decision: The holistic review — the gate's promise, the discovery route, and the private-domain findings

## Context

The operator had a second seat (Codex, in the Workspace-2 clone) review the
substrate at v3.50.0. The brief asked for a comparison with agent memory
systems; the operator corrected the framing across the session, and the
record (`review-holistic-substrate-2026-10-21-codex`, v1.1 with its
historical appendix) labels itself guided, not cold, and withdraws its own
claim that needing that correction proved a discoverability defect. Its
position: the core is coherent, no foundational primitive is missing for the
workflows examined, and the work lies at enforcement and execution
boundaries. Six findings and one proposal. The review was merged here from
the local clone on the operator's word (439a787); nothing was pushed.

## Settled by the record — no ruling asked

| Finding | Where the record already stood |
|---|---|
| F6 — the emergence heuristic excludes same-day histories | Deliberate: `MIN_DAYS = 3` and the one-day bookkeeping filter in `workflows.py`, stated in the build plan. Kept; a change needs real short-workflow evidence first. |
| The eval plan and the eval record disagree on readiness | The plan's "now only the operator's evening" was stale; `eval-record-2026` (defects 6 and 7: an aborted trial scored as failed; the launch failure undiagnosed) is the authority. The plan line is corrected by citation in this commit. |
| Maintenance may outweigh benefit | An empirical question whose instrument is already built (`reckon --rates`); what is missing is the sustained series, which accumulates and is not decided. |
| The five "untrodden" questions | Each already carried by an open plan — `closed-loop-operating-state`, `a2a-conversations-on-their-own-branch`, `substrate-native-a2a`. No new record. |

## The four questions put to the operator

1. **Routing.** Two clones each held two unpushed commits on 796aa23 — the
   review in Workspace-2, the Reckoning Phase 4 seal here — overlapping only
   in the four derived indexes.
2. **F1.** The README's FAQ said a change is refused "until its dependants
   are walked"; the gate (`touchpoints.staged_report`) refuses until a cue
   naming the dependants is on record, and its own test opens the gate with
   that cue still open and unmarked. The marks and the verdict stay the
   agent's and the human's; the open cue is re-listed in every digest until
   answered. Wording, a stricter gate, or both.
3. **The discovery route.** The operator's own proposal from that session:
   identification before classification, seven stages, the initial account
   fixed before any coaching.
4. **F2–F5.** The regulatory domain's Notion ritual (F2 connector binding, F4
   recovery between page creation and receipt), the engineering and overview
   clones' import routes needing deliberate trust grants (F3), and a derived
   evidence view (F5).

## Decision

1. **Fetch and merge here.** The review joins `main` from the local clone;
   index conflicts resolved by rebuilding, never by choosing a side. The push
   stays the operator's.
2. **F1 — fix the wording, keep the gate.** The README ("Shown" bullet and
   FAQ) and `docs/limitations.md` now say what the floor enforces: the commit
   is refused until a recorded question names every dependant, and that
   question is held open at every session start until it is answered. The
   floor cannot verify a walk it did not make; requiring the marks would prove
   only that a checklist was filled. The deliberate design stands
   (`the-verdict-is-asked-where-the-change-lands-2026-10-05`,
   `unattended-cue-carrier-2026-09-12`).
3. **The discovery route — not now.** It stays a proposal inside the review
   record, with its brief and its success test, unimplemented. A future cold
   read, when commissioned, excludes both this review and the 2026-10-17
   comparison from its first pass, as the review itself prescribes.
4. **F2–F5 — dispositions only.** F2 and F4 are the regulatory domain's to
   fix in its own procedure (operation identity, durable receipt, lookup
   before retry); a framework rule for partial-completion recovery grows only
   on cross-corpus convergence (`operating-model.md`). F3 waits on the
   operator's own trust grants in those clones — never granted automatically.
   F5 is noted on `public-docs-face-build` as a further derived view over the
   framework map, not built.

## Consequences

- One commit carries this record, the F1 wording, the eval-plan correction and
  the F5 note; the indexes are regenerated with it.
- The README's lead claim is unchanged — a model never settles "is it still
  true" silently — because the recorded question, not the mark count, is what
  makes the change unsilent.
- Nothing else in the review becomes work without a further ruling.
