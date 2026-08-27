---
id: explorer-publication-readiness
type: plan
status: in-progress
version: 1.0
created: 2026-08-27
priority: high
tags: [explorer, release, publication, windows, review, cleanup, uat]
linked_things:
  - id: explorer-publication-position
    relation: derived-from
  - id: markdownllm-explorer-comprehensive-review-2026-08-27
    relation: references
  - id: markdownllm-explorer-windows-distribution
    relation: references
---

# Explorer publication readiness

This plan is the single carrier for publishing the current in-repository
Windows preview. It closes only when the reviewed release candidate, its
installer and the public claims all describe the same state.

## Current position

- [x] Standalone read-only Explorer implemented using Clean Architecture
  boundaries.
- [x] Native per-user Windows installer, shortcuts and tray lifecycle built.
- [x] Public installation and user guides use a generated fictional estate.
- [x] The stale evidence-seal blocker from the comprehensive review was
  corrected and the full technical trace was resealed on the corrected tree.
- [ ] Operator reviews the installation guide and user guide end to end.
- [ ] Operator performs and records the human-owned UAT dispositions.
- [ ] Correct or explicitly disposition the active upgrade/uninstall shutdown
  race identified by the comprehensive review.
- [ ] Expand the retained adapter-swap evidence to all four declared ports, or
  narrow the requirement with explicit authority.
- [ ] Reconcile the remaining non-blocking review findings selected for this
  release.
- [ ] Before repository publication, resolve the two current baseline floor
  regression failures: the scaffold test's stale 12-item expectation after a
  ninth prompt was added, and the assemble test's environment-sensitive
  substring check against global Git configuration.
- [ ] Run the documented release clean-up and prove ignored construction
  output is absent from the tracked release surface.
- [ ] Rebuild the final installer from the immutable candidate, verify it,
  record its hash and attach it as a release asset.
- [ ] At the final release boundary, generate the complete changelog from the
  unpushed commit range and make the version decision.
- [ ] Push and publish only under a separate explicit operator instruction.

## Release claim

Until every acceptance-affecting item above is closed, the truthful claim is
**working Windows preview**. The source and reproducible packaging recipe are
tracked. The built executable is a separately produced release asset, not a
committed repository file.

## Done when

The final candidate passes framework and Explorer validation, all technical
blockers and human UAT items have explicit dispositions, the clean-up check is
complete, and the installer distributed to users is byte-identical to the
verified release asset.
