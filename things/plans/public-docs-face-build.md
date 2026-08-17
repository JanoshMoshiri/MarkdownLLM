---
id: public-docs-face-build
type: plan
status: not-started
version: 1.1
created: 2026-08-13
priority: high
tags: [documentation, accessibility, derivation, publication, pages, visibility]
linked_things:
  - id: public-docs-face-is-derived-not-restated
    relation: implements
    notes: "The ruling this builds. It settled the surface (Pages from docs/ on main), ruled out the wiki on mechanism, and separated the public face from `exposed`. It deliberately did not build anything or settle the selector — that residue is this plan."
  - id: every-reader-class-needs-its-own-kernel
    relation: implements
    notes: "The principle that decides what belongs on the face: derive the entry surface, author only what has no upstream owner."
  - id: derived-transport-is-not-derived-content
    relation: implements
    notes: "The gap this plan closes. The ruling satisfied the transport axis cleanly; every phase below is the content axis."
  - id: a-generated-surface-collapses-its-walk
    relation: references
    notes: "Supplies the sequencing argument for Phase 1: deriving the toolbox before the vendor plan's Phase 7 turns 28 walk steps into one."
  - id: a-shared-worktree-merges-authorship-at-the-index
    relation: references
    notes: "Names the mechanism behind this plan's hold. The contention that stopped Phase 1 was the shared git index, not the file overlap — and this plan's own hold notice is the instance that insight was harvested from."
  - id: vendor-harness-adapter-foundation
    relation: references
    notes: "Its Phase 7 owns every harness *capability claim* in the docs. This plan owns how the docs are built and where their words come from. Neither may edit the other's fact."
  - id: coherence-mechanism-build
    relation: references
    notes: "Its Phase 1 owns deriving the root AGENTS.md — the same primitive one layer in. Sibling, not overlap: that is the agent's entry file, this is the human's."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Sole owner of any new mdllm coherence check, including the accDescr drift check named below. Routed there, not built here."
  - id: evidence-and-eval-backlog
    relation: references
    notes: "Its Bucket 3 owns the authored evidence content (limitations, the why-not-CLAUDE.md answer, concurrency, the Obsidian claim test). This plan owns none of that writing."
  - id: scaffold-declares-visibility
    relation: references
    notes: "Its parked consideration — whether visibility becomes a declared frontmatter fact — is the same axis as this plan's selector question, at domain birth rather than at the framework's own face."
---

# Public Docs Face — Build The Surface, Derive Its Words

[[public-docs-face-is-derived-not-restated]] ruled *where* the documentation
face lives and *what principle* governs it. It built nothing, by design: the
surface decision cost nothing and claimed nothing, while the content had to wait
on evidence. This plan is the residue — the build, and the half of "derived" the
ruling did not reach.

## Held (operator, 2026-08-13) — release condition named

Execution is held on the operator's call, taken the day this plan was written.
The reason is contention, not doubt: `docs/operator-guide.md`,
`docs/framework-map.md`, and `README.md` were all mid-edit by the Codex agent
while it landed `--refresh-legacy`, and inserting generated blocks into files
another agent is actively rewriting buys a merge conflict in a
twenty-eight-row table.

**Release condition:** the adapter work reaches a quiet point — those three
files committed and the working tree clean of them. Phase 1 needs no other
gate.

**What may proceed under the hold, if it is lifted piecemeal:** the generator
itself is a new module (`docs_blocks.py`, shaped like `kernel_gen.py`, whose
`build_kernel` is shared by `kernel` and `coherence` so the two cannot disagree
about the artifact). It contends with nothing. Both the CLI registration
(`cli.py` is contended) and the block insertion wait regardless. Substrate code
here falls under [[code-architect-governs-substrate-code]], so that domain's
skills are read before the module is written, not retrofitted after.

The framing that makes the phases fall out is
[[derived-transport-is-not-derived-content]]. Pages-from-`docs/` satisfies
**transport** completely: same repo, same commit, same pre-commit hook, same
boundary check, same CI. It leaves **content** untouched — and the content
inside `docs/` is where the corpus's hand-restatement is concentrated.

