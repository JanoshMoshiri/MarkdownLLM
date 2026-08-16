---
id: claude-gate-6r-acceptance-2026-08-16
type: artifact
status: stable
created: 2026-08-16
tags: [harness, lifecycle, output-allocation, acceptance-gate, execution-evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Independent Claude acceptance of Gate 6R at b82061f. Releases the remaining Phase 6 Codex evidence work."
  - id: lifecycle-output-truncation-2026-08-14
    relation: derived-from
    notes: "The defect this gate closes: a bounded output that kept the wrong end, dropping the head of orientation on the largest domains."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Acceptance asserts the emitted orientation content itself; exit zero, hook_success and a generic attestation were each treated as insufficient."
---

# Claude acceptance — Gate 6R at `b82061f`

**Accepted.** The output-budget defect is closed. A regulated deployment that
previously emitted only its triggers line now emits every structural section
of its orientation, inside the same bound.

## The design, cold-reviewed

`LifecycleStep` gains `protected_characters` beside `protected_seconds`, and
`LifecycleBinding` gains an output envelope and reserve. Both are floors, not
ceilings: a step may inherit capacity earlier steps did not use, while the
binding's total stays absolute. The invariants are enforced at construction —
positive budgets, a reserve that leaves model-visible output, and protected
shares that cannot exceed the application budget.

Arithmetic, re-derived independently:

| Moment | Envelope | Reserve | Available | Protected | Sum |
|---|---|---|---|---|---|
| session-start | 2200 | 200 | 2000 | estate-sync 450, orientation **1450** | 1900 |
| post-write | 2200 | 200 | 2000 | validate 1900 | 1900 |

The allocation inverts the previous failure directly: orientation — the part
that was being dropped — holds the larger protected share, and the estate
listing the smaller one.

**Compaction is structural, and that is the crux.** `_structural_sections`
splits on Markdown boundaries only: headings, blank-delimited paragraphs,
labelled runner blocks, and top-level emphasised list headings. `_fair_limits`
then water-fills a strict budget across those sections without assigning
priority, and `_bounded` retains **both edges** of any section it must cut,
marking the elision explicitly.

This satisfies the constraint the operator set when the defect was returned:

> I don't mind cutting things of no value… but just because it's not of value
> today doesn't mean it's not going to be of value tomorrow.

Nothing decides in advance which content is disposable. Every section is
represented; none is deleted by category.

**Architecture boundary holds.** The neutral runner contains no vendor or
domain-field vocabulary — verified by search for both the harness event names
and the orientation's own field labels (Version, Velocity, Open loops,
Triggers), all absent — and imports no adapter. It knows Markdown structure,
not meaning.

## Suites and floor

| Check | Result |
|---|---|
| Focused suite (runner, ports, contract, install, codex, fitness) | **128 passed** |
| Complete suite, external basetemp | **465 passed** |
| `validate .` | 197 things, 0 errors, 0 warnings, 0 info |
| `coherence .` | no issues found |
| `git diff --check` | clean |

## Live dispatch — the assertion that matters

A **fresh real Claude Code session** was opened against the largest migrated
domain, a regulated deployment. `session-start` and `harness-event` were not
invoked by hand; the record below is harness dispatch, correlated with the
harness-owned transcript.

`hook_success` / `SessionStart:startup`, emitted context **2042 / 2200
characters**:

| Assertion | Result |
|---|---|
| within 2200 characters | PASS (2042) |
| both step labels present | PASS |
| both return codes present | PASS (`estate-sync=0, session-start=0`) |
| represents estate state | PASS |
| contains Version | PASS |
| contains Velocity | PASS |
| contains Open loops | PASS |
| contains Triggers | PASS |
| truncation marked explicitly | PASS (`[truncated]` where elided) |
| `definition_current=true` | PASS |
| `execution=passed` | PASS |

Every structural section survived — steps summary, estate sync, orientation
heading, Version, Velocity, open conflicts, open loops, watched items,
triggers fired, and upcoming triggers — each bounded to its share with an
explicit marker where cut. Before this gate the same domain emitted its
triggers line and nothing else.

## Estate currency, re-derived read-only

All fourteen artifacts — framework root and thirteen domains — inspected and
preflighted, with every file hashed before and after so read-only is
demonstrated rather than asserted:

- `current=True`, `legacy_id=None`, decision `no-op` for every one;
- **zero byte changes**, including the four carrying operator-owned local
  overlays;
- no refusals, and no composite settings or overlay touched.

## Not claimed

macOS remains designed-for. Non-`startup` SessionStart sources remain
unobserved. Codex-side live dispatch in a nested domain, and the
disposable-repo adapter-removal check, remain Codex's outstanding Phase 6
evidence — which this acceptance releases.
