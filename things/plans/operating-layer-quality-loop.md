---
id: operating-layer-quality-loop
type: plan
status: completed
version: 2.0
created: 2026-08-18
priority: medium
tags: [coherence, skills, retrospective, quality-loop]
linked_things:
  - id: the-operating-layer-has-no-quality-loop
    relation: implements
    notes: "This plan is the insight's remedy shape given a forward carrier; the insight owns the reasoning and is not restated here"
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Owns the skills-directory-vs-artifacts stub check, still open. The floor half shipped here passed that backlog's suppression-list gate and its standing advisory-scoping test; the skill-age Info it originally proposed did not, and is declined below with its lifting condition"
  - id: retrospective-specification
    relation: references
    notes: "The hook home: the judgement half landed as reflexive scan 7 (not 6 — the conditions-met pass took that slot at the 08c retrospective), and the cadence sibling landed in When To Write One"
  - id: derivation-shape-settled-2026-08
    relation: references
    notes: "Closed the original deliverable 3 on 2026-08-27, before this plan executed: both homes stay, different jobs. The prompt cites the ruling rather than re-opening it"
  - id: estate-workflow-derivation
    relation: references
    notes: "The sequencing that held this plan last: its MVP gate was met (cb68dfb), which is what released this work"
  - id: judgement-checks-need-a-suppression-list-which-is-itself-drift
    relation: implements
    notes: "The gate the vocabulary check had to pass, and the reason skill-age was routed to judgement cadence instead"
  - id: an-advisory-is-scoped-by-who-can-perform-its-remedy
    relation: implements
    notes: "Population scoped to non-deprecated skills + the entry file; generated managed blocks stripped before reading"
---

# Operating-Layer Quality Loop

**Shipped 2026-08-28.** The operating layer now has a quality loop at both
cadences — a fact-shaped check at every commit and a judgement pass at
retrospective — plus the cadence trigger that says when the judgement pass is
owed. The reasoning stays in
[[the-operating-layer-has-no-quality-loop]]; this plan records what was built,
and where the built shape differs from the planned one.

## Why the shape changed

The plan's deliverable 2 was an **age** check: a skill untouched since its
birth commit while `things/` moved N commits. Five operating-layer defects
were then found by hand across three domains on 2026-08-28, and **most were
not age-shaped.** They were schema-vocabulary drift — a class that is
mechanically decidable, because it is keyed to a declared authority:

1. A workflow skill instructing six `type:` values its `_schema.yaml` never
   declared.
2. A specification skill contradicting its schema on four status
   vocabularies — one with **zero overlap**, so every value a session could
   have written from that description would have been refused at the commit
   boundary. It had stood two and a half months and 44 `things/` commits.
3. The same skill listing 13 field names registered neither in
   `known_fields` nor in the tool's core set.
4. A write skill instructing a `linked_things` edge to a framework spec id —
   a hard Error from inside a domain corpus.
5. A write skill instructing a commit of a file the domain deleted two
   months earlier.

Cases 1–3 are keyed to `_schema.yaml` plus the tool's reserved sets and
`CORE_FIELDS`. That is a sharper instrument than age on both axes: it says
*wrong*, not *possibly stale*, and it needs no suppression list. Cases 4–5
are reference drift rather than vocabulary drift and stay out of scope; the
broken-body-reference item in the backlog is their natural home.

Age was reduced to a secondary candidate and, on its own merits, **declined
as a floor Info** — see below. Its signal was not dropped: it ships as the
retrospective trigger in deliverable 3, at the cadence where a recurring line
is the agenda rather than the noise.

## What shipped

