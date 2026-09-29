---
id: a-surface-checked-in-one-renderer-is-unchecked-in-another
type: insight
status: active
version: 1.0
created: 2026-09-24
session: 2026-09-22
source: agent
confidence: high
origin: observed
tags: [documentation, pages, rendering, verification, preview]
linked_things:
  - id: public-docs-face-build
    relation: informs
    notes: "Phase 2's two live defects, and the local preview built to catch the class."
  - id: portability-claims-need-execution-tests
    relation: extends
    notes: "The same shape at the document layer: a surface is verified where it was executed, and nowhere else."
---

# A surface checked in one renderer is unchecked in another

## The observation

Every `docs/` file was correct on GitHub's blob view, which is where every
review had ever read it. The first Pages build (2026-09-22) showed three
defects the blob view could not: the diagrams drew nothing (a `//` comment in
a config the theme compresses onto one line), the operator guide's toolbox
was one unreadable paragraph (kramdown opens an HTML block at any line
starting with a tag, and wraps a table that follows an HTML comment), and a
frontmatter-less page was served raw by a local bundle that Pages rendered.
The operator found the second by trying to read it. None was catchable by
the drift gates, which compare text to text.

## The rule

A published surface is verified in the renderer that publishes it. Where two
renderers read the same source — GitHub's and kramdown, and the Explorer is a
third — a check in one says nothing about the others. The check for this
class is the render itself: `tools/pages/preview.ps1` builds with the pinned
Pages gem set, and any change under `docs/` is looked at there before it
goes up. Nothing mechanical reads a page the way a renderer does; the
nearest thing to a gate is a test that pins the shape a renderer needs
(the blank line inside each managed block).
