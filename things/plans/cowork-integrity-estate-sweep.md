---
id: cowork-integrity-estate-sweep
type: plan
status: in-progress
version: 1.0
created: 2026-08-08
priority: critical
tags: [integrity, cowork, harness, adapters, estate, audit, sweep]
linked_things:
  - id: framework-upward-signal
    relation: references
    notes: "That plan parked with a pre-agreed deploy trigger: 'the next same-problem-in-N-domains rediscovery'. This breach is that trigger fired — the same defect class surfaced independently in three domains of the regulated deployment in one day, and the upward path it needs still does not exist. The prevention phase must say whether this sweep un-parks it."
  - id: pretooluse-action-boundary-gate
    relation: references
    notes: "Paused plan directly relevant to prevention: a mechanical gate at the tool boundary is one of the candidate shapes for making the Tier-0 contract enforceable rather than hoped."
---

# Cowork Integrity Estate Sweep — extent, rectification, prevention

## The determination this rests on

**Stated by the operator (CTO of the regulated deployment), 2026-08-08, in
session:**

> Cowork and the adapter that spins up sessions in Cowork has not been handing
> control over to the domain agents correctly. That has led to an integrity
> breach. The system works only if AGENTS.md is the first thing read; if it is
> not read and an agent runs as its own agent, all we have is a deterministic
> floor being asked to carry a system that is not working. The breach must be
> rectified completely across the estate, and there must be a deterministic
> fail-safe so it cannot recur.

Three domains of the regulated deployment hold today's first-hand evidence,
each from its own session-end ritual on 2026-08-08: the QMS domain (session
ran with roughly half of AGENTS.md followed, kernel and all four skills
unread, imports-check never run — COVERAGE 0/101 when finally run), the
overview domain (harvest: a clean floor does not mean the kernel was read;
two domains written to before their kernel or write skill had been read), and
the engineering domain (eleven convention defects found by adversarial audit
across two same-day sessions, all fixed; plan `pre-cowork-slip-domain-audit`
opened there for the historical slice). Their committed plans (the QMS
domain's `cowork-session-integrity-extent-review`) name an estate-level
investigation neither domain owns. This plan is that investigation.

## Extent — established mechanically, 2026-08-08

Cowork sessions carry a double git signature distinguishing them from every
local session: the operator's company email as author/committer **and** UTC
committer offset (`+0000`). Local Claude Code sessions in the same window
carry the operator's GitHub noreply email at `+0100` (BST — the window is
July–August, so no GMT ambiguity); a second local machine carries the company
email at `+0100`. The discriminator was verified against commits known
first-hand to be Cowork (07–08/08 sessions in the regulated deployment) and
known local (framework phase-0 work).

**Affected — 8 of 14 repos, ~163 commits, first 2026-07-22, last 2026-08-08:**

| Repo | Cowork commits | Window | Note |
|---|---|---|---|
| regulated deployment — QMS domain | 69 | 07-23 → 08-08 | largest exposure; provenance dry run, not the signed QMS |
| regulated deployment — overview domain | 28 | 07-23 → 08-08 | includes the execution-surface tooling ruling |
| regulated deployment — engineering domain | 21 | 07-23 → 08-08 | today's writes already audited in-domain |
| a private career domain | 19 | 07-24 → 07-25 | **born in Cowork** — entire scaffolding pre-contract |
| regulated deployment — PROM domain | 10 | 07-28 → 08-06 | own private repo, programme oversight |
| regulated deployment — development domain | 9 | 07-25 → 07-28 | |
| the company portfolio domain | 5 | 07-22 → 07-27 | earliest Cowork commits in the estate |
| framework root (this repo) | 2 | 07-26, 07-28 | **the v3.19.0 release itself** and the creation of `assistant-register` |

**Unaffected — no Cowork signature in history:** `agent-architect`,
`code-architect`, `eco-essentials`, `property-ventures`, and the two private
personal domains (life and finance).

**Out of scope, with reason:** five framework commits with the GitHub noreply
email at `+0000` dated 2026-06-11 predate the Cowork adapter's existence and
match a different signature (web-UI/CI edits, not sessions); the
`user@example.com` pair in `eco-essentials` (2026-05-24) likewise predates it.