## What this plan owns — and what it must not touch

The documentation surface has five owners already. Restating any of their items
here would be the exact failure this plan exists to fix, so the boundary is
stated before the work:

| Fact | Owner | Not this plan because |
|---|---|---|
| Harness **capability claims** in README, operator-guide, first-hour, domain guide, scaffold output | [[vendor-harness-adapter-foundation]] Phase 7 | Those claims change when the adapter build changes. Includes the README's live 5R gate prose. |
| Deriving the **root AGENTS.md** blocks | [[coherence-mechanism-build]] Phase 1 | Same primitive, different reader — that entry file serves the agent. |
| Any new **`mdllm coherence` check** | [[mechanical-coherence-checks-backlog]] | It holds the suppression-list gate that decides what may become a check. |
| **Evidence content** — limitations, the why-not-CLAUDE.md answer, concurrency, the Obsidian claim test | [[evidence-and-eval-backlog]] Bucket 3 | Blocked on operator sessions 1–2; it is dictation from memory, not derivation. |
| The manifesto's **Standing On Shoulders** extension | [[external-review-response-2026-08-10]] R5 | Explicitly the operator's voice. |

What is left, and genuinely unowned, is: **the build, the content axis inside
`docs/`, the selector, and the size/entry gap.**

## Phase 1 — Derive the words *(owned here; do this before vendor Phase 7)*

Two surfaces in `docs/` restate a mechanical source that already exists:

- **`operator-guide.md`'s toolbox table** restates `mdllm --help` across roughly
  twenty-eight rows. The tool already learned this lesson internally — its own
  help text records *"a hand list drifts; argparse does not"* after a review
  found it describing twelve of twenty-six subcommands. The guide did not
  inherit the fix.
- **`framework-map.md` Views 2 and 3** restate `linked_things` frontmatter and
  that same `--help`. View 3 is a subcommand→spec mapping; the subcommand column
  is mechanical and the spec column is judgement, so the split is the same one
  Phase 1 of [[coherence-mechanism-build]] draws for the Tier-2 routing table:
  generate the rows, author the annotations.

Deliverable: a generated block in each, produced from the live source and
drift-gated the way `kernel --check` gates its predecessor. The map's own
*Keeping This Map Honest* section is the specification for what to derive — it
already names each view's mechanical source, and it exists because the map has
drifted against them before.

**Why this is urgent — corrected at v1.1, by observation.** This plan first
argued the saving was a race against vendor Phase 7: reconcile the toolbox
before Phase 7 arrives, and Phase 7 pays one walk step instead of
twenty-eight. **That framing was too tidy and the same day disproved it.**

Capability claims do not wait for a reconciliation phase. They reconcile
*continuously, per flag*, because a flag ships with its documentation — which
is correct behaviour, not a process breach. The live instance: on 2026-08-13
the Codex agent added `--refresh-legacy` and the one change required **four
hand-restatements** — the argparse help in `cli.py`, the `adapter-install` row
of the operator-guide toolbox, the README's CLI listing, and the
`adapter-install` note under framework-map View 3. Three of the four are
derivable from the first.

So the cost is not a cliff at Phase 7; it is a **per-flag tax already being
paid**, and every CLI change until Phase 1 lands pays it again
([[a-generated-surface-collapses-its-walk]] — restatement count is
reconciliation cost, metered here in real time). That is a stronger argument
than the original, and it is evidence rather than projection: the framework
watched its own thesis cost it four edits where one would have done.

## Phase 2 — Stand up the build *(owned here; the switch is operator-gated)*

GitHub Pages from `/docs` on `main`, per the ruling. The agent-side work is the
build configuration and whatever nav/outline scaffolding the generator needs.

**The switch itself is not agent work.** Enabling Pages publishes this
repository to the internet, and the framework root carries `autopush: false`
precisely because publication here is a deliberate human act. The agent
prepares the diff; the operator throws the switch.

