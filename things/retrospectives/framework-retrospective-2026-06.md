---
id: framework-retrospective-2026-06
type: retrospective
status: complete
created: 2026-06-11
period_start: 2026-05-13
period_end: 2026-06-11
domain: markdownllm-framework
linked_things:
  - id: framework-continuity-brief
    relation: informs
  - id: framework-v3-transformation-plan
    relation: informs
    notes: "The 'What Should Change' section is operationalised by this plan"
  - id: status-vocabulary-universal-vs-domain
    relation: references
    notes: "Latent conflict surfaced by this retrospective's review"
---

# MarkdownLLM Framework Retrospective — May–June 2026

This is the framework domain's first retrospective — itself a finding: the
framework defined `type: retrospective` on 2026-05-27 and never applied it to
itself. This one covers the framework's entire life to date (v1.0 → v2.9) and
folds in the full independent review conducted 2026-06-11.

## What We Were Trying To Do

Build a self-describing specification framework where humans define domains, LLMs
reason within them, and git-versioned markdown is the persistent state — and push
specification-driven enforcement as far as an LLM can follow it. Period goals:
session memory (insights, continuity briefs), belief revision (conflicts), derived
indexes for reflexive behaviour at scale, hard hooks for integrity invariants, and
three live domains (jmtm-software in production, two scaffolds).

## What Worked

- **The philosophical core held.** "The notation changed, not the primitives" gives
  the framework a working razor; SOLID/SRP discipline transferred as literal
  application, validated by the May SRP review producing real, fixable findings.
- **The epistemics are load-bearing.** `confidence`/`origin`, conflicts as held
  tension, drift-as-Warning, "spec when foreseeable, deploy when felt" — these are
  used, not decorative.
- **Tiered loading was the right architectural move** and is empirically motivated
  (hook compliance correlates with scope, not awareness).
- **jmtm-software proves the model.** Real UK tax compliance with concrete phased
  workflows, completion signals, and escalation points. The one production domain
  is genuinely good.

## What Didn't Work

- **The enforcement gap is live, not theoretical.** All 17 things in jmtm-software
  fail validate.thing.md's Level 1 status check at Error severity, undetected —
  because the only validator is honor-system LLM reasoning. The framework's
  strictest mechanical rule was silently violated by its only production domain.
- **The spec contradicts itself on status vocabulary** (Level 1 fixed enum vs
  Level 3 domain state machines). Recorded as the framework's first conflict thing:
  `status-vocabulary-universal-vs-domain`. Notably, the domain's vocabulary is
  better modelling than the universal enum — the spec is wrong, not the domain.
- **The framework agent drifts on its own hard hooks** (documented in
  `hook-compliance-correlates-with-scope-not-awareness`), and tracking surfaces
  drifted from reality twice (`tracking-artifacts-can-drift-from-reality`).
- **The framework never used its own session-memory primitives on itself** — no
  continuity.md, no retrospective until this one. The fractal claim ("the rules
  apply to themselves") was aspirational at the process level.

## Patterns We Noticed

- **Each failure mode was answered with new prose machinery** (drift → index
  validation; missed hooks → more hook prose), which adds cognitive load — the
  documented *cause* of the failures. The corrective loop amplifies the disease.
- **Six tracking surfaces** (git log, WORKLOG, CHANGELOG, REVIEWLOG, continuity,
  insights) for one repo; each is an obligation the agent can miss.
- **Schema-coherence finding:** the `linked_things.relation` vocabulary has
  proliferated — thing.md blesses ~8 common values, but spec frontmatter across the
  corpus uses ~18 (`enforces`, `enforced-by`, `validates`, `operates-on`,
  `invokes`, `defines`, `evaluates`, `grounded-by`, `operationalises`, ...). No
  drift in meaning detected, but the vocabulary is undeclared and unvalidated.
- **Spec-to-data ratio:** ~330KB of specification prose manages ~30KB of production
  domain data. Operative rules are interleaved with rationale at roughly 1:4.

## What Should Change

Operationalised as `framework-v3-transformation-plan` (seven phases). Headlines:
a deterministic validation floor (`mdllm` CLI + normative per-domain schemas +
real pre-commit hooks); a deletion pass (CHANGELOG generated, REVIEWLOG folded
into retrospectives, prompt I/O chain validation removed); provenance as a
first-class spec (`origin: external` quarantine, pinned `type: decision` records);
a scoped session-start insight-staleness check; an operative kernel to cut Tier 0
by two-thirds; behavioral evals; then regeneration, proactive triggers, and CI.

## Open Questions Going Forward

- Where does `mdllm` live — `tools/` in this repo, or a sibling repo domains vendor?
- Should the relation vocabulary become declared-and-validated in the Phase 1
  schema, or stay emergent?
- Kernel format: one generated `kernel.md`, or delimited operative sections read
  selectively per spec?

*Reflexive scans:* conflict sweep performed as part of the 2026-06-11 full review
(one conflict surfaced, recorded); schema-coherence reviewed (relation-vocabulary
finding above); no derived indexes exist in this domain yet, so no rebuild applies.
