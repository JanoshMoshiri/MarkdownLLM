---
id: the-operating-layer-has-no-quality-loop
type: insight
status: promoted
version: 1.1
created: 2026-08-18
session: 2026-08-18
source: both
confidence: high
origin: synthesised
promoted_to: retrospective-specification
linked_things:
  - id: operating-layer-quality-loop
    relation: implements
    notes: "The carrier that built the remedy, 2026-08-28. It records what shipped and where the built shape departs from the shape captured below"
  - id: cumulative-drift-is-invisible-to-per-change-walks
    relation: extends
    notes: "Names the drift class and extends it to a whole layer: skills sit outside every individual blast radius because the thing that moves — practice — is not a thing with edges"
  - id: coherence-is-a-maintained-rate-not-a-state
    relation: extends
    notes: "The rate doctrine applied to a tier whose inspection interval is currently infinite: the operating layer has no scheduled read at all"
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "The floor half of the remedy already part-exists there: the skills-directory-vs-artifacts stub check (added 2026-08-08), specced and unbuilt"
  - id: retrospective-specification
    relation: informs
    notes: "Names the hook where the judgement half belongs: the retrospective is the framework's one sanctioned home for whole-corpus quality sweeps, and none of its five scans reads a skill"
  - id: session-memory-specification
    relation: references
    notes: "The asymmetry's other half: the memory layer's quality loop (session-end disposition, retrospective triage) is exactly the pattern the operating layer lacks"
  - id: workflow-run-is-the-decomposition-principle-applied-to-processes
    relation: references
    notes: "The latent tension this insight surfaces but does not open: two homes for process knowledge — the scaffolded workflow skill and the workflow-definition thing"
  - id: reflexive-behaviors-are-indexes-plus-prompts
    relation: references
    notes: "The remedy shape is that pattern's next instance: a same-builder proxy (index-grade fact) feeding a bound prompt (judgement) at retrospective cadence"
---

# The Operating Layer Has No Quality Loop

## The Insight

The framework's memory layer — things and insights — has a quality loop at
two cadences: session-end forces a disposition on every standing insight, and
the retrospective triages the population, scans for conflicts, audits the
schema vocabulary. The operating layer — AGENTS.md and the skills — has no
equivalent. Layer 3 is audited; Layers 1 and 2 are not. A skill is only ever
touched when a named inflection happens to walk through it.

And the way the operating layer degrades is precisely the way a walk cannot
catch: **the skills drift by standing still.** Nobody changes them wrongly —
the domain's practice moves around them. Practice lives in the commit stream,
not the graph; it is not a thing with edges, so no blast radius ever includes
the skills, no cue ever fires for them, and no change-time pass will ever
reach them. This is `cumulative-drift-is-invisible-to-per-change-walks`
promoted from a perimeter observation to a structural one: an entire layer of
the three-layer architecture sits permanently outside the change-driven
consistency mechanism, and the sweep that should cover it does not exist.

## The Felt Instance

The workflow skill, estate-wide (operator report, 2026-08-18). Domains in
heavy daily use; the workflow skill scaffolded at birth and forgotten since,
while the actual workflow emerged ad hoc from the ebb and flow of things
changing and insights arriving. The read, write, and specification skills at
least describe surfaces every session keeps touching, so their drift is
bounded by contact. The workflow skill describes a process nothing enacts —
while the enacted process goes unwritten. Defined process and enacted process
have diverged completely, and no mechanism noticed.

## Coverage Today (measured against the live floor, 2026-08-18)

- `validate` — skills are things: structure, references, schema. Zero content
  awareness.
- `coherence` — template residue (catches *never authored*, not *authored and
  now wrong*); stable-staleness (a label proxy).
- `candidates`/`touchpoints` — `skill` is a definition-surface type: flags a
  skill being *changed*, never a skill being *wrong*.
- Change-reconciliation Walk — reaches skills only when a human names an
  inflection; standing-still drift never names one.
- Retrospective — five reflexive scans; none reads a skill.
- Session-end — no operating-layer surface at all.

## The Remedy Shape (captured, not yet built)

Two mechanisms, forced apart by the suppression-list gate — the semantic
question cannot be floored, and the mechanical facts should not wait for
judgement:

