---
id: the-substrate-picks-no-surface-2026-11-10
type: decision
status: made
version: 1.0
created: 2026-11-10
session: 2026-11-10
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [ruling, interface, vault, obsidian, surface, vault-map]
informed_by:
  - id: interface-specification
    commit: c502b0c599993ee43cf53681b4335f154e823727
  - id: harness-native-onramp-supersedes-desktop
    commit: c502b0c599993ee43cf53681b4335f154e823727
linked_things:
  - id: interface-specification
    relation: informs
    notes: "Restates the route-agnostic contract for human surfaces: a vault tool is one optional view beside the record, like Explorer, never the chosen surface."
  - id: operator-guide
    relation: informs
    notes: "The vault-map when-line says plain notes by default and a tool's view format only by name."
  - id: harness-native-onramp-supersedes-desktop
    relation: references
    notes: "Explorer stays parked as the optional read-only viewer; this ruling does not replace it with another product."
---

# Decision: The substrate picks no surface — a vault tool gets a generated map, not the role

## Context

Obsidian was installed on 2026-11-06 and opened on the folder that holds the
workspaces, following the vault layout another operator already used with
these workspaces. A research pass on 2026-11-10 compared Obsidian with
MarkdownLLM Explorer (parked since 2026-09-02) and recommended making
Obsidian the human surface and leaving Explorer parked.

## Inputs Considered

The interface specification's route-agnostic contract; the harness-native
onramp decision, which keeps Explorer as the optional read-only viewer; the
comparison itself — Obsidian reads, searches and edits the record and is
scriptable, but cannot follow the id references in frontmatter, show the
commit stream, or know what is open; the hand-built relationship map one
operator generated for those gaps.

## Options

1. Make Obsidian the human surface and build its integration first.
2. Pick no surface; add a generated map that makes the record more
   reachable from any vault tool, with a tool's own view format only as a
   named option.
3. Un-park Explorer.

## Decision

**Option 2.** The operator, in their words: "I don't want to make Obsidian the
human surface. I want to make no claim to picking a specific thing, but I do
want to add a command that generates [the vault's] map folder. And I do want
to add a note that generates the link things." And: "I'm keen to make the
substrate more accessible through Obsidian."

So `mdllm vault-map` writes plain notes by default — every thing's structural
references as links, the open work, the newest commits — and writes a view
file in one tool's own format only when that tool is named (`--views
obsidian`).

## Consequences

- No document may call Obsidian, or any vault tool, the human surface.
- Integration work for one tool lands as a named option beside the plain
  notes, never as the default.
- Editing records from a vault tool, and how such edits reach a commit,
  stays an open question. The investigation of 2026-11-06 named the gaps:
  the session gate, frontmatter rewriting, and commits across many
  repositories.
