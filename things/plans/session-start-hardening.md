---
id: session-start-hardening
type: plan
status: in-progress
version: 1.2
created: 2026-08-19
priority: high
tags: [session-start, tier-0, emission, kernel, gates, adapters, hardening, evidence]
linked_things:
  - id: cowork-remote-phase5-evidence-2026-08-19
    relation: references
    notes: "Live remote proof of Phase 2's constraints, unprompted by this plan: the Cowork harness truncated a 76.4 KB contract emission to a ~2 KB preview (lands-whole), and the session gate accepted a marker-less attestation because it reads only the timestamp. Two defects land in Phase 2's checklist from this record."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: implements
    notes: "The plan operationalises the insight's law: content can be emitted; judgement must be pulled. The reasoning lives there and is not restated here."
  - id: a-prerequisite-declared-only-inside-its-target-cannot-gate-it
    relation: implements
    notes: "Phase 1 is that insight's named fix: lift the read gate into the kernel surface, upstream of what it gates."
  - id: session-start-loses-to-the-first-request
    relation: implements
    notes: "Executes the June directive — deliver the ritual mechanically at t=0 — at the content level it was always about."
  - id: an-honest-ledger-replicates-full-compliance-does-not
    relation: references
    notes: "Supplies the verification method throughout: evidence over assurances, the forensic probe ladder, and the smooth-yes tell."
  - id: pretooluse-action-boundary-gate
    relation: references
    notes: "Phase 5 records this plan's fork resolution: emission first; the gate stays parked with its re-open condition restated at the action boundary."
  - id: vendor-harness-adapter-foundation
    relation: references
    notes: "Phase 2 rides its projection and migration machinery and obeys its rules: per-step protected output budgets (Gate 6R) and generated-contract change as estate migration."
  - id: protecting-one-budget-displaces-the-failure-into-the-other
    relation: references
    notes: "Constrains Phase 2 directly: kernel emission through a budgeted channel must be protected or loudly degraded — silent truncation mechanically recreates the believed-loaded failure."
  - id: operating-layer-quality-loop
    relation: references
    notes: "Adjacent, distinct: that plan owns skill content quality; this one owns ritual delivery and gating. Both sequenced against the adapter workstream."
  - id: read-thing-specification
    relation: references
    notes: "Phase 1's edit target: the kernel block gains the read-side gate the write block already carries."
  - id: orchestration-specification
    relation: references
    notes: "The anchor doctrine governs every move here: hardening is moving delivery rightward without touching hard/soft."
  - id: partial-coverage-quiets-the-uncovered-steps
    relation: references
    notes: "Earned by Phase 0: the run under test articulated the masking mechanism from inside. Justifies Phase 4 — every Phase 2–3 emission deepens the quiet over the residue, so the residue gets a named invocation, never leftover pull."
---

# Session-Start Hardening

Five sessions of evidence (2026-08-18/19, two vendors, three harnesses, three
models, two effort tiers, one live domain) established the law this plan
operationalises: **content is emitted, judgement is pulled, and instructions
are heeded when the task makes them relevant.** The reasoning lives in the
linked insights; this plan is the remedy shape. Baseline evidence commits:
`2546dfe`, `c80998f`, `c692091`.

