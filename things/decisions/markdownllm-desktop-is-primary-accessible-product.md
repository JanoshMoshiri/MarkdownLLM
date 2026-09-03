---
id: markdownllm-desktop-is-primary-accessible-product
type: decision
status: made
version: 1.0
created: 2026-09-03
session: 2026-09-03
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [desktop, product, accessibility, local-first, explorer, interface]
linked_things:
  - id: explorer-publication-position
    relation: supersedes
    notes: "Supersedes Explorer's position as the direction of travel; the accepted read-only preview remains a useful optional viewer and historical proof."
  - id: interface-specification
    relation: informs
    notes: "The substrate remains route-agnostic while the first-party product adds a deliberately designed input route."
  - id: explorer-white-label-presentation-2026-09
    relation: informs
    notes: "Cancels the Explorer-specific increment and preserves its reviewed presentation model as a deferred Desktop input."
  - id: explorer-extraction-and-hosting
    relation: informs
    notes: "Replaces the hosted-Explorer hypothesis with a local-first Desktop and later paired mobile remote-control direction."
---

# Decision: MarkdownLLM Desktop is the primary accessible product

## Context

The read-only Explorer proved that the substrate and its domain estate can be made visible, but
it did not remove the operating knowledge needed to install the framework, create or import a
Domain, connect an LLM, manage Sessions and understand what happened. More documentation cannot
turn that sequence into the familiar journey a non-technical user already knows.

The operator chose a first-party MarkdownLLM Desktop application: download one file, follow a
setup journey, create/import/manage Domains through guided actions, converse through a local
Session, and explore the same ordinary Markdown and Git state in one surface. The first preview
is Windows-first and local. The user supplies inference through a supported account/API route;
MarkdownLLM does not silently become the inference vendor.

## Decision

MarkdownLLM Desktop is the primary accessibility and product direction. It is a local-first
application over the existing substrate—not a replacement for it and not a new proprietary state
format. Domains remain ordinary Markdown/Git repositories and can still be operated through
Codex, Claude Code, Copilot, Obsidian or another compatible route without the Desktop.

Preview A proves a context-only OpenAI API route with no tools. Codex subscription integration
and Claude remain gated until their unmodified client/auth/commercial boundaries can be proven
without borrowing unsafe authority. A later mobile client may pair with a live local Desktop to
observe or start Sessions; it does not justify cloud infrastructure or remote exposure now.

Explorer remains available as an optional read-only proof and integration while the Desktop is
in Engineering Preview acceptance. It is no longer the product into which new interaction,
white-label or hosted-control-plane work should accumulate.

## Consequences

- The framework stays vendor- and route-agnostic by contract; the Desktop is one replaceable,
  deliberately verified route supplied by the product.
- The paused Explorer white-label increment is cancelled. Its parked branch is retained as
  recoverable design provenance, not merged or deleted.
- The white-label value object, grammar, contrast rules and field-by-field precedence are kept as
  deferred Desktop product input; they do not expand Preview A.
- The hosted Explorer plan no longer represents the preferred product path and must be
  dispositioned before work resumes.
- Public documentation must distinguish the usable read-only Explorer from the new Desktop
  Engineering Preview and must not imply that either changes the substrate's authority.

## Exposure

No. This is product direction and does not make a graphical application mandatory for a valid
MarkdownLLM Domain.
