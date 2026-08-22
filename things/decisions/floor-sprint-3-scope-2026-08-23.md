---
id: floor-sprint-3-scope-2026-08-23
type: decision
status: made
version: 1.0
created: 2026-08-23
tags: [sprint-scope, floor, moscow, analysis, coherence, derivation]
informed_by:
  - id: floor-block-requirements-2026-08
    commit: efed48d7f589c8e5a29d70c87d4ebb251d7c7358
  - id: coherence-mechanism-build
    commit: b764aaf96096caeea4be3ce2a77f9b1c9d4039d2
  - id: mechanical-coherence-checks-backlog
    commit: 4569360f7460e4a2aa97d4993d8cf6c1691f5648
  - id: run-floor-sprint-2-2026-08
    commit: 4c7383b9221f8dd67748393d49de6d50b8521112
  - id: floor-structure-residue
    commit: 4cea3aa123c05a5d6c489f767ef08f5c0388fb0c
  - id: external-review-2026-08-10
    commit: 5425f29437e94240c60ce0032ca3c424fa7c1ef9
linked_things:
  - id: run-floor-sprint-3-2026-08
    relation: informs
    notes: "The run this analysis-stage decision scopes."
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: implements
    notes: "The cut follows the insight's measured order — delete, then derive, then check — rather than treating all three as one move."
---

# Decision: Floor Sprint 3 Scope

Made by the agent under the operator's execution handover. The subject was
fixed by sprint 2's seal ("Sprint 3 (derivation: F8's three phases)"); this
cut decides how much of it one sprint takes, against the requirements
ledger's v1.3 decomposition.

## The cut

**Necessity** — sprint 3 fails without these:

- **F8a** — the framework root's `AGENTS.md` stops restating derivable
  facts, in the loop insight's own order:
  - **delete** the Standard Thing Structure's restated enums in favour of
    pointers into `thing.md`/`kernel.md`. This is the one restatement with
    recorded *harm*, not just staleness: its `linked_things` line still
    advertises `related`, pruned from `_schema.yaml` on 2026-06-12, and a
    session read the line, used the relation, and took two validate
    Warnings for it. Deleting a wrong instruction outranks generating a
    right one.
  - **derive** the `## Thing Types In This Domain` section into a managed
    block. The section's own parenthetical already confesses it "restates
    `_schema.yaml` + the tool's reserved set and has lagged them", which is
    a surface asking to be generated.
  - **check** the two sections that carry authored prose around a derivable
    annotation — the spec catalog's `(type: X, status: Y)` pairs against
    live frontmatter, and the Tier-2 routing table against the `TIERS` map.
    Generation would destroy the authored one-liners that are the sections'
    actual value; a check leaves them and owns only the fact.

- **F16** — `held_by`/`held_until` admitted to `CORE_FIELDS`. Two lines and
  a test. It is in necessity for two reasons: it is `CORE_FIELDS`' own
  criterion 2 (the framework must never make a domain register framework
  vocabulary), and this sprint's run is the live instance — the framework's
  corpus, using the framework's reserved type, failing the framework's own
  field check while the sprint about coherence is open.

**Should** — taken if the sprint holds its shape. All three are F8b, and
`mechanical-coherence-checks-backlog` stays canonical on their content:

- **The boundary-term evidence check.** The most felt item in the backlog
  by its own record — three regressions, the third of which blocked four
  commits in one session and cost working time, with the blocking path
  primed to falsely refuse any commit touching `tools/tests/`. Its
  invariant is the only available control, because the list it reasons
  over must never be committed.
- **The perimeter currency check** (external review R2). The example
  `framework_version_seen` half already exists and is *firing right now* —
  both examples sit pinned at 3.33.0 against a 3.34.0 sentinel. Extending
  the same computed signal to README, `docs/first-hour.md` and
  `CONTRIBUTING.md` is the cheap completion of a mechanism already built,
  and it is the razor `cumulative-drift-is-invisible-to-per-change-walks`
  asks for.
- **The review-9 survivor promotions** that F8a does not delete. Ordering
  is the point, and it is the backlog's own sequencing fact: F8a runs
  first, so a survivor living in a section F8a deletes or derives needs no
  checker at all. Only the residue gets promoted.

**Stretch** — started only with necessity and should verified:

- **F8c probes 1 and 2** — fresh-clone boot and scaffold birth. These two
  and not the others: probe 1 is the one the plan records as having
  *already outperformed every cold read*, and probe 2 covers the flow whose
  first CI execution found 56 failures in one cause a month after the code
  was believed correct. Probes 3–5 (invariant breach, refresh end-to-end,
  session close) stay owned at `coherence-mechanism-build` for a fourth
  sprint.

**Deferred, with reasons** — not this sprint:

- The backlog's unfelt items — broken-body-reference check, install-hook
  self-test, the primitive sweep's null-result instance, the
  skills-vs-artifacts check. Their original build-when-felt hold was never
  lifted; only the review-9 promotions, the perimeter check and the
  boundary-term evidence check are felt. Building an unfelt check is how a
  floor grows checks nobody reads.
- **F2** (eval-isolation machinery) — unchanged from sprint 2's ruling.
  Its owner `evidence-and-eval-backlog` is operator-sequenced and now
  27 days stalled; a second sprint declining to absorb it is the honest
  move, and it is surfaced to the operator again at seal.
- **F14**, **F15** — unchanged: F14 carries a dated re-open condition it
  has not met; F15 widens a product config surface and needs its own
  analysis cut, which this sprint's theme does not supply.
- **Floor-structure-residue items 4 (remainder), 7 and 8** — the monolith's
  remaining banner lifts, the legacy-hook `--refresh-legacy` upgrade path,
  and the Node 20 action bump. None is derivation work. **Item 8 is
  routed to this sprint's seal as a human gate rather than deferred
  silently**: bumping `actions/checkout` and `actions/setup-python` moves
  pinned immutable trust roots, which is an authority-bound act, not a
  repair the agent makes on its own judgement.

## Why this cut

The theme is *stop restating, then catch what must stay prose*. F8a
subtracts load before F8b adds checks, which is the sequencing the backlog
itself asks for and the reason this sprint is not simply "build the
backlog". The two stretch probes are chosen for evidence rather than
order — each pins a flow that has already failed in a way no reading
caught.

The constraint every item inherits: a new check spends against **N3**
(pre-commit, root, ≤ 12s; 3.3s today), not a separate allowance, and the
verify stage re-measures N3 after the checks land or it has not verified
them.

## Re-open conditions

- If deriving the types block requires `_schema.yaml` to carry per-type
  prose descriptions, and that turns out to couple the schema to a
  presentation concern, the types block **reverts from derive to check**.
  Delete > derive > check is an order of preference, not a mandate to
  generate what a check already owns.
- If the boundary-term evidence check cannot be built without printing,
  copying or committing a term, it is dropped from the sprint rather than
  weakened — the never-committed property is the whole reason the control
  is local, and a check that leaks its subject is worse than the drift.
