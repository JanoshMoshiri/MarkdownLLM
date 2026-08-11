---
id: review-loop-2026-08-10
type: artifact
status: stable
version: 1.1
created: 2026-08-11
linked_things:
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: informs
    notes: "This record is that insight's evidence base — the protocol, the per-round table, and the fix-residue curve it reasons from."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: informs
    notes: "The same run read at the economic layer: the record's decay curve is what the operator's cost question converted into a stop."
  - id: coherence-mechanism-build
    relation: informs
    notes: "The plan the loop's results produced — Phase 1 (derive) and Phase 3 (flow probes) are both direct reads of this record's control group and its one executable probe."
---

# The Review Loop — an experiment record (2026-08-10 → 2026-08-11)

**What this is:** the record of a deliberate experiment, commissioned by the
operator after the v3.30.0 substrate reconciliation: run cold, adversarial,
tier-order coherence reviews in a loop — fresh unprimed reviewer each round,
verify every finding against the files, fix what's confirmed, relaunch against
the fixed HEAD — and see whether the loop converges on a contradiction-free
substrate. **It does not, and the measured reason why is this record's
finding.** (Ordinals deliberately unminted — a concurrent external review had
raised an ordinal collision; the estate settled it by practice on 2026-08-11,
both records identified by date and kind. Rounds are numbered within this loop
only.)

## Protocol

Each round: one independent agent, zero session context, barred from
`reviews/` and `things/` until after forming its own findings. Brief: walk the
substrate in load order (entry files → kernel → Tier 1 → Tier 2 →
cross-spec closure against the tool code, templates, docs, examples), severity
weighted by how early in the load path a contradiction is crossed. Between
rounds: every finding re-verified against the files by the commissioning
session; confirmed findings fixed and committed under the floor; the estate
regenerated wherever a generator string changed. Termination rule as
originally stated: two consecutive dry rounds — amended after round 5 (core
stays clean), voided by round 6 (kernel finding), and finally superseded by
the operator's ruling after round 8: **stop; the loop is the finding.**

## The data

| Round | Confirmed findings | Core (entry/T0/T1) | Of which fix-residue of earlier rounds | Character |
|---|---|---|---|---|
| 1 | 6 (+2 minor) | 4 entry | 0 | Entry-file enums, catalog statuses, generator self-contradiction, unrouted specs, tool docstrings |
| 2 | 7 | 2 | 0 | Type inventory, guide restatements, severity misassignment, frontmatter-less routed doc |
| 3 | 6 | 5 | 0 | Priority/relation enums, pre-write doctrine split, stale hook census, anchor-label inversion |
| 4 | 6 | 3 | 1 (of round 3) | Generator step-3 anchor residual, example schema comment, map counts |
| 5 | 7 | 0 | 1 | Outer ring only: README figures + self-contradiction, design record, ritual step, field example |
| 6 | 4 | 2 | 0 | Kernel anchor example (label the act, not its net), operator-guide hook count, summaries ending early |
| 7 | 3 (+2 minor) | 2 | 1 (of round 6) | session-end double definition, census cell sibling, mechanics-vs-discipline claim |
| 8 | 3 (+3 minor) | 3 | **3 (of rounds 6–7)** | Entirely fix-residue: template sibling, same-file restatement siblings |

Totals: **44 confirmed findings** across 8 rounds (41 fixed in-loop, 3
round-8 residues fixed at close), zero findings disputed after verification,
floor (validate + coherence + 282 self-tests) green after every fix commit,
two estate-wide regenerations of the generated domain blocks.

## The three measured results

**1. Author-blindness is real and large.** The v3.30.0 reconciliation was
itself a full-substrate sweep by a capable agent; the loop then found 44
further contradictions the author's walk could not see — including in lines
adjacent to the author's own edits (round 3 found two enum lines in the same
block round 1 had fixed a third line of). Cold reads and author walks catch
substantially disjoint sets. This replicates the estate's standing
`an-honest-ledger-replicates-full-compliance-does-not` posture at the review
level.

**2. Value decays; severity decays faster than count.** Raw counts fell
slowly (6→7→6→6→7→4→3→3) but the character shifted decisively: rounds 1–3
found defects that had shaped real field behavior (the fired/upcoming
mislabel, the gate cry-wolf, the routing gap, doctrine splits); round 5 found
zero core defects; rounds 7–8 found label precision and fix scatter. Constant
cost (~330k tokens/round) against decaying value: the loop's economic case
ends around round 3 — exactly the operator's read.

**3. Prose fixes scatter, and the loop converges on its own residue.** The
decisive result. A fact restated on N surfaces, corrected on k of them,
leaves N−k live contradictions *now split against the correction* — and
nothing enumerates the siblings, so every multi-surface prose fix carries
residual probability. Measured: fix-residue was 1 of 6 findings in round 4,
1 of 3 in round 7, and **3 of 3 in round 8**. By round 8 the loop was no
longer measuring the substrate's original drift; it was measuring the
incompleteness of its own corrections. A loop whose fixes are made of the
same material as its findings cannot terminate — it can only decay into
self-measurement.

## The conclusion the data forces

Looping is a **measurement instrument, not a resolution mechanism**. The
defect class — hand-restated facts with no mechanical owner — is not
reviewable out of existence, because corrections to restatements are
themselves restatements. The resolutions, in order of strength:

1. **Delete the restatement** (defer to the authority by reference) —
   removes the surface entirely.
2. **Derive the restatement** (generated blocks, mechanical censuses) — the
   loop's evidenced-consistent lists show derived surfaces held clean in all
   eight rounds while hand prose never did.
3. **Check the restatement mechanically** at the commit boundary — the
   `mechanical-coherence-checks-backlog` build (routed at high priority by
   `external-review-response-2026-08-10` R1/R2), which would have prevented
   or caught roughly three-quarters of all 44 findings, including all of
   round 8.
4. **Cold reads as periodic cadence, not loop** — the measured answer to
   that plan's open R3: one cold read after a substantial release earns its
   cost (rounds 1–3 prove it); a loop past that point does not.
5. **Flow probes for what reading cannot see** — the highest-confidence
   verification of the whole exercise was executable (the fresh-clone doctor
   probe), not editorial. The execution layer needs scenario probes, not
   more prose reviews.

## Honesty notes

- All eight reviewers were the same model family under near-identical
  briefs; shared blind spots are possible, and the consistency of their
  "evidenced-consistent" lists is not fully independent replication.
- The fix commentary applied during the loop added explanatory annotations
  to corrected lines — new hand prose, i.e. new restatement surface. Future
  corrections should prefer deletion/derivation over annotation; parts of
  this loop's own fixes are tomorrow's drift candidates.
- Round-8 minors deliberately left unfixed and logged here rather than
  chased: framework-discovery's startup ordering (explicitly deference-routed),
  the `domain/`-vs-`domains/` characterization drift, read.thing.md's missing
  kernel-suffices qualifier, operator-guide's v2.9/v3.4 framing line.
