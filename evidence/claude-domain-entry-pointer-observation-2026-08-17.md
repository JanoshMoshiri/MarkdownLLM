---
id: claude-domain-entry-pointer-observation-2026-08-17
type: artifact
status: stable
created: 2026-08-17
tags: [claude-code, entry-surface, phase-6, execution-evidence, ancestor-inheritance, relayed]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Evidence toward the open Claude adapter-optionality leg: the first domain-position pointer auto-load observation, plus the ancestor-inheritance finding that constrains the remaining probe design."
  - id: claude-entry-surface-unprovisioned-for-no-adapter-domains
    relation: references
    notes: "The observation this conflict's flip condition names — a scaffolded domain opened directly as its own workspace — now exists in relayed form. Disposition deliberately left with the operator; this record changes no conflict state."
  - id: claude-phase6-no-adapter-and-root-2026-08-16
    relation: extends
    notes: "That record proved the root pointer expands in root-workspace position and left the domain position unobserved; this record supplies the domain position and the second position of the root pointer."
  - id: a-missing-contract-degrades-to-semantic-drift-not-breakage
    relation: supports
    notes: "The inherited root pointer failed silently in exactly this shape: a two-line promise whose target never arrived, invisible from inside the session until the operator asked."
---

# Claude domain entry-pointer observation — 2026-08-17 (relayed)

**One positive observation, one finding.** A live Claude Code session opened
in the QMS domain (nested under `domain/`) as its own workspace received the domain's
`CLAUDE.md` pointer with `@AGENTS.md` expanded inline at t=0 — the entry file
was in model context before any tool call. The same session also received the
**framework root's** `CLAUDE.md`, inherited from the parent directory, with
its import *unexpanded* — a two-line pointer whose target never arrived.

## Provenance — graded honestly

This record is **operator-relayed**, not harness-correlated. The operator ran
the session on 2026-08-17, asked the in-session agent to report exactly what
was in context before its first action, and pasted that report here. No
transcript id, config SHA-256, or harness build number was captured. It is a
live observation — a run, not a belief — but it carries none of the hash-bound
correlation the Phase 6 first-hand records carry, and no claim below exceeds
that grade.

## The observation (as reported by the in-session agent)

Order of arrival, all before the agent's first tool call, before the
SessionStart hook output, before the user's message:

1. `MarkdownLLM/CLAUDE.md` — 167 bytes, title plus a literal `@AGENTS.md`.
   **Unexpanded**: the framework root's `AGENTS.md` (28,031 bytes) was not in
   context.
2. the QMS domain's `CLAUDE.md` — the domain's entry pointer.
3. the QMS domain's `AGENTS.md` — **full content**, expanded by the
   pointer's import.

The agent's first deliberate read was `kernel.md` — Tier-0 step 1, executed
correctly *because* the domain entry file had already arrived by injection.
The agent surfaced the unexpanded root pointer only when the operator asked
what had loaded first, and named the shape itself: the omission was invisible
from inside because the pointer is the instrument the load gets checked
against.

## Mechanism — documented harness behaviour, one inference

Pinned against the current Claude Code memory documentation
(`code.claude.com/docs/en/memory`, fetched 2026-08-17):

- "CLAUDE.md and CLAUDE.local.md files in the directory hierarchy **above**
  the working directory are loaded in full at launch", ordered root-down —
  which is why the root pointer arrived, and arrived first.
- "Relative paths resolve relative to the file containing the import" — so
  each pointer targets its own directory's `AGENTS.md`. The point-to-your-own
  design is correct and behaved correctly on both files.
- An import whose path resolves **outside the working directory** is an
  *external import*, gated behind a one-time approval dialog; unapproved
  imports stay disabled. From a domain workspace the root pointer's target is
  external; the domain pointer's is internal. **Inference, marked as such:**
  the docs state the gate for project-level memory files; that it also
  governs ancestor-position files is consistent with this observation but not
  explicitly documented. Nothing may rest on the gate staying in either
  state.

## Assessment

- **The domain entry surface works as designed.** Pointer → import → entry
  file in context at t=0, in a scaffolded domain opened directly as its own
  workspace. This is the domain-position half of the observation the open
  conflict waits on; the root-position half was recorded first-hand on
  2026-08-17 at this framework root.
