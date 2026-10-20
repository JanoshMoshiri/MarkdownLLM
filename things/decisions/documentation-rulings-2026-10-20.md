---
id: documentation-rulings-2026-10-20
type: decision
status: made
version: 1.0
created: 2026-10-20
session: 2026-10-20
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [ruling, documentation, wording, workspace, operator, install, readme, outward-floor]
informed_by:
  - id: review-documentation-audit-2026-10-20-claude
    commit: e59e5fb1da3064ef2e158967f1e3ee1c432601dc
linked_things:
  - id: review-documentation-audit-2026-10-20-claude
    relation: derived-from
    notes: "The audit's five rulings it could not make; four answered here, the fifth (spec consolidation scale) deferred with its package."
  - id: glossary
    relation: informs
    notes: "The wording ruling lands first in the glossary: workspace, the folder, your workspaces, operator."
  - id: first-hour-guide
    relation: informs
    notes: "Package 5 rewrites it to end in one whole session."
  - id: operator-guide
    relation: informs
    notes: "Package 1 corrects its false statements now; its restructure waits for package 8."
---

# Decision: The documentation arc — what to fix now, the outward words, and the install pin

## Context

The 2026-10-20 documentation audit (`review-documentation-audit-2026-10-20-claude`)
found the documentation short of shape rather than truth, with one root cause —
the outward surface has no floor — and named nine work packages and five
rulings it could not make. The operator answered four through the native
prompt the same day and asked for the work to land on `main`.

## Inputs Considered

The audit's findings and packages; the 2026-10-05 wording rule ("workspace"
outward, "domain" inside); the record of the first non-author operator's
onboarding, where "none of the words landed: not domain, not session, not
harness, not refresh"; the release history — the install pin has not moved
since v3.32.0 because nothing ties it to a release.

## Options

1. **Scope:** the correctness pass alone; correctness plus the people-facing
   packages; everything but the spec consolidation; all nine.
2. **Install route:** re-pin by hand; generate the pin from the release record
   and gate it; replace the verified install with a plain tagged clone.
3. **Outward words:** "workspace" for the record repository with plain "the
   folder" for what you open; "project" for the repository with "workspace"
   left meaning the harness folder; keep "domain" outward.
4. **The human role:** operator; owner; driver.

## Decision

1. **Correctness plus the people-facing packages** — package 1 (every false
   statement a reader can act on), package 2 (the install route), package 5
   (the README to shape, about 150 lines; first-hour ending in one whole
   session), package 9 (the outward floor mechanised so it cannot drift
   again). Packages 3, 4, 6, 7 and 8 — the workspace contract, the
   change-reconciliation rewrite, AGENTS.md to ~110 lines, spec consolidation,
   the record layer — are the next arc.
2. **Generate the pin.** The install block names the newest `release:` commit
   and its installers' hashes, written by the tool and drift-checked; it can
   no longer lag a release unnoticed. Version tags remain the operator's to
   push.
3. **"Workspace" outward, "the folder" for what you open.** A workspace is one
   record repository with its own entry file, skills and records; what you
   open in the agent tool is just the folder — the same folder — and the
   harness gets no term of its own in outward text. "Your workspaces" replaces
   "estate" outward. "Domain" stays the internal spec term, mapped once in the
   glossary. The operator took this on the agent's recommendation.
4. **Operator.** The one word for the human role across outward text and, in
   the next arc, the specs; driver, human and expert retire as role names.
   "Seat" stays the technical term for a clone's declared actor.

## Consequences

- The arc lands on `main` as one commit per package, each through the floor.
- The glossary carries the wording first, so the README and first-hour can use
  it without collision.
- The fifth ruling — spec consolidation scale — waits with package 7.