1. **Floor half — operating-layer vocabulary drift** (`Warning`,
   `mdllm coherence`, domain scope).
   `tools/markdownllm/skill_vocabulary.py`, joined to `coherence_findings`
   in the corpus-general section, so every domain inherits it through the
   same pre-commit hook. It reads the skills (`type: skill`, or the
   `skills/*.skill.md` layout `mdllm scaffold` writes and
   `mdllm domain-kernel` routes — the estate's *specification* skills carry
   `type: specification`, and two of the five defects lived in one) and the
   authored sections of the entry file, and names any thing type, status
   value, or frontmatter field the corpus never declared.

   - **Suppression-list gate: passed by construction.** The schema is what
     the floor enforces on every thing; the skill is prose about it. There is
     no allow-list and none is possible — the only way to quiet a finding is
     to make the two agree. When the schema moves, the check's answer moves
     with it.
   - **Advisory-scoping test: passed by scoping the population.** Remedy as
     an imperative: *correct the prose, or declare the vocabulary*.
     `deprecated` skills are out (their instructions are withdrawn; rewriting
     a retired file is not a remedy anyone performs); `draft` skills are in,
     because a draft skill is loaded at session start like any other and the
     archetype instance was `draft` while being read daily. Generated
     `<!-- generated: -->` blocks are stripped before reading, so the check
     can never name a remedy that belongs to a generator.
   - **Severity: Warning, one severity for one class.** This is the prose
     sibling of the schema-gated field-registration check, which is itself
     advisory. It is never "may be intentional" (so not Info), and blocking
     every commit in a live domain on a prose defect would wedge unrelated
     work (so not Error).
   - **Precision over recall, deliberately.** Four positions count as an
     instruction and nothing else does: a frontmatter template inside a
     fenced block; a heading naming a type; a list step or table cell naming
     one; and a `status` vocabulary line or **Key fields** list under a type
     heading. Running prose that *mentions* a type is never a finding, and
     neither is anything inside a parenthetical — `(e.g., \`type: x\`)` is
     correct writing about a type that need not exist, and it was the
     estate's one would-be false positive. Each leg stays silent where the
     corpus declares no authority: no types declared, no `known_fields`
     registered, or a type whose statuses are the universal default.

   Regression-tested against the defects it was built from: replayed against
   the pre-fix blob, it reproduces case 2 and case 3 exactly (13 fields; four
   types' status vocabularies, `income-record` first, and all three phantom
   urgency bands), and case 1 in full.

   **Known coverage limit, recorded rather than discovered later.** At the
   framework root the population is empty: the framework's own Layer 2 lives
   in `templates/`, which every corpus walk excludes, so only its entry file
   is read. That is correct for now — the template skills are *sources* for
   domains rather than this corpus's operating layer, and a newborn domain's
   copies are checked in the domain — but it means a vocabulary defect
   authored into a template would be caught at each domain's first commit
   rather than at the framework's. `template_source_findings` is the natural
   home if that becomes felt.

2. **Judgement half — `review-skill-coherence`**,
   `templates/prompts/review-skill-coherence.md`, bound to the
   `retrospective` hook; registered in `orchestration.md` (framework prompts,
   the anchor table, the retrospective binding example, the directory tree)
   and added to `retrospective.md` as **reflexive scan 7**. Also added to
   the four retrospective ritual surfaces (`.claude/commands/`,
   `.github/prompts/`, and the two shipped templates), which is where the
   scan is actually invoked.

   It reads the commit stream **first**, before any skill file, because the
   commit stream is the record of enacted practice and reading the skills
   first anchors the reviewer to the written process. It forces a per-skill
   disposition — confirm-current / update / park / retire — with
   confirm-current owing its evidence. The workflow skill gets the question
   both ways: dead vocabulary, and separately a de facto process worth
   codifying.

3. **Cadence sibling** — `retrospective.md` → When To Write One now carries
   *a skill untouched while `things/` moved more than ~25 commits*. N is read
   off the estate rather than invented: the archetype defect stood through 44
   `things/` commits, and across the estate's 58 skills on 2026-08-28 a
   threshold of 25 selected 12 and left 46 quiet — the top fifth in view,
   with the archetype raised about halfway through its life. The entry says
   so, and says to move the number when the evidence moves.

## Declined, with its lifting condition

**Skill-age as a floor Info.** Measured across the estate on 2026-08-28: at
threshold 25, 12 of 58 skills fire; at 40, 8; and one — a specification skill
at 142 `things/` commits since its last touch — would fire on every commit
for the rest of that domain's life. There is no way for a skill that is
*correct and rarely edited* to tell a git-derived pin "walked, still current"
except by modifying the file, which is the authored marker the perimeter
check deliberately refused. That check accepted the same cost for four files
at release cadence and recorded the revisit condition; this would pay it for
a fifth of every domain's operating layer at commit cadence.

Two further facts decided it. The age signal's yield beyond the vocabulary
check was one domain's four skills, where its answer is *maybe* rather than
*wrong* — and the low-activity instance, six undeclared types standing for
weeks, sat at 5 `things/` commits, so age would have missed it entirely while
the vocabulary check names it outright. **Lift when** either a skill acquires
an honest "walked, still current" marker that is not itself a
hand-maintained surface, or the retrospective trigger is observed being
ignored — that is the condition, not a schedule.

## Exit

Met. The floor half fires in the estate on its first run — three domains, ten
findings, including one defect no hand pass had found (a write skill's
supplier template instructing `status: active` against a schema declaring the
universal vocabulary). The judgement half runs at the next real retrospective
on a live domain. The original deliverable 3 was resolved on 2026-08-27 by
`derivation-shape-settled-2026-08` and is not re-opened.
