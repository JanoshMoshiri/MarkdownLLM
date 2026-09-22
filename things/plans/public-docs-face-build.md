---
id: public-docs-face-build
type: plan
status: in-progress
version: 1.8
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

**Widened by the operator, 2026-08-17 — read this before acting on the line
above.** Closing the session that produced the ruling, the operator stated the
documentation thread is picked up *"in a new session once we've finished all
the phases, and we're at a place where we're ready to work on the
documentation."* That is a **broader** gate than the contention one: not the
first quiet point in the adapter files, but the completion of
[[vendor-harness-adapter-foundation]]'s phases. The contention condition
remains true and necessary — it is simply no longer sufficient. A session that
finds the three files quiet should **not** start Phase 1 on that basis alone.

The reason is the ruling's own: content waits on evidence. Phase 1 derives the
toolbox and map views, and Phase 7 owns every harness capability claim that
flows through them — deriving a surface mid-rewrite is the wasted work this
plan already declines to do for the compatibility table.

**Narrowed to one act, 2026-09-15.** Vendor Phase 8 is ruled and built:
the harness default is gone (`scaffold-harness-is-an-explicit-selection-
2026-09-15`), the adapter-refresh offer stands in `domain-refresh.md` with
the survey in the vendor plan, and 3.41.0 is versioned and changelogged.
**The hold is lifted, 2026-09-18**: that release is published (`origin/main`
at 7409d992) and `vendor-harness-adapter-foundation` is `completed`. Both
gates — the 2026-08-13 contention one and the 2026-08-17 widened one — are
satisfied, and Phase 1 is unblocked agent work from here. Nothing above this
line is a live constraint any more; it is kept as the dated record of what
held and why. And the build that
closed the gate paid the tax this plan meters one more time: one flag's
semantics, eight hand-restated surfaces (`cli.py`, `AGENTS.md`, `README.md`
×3, `operator-guide.md`, `domain-specification-guide.md`, `first-hour.md`).
Phase 1 would have made three of those one.

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

## State after Phase 1 (2026-09-22)

**Phase 1 — complete.** `tools/markdownllm/docs_blocks.py`, `mdllm docs`
(`--check` is the pre-commit coherence leg), `tools/tests/test_docs_blocks.py`
(thirteen tests, one of them the live dogfood: this repository's own docs must
pass the same call the hook makes). Where the derive/check line fell, surface
by surface — the precedent from [[coherence-mechanism-build]] Phase 1 applied,
not re-argued:

- **The operator guide's toolbox — generated.** The 33-row hand table is now
  a managed block: subcommand, exact usage, and the tool's own help, straight
  from argparse, alphabetical (registration order is a code-layout fact a
  derived surface must not drift on). The authored half — *when a human
  reaches for it* — lives beneath the block as one line per subcommand and is
  **checked both ways**: a subcommand with no line, or a line for a vanished
  subcommand, is a coherence Error. Every sentence from the old "When" column
  survived; facts from the old "What it does" column that the tool's help did
  not carry moved into the authored line; the rest is now the tool's to say.
- **The framework map's views — checked, plus a generated companion.** A
  mermaid diagram cannot host a managed block (an HTML comment breaks the
  renderer), so View 2 and View 3 stay drawn and are gated instead: every
  spec on disk must have a View 2 node and any `(status)` tag must match its
  frontmatter; every subcommand must have a View 3 node and every node must
  be a subcommand. What *can* be wholly owned by a block is: the map gained
  **every declared spec-to-spec edge, generated from frontmatter**, beside
  the curated drawing — the drawing shows load-bearing edges, the list shows
  all of them, and the list carries each spec's live `(type, status)` so the
  drawing's tags can be checked against it. The spec each subcommand *serves*
  stays judgement and stays drawn.

**What the check found on its first run — the drift the plan predicted, now
counted.** The hand table listed 33 rows against 37 registered subcommands:
`assemble`, `bundle`, `harness-event`, `precommit`, `runtime-probe` and
`watch` had no row at all. View 2 had no node for `docs/estate-mechanics.md`.
Both were invisible to every cold read since 13 August and are now
mechanically impossible.

**The tax, re-metered.** Before: a new flag meant four to eight hand edits
across `cli.py`, the guide, the README and the map, none gated. Now: a new
flag is one edit to `help=` and the table follows; a new subcommand is the
tool's help, one authored "when" line, and one View 3 node — three edits,
all three refused at commit if missed. The 38th subcommand, `docs` itself,
was the first to pay the new rate, and the gate caught its own missing line
before this commit.

