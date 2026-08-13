---
id: claude-gate-5r3-acceptance-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [harness, adapters, migration, acceptance-gate, phase-5r]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Claude-side independent acceptance of Gate 5R.3 at 72821d0 (implementation 460bb5a). Returns to Codex for 5R.4."
  - id: codex-5r3-migration-acceptance-2026-08-13
    relation: references
    notes: "The Codex implementation record this acceptance independently checks; every claim below was re-derived rather than read across."
  - id: framework-root-tracks-both-adapters
    relation: references
    notes: "5R.3 supplies the refresh mechanism this decision waits on; the root's own migration remains unexecuted and Codex-owned at 5R.4."
---

# Claude acceptance — Gate 5R.3 at `72821d0`

Independent acceptance of the recognised-legacy refresh. Every claim was
re-derived by probing the real service against **real estate bytes** on
scratch copies, not by reading the implementation's own tests.

**Verdict: accepted.** No neutral abstraction is missing; nothing is returned.

## Suites

| Suite | Result |
|---|---|
| Complete framework suite at `72821d0` | **452 passed** (3m49s) — matches the implementation record |
| Focused `test_adapter_install.py` | 36 passed |

## Independent probe — the live root artifact, on copies

Twenty checks against the framework root's real tracked `.claude/settings.json`:

| Property | Result |
|---|---|
| root form recognised as `legacy-root-powershell-v1` | PASS |
| a recognised legacy fragment is never also `current` | PASS |
| ordinary install refuses it, and raises at apply | PASS |
| ordinary install wrote nothing | PASS |
| `--refresh-legacy` permitted, action `refresh` | PASS |
| **556 bytes before the `hooks` span byte-identical** | PASS |
| **3 bytes after the span byte-identical** | PASS |
| operator `permissions` survive verbatim | PASS |
| refreshed artifact becomes `current`, loses its legacy id | PASS |
| re-running is a `no-op`, not a second write | PASS |
| competing `settings.local.json` overlay refuses; neither file touched | PASS |
| a local command tail refuses **even with** `--refresh-legacy` | PASS |
| concurrent mutation between preflight and apply raises `InstallStateChanged` | PASS |
| concurrently-mutated bytes left alone | PASS |

The byte-span checks are the ones worth stating precisely: the refresh
replaces the `hooks` value and *nothing else*, verified by prefix/suffix
comparison against the original bytes rather than by parsing and
re-serialising.

## Independent probe — all-selected atomicity

One refusing target must veto every write, including a target that would
otherwise succeed:

- a divergent **managed** Codex group (managed matcher, wrong command) →
  whole plan refuses, apply raises;
- the cleanly creatable Claude artifact was **not** written — no partial
  estate;
- the refusing artifact untouched.

Recorded because my first attempt at this probe was wrong and it matters
why: a group under a *non-managed* matcher merges cleanly as an
operator-owned extension. Atomicity is only exercised when the conflict is
inside the managed fragment. The correct probe passes.

## Independent estate classification — read-only, copies only

Re-derived rather than read across, and it reproduces the implementation
record exactly:

- framework root → the root-specific legacy form;
- **nine** nested domains → exact `legacy-v1`;
- the regulated deployment → extended, **no** legacy id (its command tail
  correctly withholds recognition);
- one domain → operator-only/permissions artifact, no managed fragment;
- two domains → no primary managed artifact.

Every live artifact was byte-identical after inspection, asserted per
domain. All thirteen nested repositories are clean: **no domain was
migrated**, and `.codex/` is untouched.

## Contract capture

`recognised-legacy-refresh-boundary` was captured into the code-architect
domain's previously empty `interface-contracts/`. That is the first
substrate work executed under `code-architect-governs-substrate-code`, and
the capture direction it asks for is being honoured.

## Boundary held

Recognition is not authority: an adapter supplies immutable recognition data
only, while the application service owns authorisation, all-target
preflight, concurrent-state recheck, atomic apply, and rollback. No adapter
round-trips or rewrites the composite document.

## Not claimed

This is mechanism acceptance. No live domain has been migrated, no root
adapter byte written, and the framework root's own tracking decision
(`framework-root-tracks-both-adapters`) remains unexecuted — its rerender is
Codex-owned at 5R.4. Automatic-dispatch `verified-on` remains Phase 6.
