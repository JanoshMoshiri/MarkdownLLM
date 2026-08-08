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
| 4 — Engineering domain | Execute its `pre-cowork-slip-domain-audit` | ✅ done 2026-08-08 — plan executed to completion under its own contract: full native coverage, one defect (as-is map at `current` with no staleness trigger) fixed; fired-trigger status lines exemplary; finding rate re-scopes the commissioning insight from "never loaded" to "never guaranteed — defects cluster where it failed to load"; 1 stale import re-adopted |
| 5 — PROM domain | Cowork-window audit | ✅ done 2026-08-08 — 10 Cowork commits sampled conformant (dated source reads, licence provenance, hypothesis labelling); 2 stale overview imports re-adopted + re-quarantined; floor green |
| 6 — Development domain | Cowork-window audit | ✅ done 2026-08-08 — 9 Cowork commits sampled conformant (annotate-not-delete honoured; one source-side edit predicted its own consumer staleness); 2 stale imports re-adopted; v3.27.0 sealed mechanically; 3 INCOMPLETEs are Drive-sourced review records, triple inapplicable |
| 7 — Career domain | Full-corpus audit — the domain was born pre-contract | ✅ done 2026-08-08 — born in Cowork but already repaired: the 01/08 + 04/08 local sessions backfilled every birth gap (prompts, boundary, gitignore, hooks) and the 25/07 session-end had corrected its own record in six places; floor 0/0/0 over 32 things; v3.27.0 sealed |
| 8 — Company portfolio domain | Cowork-window audit | ✅ done 2026-08-08 — 5 Cowork commits sampled clean; the VAT reverse-charge resolution is a model record (director determination, named human, invoice-level evidence); v3.27.0 sealed |
| 9 — Clean verdicts | Record the 6 unaffected repos' evidence basis; no entry, no edits | ✅ done 2026-08-08 — `agent-architect`, `code-architect`, `eco-essentials`, `property-ventures`, and the two private personal domains carry zero commits with the Cowork signature across their entire histories (per-repo email+offset clustering, method in Extent above). Verdict recorded on that mechanical basis; no repo entered, nothing edited |
| 10 — Prevention | Three deterministic fail-safe options, evaluated; one recommended; the v0.4.0 plugin repair tested as one candidate, not assumed | ✅ done 2026-08-08 — Option 2 (session gate at the floor) built as v3.28.0, rolled out strict to the affected domains, live-tested; v0.4.0 adapter reviewed at source and kept as workspace assembly; its live drive doubles as the gate's first field test |

## Phase 10 — Prevention: three options, evaluated (2026-08-08)

The requirement, in the operator's words: a **deterministic** fail-safe, built
for the general case — Cowork is not the last harness that will need an
adapter. The evaluation frame is the framework's own anchor taxonomy
(orchestration.md): `interpretation` < `harness-session` < `git-fs`, with the
standing doctrine that **adapters stay optional — never the difference between
working and not**. The estate evidence gathered by phases 1–9 is the test
every option must pass: in every breached session, the interpretation-anchored
controls vanished silently while every git-fs control held.

**Option 1 — the hardened adapter (v0.4.0 bootstrap), tested and trusted.**
Reviewed this session at source. It is a real improvement: bootstrap performs
estate-sync/doctor/session-start mechanically, prints a HANDOFF CONTRACT and
branch map, orders Tier-0 reading before the first write, and states plainly
that Cowork cannot fire the domain's own adapters. But its Step 2b names
itself: *"the gate with no backstop… nothing enforces this step."* It raises
the probability the contract loads; it cannot make the failure loud. And
adopted alone it inverts the adapter doctrine — the adapter becomes exactly
the difference between working and not. **Verdict: keep, as the Cowork
workspace-assembly layer; not the fail-safe.** Its live test remains owed and
is now cheap: the next Cowork session either passes the Option-2 gate or is
stopped by it — the gate is the test harness.

