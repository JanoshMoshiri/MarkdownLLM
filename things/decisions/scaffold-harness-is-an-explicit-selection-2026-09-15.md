---
id: scaffold-harness-is-an-explicit-selection-2026-09-15
type: decision
status: made
version: 1.0
created: 2026-09-15
session: 2026-09-15
decided_by: Janosh Moshiri, 2026-09-15, in session, on the first of the vendor plan's three Phase 8 boxes
priority: high
tags: [scaffold, harness, adapters, default, phase-8, rollout]
informed_by:
  - id: vendor-harness-adapter-foundation
    commit: 81b34e80c4f53922776d7dd2ebab16f74241aee0
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: implements
    notes: "Phase 8's first box. The other two boxes stay the operator's; this ruling settles only the default."
  - id: installation-is-not-activation
    relation: references
    notes: "The reason a silent default lost: a rendered projection is not a working one, and a default renders on the operator's behalf."
  - id: a-generated-contract-change-is-an-estate-migration
    relation: references
    notes: "Why the question is asked at birth: choosing a projection is a prompt; retrofitting one is a migration."
---

# Decision: the scaffold's harness is an explicit selection

**Ruled by Janosh Moshiri, 2026-09-15, in session**, on Phase 8's first
box. His words: *"The default is going to be a selection. When you do the
scaffold, you'll be asked the question — which do you want to pick? — and
have it picked from the list."*

## The ruling

`mdllm scaffold` no longer selects a harness when `--harness` is omitted.
It asks. With a human at the keyboard, the registered list is offered and
one entry (or `all`, or `none`) is chosen; with nobody there — a script, a
dispatched run, a CI job — omission is refused, and the refusal prints the
list so the caller can name its choice and rerun. Nothing is rendered
until a harness is named.

## Why, and what lost

Three answers were on the table (`vendor-harness-adapter-foundation`,
Phase 8):

- **Keep the historical Claude compatibility default.** Lost. A silent
  default is a capability claim made on the operator's behalf: every
  domain born by omission carries a Claude Code projection whether or not
  that harness is in use, and `installation-is-not-activation` already
  records that a rendered fragment is not a working one. Silence should
  not author permission-bearing configuration.
- **Render more than one project-bound adapter by default.** Lost, harder.
  It multiplies the same claim across harnesses, and each managed fragment
  is a file the operator will be asked to trust in that harness.
- **Explicit selection.** Ruled. The question is cheap at birth and
  expensive after: retrofitting a projection is an estate migration
  (`a-generated-contract-change-is-an-estate-migration`); choosing one is a
  prompt.

## What this does not settle

- **The build.** This is a floor change on the scaffold path: the
  interactive prompt, the non-interactive refusal, tests for both, and the
  help text — which today reads *"omitting preserves the compatibility
  default"* and will read the opposite. Substrate code is written under
  code-architect's skills, read first; it is sequenced before Phase 8's
  release act, which carries it.
- **Existing domains.** Untouched. Their projections were rendered under
  the old default and stay as they are; refresh is Phase 8's second box,
  opt-in per domain, never a batch.
- **The `none` answer's consequence.** A domain born with no adapter runs
  on the interpretation anchor alone. That was always true and is not
  changed here; it is named so the prompt can say it.
