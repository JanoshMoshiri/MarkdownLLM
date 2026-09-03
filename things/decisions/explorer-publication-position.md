---
id: explorer-publication-position
type: decision
status: made
version: 1.0
created: 2026-08-27
session: 2026-08-27
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [explorer, publication, preview, windows, interface]
informed_by:
  - id: markdownllm-explorer-comprehensive-review-2026-08-27
    commit: a8f4034dffd84df1196160ef07d68516f47bf3fb
  - id: markdownllm-explorer-windows-distribution
    commit: 3c1b449acf2c927cad3850d55c7b393f3a67f569
linked_things:
  - id: markdownllm-desktop-is-primary-accessible-product
    relation: superseded-by
    notes: "The 2026-09-03 product decision preserves this preview as an optional viewer but replaces it as the primary accessibility direction."
  - id: interface-specification
    relation: informs
    notes: "Distinguishes the optional read-only inspection surface from the human-to-agent I/O contract."
  - id: explorer-publication-readiness
    relation: informs
  - id: explorer-extraction-and-hosting
    relation: informs
---

# Decision: publish Explorer as an in-repository Windows preview

## Context

MarkdownLLM Explorer now provides a working, read-only window into the
substrate and its domain estate. It was built inside this repository so its
requirements, architecture, tests, Windows packaging and documentation could
evolve against the real framework. The operator intends to publish that useful
current shape after reviewing it and completing a release clean-up. A later
move to a separately owned and differently hosted product is wanted, but its
deployment and trust model have not yet been decided.

The independent comprehensive review found the implementation coherent but
with technical and human acceptance work still open. Its stale evidence-seal
finding has since been corrected and the evidence rebound to the then-current
Explorer tree. The active upgrade/uninstall race and the too-narrow
adapter-swap proof still require disposition, and operator UAT remains pending.

## Options considered

1. Withhold Explorer until it has been extracted and remotely hosted. This
   would couple present value and learning to an undecided future architecture.
2. Publish the current implementation as stable. This would overstate the
   outstanding review and acceptance evidence.
3. Publish the current in-repository implementation as a clearly labelled
   Windows preview after review, remediation and clean-up, while tracking
   extraction and hosting as a separate future change.

## Decision

Choose option 3. Explorer is an optional, local, read-only presentation layer
over MarkdownLLM files and Git history. Its current public position is
**Windows preview**, not technically accepted production release. It does not
replace an LLM harness, accept agent intent, invoke skills, edit domain state,
run estate synchronisation, validate, reconcile or publish.

The current release-readiness work and the future extraction/hosting work are
separate plans because they change at different rates and answer different
questions. Extraction is not a prerequisite for learning from the preview.
No push or release is authorised by this decision; publication remains a
deliberate later act after the operator's review and release gate.

## Consequences

- Public documentation may make Explorer discoverable, but must carry the
  preview label and its read-only boundary.
- The outstanding cold-review findings, operator UAT and local build clean-up
  stay visible in the release-readiness plan.
- The Windows installer is rebuilt from the final candidate and distributed
  as a release asset; ignored build output is not added to Git.
- Repository extraction, hosting, authentication, update delivery and
  migration are designed later from observed preview use rather than assumed
  here.

## Exposure

No. This records the release position of one product in this repository. It
does not establish a general framework rule that domains require a UI.
