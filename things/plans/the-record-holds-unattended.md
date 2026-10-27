---
id: the-record-holds-unattended
type: plan
status: in-progress
version: 1.0
created: 2026-10-27
priority: high
tags: [unattended, pause, refresh, heartbeat, sensors, estate, floor, seat-protocol]
informed_by:
  - id: llm-driven-systems-manifesto
    commit: 992bf04ddf69bc44bd8ef7d16985c7dc0e2cfe6d
  - id: closed-loop-operating-state
    commit: 992bf04ddf69bc44bd8ef7d16985c7dc0e2cfe6d
triggers:
  - type: time
    condition: "2026-11-24 reached"
    action: "surface — has one paused workspace been brought current by an unattended run and resumed at zero cost (Phase 1's Done line), and does every session start in any repo now say when the dispatcher last filed (Phase 2)? If neither, name what the operator's attention was pulled to instead; this plan exists because that pull is the standing condition, not a surprise. Re-date once answered."
linked_things:
  - id: llm-driven-systems-manifesto
    relation: implements
    notes: "The Accumulation section's second commitment, made operative: a workspace set down costs nothing to set down and nothing to pick up; its silence is distinguishable from a stopped process; its declared dates reach the operator without a session opening."
  - id: closed-loop-operating-state
    relation: extends
    notes: "That plan built the dispatcher and armed the dead-man as a dated trigger read at the operator's own session cadence — 'the chase pattern, not a monitor', by its own words. Phase 2 here gives the silence a mechanical line at every session start in every repo, which the chase could not."
  - id: cohesiveness-sensors
    relation: extends
    notes: "Completed 2026-10-20 at domain radius. Phase 3 here is its continuation one radius out: the estate measurements a session produced by hand on 2026-10-24 — the exact re-performance of mechanical checks by reasoning that the floor exists to end."
  - id: domain-refresh-specification
    relation: extends
    notes: "Refresh today is an attended act per domain: regenerate the managed blocks, commit. Phase 1 makes a paused domain's debt zero — drift is measured against the pin the domain declared, and the unattended run performs the regeneration the spec already names as deterministic."
  - id: cue-carrier
    relation: references
    notes: "Phase 4 files the one question this plan may not settle: the gate checks that a cue exists, not that it is answered. That plan's Phase 7 ruled the walk runs on detection; the cue's persistence rule says it may wait. Both are specified; the floor enforces the weaker. The operator rules."
  - id: standing-watch-specification
    relation: references
    notes: "The doorbell. Phase 2's outward half is a watch armed on the dispatch digest's age — the condition declared, the floor polling the remote, the operator woken — with no new mechanism."
  - id: framework-upward-signal
    relation: complements
    notes: "Paused; its aggregation line is the same read Phase 3 makes, with the opposite subject — that plan asks what the domains say about the framework, this one asks what the estate's own health signals are. Neither builds a registry."
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: implements
    notes: "Phase 1's refresh lands at the pin bump — one deliberate change with its cue — never as a sweep across paused domains."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: informs
    notes: "Every line Phase 3 emits is quiet when healthy. A heartbeat that prints 'quiet' daily is a line the operator learns to skip; it prints only when silence exceeds the cadence."
  - id: judgement-checks-need-a-suppression-list-which-is-itself-drift
    relation: informs
    notes: "The admission gate for Phase 3: each measurement is keyed to a same-builder source (git log, frontmatter, the floor's own evaluations). None needs an allow-list to stay quiet."
  - id: the-record-answers-the-direction-question-first
    relation: supports
    notes: "The session that wrote this plan predicted the operator's choice from the session's own record at better than 95% by the operator's reckoning. The record answered; the plan is what the record asked for."
---

# The Record Holds Unattended

One person's attention is always pulled elsewhere. Between 26 and 28 August
2026 eight of fourteen workspaces went quiet, and they lost nothing — ids
stable, links intact, exit conditions still declared. That is the
accumulation half of the manifesto's second commitment, demonstrated. The
other half failed in three places, and this plan is the three places:

- **Pausing accrued debt.** A one-line note in a paused workspace was refused
  by coherence in four of them on 2026-10-25, because the framework had moved
  from 3.31 to 3.50 beneath them and their generated blocks had drifted. The
  resume cost was the regeneration, the commit, and the walk — paid by the
  session that only wanted to leave a note.
- **Silence was indistinguishable from death.** The dispatcher's tick last
  filed a digest on 2026-10-15 and died on an expired OAuth session on
  2026-10-22. Nothing said so until a session at the framework root read the
  dead-man five days later. The dead-man is a dated trigger read at the
  operator's cadence — it chases, it does not monitor.
