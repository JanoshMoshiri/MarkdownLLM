---
id: codex-5r3-migration-acceptance-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [harness, adapters, migration, ownership, atomicity, phase-5r]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Codex implementation and test record for Gate 5R.3; stable only after Claude's independent acceptance."
---

# Codex Phase 5R.3 migration acceptance

Phase 5R.3 adds an explicit migration use case without weakening ordinary
adapter installation. Claude independently accepted implementation commit
`460bb5a` at Gate 5R.3 (`f7adeb4`), stabilising this record.

## Boundary

The application service owns authorization, selection, all-target preflight,
concurrent-state recheck, atomic apply, and conflict-safe rollback. An adapter
may implement the narrow legacy-definition port to supply immutable IDs and
exact historical managed fragments. Its schema policy rechecks that exact
semantic form and calculates a replacement of only the owned JSON value span.

Recognition is not authority: ordinary install refuses a known legacy form and
names the reviewed command. Only `--refresh-legacy` enables the migration path.
Current state remains a no-op. Unknown stale state, command tails, duplicate or
malformed JSON, unreadable state, competing local overlays, and ambiguity all
refuse with zero writes.

## Exact Claude forms

- `legacy-v1` — the standard two-SessionStart-handler projection parameterised
  only by the framework-relative path.
- `legacy-root-powershell-v1` — the exact tracked framework-root combined
  PowerShell projection, declared only when the framework-relative path is `.`.
- the estate's `--assistant` command tail is reported as an extension and
  deliberately receives no legacy ID.

The root dry-run recognized `legacy-root-powershell-v1` and proposed a diff
confined to the `hooks` value. Root permissions remained outside the changed
span. The command ran with `--dry-run`; no root adapter byte was written.

## Estate read-only classification

The framework root classified as the root-specific legacy. Nine nested domains
classified as exact `legacy-v1`. The regulated deployment classified as
extended with no
legacy ID. `eco-essentials` carried an operator-only/permissions artifact with
no managed fragment. `code-architect` and `property-ventures` had no primary
managed artifact. No nested adapter configuration was changed.

## Verification

- Focused adapter/diagnostic/architecture suite: **89 passed** before the final
  matrix additions.
- Complete framework suite after the final matrix additions: **452 passed**.
- The matrix includes permissions-only insertion, permissions-plus-legacy span
  refresh, root permissions preservation, current no-op, unrelated bytes and
  hook groups, duplicates, malformed JSON, unknown stale state, local command
  tails, read-only overlays, all-selected refusal, concurrent mutation, staged
  apply failure, and conflict-safe rollback.
- Root validation and coherence are run again at the commit boundary.

The reusable architectural contract was captured in the code-architect domain
as `recognised-legacy-refresh-boundary` at nested commit `5bd35f3`.
