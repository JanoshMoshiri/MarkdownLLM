---
id: vantage-brief-cluster
type: plan
status: in-progress
version: 1.0
created: 2026-08-05
priority: high
tags: [membrane, imports, orientation, watched, provenance, cross-domain]
linked_things:
  - id: provenance-specification
    relation: implements
    notes: "Asks 2 and 4 make imports-check tell the truth about why a mirror is flagged — a pin false-STALEd by a YAML type coercion, and a pin-move with no crossable change, both currently prescribe the re-quarantine ritual that spends the human's attributed flip for nothing."
  - id: session-memory-specification
    relation: implements
    notes: "Ask 1 changes the orient view's forward computation: a mirror's status is the source's state restated, not this domain's forward work. Same defect-shape as v3.19's terminal_statuses (steady-state things counted as open work), one membrane out."
  - id: substrate-currency-sweep
    relation: references
    notes: "The preceding correction pass. This plan executes the build brief pulled from a regulated estate's vantage domain porch the same day."
---

# Vantage Brief Cluster — the watched line, and the membrane telling the truth

## The finding (external brief, 2026-08-05)

A regulated estate's vantage domain (thirteen consumer/producer repos, ~100
imports at its largest consumer) exposed a build brief on its porch for the
framework to pull: four asks and one observation, each carried with evidence
and re-verified on the day of writing. Pulled and walked 2026-08-05. The
operator ruled: build asks 1–4; record the observation unbuilt.

1. **Watched is not owned.** `_orient_forward()` counts any non-terminal,
   non-knowledge-type thing as an open loop — `origin` never enters the
   computation. A consumer domain's imported mirrors therefore inflate its
   open-loop count in proportion to how *well* it consumes: the estate's
   measurement moved 58% → 81% distortion within one session purely by
   landing the imports it was ruled to take. An orientation figure that
   degrades when the membrane improves measures the wrong thing.
2. **An all-digit pin false-reports STALE against itself.** YAML parses an
   unquoted all-digit short hash (`source_commit: 2399917`) as `int`; the
   face pin is `str`; `current != pin` fires; a healthy import is prescribed
   re-quarantine. Hit independently by two estate domains eight days apart,
   each fixed locally with no shared knowledge — and **the framework's own CI
   hit it hours after the brief named it** (three imports tests share one
   commit hash on CI runners; ~1/16 of runs mint it all-digit; all three
   flake together). ~1 in 16 short hashes qualify.
3. **The expose-at-creation step** (approved 2026-07-28, re-verified
   unlanded): `write.thing.md` never asks "does another domain need to rest
   on this?" at the write. Retrofitted exposure arrives as a cliff (3 → 50
   exposed in one sweep, porch unread for days); per-thing exposure arrives
   as a trickle.
4. **Two stale species, one label.** A source-side commit touching only a
   mirror's `triggers:` block moves the pin with no crossable change —
   `imports-check` reports the same STALE and prescribes the same
   re-quarantine as a real content change. Verified absent from `tools/`
   before building (the brief's own instruction).

## Phases

| Phase | Scope | Status |
|---|---|---|
| 1 — Pin comparison honesty (Ask 2) | `imports_check` normalises both sides of every pin comparison to `str`; deterministic regression test with an unquoted all-digit pin; un-flakes CI | ✅ done |
| 2 — The watched line (Ask 1) | `_orient_forward()` partitions non-terminal things by `origin: external` → `Open loops (n)` + `Watched (n)` as separate lines; exclusion not hiding; fired triggers on watched things re-enter attention | ✅ done |
| 3 — Expose-at-creation (Ask 3) | `write.thing.md` v2.2 gains the authoring-time exposure question (yes / no / not-yet-with-condition); kernel block updated + regenerated | ✅ done |
| 4 — Stale species (Ask 4) | pin moved + face body identical → `stale (content identical)` (re-pin, no re-quarantine); body differs → `stale (content changed)` (ritual stands); `estate-check` display follows via shared renderer | ✅ done |
| 5 — Release v3.27.0 | CHANGELOG, three version sentinels, kernel + indexes regenerated, examples re-pinned, full suite green | in progress |

## Ruled out of scope / recorded unbuilt

- **`mdllm import` (the observation):** no command helps *create* a mirror;
  the estate hand-authored 69 in one session (26 malformed on first pass, all
  caught at the boundary). Recorded here as a weighed candidate — the
  mechanical shape (read face, strip relational graph + triggers, stamp the
  triple, quarantine, declare type) is real, but it is one estate's session
  pattern so far. Revisit on second independent sighting, per the estate's
  own convergence rule.
- **Consumer-side sequencing is the consumer's:** the estate's refresh-and-seal
  sweep must run with all its domains loaded — their constraint, noted, not
  ours to schedule.

## Success criteria

- The three flaky imports tests pass deterministically; a regression test
  pins an all-digit hash on purpose.
- A consumer corpus with imported mirrors reports owned and watched counts
  separately; the owned count matches hand-count.
- `write.thing.md` (and its kernel block) carry the exposure question.
- `stale (content identical)` and `stale (content changed)` appear in
  `imports-check` and `estate-check` output, correctly discriminated by test.
- Full suite green; validate + coherence clean; framework root left unpushed
  for the operator's deliberate release.
