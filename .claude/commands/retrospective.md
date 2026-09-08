---
description: Periodic domain retrospective + the reflexive sweeps it binds — conflict scan and triage, reconciliation, insight consolidation, schema/skill coherence — operator-invoked
---

Write a `type: retrospective` thing for this domain (periodic quality reflection;
see `retrospective.md`), then run the reflexive scans that spec binds to this
ritual. `retrospective.md` → *Reflexive Scans At Retrospective* owns each scan's
definition and its number; this file is the invocation, and until 2026-09-08 it
fired three of the seven — the net beneath the net was never wired to the hand
that casts it.

1. `detect-conflicts` (scan mode; spec scan 1) — sweep every `linked_things` edge
   across the domain for contradictions;
   `templates/prompts/detect-conflicts.md`.
2. **Triage every open conflict** (spec: What A Retrospective Produces, item 3) —
   walk `things/conflicts/` at `status: open`, the whole set and not only what the
   floor aged, and force a disposition on each: rule (superseded / both-valid /
   dismissed → `status: resolved`), link it from the work that will resolve it, or
   hold it with `disposition: keep-active` + a `disposition_reason` naming what
   would resolve it. Creation runs at three cadences; this and the end-session
   brake are the two that read.
3. `review-schema-coherence` (spec scan 2) — audit the emergent frontmatter
   vocabulary for fields that have drifted apart in name but converged in meaning;
   `templates/prompts/review-schema-coherence.md`.
4. **Index rebuild** (spec scan 3) — `python tools/mdllm.py index . rebuild`.
   The floor refuses a drifted index at every commit, so this resets the
   provenance anchors to the period's end; content parity never depended on it.
5. **Change-driven reconciliation** (spec scan 4) — for every change the period
   landed without a declared inflection, run the backward pass
   (`change-reconciliation.md` → Retrospective Reconciliation): freeze a
   baseline, reconstruct the delta from `git log` over the period, assimilate each
   changed thing's affected set (`mdllm touchpoints`), walk it, and seal
   contradictions as `type: conflict` things. This is the only pass that catches
   an inflection nobody declared — including every change an unattended agent
   commits.
6. **Insight triage and consolidation** (spec scan 5) — act on the insight
   orphan findings (`validate`), then cluster `active` insights sharing two or more
   `linked_things` targets as merge candidates and judge each cluster.
7. **Conditions-met pass** (spec scan 6) — re-read every `disposition_reason` on
   the kept insights *and* the held conflicts, and rule on each condition that has
   since come true.
8. `review-skill-coherence` (spec scan 7) — read the skills and the entry file
   against the commit stream since the last retrospective and force a per-skill
   disposition (confirm-current / update / park / retire);
   `templates/prompts/review-skill-coherence.md`.

Commit the retrospective, the conflicts surfaced and the dispositions ruled, the
reconciled things, and the skill edits the dispositions imply.