- **The measurements were made by hand.** The same session measured, by
  reasoning over fourteen repositories: maintenance share of commits (6% in
  the busiest, 41–69% in the small ones), import-pin lag (no pin at its
  source head; 34–1,370 commits behind), fired-trigger backlogs (42 and 100,
  most older than a month), cue precision (38% where measured), and the
  openness of insights, conflicts and plans (90%, 59%, 54%). Every one is a
  git or frontmatter fact. The floor's own rule — never re-perform a
  mechanical check by reasoning — was broken because the floor had no surface
  that performed it.

Three phases build what is missing; a fourth files the one question that is
the operator's. Nothing here scopes what a workspace is for. All of it is
about whether the foundation keeps its own commitment when nobody is looking.

## Current state (honest, evidenced at 992bf04)

- `mdllm domain-kernel` regenerates a domain's managed blocks with the
  *running* framework and `mdllm coherence` refuses the commit when the bytes
  differ. `framework_version_seen` governs only the *behind* guard (a clone
  older than the blocks). So a domain pinned at 3.31 is refused the moment
  the clone beside it runs 3.50 — the substrate's motion is the domain's debt.
- `dispatch-loop` v1.6 step 8 already permits an unattended run to regenerate
  a stale generated artifact when the floor prints the command, commit it
  alone, and continue. It has never done so for a domain-kernel block because
  no run has reached a paused domain since the tick died.
- The dead-man lives as a dated trigger on `closed-loop-operating-state`,
  answered twice (2026-09-15: switched off, no record; 2026-10-08: ticking).
  `estate-sync` walks every local clone at every session start in every repo
  and reads nothing about dispatch.
- `mdllm estate-check` batches `imports-check` per consumer, stdout only, no
  persisted artifact — the doctrine this plan keeps. It reports the membrane
  and nothing else.
- `mdllm watch` exists and reads the remote ref for a declared condition; no
  watch is armed on anything in the estate today.
- The commit gate (Claude Code `PreToolUse`) refuses a definition-surface
  change until a cue *exists* on disk; it does not read the cue's `verdict`.
  Confirmed by probe 2026-10-24 (`cue-carrier` Phase 6 observations; the
  holistic review's F1).

## Route

- [x] **Phase 0 — Define it.** This document, pinned to the manifesto at
  2.10 and dated. *Done 2026-10-27.*

- [ ] **Phase 1 — Pausing is free.** Two halves, both in the floor. *(a)
  shipped 2026-10-27: `pin_behind` in the domain-kernel module; coherence
  reports a behind pin's differing blocks as Info, `domain-kernel --check`
  prints `PIN-BEHIND` and exits 0; three tests; `domain-refresh.md` 1.7 →
  The Pin Governs Drift. Live at ship: three workspaces (3.36–3.41 pins)
  went from DRIFT-refused to PIN-BEHIND on the same bytes. The version-named
  renderer was not needed — the fallback the phase named is the design. (b)
  written into `dispatch-loop` 1.7 as the narrow allowance's sibling —
  regenerate, never seal — and unexercised: no run has entered a paused
  domain since the tick died.)*
  *(a) Drift is measured against the pin.* `coherence` compares a domain's
  generated blocks to what the framework version the domain declares
  (`framework_version_seen`) would generate, not what the running framework
  would. A domain at 3.31 is coherent at 3.31 until it bumps its pin; the
  bump is one deliberate change — `refresh: absorbed framework v…` with its
  cue — exactly as `domain-refresh.md` already describes, now the *only*
  moment debt is paid. Requires the generator to render for a named version;
  if the renderer cannot (templates not versioned), the fallback is that
  coherence reports pin-behind as Info, never Error, in a domain whose pin is
  behind the running version. *(b) The unattended run pays it.* When the
  dispatcher enters a domain whose pin is behind, it performs the refresh the
  spec names as deterministic — regenerate, commit alone naming the run,
  raise the cue, file it to the seat — so a paused domain is current before
  its operator returns. Depth-limit, scope and stop-condition unchanged.
  *Done when:* a paused workspace accepts a one-line commit with no
  regeneration, and a run brings one current with the resume costing the
  operator a read of the cue and nothing else.

