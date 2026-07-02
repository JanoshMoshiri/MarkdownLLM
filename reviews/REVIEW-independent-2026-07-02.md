---
id: independent-review-2026-07-02-fable
type: artifact
status: stable
created: 2026-07-02
linked_things:
  - id: independent-review-2026-06-15-cowork
    relation: extends
    notes: "Fifth independent review; first full Fable read since v3.4.0 (2026-06-11). Covers the v3.5 → v3.17.3 arc end-to-end."
---

# Independent Review — MarkdownLLM Framework v3.17.3

Full read of every tracked file: all 23 foundational specs, kernel, AGENTS.md,
`tools/mdllm.py` (2,935 lines) and its 97-test suite, all 56 insights, 5 plans,
3 decisions, 1 conflict, 5 retrospectives, 4 prior reviews, all templates,
adapters, evals (fixtures, seeds, README, results conventions), both examples,
docs, installers, CI. Verified from HEAD: `mdllm validate .` clean across all
corpora, `coherence` 2 Info only, 97 floor self-tests green.
Reviewer: Claude (Fable), 2026-07-02. Prior Fable review: v3.4.0, 2026-06-11.

## Verdict

The last Fable review closed on: *"point the v3 medicine at the periphery and
at one user who isn't you, and this stops being an elegant self-describing
system and starts being a product."* Half of that happened, and the half that
happened is genuinely impressive. The corrective loop **reversed polarity** —
where the framework once answered every failure with new prose machinery, the
v3.14 → v3.17.3 arc is a run of *deletions and reverts executed on principle*:
two orchestration prompts removed, the WORKLOG retired, `continuity.md`
dissolved into the graph, the MCP live-agent surface built and then reverted in
full, and a freshly built coherence check (retired-vocabulary) reverted within
a day because it needed a suppression list — with the razor that killed it
(`judgement-checks-need-a-suppression-list-which-is-itself-drift`) captured as
a reusable gate. A system that can build a mechanism, recognise within
twenty-four hours that the mechanism is judgement in mechanical clothing, and
delete it *without losing the reasoning* is doing something almost no software
project does. That is the strongest single finding of this review.

The half that didn't happen is the same half as June: **the evidence**. The
framework has spent three weeks perfecting the machine and zero sessions
producing the disclosable proof every reviewer since June 11 has ranked first.
`evidence/` contains a README and a template and no records;
`evidence-and-eval-backlog` sits at `not-started`; the longitudinal
drift-resistance eval — the untested half of the actual thesis — remains
untested; the bare-control isolation fix is specified and undeployed. The
framework is now systematically better at the work it can control (internal
coherence) than the work it can't (external proof), and it keeps choosing the
former. That is the review's headline risk, unchanged in kind since June,
sharpened by three more weeks of the pattern.

## What Works Well

**The floor is now a family with one signature.** In June the floor was
`validate` plus early satellites. It is now twenty subcommands that all share
one design signature: *detect mechanically, dispose semantically, never mutate
domain state* — `touchpoints`/`cascade` as an explicit mirror pair, `coherence`
self-scoping between framework and domain roots, `doctor` execution-testing
rather than resolution-testing, `scaffold` exiting non-zero on partial birth,
`session-start` generating orientation instead of trusting recall,
`imports-check` reporting stale pins without flipping them. The consistency of
that signature across the whole surface is rare, and it is what makes "never
re-perform a mechanical check by reasoning" safe to obey.

**The insight lifecycle has teeth now.** Graph-keyed liveness (an inbound edge
from a non-terminal thing), the floor orphan check, `keep-active` with a
mandatory reason, the end-session disposition brake paired with capture, and
triage at retrospective — this is the first agent-memory design I have seen
with an actual *retirement* mechanism rather than an append-only pile. The
continuity dissolution that produced it was clean architecture: backward →
commit stream, forward → thing graph, liveness → graph property. The fade-class
diagnosis (insights rot because their end-of-life is a fade, not an event) is
exactly right.

**The epistemics are still the best-in-class feature.** Three claims kept
deliberately apart in the manifesto (thesis / utility / model-tier corollary),
excluded eval trials preserved with evidence rather than deleted, the
control-leak kept as a result (`withholding-is-not-isolation`), and the
premature-publish incident recorded symmetrically about both parties rather
than smoothed over. `the-rough-true-account-is-generative-infrastructure` is
not a platitude here; the corpus visibly lives it.

**The razor corpus is becoming the real product.** Discovered-not-authored;
same-builder checkability as the gate for floor checks; the same-builder
blindness caveat; existence ≠ currency; repeated-drift-promotes-a-fact;
hard-invariants-encode-a-semantic-assumption; the two reflection axes as a
mechanism generator. These are transferable engineering principles, each paid
for by a documented incident. They generalise beyond this framework, and they
are the part of the corpus a future reader will quote.