**Classification of the checks, for the backlog's benefit.** Nothing here is
a new check *class*: block drift is the same-builder drift check the kernel
and every domain's AGENTS.md already run; the three completeness checks are
the one-direction routing check the Tier-2 table already runs, applied to
three more authored halves. No suppression list, no judgement — the
[[mechanical-coherence-checks-backlog]] gate is satisfied by construction,
and no new item is routed there.

**Two things deliberately not touched.** The README's CLI examples are
vendor Phase 7's fact (capability claims), and the mermaid `accDescr` prose
still restates the subcommand count by hand — it was walked (37 → 38) and it
remains the accDescr drift check's problem, routed to the backlog below and
unbuilt. A hand-walked count inside a derived-and-gated view is the last
restatement standing in Phase 1's two surfaces.

**Versioned and changelogged as 3.42.0, 2026-09-22.** Between the Phase 1
commit and the release, the full suite's architecture gate refused the
module's one recorded shortcut — a function-local import back into `cli` for
the subcommand inventory closes an import cycle — so the seam was inverted
rather than the scan evaded: the composition root computes the rows once its
parser is complete and hands them down to `mdllm docs` and to coherence's
docs leg; a call without them says *could not look*, never clean
(`f29c96e`; two more tests pin it). The push is the operator's act.

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

**State after Phase 2 (2026-09-22) — thrown.** The operator published 3.42.0
and the build (`632cd4c`) in one instructed act, and Pages was switched on:
`main`, `/docs`, the classic builder, live at
https://janoshmoshiri.github.io/MarkdownLLM/. The build is
`docs/_config.yml` + `docs/index.html` + three `docs/_includes/` files; no
document was touched. Nav labels and order and the `plans/` exclusion are the
build's facts, held in the build. The front door lists every page from its own
frontmatter at build time, and the footer names the commit it was built from.

The first live build served every page and drew no diagram: the theme
compresses a page onto one line, and `//` comments in the mermaid config
swallowed the script. Fixed at `e4a1358` and verified **locally** before
going up — the operator asked to be able to look before it is public, so
`tools/pages/` now holds a Pages-pinned preview (`preview.ps1`; Ruby 3.3 with
the devkit). The preview found a second divergence the live site hid: the
Pages default plugins are only partly active in a bundle unless named, so
`_config.yml` names the four the site leans on. The operator's own read of
the live guide found the third: the toolbox rendered as one unbroken
paragraph. Two renderer differences, both invisible on GitHub's blob view —
kramdown opens an HTML block at any line that starts with a tag (a code
span wrapped onto `<subcommand>`), and it runs a table straight after an
HTML comment into a paragraph. The first was a reflow; the second is now
part of the managed blocks' canonical body (a blank line inside each
marker), so the drift check keeps it. The preview is the check for this
class; nothing mechanical reads a page the way a renderer does.

What the build cannot fix, handed to Phase 3: ten links from `docs/` reach
outside it (README, `kernel.md`, `thing.md`, one insight, the Explorer's
docs) and do not resolve on the site.

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

**State after Phase 3 (2026-09-22) — settled.** Answer (1), with a mechanism
this plan had not named: **the site links out** — a link that leaves `docs/`
is resolved on the site to the repository's own page for the file, at `main`,
so nothing outside `docs/` is rendered twice and the documents keep the
relative links that work in the repository. Ruled by the operator on seeing
the live count of ten: [[public-face-links-out-not-hosts-2026-09-22]]. The
README now carries the site's address at the top and beside its list of the
human-facing documents, on the same ruling ("a must"). What answer (1) costs —
a reader following a link out lands on the blob view — is accepted there in
words, and it is exactly what makes Phase 4 the last door.

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

- [x] Phase 1: toolbox and map Views 2–3 carry generated blocks, drift-gated
      *(2026-09-22 — the toolbox generated; the views checked and given a
      generated edge-list companion, because mermaid cannot host a block)*
- [x] Phase 2: build configured, diff reviewed, operator has thrown or declined the switch
      *(2026-09-22 — thrown: https://janoshmoshiri.github.io/MarkdownLLM/)*
- [x] Phase 3: selector settled — one of the three answers, recorded as a decision
      *(2026-09-22 — answer 1, the site links out:
      [[public-face-links-out-not-hosts-2026-09-22]])*
- [ ] Phase 4: decomposition-or-digest judged, or consciously declined
- [ ] accDescr check routed to the backlog and accepted or rejected by its gate
- [ ] The deferred compatibility-table question asked once Phase 7 closes

## What this plan deliberately does not do

No umbrella restatement of the five owners' items — one owner per fact applies
to plans as much as to prose. No new authored guide: every phase either derives
an existing truth or asks a question whose answer is a decision. No content
about the harness adapters, which the ruling held until their gates are green
and which is Phase 7's regardless.
