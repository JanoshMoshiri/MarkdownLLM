---
id: a-degrading-command-cannot-trigger-approval-by-succeeding
type: insight
status: active
version: 1.0
created: 2026-08-18
session: 2026-08-18
source: both
confidence: high
origin: synthesised
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: informs
    notes: "Splits Gate 7.0 runtime parity from the still-unproven Codex workspace-write Git-authority leg."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "The degraded exit-zero result is the exact reason an executed harness path did not prove the freshness consequence the operator asked for."
  - id: agents-cannot-self-install-permission-bearing-hooks
    relation: complements
    notes: "Repository code cannot grant itself Codex sandbox authority; it can only emit a consequence the approval layer can route."
---

# A Degrading Command Cannot Trigger Approval By Succeeding

## The Insight

A command cannot use one exit contract for both **best-effort lifecycle work**
and an **explicitly required consequence**. `estate-sync` correctly returned
zero when automatic startup could not fetch: session start must continue from
cached state. But the same return code on an operator-requested manual rerun
told Codex that the command had succeeded, so its approval path had no failure
to route. Prose saying “retry with approval” did not change that mechanical
fact.

The reusable split is:

- keep the automatic lifecycle form bounded, degrading, and exit-zero;
- give the explicit manual form a strict option that preserves the diagnostic
  but exits nonzero when the requested consequence did not occur.

The strict option does not grant network or filesystem authority. It makes the
missing consequence visible to the harness layer that owns approval.

## Why It Matters

“Command executed” and “remote state became fresh” are different claims. A
safe fallback can prove the first while disproving the second. If a harness
only sees exit status, a deliberately successful fallback suppresses the very
approval that could complete the operator's request.

The same distinction applies beyond Git: any command that degrades for
automatic continuity needs a separate strict surface when a human explicitly
asks it to establish freshness, publication, delivery, or another externally
observable consequence.

## Evidence From QMS

- The automatic Codex SessionStart lane fetched the private QMS remote
  successfully.
- In the same restricted “Approve for me” task, the ordinary manual tool-shell
  invocation fell back to cached refs. A generic local `Permission denied`
  warning was also misclassified as `auth-failed`, even though the credential
  was healthy.
- Full Access made the authority boundary disappear: manual sync succeeded,
  and real QMS commit `ef5e820` passed the floor and published. That proves the
  remote and credential; it does not prove the middle approval path.

## Partial Plan Attached To The Insight

1. Preserve plain `estate-sync` for non-blocking automatic startup.
2. Add `estate-sync --require-fresh`; cached or unresolved state must exit
   nonzero so Codex can request one-command network/filesystem approval.
3. Classify sandbox/local permission denial separately from authentication,
   and test the mixed stderr shape that produced the false diagnosis.
4. In QMS under “Approve for me,” prove both legs: restricted strict sync
   fails visibly then succeeds when approved; a real frontmatter commit passes
   pre-commit and autopushes through the approved Git write.
5. Only after that live proof, offer the authored entry contract to other
   domains at the Phase 8 migration boundary; do not sweep the estate.

## Exposure

No downstream domain needs to import this framework-internal insight. The
operator-facing consequence belongs in shared CLI/docs and reaches a domain
through deliberate framework refresh; QMS is the live acceptance target, not
the start of an estate rewrite.
