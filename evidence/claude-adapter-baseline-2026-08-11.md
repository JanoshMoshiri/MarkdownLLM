---
id: claude-adapter-baseline-2026-08-11
type: artifact
status: stable
created: 2026-08-11
tags: [harness, adapters, claude-code, baseline, phase-0]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Phase 0 deliverable: the frozen Claude adapter evidence and the live-test checklist that Phase 6 executes."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "Separates what is designed and configured (recorded here) from what only a live run can verify (the checklist)."
---

# Claude Adapter Baseline — Phase 0 Freeze (2026-08-11)

The state of the Claude Code adapter surface at the moment the
vendor-harness-adapter-foundation extraction began. Anything not recorded here
was not part of the contract being preserved.

## 2026-08-12 erratum — byte baseline retained; ordering interpretation withdrawn

This artifact remains the stable historical record of the bytes and tests that
existed at the Phase 0 boundary. It is **not** evidence that those bytes execute
the lifecycle intent correctly. A later live-contract review found that current
Claude Code launches all matching hook handlers in parallel. The two handlers
inside the frozen SessionStart group therefore do not guarantee
`estate-sync` → `session-start`, and their cwd-relative bare `python` commands
do not establish runtime or project-root portability.

The original golden is now named conceptually as the **legacy v1 projection**.
It must remain immutable as a migration input. Phase 5R of the linked plan must
earn a new current golden: one matching handler per lifecycle moment, invoking
the neutral ordered lifecycle runner through the shared launch policy. Existing
project files are not rewritten by this erratum.

## What exists, and where its truth lives

| Artifact | Owner of the bytes | Frozen by |
|---|---|---|
| `.claude/settings.json` (scaffolded) | `scaffold.py` inline projection | `tools/tests/fixtures/claude_golden/settings.json.golden` + `test_scaffold_settings_matches_golden` |
| `.claude/commands/*.md` | copies of `templates/commands/*` | `test_scaffold_commands_are_template_copies` (template is the golden) |
| Scaffold completion guidance | `scaffold.py` stdout | `claude_golden/scaffold-guidance.golden` + test |
| Doctor's adapter reading | `doctor.py` (`SessionStart` key presence) | `test_doctor_current_reading_of_each_shape` — pins the *present* presence-as-capability behaviour until Phase 3 replaces the vocabulary |
| Estate configuration shapes | the live estate (operator-owned) | `tools/tests/fixtures/estate_shapes/*` — representative hooks-only, permissions-only, permissions-plus-hooks, extended-startup, and absent shapes |
| Lifecycle intents | application contract | `LIFECYCLE_INTENTS` in `test_adapter_contract.py` — session-start = (estate-sync, session-start) ordered; post-write = (validate,) advisory |
| Example adapter | `adapters/claude-code.settings.example.json` | unchanged by this plan until Phase 7 reconciliation |

Estate snapshot date: 2026-08-11. Eleven of 13 domain repos carry
`.claude/settings.json`, one carries `.claude/settings.local.json`, and one has
neither. Across both filenames the structure is hooks-only ×8,
permissions-only ×2, permissions-plus-hooks ×1, extended-startup ×1, and
absence ×1 (structure inspected, no content copied). Existing files are estate
state, not generated cache.

## Original ordering interpretation (withdrawn by the 2026-08-12 erratum)

The Phase 0 interpretation was that Claude expressed session-start ordering as
one hook group with two sequential commands. That interpretation is false under
the current documented contract: matching handlers run in parallel. The
ordering intent still belongs to the application contract, but the correct
mechanism is one matching vendor handler invoking the inward sequential runner
once. The named test freezes the legacy shape; it does not prove execution
order.

## Claude live-test checklist (Phase 6, Claude side — owned here from Phase 0)

Static tests earn *designed-for*; only these runs earn *verified-on*. Record
harness version, platform, and date with each.

1. Scaffold a fresh domain from the corrected current renderer; open it
   directly in Claude Code.
2. Confirm the project projection contains one SessionStart handler and observe
   the neutral runner execute estate-sync **then** session-start, in order,
   with output visible to the model at t=0.
3. Correlate the real Claude event transcript with a fresh, definition-hash-bound
   execution record. A manually invoked runner record is not harness evidence.
4. Edit a thing; observe PostToolUse validation feedback (advisory, quiet).
5. Commit; observe the git pre-commit floor validate and the post-commit
   autopush leg respect the repo's `git: autopush` declaration.
6. Explicitly refresh one exact known-legacy composite settings file, proving
   permissions and unrelated groups byte-identical, then repeat 2–5. A legacy
   managed command with a local extension must refuse rather than be inferred.
7. Confirm deleting `.claude/` in a disposable repo leaves interpretation and
   Git-floor behaviour whole.

## Not recorded here, deliberately

Codex contract evidence (documentation dates, live-harness checklist) belongs
to the Codex-owned Phase 2B, per the v1.3 ownership correction. Nothing in
this baseline encodes an assumption about any harness other than Claude Code.
