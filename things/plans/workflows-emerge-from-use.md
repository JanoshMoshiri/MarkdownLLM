---
id: workflows-emerge-from-use
type: plan
status: in-progress
version: 1.2
created: 2026-10-07
session: 2026-10-05
priority: critical
tags: [workflow, carrier, emergence, reckoning, repeatability, floor]
linked_things:
  - id: workflows-emerge-from-use-2026-10-07
    relation: implements
    notes: "The ruling this plan builds: workflows emerge from use, organically, and the work is the run."
  - id: workflow-state-specification
    relation: extends
    notes: "Carrier Binding and Workflows Emerge From Use are its new sections."
  - id: the-reckoning
    relation: references
    notes: "The reckoning dissolves an inferred workflow nothing moves through, and carries the emerged candidate as an item for the agent."
triggers:
  - type: time
    condition: "2026-10-21 reached"
    action: surface
    note: "Two weeks: has a workflow emerged in a live workspace, and has the agent followed one when working on its carrier type? If neither, the actor is the problem."
---

# Plan: Workflows Emerge From Use

**What this delivers.** A workspace learns its own process from the record.
The floor finds the paths things of one type keep travelling; the agent
writes them as workflows without asking; the work itself is the run; the
agent follows the steps every time it touches that type; the workflow
revises itself when practice moves and is let go when practice stops. The
operator can still craft a workflow deliberately and keeps it as theirs.

**What it does not deliver.** Any removal or invention of a human gate by
the agent. Any change to explicit `workflow-run` things, which keep their
semantics and checks. A Codex binding before Claude Code proves it.

## Phases

- [x] **Phase 0 — Record it.** `workflows-emerge-from-use-2026-10-07` in the
      operator's words; `workflow-state.md` 0.8 → 0.9 gains *Carrier
      Binding* and *Workflows Emerge From Use*; this plan. *Done 2026-10-07.*
- [x] **Phase 1 — The floor finds.** *Done 2026-10-07: first live read — the busiest live domain's specification loop on all three spec types and its ticket loop, each with the unbound definition that already describes it named; none in the root and five other workspaces.* `mdllm workflows [path] --emergent`:
      one pass over the commit stream, the observed state machine per domain
      type, the dominant paths with their support, candidates where a path
      of three or more stages is travelled by enough things across more than
      one day each and no definition binds the type, evidence attached, an
      honest none. Read-only. Done when it names the specification loop and
      ticket loop in the busiest live domain and nothing in the quiet ones.
- [x] **Phase 2 — The floor binds.** *Done 2026-10-07; `carrier.type` takes a list, because the first live read found one loop running through three types.* The `carrier` field validated
      (shape; stage map members of the stage set; two live definitions on
      one type refused); `mdllm workflows` lists each definition's derived
      runs by stage and its departures read from history; the zero-run check
      counts carrier things. Done when a bound definition in a live domain
      shows its runs without a run thing written.
- [x] **Phase 3 — The agent writes.** *Done 2026-10-07: `--draft`, and `mdllm reckon` carries each emerged path as a settled item — write it, or bind the definition that already describes it.* `--emergent --draft` writes the
      candidate as a `workflow-definition` marked inferred, bound to its
      carrier, its edges from observed transitions, its terminal stages from
      the type's terminal statuses, and per stage the acts the commit stream
      shows on the way in; the agent completes each stage's do, produce and
      check lines from the record and marks the gate stages. The reckoning
      carries an emerged candidate as an item for the agent, so emergence
      runs at the boundaries the reckoning already has.
- [x] **Phase 4 — The agent follows.** *Done 2026-10-07: the `workflows` block, generated from the definitions' own carrier and stages with no history read so session start stays fast; in the template for new workspaces; inserted once after the `types` block on an existing workspace's next refresh.* A generated block in the entry file
      naming, per bound type, the workflow and its stages, kept current by
      the drift check the entry file's other blocks already have.
- [x] **Phase 5 — Evolve and dissolve.** *Done 2026-10-07 in the reckoning: departures settled or residue by authorship, idle inferred workflows dissolve mechanically; the exit table carries the row.* Departures from an inferred
      workflow become settled reckoning items (revise, or name the slip);
      from an authored one, residue. An inferred workflow nothing has moved
      through within its interval is dissolved; an authored one is asked
      about. `session-memory.md`'s exit table gains the row.
- [ ] **Phase 6 — See.** Four weeks in the live workspaces: a workflow that
      nobody defined governing work, followed, revised once, and nothing
      emerging where nothing repeats.

## Done when

- [ ] A workflow nobody defined is governing work in a live workspace.
- [ ] The agent follows it when working on its carrier type, unprompted.
- [ ] A departure revised it once, and the revision is on the record.
- [ ] A quiet workspace shows none, honestly.