**Option 2 — the session gate at the floor (git-fs). The fail-safe.**
`mdllm session-start` — the command whose output *is* the contract entering
context — records a per-clone attestation in `.git/` (timestamp + HEAD;
uncommittable by construction). `mdllm validate`, which every pre-commit hook
already runs, gains a check: a domain whose schema declares
`options: {session_gate: warn|strict}` requires a fresh attestation before
any commit — absent or stale ⇒ Warning (`warn`) or commit-blocking Error
(`strict`), with the remedy in the message (*run
`python {framework_root}/tools/mdllm.py session-start .`*). Properties that
decide the evaluation: **harness-agnostic** (any future harness meets the
same wall — no adapter required, satisfying the doctrine); **deterministic**
(the failure mode of "contract never loaded" becomes "cannot commit", which
is loud in precisely the place every breached session stayed green);
**self-remedying** (the block names the one command, and that command emits
the contract); **honest about its limit** (it proves the contract was
*emitted into the session*, not that it was heeded — the residual is the
register/seed problem `assistant-register` already works, a categorically
smaller failure class than "never saw it"). Costs: one tool change + tests;
a per-domain schema declaration; a staleness window (24h) that long-lived
local clones must refresh with one command.

**Option 3 — inject, don't instruct (emission as the entry surface).**
Make the terminal act of any bootstrap the *printing of the contract itself*
(AGENTS.md + kernel) into the transcript, so reading has happened before
acting can start — the t=0 anchor evidence from `assistant-register` legs
1–7 shows injected seed text out-competes instructions to go read. Real, and
partially shipped already (v0.4.0 prints the handoff contract; session-start
emits the seed). But it is still interpretation-anchored — a competing
program at the anchor can swallow it (leg 6, lived) — and multi-domain
sessions pay its token weight per domain. **Verdict: correct as doctrine,
insufficient as the fail-safe.**

**Decision: Option 2 as the spine, 3 as what session-start's emission already
is, 1 as the per-harness convenience whose job shrinks to workspace assembly.**
This is the same composition the framework chose for the response register
(B spine / C doctrine / A optional hardening) — the anchor pattern, applied
to its own entry problem. Built and sealed this session as **v3.28.0** (the in-session seal follows
the estate's own release precedent — v3.26.1 and v3.27.0 were sealed the
same way; **publication of the public root stays the operator's deliberate
act**, `autopush: false`): attestation written by `session-start` into the
git dir, `session_gate_findings` in `validate`, 192 floor self-tests (+7),
spec coverage in validate.thing.md v2.3 shipped in the same release — the
v3.19.0 defect class does not recur in the release that closes it.
`session_gate` declared `strict` by their own commits in the seven
breach-affected domains, `warn` at the framework root; the gate was
live-tested (attestation removed ⇒ commit-blocking Error with the remedy;
session-start ⇒ clean). The six untouched repos opt in at their next
contract-loaded session — entering them without reading their contracts,
to install a contract-enforcement gate, would be the breach re-enacted as
prevention; the scaffold template now births all future domains `strict`.

**Also surfaced by this phase, not built here:**
- `framework-upward-signal`'s pre-agreed deploy trigger **has fired** (same
  defect class, three domains, one day). Un-parking it is the operator's
  scheduled decision; this sweep is itself evidence for the plan's premise.
- `imports-check`'s `INCOMPLETE` bucket conflates *unpinnable by design*
  (Drive/document-sourced, no git face) with *defectively unpinned* — the gap
  the 08/08 misreading walked through. Candidate: a declared
  `source: document`-class marker so coverage lines read honestly. Belongs
  with `mechanical-coherence-checks-backlog`.

## What would close this

Every affected repo either rectified under its own agent's contract or
carrying a recorded disposition; the six clean repos' verdicts recorded with
their evidence basis; a prevention recommendation accepted or rejected by the
operator; and the operator's open decisions listed above surfaced in one
place — taken by him, not by this sweep.
