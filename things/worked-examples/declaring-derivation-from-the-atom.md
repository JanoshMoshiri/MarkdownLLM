---
id: declaring-derivation-from-the-atom
type: example
status: draft
version: 1.0
created: 2026-08-28
pattern_type: workflow-definition-derivation
demonstrates: good-practice
applies_to: [workflow-definition, domain-refresh, universal-workflow]
exposed: false
tags: [derivation, universal-workflow, workflow-definitions, declaration, domain-pass]
informed_by:
  - id: derivation-shape-settled-2026-08
    commit: 1a278dd11b6e2db4a24c36b3c64b765abc90f298
  - id: estate-workflow-derivation
    commit: 1a278dd11b6e2db4a24c36b3c64b765abc90f298
linked_things:
  - id: universal-workflow-methodology
    relation: implements
    notes: "The atom being derived from. This example teaches how a definition declares that relationship without restating the atom's stages."
  - id: derivation-shape-settled-2026-08
    relation: derived-from
    notes: "The settled shape: declaration not rebuild, corpus-local anchoring, three routes."
  - id: estate-workflow-derivation
    relation: implements
    notes: "WP1 — the pattern this programme ships so the per-domain passes have something to follow."
---

# Declaring Derivation From the Atom

## The Pattern

A workflow-definition authored **before** `universal-workflow.md` entered the
foundation (2026-08-25) usually already realises the atom's seven decisions —
it was written by someone solving the same problem the atom describes. It is
reconciled by **declaring** that relationship, not by rebuilding it.

The declaration is one body section, `## Derivation from the universal
workflow`, carrying four things:

1. **The lineage sentence** — this definition specialises the methodology, at
   a named framework version, anchored in-corpus through the definition's
   existing edge to the domain's own workflow skill.
2. **The mapping table** — every one of the seven decisions, against the
   stage(s) that realise it.
3. **The departures, named** — decisions collapsed into another stage (with
   why that is proportionate), and stages added beyond the seven (with what
   they exist for).
4. **The progression outcomes and the shape** — which of continuing /
   revising / deferring / stopping the definition declares, and whether the
   definition is accumulative or repeatable.

## Why It Matters

Composition is auditable only by reading declarations. An estate whose
processes each follow the method but none says so cannot answer *does this
process follow our method, and where does it deliberately depart?* — and that
question becomes load-bearing the moment unattended sessions execute those
processes, because automating undeclared process automates whatever has
drifted inside it.

Naming a collapse is the audit property. A silent collapse and a missing
decision are indistinguishable from outside; a named one is a decision an
assessor can accept or challenge.

## Structure — the worked case

The first pass ran on a regulated domain's template-document-authoring
definition: eight stages, authored two days before the atom became foundation,
exercised by two runs. Its mapping:

- Five decisions map one-to-one onto stages.
- **Three collapse into the first stage.** `define-prioritise` and
  `set-mvp-target` are made once, at scoping, because a document demand
  arrives with its direction fixed by the intended act and the control route,
  and the target state is fixed by the template. Stated justification: the
  atom's proportionate-use rule sets process weight by what failure costs, and
  a separate gate here would be "ceremony inherited rather than control
  required."
- **`review-verify` subdivides into three stages** — deterministic gates, then
  attributable human acceptance, then outcome-against-need.
- **One stage is added** with no counterpart in the seven: the human-only
  irreversible act. Justified by the framework's own law that a consequence
  which cannot be recovered afterwards belongs to the human — the
  gate-authority boundary made a stage rather than left to discipline.

The result is a definition that reads as a specialisation, with its
deviations legible, and not one stage renamed.

## Anti-Patterns (What NOT to Do)

- **Adding a `linked_things` edge to `universal-workflow-methodology` from a
  domain thing.** A cross-corpus reference target is a hard validation Error;
  the domain's floor rejects it at the first commit. Only a framework-root
  definition can carry that edge, because it shares the corpus. *The root is
  not a representative domain* — a pattern authored and validated there can be
  invalid everywhere else, and this one was, in the first draft of this very
  programme's brief.
- **Renaming stages to match the atom's vocabulary.** The atom explicitly
  licenses a specialisation to re-name and subdivide. Domain stage names often
  *are* the controls; genericising them loses meaning and buys cosmetics.
  Restructuring is for a mapping that genuinely **fails**, and then it is
  process repair, not reconciliation.
- **Leaving a collapse silent.** "Only five decisions appear here" with no
  explanation is indistinguishable from a process missing two decisions.
- **Inventing a stage to complete the table.** If no stage realises a decision
  and no honest collapse explains it, that is a finding about the process.
  Record the gap; do not paper it.
- **Retiring a zero-run definition as part of a derivation pass.** Retire-or-run
  on a mandated process is a governance ruling, not a reconciliation act.
  Declare it, record the zero-run fact honestly, and date the ruling.

## How to Adapt

Run one pass per definition, inside the owning corpus, as that domain's agent:

1. Spin up properly — session-start (the gate attestation), the domain's
   specification and write skills, then the definition.
2. Map the seven decisions against the stages.
3. **Mapping succeeds** → declare: write the section, name the departures,
   bump the version.
4. **Mapping fails** → the gap is a process finding; repair the process, then
   declare. Never rename to force a fit.
5. **Zero runs and no live demand** → retire honestly with the reasoning
   recorded — or, where the process is mandated, declare it and date the
   first-run-or-retire ruling for the human.

Depth is the domain's own call under its own lenses. A regulated domain's
regulator lens forces all seven named and every departure justified; a
low-stakes domain may map proportionately. The framework ships this example
and the question — never the verdict.