1. **Floor half — same-builder proxies.** The backlogged
   skills-directory-vs-artifacts stub check, plus a new
   *skill-age-vs-domain-velocity* Info: this skill was last touched at the
   birth commit while `things/` has moved N commits. Pure git, no suppression
   list, fires at every pre-commit like stable-staleness — the fact that makes
   the forgotten skill impossible not to see, regardless of whether anyone
   steps back.
2. **Judgement half — a `review-skill-coherence` bound prompt** at the
   `retrospective` hook: sibling of `review-schema-coherence`, scan #6 in the
   reflexive list. Inputs: the skill files + AGENTS.md, the schema index, and
   the commit stream since the last retrospective — because the commit stream
   *is* the record of enacted practice, the thing the skills claim to
   describe. It forces a per-skill disposition — confirm-current / update /
   park / retire — the same brake that keeps insight triage from becoming
   observation without action.
3. **The workflow skill gets a bidirectional question.** Not just "is the
   defined workflow stale?" but: (a) is it dead vocabulary — never enacted,
   park or retire it honestly; and (b) has a *de facto* workflow emerged in
   the commit stream that deserves codifying? The ad-hoc ebb and flow is a
   workflow; it is just unwritten. Two names for one meaning, process-shaped.

## The Latent Conflict (named, not opened)

The framework now keeps process knowledge in two homes: the scaffolded
workflow *skill* (Layer 2, prose capability) and the `workflow-definition`
*thing* (Layer 3, stages as data). Lived use suggests the skill file is the
wrong grain for emergent process and the thing is the right grain for
repeatable process. A candidate `type: conflict` at the framework root —
deliberately not opened here. Capture first; broaden soon.

## The Caveat That Shapes The Build

A mechanism bound only to the retrospective inherits the retrospective's
silence: it is operator-invoked, and the very condition this insight
describes — lost in the inputs and outputs, no stepping back — is the
condition under which retrospectives don't get written. The floor half is
what breaks that circularity: it runs at every commit and keeps the fact in
view until the retrospective happens. And `retrospective.md`'s "triggered by
volume" clause has an obvious sibling waiting: *skills untouched while the
domain crossed N commits* as a trigger to write one.

## Promoted — 2026-08-28

Built by [[operating-layer-quality-loop]], which holds the build record. The
title claim no longer holds: the operating layer now has a quality loop at
both cadences — a Warning at every commit, `review-skill-coherence` as
reflexive scan **7** (not 6; the conditions-met pass took that slot at the 08c
retrospective), and the cadence trigger this file's last paragraph called for,
landed in `retrospective.md` → When To Write One at ~25 `things/` commits.

**The floor half is not the one captured above, and the difference is the
point.** Five defects found by hand on 2026-08-28 across three domains were
mostly not age-shaped — they were *schema-vocabulary* drift, which is keyed to
a declared authority and therefore mechanically decidable. So the floor half
shipped as a vocabulary check (a type, status, or field a skill instructs that
`_schema.yaml` and the tool's reserved sets never declared) rather than as the
skill-age proxy. It says *wrong* where age says *possibly stale*, and it needs
no suppression list for the same reason age didn't.

**Skill-age was declined as a floor Info, and its signal re-homed rather than
dropped.** Measured: at threshold 25 it fires on 12 of the estate's 58 skills
at every commit, permanently, with no honest way for a correct-and-rarely-
edited skill to say "walked, still current". It ships instead as the
retrospective trigger, where a recurring line is the agenda. And the evidence
cut against it twice: the low-activity instance — six undeclared types
standing for weeks — sat at five `things/` commits, so age would have missed
it while the vocabulary check names it outright. The lifting condition is
recorded on the plan.

**The Latent Conflict above was resolved before this built**, on 2026-08-27 by
`derivation-shape-settled-2026-08`: both homes stay, doing different jobs, and
the workflow skill is the corpus-local anchor for framework lineage. The
bidirectional question survives into the prompt; the conflict was never opened
and does not need to be.

**What did not land.** The backlogged skills-directory-vs-artifacts stub check
remains open in `mechanical-coherence-checks-backlog`, and cases 4–5 of the
2026-08-28 set (a skill instructing an edge to a foreign id; a skill
instructing a commit of a deleted file) are reference drift, not vocabulary
drift — the broken-body-reference item is their home.
