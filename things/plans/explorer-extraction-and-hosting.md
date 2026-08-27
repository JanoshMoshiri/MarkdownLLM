---
id: explorer-extraction-and-hosting
type: plan
status: not-started
version: 1.0
created: 2026-08-27
priority: medium
dependencies: [explorer-publication-readiness]
tags: [explorer, extraction, hosting, architecture, distribution]
linked_things:
  - id: explorer-publication-position
    relation: derived-from
  - id: interface-specification
    relation: references
  - id: markdownllm-explorer-windows-distribution
    relation: references
  - id: code-architect-governs-substrate-code
    relation: references
---

# Extract and host MarkdownLLM Explorer

## Intent

After the local Windows preview has produced real operating evidence, move
Explorer out of the framework release surface and decide how it should be
owned, hosted and delivered. This is a future architecture and migration
exercise, not a relocation of files disguised as clean-up.

## Questions to resolve

- Repository and package ownership, version cadence and release governance.
- Local, desktop, hosted or hybrid runtime shape and the trust boundary each
  creates.
- Authentication, authorisation and tenant isolation if any substrate content
  crosses a network boundary.
- How a hosted surface obtains files and Git history without becoming a hidden
  second source of truth.
- Update delivery, signing, telemetry and support expectations.
- Migration of history, documentation, issue tracking and public release links.
- Cutover and deprecation path for the in-repository preview.

## Non-goals for the current release

- Do not move Explorer now.
- Do not expose the current loopback service to a network.
- Do not invent an authentication model before a hosting shape and user model
  exist.
- Do not make future extraction a blocker to a truthful preview release.

## Exit condition

An accepted design names the product boundary, trust model, deployment path,
migration sequence and evidence required for cutover. Only then should source
move or the local preview be deprecated.
