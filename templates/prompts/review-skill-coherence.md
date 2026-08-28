---
id: review-skill-coherence
type: prompt
status: draft
version: 1.0
created: 2026-08-28
inputs:
  - name: skill-files
    description: "Every file in the domain's `skills/` directory — the Layer-2 operating surface, read whole, not summarised"
  - name: entry-file
    description: "AGENTS.md — the Layer-1 contract; its authored sections only, since managed `<!-- generated: -->` blocks are the generator's"
  - name: schema-index
    description: "things/_schema.yaml plus `mdllm index things rebuild --signal schema` — what the domain actually declares and what its things actually carry"
  - name: commit-stream
    description: "`mdllm worklog` / `git log` over things/ since the last retrospective — the record of ENACTED practice, which is the thing the skills claim to describe"
  - name: floor-findings
    description: "The vocabulary Warnings `mdllm coherence` already raised — the mechanical half; this prompt starts where they stop"
outputs:
  - name: per-skill-disposition
    description: "For every skill file: confirm-current | update | park | retire, each with its reason"
  - name: workflow-verdict
    description: "The bidirectional answer for the workflow skill: is the written process dead vocabulary, and separately, has a de facto process emerged worth codifying?"
  - name: changes
    description: "The edits the dispositions imply, and any workflow-definition worth minting"
bound_to:
  - hook: retrospective
linked_things:
  - id: orchestration-specification
    relation: implements
  - id: retrospective-specification
    relation: complements
  - id: the-operating-layer-has-no-quality-loop
    relation: implements
    notes: "The judgement half of that insight's remedy; the floor half is the vocabulary check in `mdllm coherence`"
  - id: change-reconciliation-specification
    relation: references
    notes: "The Walk reaches a skill only when a human names an inflection; standing-still drift never names one, which is why this pass exists"
  - id: derivation-shape-settled-2026-08
    relation: references
    notes: "Settles the workflow-skill vs workflow-definition question this prompt asks: both homes stay, different jobs, and the skill is the corpus-local anchor for framework lineage"
---

# Review Skill Coherence

## Purpose

The memory layer has a quality loop at two cadences — session-end forces a
disposition on every standing insight, the retrospective triages the
population. The operating layer has none. Layer 3 is audited at every commit;
Layers 1 and 2 are audited when a named inflection happens to walk through
them, which for a skill is almost never.

And the way a skill degrades is precisely the way a change-time walk cannot
catch: **it drifts by standing still.** Nobody edits it wrongly — the domain's
practice moves around it. Practice lives in the commit stream, not the graph;
it is not a thing with edges, so no blast radius ever includes a skill.

This is the pass that reads them. It is the sibling of
`review-schema-coherence`: same cadence, same shape, one layer up.

**Where the floor already answered, do not re-answer.** `mdllm coherence`
raises a Warning for any type, status, or frontmatter field a skill instructs
that the schema does not declare. Those are facts; take them as given and
spend the judgement here on what no check can read — whether the skill still
describes what the domain *does*.

## Reasoning Template

### 1. Reconstruct enacted practice from the commit stream

Read `git log` over `things/` since the last retrospective **before** opening
a single skill file. The order matters: reading the skills first anchors you
to the written process and you will then read the commits as confirmation of
it. Ask of the commits alone:

- Which thing types were actually created, and at which statuses?
- What sequence do commits fall into — is there a repeated shape (intake →
  work → verify → file) nobody has written down?
- Which declared steps have no commit anywhere that enacted them?
- What did sessions do *instead* of what the skills say?

Write that down as a paragraph before proceeding. It is the yardstick.

### 2. Read each skill against it

For each file in `skills/`, and for the authored sections of `AGENTS.md`:

- **Does it describe what happens?** Not "is it well written" — is it *true*
  of the period you just reconstructed?
- **Does it describe something that never happens?** Vocabulary, steps, or
  ceremonies with no trace in the commit stream.
- **Does the period contain work the skill has no account of?** The gap in
  the other direction, and the harder one to see.
- **Does it contradict a sibling?** The estate's sharpest instance had a
  specification skill and a write skill giving different status vocabularies
  for the same type, in two files a session is required to read together.

### 3. Force a disposition on every skill — no file left unruled

This is the brake. A review that produces observations without dispositions
is the insight backlog rotting, one layer up.

| Disposition | When | What it costs you |
|---|---|---|
| **confirm-current** | It is true of the period, and you checked rather than assumed | Name the commits that confirm it |
| **update** | True in outline, wrong in detail | The edit, in this session |
| **park** | Describes a capability the domain has stopped exercising, and may resume | A dated note in the file saying so, and why |
| **retire** | Describes a capability the domain does not have and will not | `status: deprecated`, and a note naming what replaced it |

"Leave it alone" is not a disposition. If nothing needs to change, the answer
is **confirm-current with its evidence**, which is a different claim.

### 4. The workflow skill gets the question asked both ways

The workflow skill is the one most likely to be dead — it describes a process
rather than a surface, so nothing touches it by contact. Ask both halves, and
do not let the first answer stand in for the second:

- **(a) Is the written process enacted?** If no commit in the period followed
  it, that is dead vocabulary. Park or retire it honestly rather than leaving
  a fiction in the operating layer.
- **(b) Has a de facto process emerged?** The ad-hoc ebb and flow of a working
  domain *is* a workflow; it is just unwritten. If step 1 found a repeated
  shape, it deserves codifying.

Where (b) is answered yes, the shape is settled and is not re-opened here
(`derivation-shape-settled-2026-08`): **both homes stay, doing different
jobs.** The repeatable stage graph belongs in a `workflow-definition` thing,
where runs can point at it and the floor can enforce membership and
transitions. The workflow *skill* holds the domain's doctrine — its loop, its
boundaries, its trust semantics — and is the corpus-local anchor a definition
declares lineage through, since a domain definition cannot carry an edge to a
framework spec. So minting a definition never empties the skill; the chain
reads definition → workflow skill → the framework's universal workflow, and
removing the skill would leave the definition nothing in its own corpus to
anchor to.

### 5. Carry the residue

Anything you could not rule on is an open-loop thing, not a note in the
retrospective body. Dispositions land as edits and commits in this session;
what remains goes to the orient view.

## Output Format

```
Skill coherence review — [domain], [period]:
  Practice reconstructed from [n] commits over things/: [one paragraph]
  Floor findings taken as given: [n vocabulary Warnings, or none]

  skills/[file] — [confirm-current | update | park | retire]
    Evidence: [the commits, or their absence]
    Action: [none | the edit made | the status change made]
  ... one row per skill, plus AGENTS.md ...

  Workflow skill, both ways:
    (a) enacted? [yes, by <commits> | no — dead vocabulary]
    (b) de facto process? [none observed | <shape>, worth a workflow-definition]

  Unruled, carried forward: [open-loop things created]
```

Dispositions feed the retrospective's "What Should Change"; the reconstructed
practice usually feeds "Patterns We Noticed". Acting on a disposition is a
normal write operation and is never applied silently.
