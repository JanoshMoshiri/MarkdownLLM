---
id: verified-flip-enforcement
type: plan
status: in-progress
version: 1.0
created: 2026-07-16
priority: critical
tags: [floor, quarantine, provenance, alcoa, qms-ratification, no-shadow-ai]
linked_things:
  - id: independent-review-2026-07-14-fable
    relation: implements
    notes: "Review 7's #1 under-engineered finding: the verified flip is the QMS's load-bearing control and it is an honour-system flag. Closing it before the second operator ratifies anything."
---

# Verified-Flip Enforcement

The quarantine rule (`origin: external` ⇒ `verified: false` until a human
confirms) is enforced on the *consumption* side — no decision may pin an
unverified thing (provenance.md, Error) — but the **flip itself is an
honour-system bit**: `verified: true` is frontmatter any agent can write, in
the same commit that created the content it supposedly gates. This plan makes
the flip an auditable event.

## Design stance

The floor can never verify **truth** ("did a human actually review this?") —
that is judgement, and judgement never wears mechanical clothing here. The
floor *can* verify **procedure**, because git is a same-builder event stream
that cannot disagree with itself. The fix therefore converts the failure mode
from an *omission* (a bit silently set) into an *affirmative, attributable,
visible record*: bypassing the control remains possible, but never silent and
never anonymous — which is the property an inspector actually asks for.

## The three checks

Scope: things with `origin: external` (the quarantined class — the only class
whose `verified` field the floor defines).

1. **Born-verified** (`validate`, hook-enforced). A thing whose most recent
   `verified: true` flip commit *is* its creation commit had no review window
   — verification and content arrived in one keystroke. Also fires
   pre-commit: a working-tree thing not yet in HEAD carrying `verified: true`
   is about to be born verified, and can be fixed before the commit exists.
   Healable even historically: re-verify properly (flip false → true again in
   a separate, attributed commit) and the newest flip no longer matches
   creation.
2. **Attribution** (`validate`, hook-enforced). `verified: true` requires a
   non-empty `verified_by` naming the human verifier — ALCOA "attributable",
   mechanised. `verified_by` joins CORE_FIELDS (the tool now reads it).
   Forgeable, deliberately: a false attribution is a falsifiable record a
   named human can deny, which is a categorically better failure mode than an
   anonymous bit.
3. **Session-start surfacing** (`session-start`). Every `verified: true`
   flip since the last `session-end:` commit (fallback: last 15 commits) is
   listed in the session-start block the operator already reads. Silent when
   there are none. Detection mechanical; disposition human.

## Severity policy

Warning by default; a domain opts into strictness via `_schema.yaml`
`options: { quarantine: strict }`, which raises checks 1–2 to Error (the
pre-commit hook then blocks). The QMS domain opts in; a casual domain never
meets the ceremony. Historical findings are healable (see check 1), so
strict mode cannot brick a repo on its own past.

## Admission criteria check (floor rules)

Same-builder source: git history + frontmatter, which cannot disagree with
truth about *which commit did what*. No suppression list: the only way to
quiet a finding is the remediation itself (separate attributed flip). No
judgement in mechanical clothing: the floor checks procedure, never whether
the review was real.

## Known day-one true positive

`things/insights/divergence-is-an-unrouted-decision.md` — the framework's own
MCP import from code-architect — was born verified (creation == flip ==
`5911cce`, no `verified_by`). The check's first firing is against our own
corpus; remediation (a proper attributed re-verification) ships with this
plan. The control's first catch is its own builder — recorded, not smoothed.

## Execution

1. `quarantine_findings(root, corpus)` in `markdownllm/validation.py`, wired
   into `cmd_validate`; `verified_by` into CORE_FIELDS; floor self-tests
   (born-verified fires · two-commit flip passes · attribution missing/present
   · strict escalation · uncommitted-new-file boundary case).
2. Session-start surfacing in `markdownllm/session.py` + test.
3. Remediate the day-one true positive (attributed re-verification commit).
4. provenance.md: document the flip discipline + the strict option (kernel
   regen if its kernel block changes); template comment in
   `templates/_schema.yaml.template`.
5. CHANGELOG 3.18.0 (new floor behaviour = minor) + sentinel/AGENTS bump +
   example re-pins; close this plan with outcome.

## Exit criteria

All new self-tests green (105 + new) · framework + examples validate clean
after remediation · `quarantine: strict` verified in a test corpus · the
day-one positive healed with an attributed flip in git history · CHANGELOG
records the check catching its own builder first.
