---
id: a-vault-tool-writes-back-what-it-shows
type: insight
status: active
version: 1.0
created: 2026-11-10
session: 2026-11-10
source: both
confidence: high
origin: stated
linked_things:
  - id: the-substrate-picks-no-surface-2026-11-10
    relation: informs
    notes: "The decision's open question — how vault edits reach a commit — has to start from this: the tool writes even when nobody edits."
  - id: interface-specification
    relation: informs
    notes: "Its 'optional inspection' section assumes a viewer that never writes; a vault tool is not one."
  - id: portability-claims-need-execution-tests
    relation: supports
    notes: "Each of the three rewrites was found by running the tool on real files, none by reading its documentation."
disposition: keep-active
disposition_reason: "Parked until an edit route from a vault tool is designed; the operator deferred that design on 2026-11-10. Promote into interface.md's optional-inspection section when it is."
settles_when: 2027-01-10
---

# A vault tool writes back what it shows

## The Insight

A markdown-vault tool is not a read-only viewer, even when nobody types in it.
On Obsidian 1.15, three rewrites happened on this machine without an edit:

- **Opening a note re-saved it.** A business-modelling workspace's model
  record was opened once to check its backlinks, and came back with
  different line endings and identical text. Git then showed the
  workspace as modified, and a modified tree is exactly what makes
  `estate-sync` skip its pull, so the operator would silently stop receiving
  another operator's work.
- **Showing a view file rewrote it.** A generated `.base` file was reformatted
  seconds after it was first shown: YAML comments dropped, quoting changed,
  `note.type` shortened to `type`, unknown top-level keys kept.
- **Any property edit rewrites the whole frontmatter** (documented, and
  described by the vendor as intentional). On this estate that touches comments
  in 28 records and trailing-zero decimals in 454.

## Why It Matters

- **Ownership marks must be data, not formatting.** `vault-map`'s first mark was
  a YAML comment and the tool deleted it. The working mark is a
  `generated_by` key plus a hash of the view's data, written in the tool's own
  canonical form, which it then leaves byte-identical.
- **A projection beside the record is safe. Opening records is not.** The
  generated map lives outside every repository, but the records the map links
  to are inside them.
- **Any future edit route must expect writes nobody intended.** Commit
  boundaries and line-ending normalisation have to absorb them, or the floor
  will either refuse them or carry noise into the history.

## Open Question

Should the floor treat a whitespace-only or line-ending-only change as no
change, for example in `estate-sync`'s dirty check, or should the vault be
configured not to rewrite? Neither has been tried.