What the build buys, and could not be had otherwise: a document outline,
landmarks, a skip link, in-page search, a sensible measure, and
`prefers-color-scheme`. These are the accessibility items that are *free from
structure* — the build derives them from headings that already exist.

## Phase 3 — Settle the selector *(operator decision; no build)*

The ruling parked this as "only real once something outside `docs/` wants
publishing." It is already real, and its own accessibility section is why: it
names `orchestration.md` (48KB), the manifesto (41KB), and
`domain-specification-guide.md` (40KB) as the entry problem — all three at root,
outside `docs/`, where the largest file is 25KB. The chosen selector excludes
the files the accessibility argument is about.

Three answers, and the choice is the operator's:

1. `docs/` stands; the root specs stay on the blob view and the entry gap is
   accepted as scoped-out.
2. The selector widens to a named set including the Tier-1 and Tier-2 specs.
3. A per-thing public marker is earned — **distinct from `exposed`**, which
   [[public-docs-face-is-derived-not-restated]] ruled against reusing, because a
   consuming domain is an authorised reader and the internet is not.

If (3), note that [[scaffold-declares-visibility]] parks the same axis at domain
birth. Whoever settles one should read the other; a declared visibility fact in
frontmatter would serve both, and inventing two vocabularies for one axis is the
conflation that ruling already warned about.

## Phase 4 — The size and entry gap *(owned here; unstarted, deliberately)*

The real accessibility finding is that a build cannot fix a 48KB specification.
Nav and search make a long document navigable; they do not make it enterable.
The honest options are spec decomposition (high blast radius — these are Tier-1
and Tier-2 surfaces every domain reasons from) or a derived human digest, which
is [[every-reader-class-needs-its-own-kernel]] taken literally: the agent got
`kernel.md` for exactly this reason, and the human reader has no equivalent.

Not started here because it depends on Phase 3's answer and because a
decomposition proposal is a spec change, not a docs change. Named so it is a
decision when it is taken rather than a discovery at the next release walk.

## Routed elsewhere, recorded so it is not lost

- **accDescr drift check** — a mermaid block changing without its `accDescr`
  changing in the same commit. Nine hand-authored descriptions landed 2026-08-13
  and nothing checks them; by this plan's own principle that is walk debt, and
  since prose-from-graph cannot be derived, the honest answer is a check.
  Same-builder, diff-scoped, no suppression list — it passes
  [[mechanical-coherence-checks-backlog]]'s gate. **Routed there, not built
  here.**
- **README's live 5R gate prose** — three paragraphs of in-flight adapter state
  in a project README, which the perimeter-currency item and vendor Phase 7 both
  reach. **Vendor Phase 7's**, as a capability claim.

## Deferred until vendor Phase 7 lands

Whether the README compatibility table should be **derived** from evidence
records and `doctor` output rather than hand-maintained — the verified-vs-
designed-for surface a cold evaluator currently cannot get in one place
(`evidence/README.md` names this scatter as the meta-risk). It is the right
question and the wrong moment: Phase 7 is about to rewrite those rows, and
deriving a surface that is about to be rewritten is wasted work. Ask it
immediately after, when the question becomes *should this table ever be
hand-written again?*

## Done when

- [ ] Phase 1: toolbox and map Views 2–3 carry generated blocks, drift-gated
- [ ] Phase 2: build configured, diff reviewed, operator has thrown or declined the switch
- [ ] Phase 3: selector settled — one of the three answers, recorded as a decision
- [ ] Phase 4: decomposition-or-digest judged, or consciously declined
- [ ] accDescr check routed to the backlog and accepted or rejected by its gate
- [ ] The deferred compatibility-table question asked once Phase 7 closes

## What this plan deliberately does not do

No umbrella restatement of the five owners' items — one owner per fact applies
to plans as much as to prose. No new authored guide: every phase either derives
an existing truth or asks a question whose answer is a decision. No content
about the harness adapters, which the ruling held until their gates are green
and which is Phase 7's regardless.