- [ ] **Phase 2 — Silence is distinguishable from death.** *(a) shipped
  2026-10-27: `dispatch_silence` in the sync module reads the newest
  `type: dispatch-digest` across the clones this machine holds — from a
  workspace, through its `framework_root` to the estate — and judges the age
  against the cadence the digests themselves show (median gap of the last
  six; silent past twice it); `estate-sync` prints the one line first among
  the attention lines, in every clone, only when silent. Live at ship: "last
  digest 12d ago, cadence observed 2d — silent". Four tests. (b) built as
  `estate-sync --silence-exit` → exit 5 rather than as a `watch` condition:
  the watch is keyed to workflow boards on a remote ref, and a silence read
  needs the digests' dates, which live in the clones; a scheduled task on
  the operator's machine running the flag is the ring, and arming it stays
  the operator's act. (c) filed on `closed-loop-operating-state` as the seat
  item, three options, no recommendation.)* *(a) The line.*
  `estate-sync` already walks the clones; it reads the newest
  `dispatch-digest` across them and emits one line at every session start,
  in every repo — *only* when the age exceeds the declared cadence (daily
  plus one day of grace): `dispatch: last digest N days ago (cadence daily) —
  silent`. Quiet when healthy. The dead-man trigger on
  `closed-loop-operating-state` keeps its question; this line is what makes
  the question reach a session in any repo rather than waiting for one at
  the root. *(b) The ring.* A `mdllm watch` armed on the same condition
  against the remote — the digest's age on the pilot repo's published ref —
  so the operator is woken on their own surface when no session opens at
  all. The watch is the operator's to arm (it is a standing process on a
  machine of theirs); this plan supplies the condition and the exit code.
  *(c) The credential.* The tick dies on an OAuth session the operator must
  renew by hand. Record, as a seat item on `closed-loop-operating-state`,
  what an owned credential for the run would be and what it would cost; do
  not build it here — it is an irreversible grant and the operator's.
  *Done when:* a session in any domain says the dispatcher is silent within
  a day of it going silent, and the operator has been rung once by the watch.

- [ ] **Phase 3 — The measurements are the floor's.** Extend `estate-check`
  with a `--health` read, per repo, stdout only, no artifact, ranked when
  loud and silent when not: maintenance share (commits in the window whose
  changed paths are only generated or index paths ÷ all commits, 30d and
  90d); fired-trigger backlog (count, oldest age); retrospective age (already
  a validate Info — reuse); open ratios for insights, conflicts and plans
  with the thresholds `retrospective.md` already names (~20 insights, ~10
  conflicts since the last retrospective); cue precision (answered cues ruled
  not-inflection ÷ answered); dispatch-digest age (Phase 2's line, same
  source). Each keyed to git or frontmatter; none admits an allow-list. The
  session-start digest gains nothing — this is a read the operator or a
  retrospective asks for, and a line too many at t=0 is skimmed. *Done
  when:* every figure in this plan's opening can be reproduced by one
  command, and the 2026-10 framework retrospective cites the command, not a
  session.

- [ ] **Phase 4 — The gate question, filed to the seat.** The gate demands
  that a cue exist; the spec says the walk runs on detection and is sealed
  in the same commit; the cue's persistence rule says the question may wait
  until answered. Three readings are each specified somewhere: *(i)* the
  gate reads the verdict and refuses an unanswered cue — the walk is sealed
  or the change does not land; *(ii)* presence is enough at the gate and the
  digest's re-listing is the enforcement — what runs today; *(iii)* presence
  is enough for an unattended seat and the verdict is required for an
  attended one — the seat decides. File this as a `type: conflict` between
  `change-reconciliation-specification` and the cue's persistence rule, the
  three options stated, `status: open`, no recommendation in the record.
  Nothing in Phases 1–3 waits on it. *Done when:* the conflict is on record
  and listed at session start; its resolution is the operator's and is not
  this plan's.

## What this plan refuses

- A registry. Phase 3 reads local clones the way `estate-sync` does — a
  filesystem fact — and persists nothing. A domain still cannot enumerate its
  consumers.
- An automated writer across paused domains. Phase 1(b) runs under the
  dispatcher's existing depth limit, scope and stop condition, one repo at a
  time, and does only what the floor prints the command for.
- A line at every session start that is always there. Phase 2(a) prints
  when silent, not when quiet.
- Any statement of what a paused workspace is *for*. Its operator paused
  it; the record says only that it is held.

## Done when

- [ ] A paused workspace at an older pin accepts a one-line commit without
  regeneration (Phase 1a).
- [ ] An unattended run has refreshed one paused workspace and its operator
  resumed by reading one cue (Phase 1b).
- [ ] The dispatcher's silence is named at a session start in a domain, not
  only at the root, within a day (Phase 2a).
- [ ] The operator has been woken once by the watch on that condition
  (Phase 2b).
- [ ] `mdllm estate-check --health` reproduces every figure in the opening
  (Phase 3).
- [ ] The gate conflict is on record and open (Phase 4).
