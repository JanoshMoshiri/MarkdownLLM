---
id: codex-5r4-root-reconciliation-2026-08-13
type: artifact
status: evolving
created: 2026-08-13
tags: [harness, adapters, codex, claude-code, migration, phase-5r]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Codex implementation and root-state record for Gate 5R.4; stable only after Claude independently accepts the handoff commit."
  - id: framework-root-tracks-both-adapters
    relation: implements
    notes: "Records the reviewed rerender and tracking of the root Codex projection required by the operator decision."
  - id: codex-5r3-migration-acceptance-2026-08-13
    relation: extends
    notes: "Exercises the accepted recognised-legacy transaction against both real framework-root artifacts."
---

# Codex Phase 5R.4 root reconciliation

Phase 5R.4 reconciles the Codex projection without weakening the refusal that
protected the stale root file. The ordinary installer first refused the
artifact. Codex then declared its exact pre-5R root projection as immutable,
root-scoped legacy data (`legacy-root-v1`), and the generic migration service
gained a nested-array policy that replaces only adapter-owned event arrays.

## Reviewed root transaction

Before apply, `doctor --harness all` reported both adapters stale and named two
exact legacy IDs:

- Claude: `legacy-root-powershell-v1`;
- Codex: `legacy-root-v1`.

`adapter-install . --harness all --refresh-legacy --dry-run` proposed exactly
two `REFRESH` decisions. The explicit apply used that same all-selected plan,
so neither projection could advance without the other. Claude's top-level
`permissions` bytes remained outside the owned span; Codex replaced only its
`SessionStart` and `PostToolUse` arrays. No nested domain was read as a write
target or migrated.

The managed Codex shell stalled while flushing a staged file inside the
watched `.claude` directory; the transaction had not replaced either target
and left only its named temp file. After removing that abandoned temp, the
same reviewed command completed outside the managed filesystem interception:
two writes, zero unchanged. This is a harness-sandbox observation, not a
change to migration authority or atomicity.

## Resulting root state

| Projection | SHA-256 after refresh | Diagnostic state |
|---|---|---|
| `.claude/settings.json` | `32180554f24029645d723093a7317bc3d36c4f4be0762fd96190ce0bd0038415` | configuration/current; launch/current; execution/untested |
| `.codex/hooks.json` | `d9bed7d74a68dcf5c4d0e36e3df0b8978670e942a073643165dc5baf0d478ae2` | configuration/current; launch/current; execution/untested |

The old Claude attestations are still visible as provenance but explicitly
`definition_current=false`; they do not promote execution. Codex has no event
attestation for the new definition. Static currency remains distinct from
automatic-dispatch evidence, which Phase 6 alone may promote.

The operator's `framework-root-tracks-both-adapters` decision is implemented:
the corrected `.codex/hooks.json` enters tracked framework state in the 5R.4
handoff commit. The exact old bytes remain only as adapter-owned recognition
data for this one root migration; nested contexts expose no Codex legacy ID.

## Trust and product boundary

The official Codex hooks contract was rechecked on 2026-08-13. Project-local
hooks require trust, exact changed definitions require review, and `/hooks` is
the documented CLI review surface. The Desktop chat command palette observed
on 2026-08-12 did not expose `/hooks`. Configuration presence, current bytes,
and Desktop execution therefore remain incapable of asserting CLI review or
project trust.

## Acceptance boundary

Codex owns the implementation, root transaction, managed-shell suite,
validation, coherence, and scaffold matrix. Claude independently reruns the
full suite and checks the current/legacy boundary before this record becomes
stable. No final PowerShell 5.1 rerun is required unless the handoff changes
shared launch, runtime, or lifecycle-runner code after the accepted 5R.1
commit; this implementation changes migration recognition and policy only.

Codex-shell results at handoff:

- focused adapter/install/architecture/scaffold run: 85 passed and one
  historical-fixture assertion exposed its dependency on the now-current live
  root; the corrected fixture plus complete scaffold matrix then passed 16;
- complete suite with an external pytest base: 456 passed;
- root validation: 185 clean; example corpora: 6 and 14 clean;
- coherence: no issues;
- current Git hook reinstalled and its execution test passed.

An initial complete run placed pytest's base inside the framework repository.
It produced 454 passes and two correct failures from tests that require a
non-repository temp path. Both tests passed immediately with an external base,
and the complete external-base rerun produced the 456-pass result above.