- **The root pointer served a second position it was never written for.**
  The right outcome occurred — a domain session must not inherit the
  framework's own entry file — but it held only because the external-import
  gate stayed unapproved. One approval in any domain project would invert it
  silently for every later session there.
- **Neither the declaration nor the load is wrong.** Both behave as
  documented. The file was written for one of the two positions it is read
  from.

## Correction applied (committed with this record)

The root wrapper now names both positions and routes each: workspace
sessions follow the import; inherited appearances are told the workspace's
own `CLAUDE.md` → `AGENTS.md` governs and the framework root's entry file is
not theirs, whether or not the import expanded. The same wording is written
by `install.sh` and `install.ps1`, and
`test_root_wrapper_routes_both_positions_and_no_surface_drifts` holds the
three surfaces identical. Domain pointers are untouched — nothing nests
beneath a domain. `docs/estate-mechanics.md` §3 now names the ancestor
mechanic.

## What this record does not establish

- **Not the no-adapter leg.** The QMS domain carries the Claude adapter; the
  Phase 6 checkbox demands a fresh `--harness none` scaffold, first-hand.
- **The prepared probe pair no longer exists on disk** — estate, Projects and
  temp scratchpads were searched 2026-08-17; only the 5R dispatch probes
  survive. The probes must be re-scaffolded, and this finding adds a design
  constraint: the pointer-removed control must sit **out of the estate
  directory tree**, or the inherited root pointer contaminates exactly the
  surface being measured.
- ~~The corrected wrapper's live behaviour is unobserved.~~ **Observed the
  same day — see the re-test below.**
- **Whether Codex's native `AGENTS.md` discovery walks above a domain's git
  root is unverified.** If it does, it has no import gate to stop the root
  entry file loading; that question belongs to the Codex seat.
- The conflict's disposition is deliberately unchanged: the operator holds
  the call on whether a relayed observation meets its flip condition.

## Re-test after the correction — 2026-08-17 (relayed)

A second QMS session was opened after `09200dd`. The loading behaviour is
**unchanged, as predicted**: root pointer first (unexpanded), domain pointer,
domain `AGENTS.md` in full — all before the first tool call, with the
SessionStart hook output and the user message behind them. The correction was
never expected to change *what loads*; the external-import gate already
produced the right outcome. What it changed is whether the receiving agent can
account for it.

| | Pre-fix session | Post-fix session |
|---|---|---|
| Root `AGENTS.md` in context | no | no |
| Domain `AGENTS.md` in context at t=0 | yes | yes |
| Agent's account of the root's absence | *"either the declaration is wrong or the load is"* — flagged as an unresolved discrepancy, surfaced only because the operator asked | *"the routing rule in the root pointer held: nested workspace, root's entry file stayed out"* — read as correct and intended |
| Residual discrepancy for the operator | one | none |

That is the delta the correction targeted, and the phrase *"the routing rule
in the root pointer"* can only refer to text that did not exist before
`09200dd`. **Attribution wobble, recorded:** the same account credited commit
`30c5a35`, which is not in the framework repository — it is a domain-repo
commit, so the agent named the domain's own pointer rather than the framework
wrapper it had just read. The observation stands; the citation was wrong.

### One structural fact the re-test settled

Asked whether `AGENTS.md` was *first* in context, the answer is **no, and it
cannot be**: the harness system prompt precedes the whole memory block, and
within that block ordering is filesystem-root-down by documented behaviour
("content is ordered from the filesystem root down to your working
directory"), so a nested domain's entry file necessarily lands after the
pointers above it. The in-session agent inferred this from observation and
hedged it; the documentation confirms it. This is not a defect and there is no
mechanism that would change it — the two pointers ahead of the entry file
total under a kilobyte, and the framework's claim is that the entry file is in
context at workspace open, which holds. Worth stating plainly so no future
session re-opens it as a gap: **the pointer controls presence, never
position.**

### What the re-test still does not establish

Both sessions ran in an **adapter-carrying** domain whose SessionStart hook
also fires, so neither is evidence for the no-adapter leg — with the adapter
present, the entry surface was never the only automatic route in. The
expanded-inherited case (an operator approving the external-import dialog,
after which the root's entry file *would* reach a domain session) remains
untested by construction; the wrapper's second bullet is written for it, and
its value there is reasoned, not observed.
