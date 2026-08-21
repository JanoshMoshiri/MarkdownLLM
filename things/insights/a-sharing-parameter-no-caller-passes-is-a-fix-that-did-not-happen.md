---
id: a-sharing-parameter-no-caller-passes-is-a-fix-that-did-not-happen
type: insight
status: active
version: 1.0
created: 2026-08-21
tags: [floor, partial-fix, call-sites, review, performance]
linked_things:
  - id: partial-coverage-quiets-the-uncovered-steps
    relation: complements
    notes: "Same quieting force one layer down: there the mechanised steps quiet the unmechanised remainder; here the capability's existence quiets the missing call."
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: references
    notes: "The remedy's Phase 3A structural-test requirement is this insight's mechanical answer, landed as floor-sprint-1 F9."
---

# A Sharing Parameter No Caller Passes Is a Fix That Did Not Happen

Commit `3017f64` added an optional `corpus` parameter to session-start's
consumers so four rescans of the same corpus could become one — and wrote a
comment saying the sharing existed. No caller ever passed it. The four scans
continued for two days while everyone involved, the author included,
believed the fix was in: the parameter was visible, the comment described
the sharing, the commit message claimed the win. The fix existed and did not
happen, simultaneously.

**The mechanism:** a capability added without its call site is documentation
of intent wearing the costume of behaviour. Every later reader — reviewer,
author, cold read — sees the parameter and the comment and *stops looking*,
because the surface that would normally prompt the question ("is this ever
used?") is the very surface asserting it is. The gap is quieter than an
absent fix: an absent fix leaves the slow path looking untreated; a
half-wired fix leaves it looking treated.

**Why:** behaviour lives at call sites, not definitions. A change is not the
new parameter, the new branch, or the new helper — it is the moment an
existing execution path starts flowing through them.

**How to apply:** when landing a change whose value depends on callers
adopting it, the same commit must either wire every intended call site or
add the structural test that fails while any remains unwired (floor-sprint-1
F9 is the pattern: count the scans, bound the spawns — the test makes an
unwired sharing parameter a red build instead of a plausible comment). In
review, treat "adds capability X" claims as unverified until a call site is
shown; grep for the parameter's default being overridden, not for the
parameter.

**Dismissal condition:** absorbed into doctrine if a future coherence check
or review checklist mechanically asks "which call sites adopted this?" —
at that point the insight is the check's rationale and can be marked
promoted.
