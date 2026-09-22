---
id: cue-operator-guide-2026-09-22
type: cue
status: answered
version: 1.0
created: 2026-09-22
subject: operator-guide
raised_at: 042433c5c817d73333f9ae5801ed29cf39af2e98
raised_by: "agent — the framework domain agent, 2026-09-22, in the modifying commit (public-docs-face-build Phase 1)"
verdict: inflection
verdict_reason: "The guide's toolbox stopped being authored prose and became a generated block plus a checked authored half. That changes how the guide is maintained — a rule about the surface, not a wording — so the dependants that describe the dark-region residue were walked: AGENTS.md's step-3 sentence no longer names View 2 nodes as prose-only and now names the guide's authored lines as the residue that remains."
informed_by:
  - id: public-docs-face-is-derived-not-restated
    commit: 35aae16b2c185b6aa2d63c20d8eabae8d9432f28
tags: [cue, docs, derivation, toolbox]
---

# Cue: `operator-guide` was modified — inflection?

## The Change
The 33-row hand-maintained toolbox table became a managed
`<!-- generated:toolbox -->` block — subcommand, exact usage, the tool's own
help, from argparse — followed by one authored line per subcommand under
*When you'd type each one yourself*, checked both ways for completeness by the
pre-commit coherence leg. `public-docs-face-build` Phase 1; the ruling it
implements is `public-docs-face-is-derived-not-restated`.

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer
**Inflection.** Not because the words moved — every authored sentence
survived — but because the *maintenance rule* for the surface changed: a
future CLI change no longer edits this table by hand, and a commit that
forgets the authored line is refused. That is a rule others reason from.

The four-beat pass, in this commit: **cue** — this thing. **Assimilate** —
`mdllm touchpoints operator-guide` plus a grep for the residue sentence:
one restatement found, `AGENTS.md` step 3, which listed what the tool cannot
read. **Walk** — that sentence rewritten: View 2 nodes and their status tags
are mechanical now; the guide's authored *when* lines join the named residue.
`change-reconciliation.md` → Walking the Dark Region describes the tiers
without naming this surface, so it holds as written. **Seal** — this commit.

*Raised and answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`, citing the ruling that
made the change. The operator may overturn it by editing the verdict.*