## The operating law of this sweep

Stated by the operator and binding on every leg: **the read-only scoping runs
as the framework agent; any change inside a domain is made only after reading
that domain's AGENTS.md and operating as that domain's agent.** The breach
under investigation is exactly this law skipped — the sweep must not
re-instantiate it.

## Method, per affected repo

1. Read the domain's AGENTS.md (and the skills it declares Tier-0) before
   touching anything.
2. Run the floor: `validate`, `doctor`, and whatever the domain's own contract
   names (`imports-check`, `triggers`, `touchpoints`, …) — noting that a green
   floor is evidence only of what the floor checks.
3. Audit the Cowork-window commits and the things they touched against the
   domain's own conventions — the engineering-domain plan's two-tier method
   (mechanical countables first, judgement questions second).
4. Disposition: fix defects as the domain agent; annotate rather than rewrite
   where the record was honest on its information; record genuine
   practice-differences as skill-change proposals, not breaches.
5. Commit per meaning boundary with the domain's own message conventions.

## What stays the operator's

- The QMS-domain **disclosure decision** (its management-review SOP) once its
  extent is characterised.
- Any `verified: false → true` quarantine flip (the floor rejects unattributed
  flips by design).
- The `informed_by` backfill-vs-forward sequencing call named in the
  engineering-domain plan.
- Acceptance of the prevention recommendation, and the release act for any
  framework version this sweep produces.

## What this sweep must not become

Not a rewrite of the estate's history — the engineering-domain plan's words
hold estate-wide: an audit that quietly makes the past look compliant destroys
the thing it exists to protect. And not a plugin test mistaken for an
investigation: `markdownllm-bootstrap` v0.4.0 is a forward repair and evidence
of nothing about the past (the QMS-domain plan's scope guard, carried here
verbatim).

## Phases

| Phase | Scope | Status |
|---|---|---|
| 0 — Extent scan | Signature discriminator verified; 14 repos clustered; extent table above | ✅ done 2026-08-08 |
| 1 — Framework root | Audit cd2e0f7 (v3.19.0) + 8385654 (assistant-register creation); floor run | ✅ done 2026-08-08 — one defect: `terminal_statuses` shipped in the floor with zero spec coverage; fixed (thing.md v2.17 + kernel). `assistant-register` clean — re-audited implicitly by seven contract-following legs since creation. Floor green |
| 2 — QMS domain | Agent-executable slices of its `cowork-session-integrity-extent-review` | ✅ done 2026-08-08 — gap dated (13–15 sessions from 07-23); the breach-discovery session's own imports conflict was the one record found reading differently (claimed 0/101 pinned; truth 77/101, control working) — amended with full-estate re-check; 2 stale imports re-adopted + re-quarantined; import darkness aged at 11 days; `decided_by` absence shown NOT harness-correlated; disclosure decision surfaced for the operator, untaken |
| 3 — Overview domain | Historical Cowork-window audit (today's writes already corrected) | ✅ done 2026-08-08 — consume porch 13/50 stale (content changed), all re-adopted, coverage 50/50 fresh; two re-quarantined copies owe an attributed re-flip; view re-derivation flagged, not performed; earlier Cowork commits sampled conformant (the 07-28 session ran flips attributably — the contract sometimes held by interpretation; the harness never guaranteed it) |
| 4 — Engineering domain | Execute its `pre-cowork-slip-domain-audit` | pending |
| 5 — PROM domain | Cowork-window audit | pending |
| 6 — Development domain | Cowork-window audit | pending |
| 7 — Career domain | Full-corpus audit — the domain was born pre-contract | pending |
| 8 — Company portfolio domain | Cowork-window audit | pending |
| 9 — Clean verdicts | Record the 6 unaffected repos' evidence basis; no entry, no edits | pending |
| 10 — Prevention | Three deterministic fail-safe options, evaluated; one recommended; the v0.4.0 plugin repair tested as one candidate, not assumed | pending |

## What would close this

Every affected repo either rectified under its own agent's contract or
carrying a recorded disposition; the six clean repos' verdicts recorded with
their evidence basis; a prevention recommendation accepted or rejected by the
operator; and the operator's open decisions listed above surfaced in one
place — taken by him, not by this sweep.