The remedy has four legs, phased below: complete the baseline (the Fable
run), fix gate *position* (read gate upstream), fix content *delivery*
(emit Tier 0, don't instruct it), and *route the pull* for the judgement
residue no delivery mechanism can perform.

## Non-goals

- No per-domain skill emission is built here. It is named as a possible
  `session_emit:` declaration and deployed only if Phase 5 evidence shows
  the skill layer still failing after the gate lift — spec when foreseeable,
  deploy when felt.
- The PreToolUse action-boundary gate stays parked. This plan resolves the
  emission-vs-gate fork in emission's favour; Phase 5 restates the gate's
  re-open condition at the action boundary where it belongs.
- No estate batch migration. Generated-contract changes are versioned and
  adopted per-domain via refresh, per the adapter foundation's rules.
- The operating-layer quality loop (skill content quality) stays its own
  parked plan.

## Phase 0 — Complete the baseline (operator-run; contract frozen)

The Fable run: Claude Code harness, Fable, **xhigh effort** (matching the
Opus 5 runs), same live domain, same probe ladder — casual grill ("are you
running as the domain agent?"), then forensic ("read end-to-end?"), then
the steps 4–6 probe. **Contract surfaces are frozen until this closes**: no
changes to kernel.md, AGENTS.md, the session-start projection, read.thing.md,
or the test domain's skills land before the run, or the five-run baseline
stops being comparable.

Pre-registered predictions (scored at the gate, not adjusted after):

- **P1** — mechanical floor consumed, digest relayed, near-certain.
- **P2** — unprompted interpretive extent ≥ the Opus 5 runs (model gradient
  within one vendor).
- **P3** — **domain skills still not loaded before first output.** The
  discriminating cell: confirms position over capability. If Fable loads
  the read skill unbidden, the gate insight weakens and capability
  re-weights the diagnosis — Phases 1–2 still proceed, but Phase 4's
  residue design re-opens.
- **P4** — honest ledger at the first forensic probe.
- **P5** — version refresh deferred as change-control, unprompted.

- [x] Run executed and transcript captured (fifth column of the evidence
  table)
- [x] Predictions scored; insights updated with the outcome (confidence
  moves recorded, either direction)

**Phase 0 outcome (2026-08-19, scored):** Fable in Claude Code at xhigh.
All five predictions confirmed. **P1** ✓. **P2** ✓ — validate and the full
trigger evaluation run unprompted, fired triggers judged, a curated
lookahead produced: clearly above the Opus 5 run in the same harness at the
same effort, giving the second clean within-harness gradient pair
(mirroring Terra < Solo). **P3** ✓, the discriminating cell: no domain
skills before first output — the invariant is now five for five — and the
kernel was again skipped under instruction-delivery at the strongest
available tier. **P4** exceeded: the ledger arrived at the first *casual*
probe, itemised, with the substitution self-diagnosed ("the tool's output
substituted for the operative rules"). **P5** ✓. Beyond the predictions:
the run articulated the masking mechanism from inside — "the adapter's
partial coverage makes the uncovered steps quieter, not louder" — captured
as [[partial-coverage-quiets-the-uncovered-steps]], now the standing
argument for Phase 4. A no-adapter control run is that insight's named
discriminating test and an optional Phase 5 cell.

**Gate: CLOSED 2026-08-19.** The scored run is committed; contract surfaces
are unfrozen and Phase 1 may begin on the operator's word.

## Phase 1 — Position: lift the read gate upstream

The one-line fix the gate insight names: `read.thing.md`'s `<!-- kernel -->`
block gains the read-side gate, mirroring the write block — before domain
read work, load the domain's read skill (its specification skill first).
This is a declared inflection on a stable spec: the operator declares it by
starting this phase; the four-beat reconciliation walk applies.

- [x] Read gate line added to `read.thing.md`'s kernel block (v2.3); version
  bumped
- [x] `mdllm kernel` regenerated (read block 311 tokens); `mdllm coherence`
  clean
- [x] Reconciliation walked: `mdllm touchpoints read-thing-specification`
  found 8 declared edges + 1 literal — all consistent under an additive
  gate; templates carry no self-referential gate text; the QMS read skill's
  own prereq is across the membrane and inherits the upstream gate via
  refresh (Phase 5 offer)
- [x] In-phase decision: the general authoring rule ("declare gates upstream
  of their target") stays carried by the insight — no write.thing.md line;
  minimal core
- [x] Gate insight promoted: `promoted_to: read-thing-specification`

**Gate: CLOSED 2026-08-20.** The kernel carries the read gate; validate and
coherence clean.

## Phase 2 — Delivery: emit Tier 0, don't instruct it

Change the generated session-start projection so the kernel arrives as
content, not as a load instruction — one change serving all three harness
routes (adapter-injected in Claude Code, bootstrap-emitted in Cowork,
agent-run or native in Codex). Constraints inherited from the adapter
foundation, named so they cannot be rediscovered the hard way:

- **Lands-whole or loudly absent.** The injection channels have character
  budgets, and Gate 6R already proved silent truncation drops orientation
  content. A truncated kernel emission mechanically recreates the Terra
  believed-loaded failure. The kernel's share is protected per-step; where
  it cannot fit, the projection must degrade to an explicit
  "kernel NOT emitted — load `kernel.md` before proceeding" line, never a
  silent partial emission. Truncation marked is not landing.
- **Emission-integrity marker.** The emission carries a trailer the agent
  and the grilling can check mechanically (kernel line count + content
  hash), so "did it land whole" stops being a memory claim. The session
  gate's honest limit is stated: attestation proves emission, the trailer
  makes landing checkable, nothing proves reading.
- **Generated-contract change = estate migration.** The managed-block
  change is versioned; the framework root adopts immediately; domains adopt
  via `refresh` on request; everything else is an offer, never a sweep.
- **Scope: kernel only.** Cost measured with `mdllm tokens` before/after
  and recorded in the changelog — not restated in prose.

- [x] `mdllm session-start` emits kernel content whole, with integrity
  trailer and loud degradation path. The default path is channel-aware:
  direct channels (manual CLI, Codex, bootstraps) emit the kernel whole
  with the trailer (line count + sha256 — the mark whose absence reveals
  truncation); the hook/runner channel, marked via `MDLLM_LIFECYCLE_CHANNEL`
  set by the runner, gets the loud checkable deferral ("Kernel NOT emitted
  — N lines, sha256 X, read END TO END") because a partial kernel, even
  elision-marked, recreates the believed-loaded failure. `--contract`
  gains the same trailer.
- [x] Budget shares verified on the largest live domain: hook channel
  5,886 raw chars with the deferral as step 1 (the runner bounds to its
  2,200 budget structurally); direct channel 22,236 chars, kernel whole,
  trailer present.
- [x] Token cost measured: the kernel adds ~18,000 characters (~4,250
  tokens, `mdllm kernel`'s own figure) to big-channel session starts;
  framework-root direct emission measured at 18,056 chars. The hook
  channel is unchanged at 2,200 chars.
- [x] The gate now reads the marker the emitter writes: the attestation
  carries a kernel token (`whole:<sha>:<lines>` / `deferred` / `elided` /
  `absent`); `elided` and `absent` surface as Warnings in **both** modes —
  never a strict Error, because the remedy (read the named file in full)
  is evidence the floor cannot receive, and a commit-block the session
  cannot clear is a dead-end gate. The remedy text and docstring now name
  what actually emits. Legacy attestations carry no token and stay silent.
- [x] Receipt path for preview-truncating harnesses: `--contract` also
  writes the full emission to `<git-dir>/mdllm-contract-emission.md`
  (uncommittable by construction) and names it in-band — recovery is one
  file read on any harness, no manual surgery. Chunked emission was
  considered and rejected: chunk thresholds are harness-specific; a file
  read is every harness's native full-content channel.
- [x] Migration: none triggered, by construction — the runner marks the
  channel via environment, not argv, so rendered hook configs and their
  definition hashes stay byte-identical estate-wide. Domain-side prose
  (managed blocks still instructing the kernel load) rides the versioned
  refresh offer in Phase 5, per Gate 7.0's migration-boundary rule.

**Gate: implementation closed 2026-08-20; acceptance PENDING OPERATOR
RUNS** — a fresh session in each of the three harnesses showing the kernel
landed whole (trailer verified) or loudly deferred, with no silent
truncation on the largest domain. Suite green at commit (12 emission tests
+ full run; four pre-existing tests updated where the old expectations
pinned the instruction-era output).

## Phase 3 — Digest: compute the computable cores of steps 4–6

Every cue the digest emits is a pull-router — the evidence shows emitted
cues get judged (all five sessions deferred the version refresh unprompted)
while un-emitted duties get skipped. Move the computable cores of the
orientation walk into the floor's output:

- [ ] Velocity as week-over-week trend buckets, not a 30-day total (the
  85→16→9 deceleration the flat total masked)
- [ ] Stall-line findings surfaced by the floor: critical/high non-terminal
  things past the velocity prompt's 21-day line, named per thing
- [ ] Self-answering armed triggers: an armed future-dated trigger whose
  action text answers its own condition (the do-not-re-ask pattern) → Info
- [ ] Dead-trigger candidates only if a mechanical test exists; otherwise
  the check stays judgement — label the act, not its net
- [ ] Session-start prompts updated to consume the computed signals rather
  than recompute them; the judgement residue in each prompt shrinks to what
  is genuinely semantic

**Gate:** the digest shows each new signal on a fixture where it is
known-present; prompts reference the computed output.

## Phase 4 — Residue: route the pull, reconcile the two voices

What remains after Phases 2–3 is judgement no channel can perform. Decisions
this phase owns:

- [ ] The deep orientation walk becomes explicitly invoked (session-end
  symmetry — a bound prompt the operator or the agent deliberately
  triggers), and/or intent-scoped on the first substantive request; the
  entry file stops demanding un-pulled judgement at t=0 and names the
  invocation instead
- [ ] The two-voices collision is resolved in prose: Tier-0 emission is not
  subject to the tier-economy rule (emitted content requires no loading
  decision); the economy rule governs Tier 1/2 only. The Codex first-grill
  defence must have nothing left to recruit
- [ ] The forensic probe ladder (casual → end-to-end → steps 4–6) is
  recorded as operator verification practice in the operator guide —
  evidence over assurances, the smooth-yes tell named

**Gate:** AGENTS.md, kernel, and the projection agree with each other;
reconciliation walked; no surface still instructs what another surface
emits.

## Phase 5 — Re-test, disposition, seal

- [ ] Probe ladder re-run on at least two harnesses (one Claude, one
  non-Claude) against the changed contract; results scored against the
  five-run baseline
- [ ] `emitted-content-is-read-instructed-content-is-economised`
  dispositioned per its own dismissal condition (promoted if content-level
  variance is gone)
- [ ] `a-prerequisite-declared-only-inside-its-target-cannot-gate-it`
  promoted (Phase 1 is its fix landing)
- [ ] `pretooluse-action-boundary-gate` updated: fork resolved-for-now in
  emission's favour; re-open condition restated — if post-emission variance
  persists at the *action* boundary, the gate is the next rightward move
- [ ] Per-domain skill emission decision made from evidence (build only if
  the skill layer still fails post gate-lift)
- [ ] CHANGELOG entry; framework version bump; refresh offered per
  migration rules

**Exit:** the next cold session in any harness starts with Tier 0 landed
whole, the read gate visible before read work, the computable cues in the
digest, and a named invocation for the judgement residue — and a grilled
session's ledger shows gaps only where judgement was genuinely never
pulled.