**The eval discipline matured.** `sleeping-bag-fac` is a genuinely
well-designed discriminator (unleakable synthetic rule, per-trap trips,
condition-neutral core), and the honest reading — structure decided the
figures, scale decided only the convention — is the right emphasis. The
fairness notes and per-assertion reporting remain more honest than most
published benchmarks.

**The cross-domain arc held the line.** Read-only face, opt-in `exposed:`
membrane, egress source-scoping (the producer's private graph never crosses),
per-thing commit pins, consumer-side re-quarantine — minimal and disciplined.
And the Phase 3 revert is the razor working at the moment of maximum
temptation: the capability was *built* and still removed because dormant
execution code behind an opt-in flag is the honour-system control the floor
exists to replace.

## Contradictions and Staleness (new, specific)

The corpus is remarkably coherent for its size — my full read found only
small drift, and all of it in exactly the tier the framework predicts (prose
dark region, periphery). That prediction being right is itself a finding.

1. **`templates/workflow-definition.md.template` contradicts
   `workflow-state.md`.** Its body says runs "link here with
   `relation: instance-of`" — the pre-v3.10 design. The spec moved the pointer
   to the structural `definition:` field (v3.10 review action #1), and the run
   template correctly uses it. Prose residue in a birth-path file: the exact
   class review #1 flagged, one template over.
2. **`session-memory.md` still speaks of the brief in live voice.** Its
   Relationship section reads "Insight things and continuity brief updates are
   committed following standard conventions" — a live reference to an artifact
   the same spec declares retired. The v3.17.1 sweep fixed this class in
   `things/insights/` and missed it in the spec that owns the retirement.
3. **`git-workflow.md` heading residue:** "## Three Layers Of Auditability"
   sits over text that says "two complementary audit layers — both git."
   WORKLOG-retirement editing residue.
4. **`CONTRIBUTING.md` is a third hand-maintained catalog copy, and it is
   stale.** It lists ~12 foundational specs (missing provenance,
   change-reconciliation, workflow-state, coordination-claim, derived-index,
   trigger-specification, and more) and says frontmatter requires "at minimum:
   id, type, status, **version**, created" — `version` is not required by
   `thing.md`. `coherence` guards `.markdownllm` ↔ disk and `TIERS` ↔ catalog;
   CONTRIBUTING restates the catalog with no guard. Per the framework's own
   principle: point it at the sentinel rather than policing a restatement.
5. **The `stale` trigger reads file mtime, not git.** `cmd_triggers` uses
   `t.path.stat().st_mtime` — wrong after any fresh clone (mtime = checkout
   time) and inconsistent with `thing-lifecycle.md`, which defines
   `last_active` from git history. A spec/floor divergence in the lit region;
   `git log -1 --format=%cd -- <file>` is the same-builder source.
6. **The examples are the periphery going stale again.** Both examples carry
   `framework_version_seen: 3.4.0` (thirteen minor versions behind) and
   pre-domain-kernel AGENTS.md shapes, while the template teaches managed
   blocks. The `session-start:version-check` hook never fires for them —
   nobody opens an example as a workspace — so no net catches this. Newcomers
   read examples first; they currently teach the pre-v3.15 entry surface. A
   floor-shaped fix exists: `coherence` at a framework root could compare each
   example's `framework_version_seen` against the sentinel (same-builder, no
   suppression list needed).
7. **Terminology drift: "Level 4" vs "Layer 2."** `validate.thing.md` renamed
   the semantic layer to Layer 2; the `mdllm.py` docstring and
   `operator-guide.md` still say "Level 4."
8. **The framework's own root `AGENTS.md` (~250 lines) is not kernel-shaped**
   while the framework mandates the domain-kernel discipline for domains —
   the 06c retrospective's open question, still open. A mild fractal
   violation: the rules apply to themselves, except this one.

## Over-Engineered

**The standing-razor population is becoming a second spec layer.** 56 insights,
~15 held `keep-active`. The disposition machinery keeps the population
*triaged* but not *small*, and the razor family fragments: existence ≠
currency, repeated-drift-promotes, suppression-list, same-builder-blindness
are four files a reader must cross-reference to hold one idea-cluster.
"Relate, don't merge" is right per-pair, but the aggregate read cost grows
every session. Consider a *generated* razor index — one line per keep-active
insight, drift-checked like every other generated artifact — so the standing
razors are loadable at kernel-like cost. (Deliberately not a merge; a map.)

**Prompt frontmatter still carries typed inputs/outputs nothing consumes.**
The soft-orchestration critique from review #1 was half-answered — two prompts
deleted, anchors named, honest labelling — but the `inputs:`/`outputs:`
declarations on the eight framework prompts remain ceremony for an event
system with no runtime. The prose templates are the value; the typing is
residue of the deleted chain-validation.

**`thing-lifecycle.md` has been a parked ghost for six weeks and is now
drifting against the live corpus** (the mtime/`last_active` divergence above
is between it and the trigger floor). Spec-when-foreseeable licenses the spec;
it does not license letting a 473-line draft rot against the tool. Either
trim it to the design skeleton or reconcile its `last_active` definition with
what `triggers` actually does.

**`mdllm.py` at 2,935 lines is a watch-item against the framework's own
cohesion test.** One file now holds a validator, an MCP server *and* client,
an eval harness that spawns headless agents, a scaffold engine, and three
generators. Single-file was a portability virtue at 800 lines; at 3k with a
test suite it is one file with many reasons to change. Not urgent — the
internal seams are clean — but the framework applies SRP to 60-line specs and
exempts its largest artifact.

## Under-Engineered

1. **The evidence, still.** The sanitised validation record has been every
   reviewer's #1 since 2026-06-15 and is worth more than the next three
   releases. It is also the cheapest item on this list — the template exists,
   the shape (a redacted workflow-definition) is mechanically natural, and it
   needs one session with the operator. The pattern to name honestly: evidence
   work keeps losing to mechanism work because mechanism work is what the
   framework-agent loop is *good* at. It will keep losing until it is made the
   explicit next session rather than a backlog row.
2. **The longitudinal eval.** The thesis's drift-resistance half — the one the
   README leads with ("is any of it still true") — has never been tested. The
   sleeping-bag rule is reusable as a component; a three-session fixture
   (build → perturb → resume) would be the first direct evidence for the
   framework's actual differentiator. Single-shot evals test structure supply;
   only a multi-session eval tests coherence maintenance.
3. **Bare-control isolation** — specified since 2026-06-17, undeployed. Every
   future eval inherits the caveat until workspaces leave the repo tree.
4. **The read-side of quarantine, now sharper than when first flagged.**
   `mdllm provenance` blocks *pinning* an unverified external thing; nothing
   constrains *reading* one into context, and `verified: true` is a frontmatter
   flag any agent can write. In June this was theoretical; with MCP imports
   live, external things now arrive over a channel by construction. At minimum:
   an Info when `verified` flips in the same commit that created the thing, and
   the L1-only-until-verified loading rule from review #1 written into
   provenance.md.
5. **Schema migration** — still unspecified (rename a status, retire a field,
   what happens to the existing corpus). Carried since June 11.
6. **`limitations.md` and the comparison answer** ("why not CLAUDE.md plus a
   notes folder?") — still absent. The answer is favourable and the corpus
   still never makes it.

## The Meta-Observation

Four reviews in three weeks converged on the same top action, and the
framework actioned everything *except* it — while executing the other findings
faster and better than any project I have reviewed. The loop from finding →
insight → mechanism → test → deletion-when-wrong is now genuinely excellent.
What the loop cannot generate from inside is the thing it most needs: proof
that lives outside the loop. The maturity of everything else makes the gap
more visible, not less. The framework's own idiom applies: this divergence
between its model of itself ("evidence is the highest-leverage item") and its
reality (three weeks of mechanism) is an unrouted decision. Route it — commit
a session to the validation record and the longitudinal fixture, or revise the
model with recorded rationale and stop carrying the backlog row.

## Priority Recommendations

1. **Produce the sanitised validation record** — one session, template exists,
   worth more than the next three specs. Then the longitudinal fixture.
2. **Fix the six drift findings** (workflow-definition template,
   session-memory brief residue, git-workflow heading, CONTRIBUTING catalog,
   `stale`-trigger mtime, Level-4/Layer-2) — one small reconciliation pass.
3. **Refresh the examples to v3.17 shape** and add the floor-shaped
   example-staleness check to `coherence` (same-builder: the sentinel).
4. **Decide the root-AGENTS.md kernel question** — apply the domain-kernel
   discipline to the framework itself, or record why not.
5. **Generate a razor index** over the keep-active insights instead of growing
   the standing set unindexed.
6. Then the carried queue, in its standing order: read-side quarantine, schema
   migration, limitations.md, bare-control isolation.

The honest summary, in the framework's own idiom: the machine is built, the
loop closes, and the corpus is the most internally coherent it has ever been —
validate clean, coherence quiet, 97 tests green, and a full cold read
surfacing only prose-tier drift exactly where the model says drift hides. What
stands between "an exceptional self-describing system" and "a product someone
else can trust" is no longer any mechanism. It is one document and one eval
the framework keeps deferring, and a periphery that goes stale precisely
because no one lives there. Point the discipline outward.
