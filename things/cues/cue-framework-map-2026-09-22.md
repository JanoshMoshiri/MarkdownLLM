---
id: cue-framework-map-2026-09-22
type: cue
status: answered
version: 1.0
created: 2026-09-22
subject: framework-map
raised_at: 042433c5c817d73333f9ae5801ed29cf39af2e98
raised_by: "agent — the framework domain agent, 2026-09-22, in the modifying commit (public-docs-face-build Phase 1)"
verdict: inflection
verdict_reason: "Views 2 and 3 are now gated (every spec a node, tags match frontmatter; every subcommand a node) and the map carries a generated edge list. The map's own *Keeping This Map Honest* section — the rule it states for itself — was rewritten in the same commit to say which of its facts are mechanical now; AGENTS.md's residue sentence was walked to match."
informed_by:
  - id: public-docs-face-is-derived-not-restated
    commit: 35aae16b2c185b6aa2d63c20d8eabae8d9432f28
tags: [cue, docs, derivation, framework-map]
---

# Cue: `framework-map` was modified — inflection?

## The Change
Four things in one commit. View 2 gained the node it was missing
(`docs/estate-mechanics.md`) and View 3 the node for the new `docs`
subcommand — both surfaced by the check the same commit introduced. The map
gained a managed `<!-- generated:spec-edges -->` block: every declared
spec-to-spec edge from frontmatter, with each spec's live `(type, status)`.
And *Keeping This Map Honest* — the map's statement of its own sources of
truth — now says which of those sources are gated: View 2 node completeness
and status tags, View 3 node completeness both ways.

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer
**Inflection.** The map's honesty rule changed from "check against these
sources by hand, in the same commit" to "the floor checks nodes and tags; you
draw the edges and write the prose". That is the rule the map asks its
maintainers to follow, and it is different now.

The four-beat pass, in this commit: **cue** — this thing. **Assimilate** —
`mdllm touchpoints framework-map` plus a grep for prose that describes the
map's residue: `AGENTS.md` step 3 ("View 1 counts + View 2 node"). **Walk** —
that sentence rewritten to name what remains prose-only in the map (View 1
counts, the drawn edges, the `accDescr` text) and what no longer is. The
`accDescr` subcommand count was walked by hand from 37 to 38 and stays the
backlog's routed accDescr-drift item, unbuilt — named in the plan, not hidden.
**Seal** — this commit.

*Raised and answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`, citing the ruling that
made the change. The operator may overturn it by editing the verdict.*
