---
id: change-reconciliation-specification
type: specification
status: draft
version: 1.8
created: 2026-06-13
linked_things:
  - id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
    relation: references
    notes: "The ruling behind The Walk Runs On Detection: the agent walks on detection within four bounds, the driver rules on the residue through the harness's own prompt, and the agent's commit waits for the walk's record"
  - id: a-preserved-question-is-not-a-done-walk
    relation: references
    notes: "The diagnosis that ended the human cue: five backstops preserved the question, none walked"
  - id: the-verdict-is-asked-where-the-change-lands-2026-10-05
    relation: references
    notes: "The first shape of the gate, superseded the same day: it asked the operator first. Kept as the record of the wrong half."
  - id: thing-specification
    relation: extends
  - id: unattended-cue-carrier-2026-09-12
    relation: references
    notes: "The ruling behind The Cue Persists: any session may raise a cue; a human answers, or the framework agent by citing the ruling that covers it (framework-agent-closes-settled-cues-2026-09-13)"
  - id: inflection-candidates-are-computable
    relation: implements
    notes: "The cue question is mechanical and the verdict is human — the carrier is that split, persisted"
  - id: belief-revision-specification
    relation: complements
  - id: provenance-specification
    relation: complements
  - id: derived-index-specification
    relation: complements
  - id: validate-thing-specification
    relation: complements
  - id: retrospective-specification
    relation: complements
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: implements
  - id: mechanical-assimilation-is-blind-to-prose-dependencies
    relation: implements
  - id: structural-pointers-need-reverse-edge-indexing
    relation: implements
  - id: divergence-is-an-unrouted-decision
    relation: implements
  - id: cross-domain-handoff-is-built-inbound-only
    relation: implements
    notes: "The re-opened quarantine it names as the cue is this spec's inbound external-inflection edge"
  - id: mcp-domain-server-design
    relation: complements
    notes: "Its drift path terminates here: stale/diverged imports hand the human an external inflection"
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Change Reconciliation

## What This Specifies

How a domain stays internally consistent **across change**. Structural validity
is enforced at write time by the deterministic floor; this spec governs the
other half — the semantic consistency that no schema can check, because a
contradiction lives *between* two individually-valid things and is *created*,
never prevented, by a change to one of them.

The premise is deliberately narrow: consistency risk enters whenever the
accepted corpus changes — **addition, modification, deletion, or rename**. A
fresh leaf may have no inbound dependents yet, but it can still duplicate or
contradict an existing claim, seize an existing identity, or expose a new
publication surface. A deletion can withdraw a load-bearing truth; a rename can
break path identity without changing content. Consistency is therefore
maintained at the moment of corpus change, by reconciling the candidate against
everything it touches. This is change management, applied to knowledge.

After this spec, any meaningful change can answer: **"what did I just put at
risk, and is each of those things still true given what I changed?"**

## The Walk Runs On Detection; The Driver Names The Residue

Until 2026-10-05 this section was *The Driver Names The Inflection*: the cue
was human, the pass was entered when the driver declared an inflection, and
the agent did not initiate it from edit-detection alone. The record at 3.46.0
measured what that produced. Roughly 1,250 domain commits in six weeks, zero
declarations; the pass run nowhere but the framework root, where the agent
held the verdict on settled questions and closed 83 of 125 cues by citation;
two live domains carrying 184 and 146 unraised subjects; the drift of
unwalked change surfacing late, through sweeps and accidents
(`a-preserved-question-is-not-a-done-walk`). The operator ruled the reading
below (`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

> **The pass is entered on detection.** A definition surface changed; the
> floor sees it; the agent in the session runs the pass there and then —
> touchpoints, each dependant judged, revisions in the same commit, derived
> surfaces regenerated — and records the walk in the cue. The driver is not
> asked whether to start. **The driver rules on the residue:** a touchpoint
> the agent may not settle, put to them through the harness's own choice
> prompt with the concrete alternatives as its options.

What the old reading protected still holds, as four bounds rather than a
veto. The churn it feared — cascade through the graph, and an agent rewriting
meaning it does not hold — is real; the alternative to bounded churn turned
out to be no walk at all.

1. **Scope.** Definition surfaces only — the types that exist to be reasoned
   from (`specification`, `skill`, `guide`, `manifesto`, `prompt`,
   `workflow-definition`, `insight`, `decision`). A data thing reasoned from
   by fan-in — a register, a requirement — does not trigger a walk; it stays
   with the digest and the retrospective's net.
2. **Depth and kind of edit.** One hop: the declared and literal dependants.
   The agent revises on its own only at restatement level — a name, a path, a
   count, a reference, a regenerated block. A revision that would change a
   dependant's meaning, or a dependant that contradicts the change, is the
   driver's. That line is where knowing ends and pattern-following would
   begin; the old reading drew it around the whole pass, this one draws it
   where it belongs.
3. **Rate.** One walk per subject per day. Autocommit saves every write; the
   gate walks the first commit of a subject in a day, and the agent judges
   whether a later edit the same day is material enough to walk again.
4. **Attendance.** An attended session walks. An unattended run assimilates
   and files — the checklist and its proposed revisions, applied to nothing
   (`unattended-cue-carrier-2026-09-12`).

Most walks end with nothing to rule on. That is the point, not a failure of
the human beat: the expert's knowing is spent on the few touchpoints that
need it, instead of on permission to look.

### The Cue Persists — The Carrier

The cue *verdict* is the driver's; the cue *question* is not — it is a
mechanical predicate (`inflection-candidates-are-computable`), and the floor
asks it at every commit through the pre-commit `candidates` advisory. Until
2026-09-12 that was the whole mechanism, and it had a hole the record had
already felt: the question was printed to a terminal and gone. A human who did
not act on it at that moment had to *remember* it, and an unattended session
had nobody to print it to. Both nets — the change-time cue and the
retrospective beneath it — were observed down together in August 2026.

The cue now **persists as a thing** (`type: cue`, reserved;
`templates/cue.md.template`), and the question **waits in the session-start
digest until a human answers it**:

- **`subject`** names the reasoned-from thing that was modified — a structural
  reference, validated and reverse-indexed, and deliberately *not* counted
  toward the subject's fan-in, so raising a cue cannot make the next
  modification more likely to raise another. **`raised_at`** pins the commit
  that modified it (a local pin the structural-pin check resolves) — or, when
  the cue is raised *in* the modifying commit, the commit that change lands on
  top of, since the modifying commit's own id does not exist yet; the commit
  that adds the cue file is covered by construction. **`raised_by`** says who
  raised it: the operator, an agent, or a dispatch launch.
- **`status: open`** until the walk is marked and **`verdict: inflection |
  not-inflection`** recorded with a **`verdict_reason`** — `inflection` when a
  touchpoint was revised or ruled, `not-inflection` when every one held. The
  pair is the *receipt*: a named question with a recorded answer, where not
  being asked was drift. The floor checks the receipt's shape — an answered
  cue without a verdict and a reason is an Error — and never supplies the
  mark on any line.
- **The floor computes what is missing.** `mdllm cues` walks the commit stream
  since the newest retrospective (thirty days when none exists), keeps
  modifications of reasoned-from things — the same predicate `candidates`
  applies, so the two cannot disagree — and subtracts what a cue already
  covers (a cue covers its subject at and before its `raised_at` commit, and
  on the day it was created — one ask per subject per day). What remains is
  **unraised**; open cue things are **unanswered**. The
  session-start digest emits both, every session, under one heading. Nothing
  here depends on anyone's memory.
- **`verdict: inflection`** means a dependant was revised or a ruling given,
  in the carrying commit; the cue's body names each touchpoint with its mark.
  **`verdict: not-inflection`** means the dependants hold as written, and the
  reason says why.
- **A cue may be answered by citation.** When a decision already on the record
  covers the change, the cue's `informed_by` pins that decision and the
  `verdict_reason` says so: the human ruled once, the citation propagates it,
  and *one ruling answers many cues*. This is what keeps the digest's line
  from becoming wallpaper — a backlog of unraised modifications almost always
  traces to a handful of rulings already made
  (`feels-automatic-is-persistence-of-the-question`). The floor checks the
  pin resolves; it does not judge whether the decision covers the change.

**Who raises, who walks, who rules.** The floor *raises* — at the gate, with
the walk list prefilled — and any session may. The **agent** in an attended
session *walks*, within the four bounds, and marks the verdict: that is its
standing authority since 2026-10-05, the same grant
`framework-agent-closes-settled-cues-2026-09-13` made for settled questions
in the framework root, extended one step earlier and to every domain
(`settled-reasoning-is-standing-authority`). The **driver** *rules* on the
residue — a touchpoint the agent may not settle — and may overturn any mark
by editing the cue, which is why the grant is safe to make. In a harness that
projects the `pre-commit` moment the agent's commit waits for the walk's
record (*The Walk, Where The Change Lands*, below); elsewhere the cue is
raised at the moment `candidates` asks and the walk is the session's own
discipline. An unattended run — a dispatch tick, a scheduled session — that
modifies a reasoned-from thing raises the cue with its checklist as part of
its own commit, writes its proposed revisions beneath it, applies nothing,
and files it in its digest as a seat-queue item
(`unattended-cue-carrier-2026-09-12`), with scan 4 as the net beneath
(`retrospective.md`): whatever is still open at retrospective cadence is
walked there. A cue missed at change time is a walk done late, never a walk
lost.

What this does not change: the ruling on what the walk cannot settle stays
the driver's, and the retrospective remains the cost of reconciliation
skipped, not a licence to skip it. What it changes is who starts the pass:
the change does.

### The Walk, Where The Change Lands

The carrier made the question persist; it did not make the walk happen. Where
a harness projects the `pre-commit` lifecycle moment (`orchestration.md` → the
hook table; Claude Code today), `mdllm cues --staged` runs before the agent's
`git commit`:

- **The gate.** A definition surface changed in the commit in hand with no
  cue on disk for it is a refusal: the commit does not go through, and the
  refusal's text, read in the tool's own channel, is the walk. `cues --staged
  --raise` writes the cue with every declared and literal dependant as a
  checklist — the Assimilate beat, done by the floor. The agent marks each
  line `consistent`, `revised` (restatement level, in this commit, saying
  what) or `ruling`, asks the operator through the native choice prompt only
  for what it may not settle — one question per touchpoint, the alternatives
  as options, *defer to the seat* among them — and commits again carrying
  the cue and the revisions. `verdict: inflection` records that something
  was revised or ruled; `not-inflection` that every line held.
- **What does not count.** A change confined to managed generated blocks: the
  generator did that walk (`a-generated-surface-collapses-its-walk`). A change
  that only records a disposition — status, a hold and its reason, a
  look-again date, a trigger re-dated, the version beside them — moves no
  claim (`session-memory.md` → The Reckoning); withdrawing a claim
  (dismissed, superseded, deprecated, cancelled) still counts. The cue
  listing reads the same exemption back off the commit stream. A data thing
  with fan-in: the digest and scan 4. A second edit of the same subject the
  same day: the agent's judgement, not the gate's.
- **Unattended.** The same refusal, the other instruction: raise the
  checklist with proposed revisions beneath it, apply nothing, file it. The
  dispatcher's tick marks its launches (`MDLLM_UNATTENDED`) and the floor
  tells the run so.
- **What it proves.** The commit carries the walk — each touchpoint named
  with its mark — and the revisions beside it. What it cannot prove is that
  the agent read what it marked consistent; the retrospective's scan 4
  samples that, and every revision is a visible, reversible commit. A seat
  whose harness has no such moment (a Codex session, a hand commit) keeps
  the `candidates` advisory and the digest, and the retrospective remains the
  net.

### External Inflections — The Inbound Edge

An inflection does not have to originate inside the domain. When a
cross-domain import drifts — `mdllm imports-check` reports it `stale` (the
source moved under the pin) or `diverged` (the mirror no longer matches the
face) — the domain's reasoning may now rest on ground that shifted *outside*
it. That report is the mechanical signal; re-opening the quarantine
(`verified: false`, `status: stale` — `provenance.md` → Cross-Domain Imports)
and entering this pass on the import's dependents is an **external
inflection**.

The cue discipline is unchanged: `imports-check` is report-only, and the
declaration that the drift is consequential enough to reconcile stays the
driver's — exactly as above. The floor makes the drift impossible to not see;
it never dispositions. What the external origin changes is only the *entry
point*: the changed thing walked from is the import itself, and the affected
set is its dependents inside this corpus.

**Scope boundary, stated rather than implied:** the four beats run within a
single corpus. The Assimilate indexes, the textual grep, and the Walk never
cross the membrane — the outside world enters this spec only as a cue, already
quarantined as an `origin: external` thing. Reconciling the *producer's*
corpus is the producer's own pass, in its own repo, if its driver declares
one.

## The Four Beats

Once entered, the pass is the same four beats at every scale — one touched
thing or a thousand. The assimilation is **holistic**; the reconciliation is
**serial**. You gather the whole affected set *first*, precisely so the
step-through is stable: if you walked and discovered at once, reconciling one
touch point could be undone by the next, which is the thrash this spec exists to
prevent.

1. **Cue** — the change itself: a definition surface moved and the floor saw
   it (*The Walk Runs On Detection*); or the driver declares one — *this
   change is consequential* — for anything the predicate does not reach.
   This is the beat that initiates; since 2026-10-05 it needs no hand.

2. **Assimilate** — gather the *complete* affected set, mechanically, in two
   passes of widening visibility:
   - **Declared edges** — the `relationships` derived index supplies every inbound
     field owned by the tool's structural-reference registry: relation objects,
     list pointers, singular pointers, trigger watches, workflow definitions,
     conflict parties, and other registered reference shapes. The same registry
     drives validation, reverse indexing, candidate relevance, and private egress,
     so adding a structural field cannot silently update only one consumer. The `provenance`
     (reverse) index supplies every decision pinned to the changed thing and every
     output derived from it. Total recall over what is *declared*, like a compiler
     listing every call site.
   - **Textual references** — then grep the corpus for the changed thing's `id` and
     its canonical name(s). This lights the dependencies expressed in *prose* that
     carry no declared edge — routing tables, cross-references, restatements: the
     part of the dark region a literal-name search can reach. Like *find in files*
     after *find all references*.

   Both decide nothing; together they reveal the shape. What stays unlit after
   both is the conceptual residue — only the Walk sees that (see Walking the Dark
   Region).

3. **Walk** — step through each touch point in turn, asking one question of each:
   *does this still hold, given what changed?* Three outcomes per point —
   **consistent** (leave it), **revise** (update it in place), or **contradiction**
   (surface it; if the change was a rule change, record the superseding decision
   per `belief-revision.md`). This beat is semantic and is the agent's
   `validate.thing.md` Layer 2 work — never re-perform the mechanical
   assimilation by reasoning.

4. **Seal** — record the resolutions. A change to a rule that governs reasoning
   is written as a `type: decision` that `supersedes` the prior rule, which makes
   "what was produced under the old rule" a computable set rather than a manual
   hunt. Revisions land as commits at meaning boundaries; anything unresolved is
   surfaced, not silently dropped. The edges this pass touched are now explicit —
   so the next change inherits a more connected corpus and assimilates wider. The
   pass builds the connectivity it depends on.

## Fractal By Construction

The four beats are scale-free. A one-line correction to a leaf fact runs the
whole pass in a beat — cue, assimilate finds nothing pointing in, done. A
workflow restructure runs the identical pass with a wall of touch points. There
is no separate "big sweep" procedure and no "small edit" procedure; there is one
pass, sized by the blast radius the change actually has. That self-similarity is
the signal that this is a primitive, not a checklist.

## Walking the Dark Region

The dark region is the set of dependencies a change touches through **prose**
rather than through a declared edge. It is not monolithic — it is tiered by how
reachable each dependency is, and each tier has its own mechanical reach:

- **Declared edges** — every field in the structural-reference registry,
  including `linked_things`, prerequisites, singular pointers, trigger watches,
  conflict parties, workflow definitions, and `informed_by` pins. The
  `relationships` and `provenance` indexes walk these in full — a declared edge is
  walked wherever it lives, whether in `linked_things` or in its own structural field.
- **Literal references** — the thing's `id` or canonical name appearing as text in
  another thing's body: routing tables, cross-references, restatements. A corpus
  grep reaches these (the textual-trace step of Assimilate).
- **Conceptual references** — a thing that reasons about the changed rule *without
  naming it*. No mechanical pass reaches this; only the Walk does.

The indexes plus grep narrow the dark region to that last tier — but never empty
it. This is not a defect to automate away; it is the structural reason the **Walk
is human-backed**. The mechanical assimilate guarantees the *declared* and
*literally-named* sets are complete; the expert is the irreducible backstop for
the conceptual residue the machine cannot read. So when a change is significant,
still ask explicitly: *what reasons about this without naming it?* And shrink the
region over time by promoting prose mentions into declared edges — the same reason
the framework says to link rather than mention. Captured as the insight
`mechanical-assimilation-is-blind-to-prose-dependencies`.

**Scope: an inflection walks the whole corpus — every file, the insight corpus
included.** The dark-region tiers above say *how reachable* a dependency is; they
do not narrow *where* to look. The Walk is full-corpus by definition, and the
trap is to reconcile only the surface a change visibly touched (the specs it
edited) while the things it *didn't* touch carry stale references to it. After a
significant inflection — a mechanism dissolved, an artefact retired, a rule
inverted — the part most likely to drift is `things/insights/`: active insights
written *before* the inflection still describe the old model as live, and nothing
in the change's own diff points at them. Do not lean on a mechanical guard to
remember this for you; resist the urge to spec a "retired-term check" or similar.
A check that needs a hand-maintained suppression list to stay quiet is judgement
in mechanical clothing — it adds a silent-failure surface (an over-broad
suppression hides real drift) and a false sense that the Walk is covered. The
floor is for checks that cannot disagree with truth (same-builder drift); the
retire/rename case is irreducibly semantic, so it stays the human Walk's, over
**all** files — see the retrospective's reflexive scan for the periodic net.

## Retrospective Reconciliation

The four beats assume the pass runs *at* the change. A domain that was already
changed without it — twisted, with contradictions latent in the corpus, whether
a legacy domain not yet under the discipline or a live one where an inflection
went undeclared — needs the same pass in a different mode: **full-corpus,
reconstructed from history**, not delta-scoped from a clean inflection. This is
the `retrospective.md` net catching what the change-time net never saw; the beats
still hold, but their inputs change.

1. **Freeze a baseline.** You cannot reconcile a moving target. Stop the change
   and commit the current state to a known point — *even if it is internally
   inconsistent* — before any sweep. Half-applied changes underneath make every
   check untrustworthy and specifically poison the git-pinned tools. Reconcile
   from a stable baseline to a stable baseline.

2. **Assimilate from history and connectivity, not from a delta.** With no single
   inflection to walk from, reconstruct the affected set two ways: `git log` /
   `git diff` over the range of the twist — and `mdllm provenance`'s Freshness
   check, which walks commits since each pin — supply *what changed*; the
   `relationships` and `provenance` indexes supply *what is load-bearing now* (the
   high-fan-in nodes worth checking regardless). Then the textual trace as in any
   pass: grep for the touched things' ids and names.

3. **Walk the whole field, expecting a larger human share.** Retrospectively you
   are partly reconstructing intent you never recorded, so more touch points
   resolve by judgement than by mechanism. The reconstruction is only as good as
   the git history: well-committed twists are largely recoverable; loose or
   uncommitted ones fall back to a full-corpus consistency scan plus the expert's
   knowledge of the domain.

4. **Seal to a new clean baseline.** Record contradictions through
   `belief-revision.md`; commit the reconciled state as the point future passes
   measure from.

Retrospective reconciliation is not a substitute for the change-time discipline
— it is its **backward-looking mode**, and it runs in two situations. The first
is **one-time realignment**: a domain that accumulated change before the
discipline was adopted is twisted once, swept once, and reconciled at each change
thereafter. The second is **recurring maintenance**: the walk at the change is
the agent's, and an expert will sometimes edit by hand with no agent in the
room, or in a seat whose harness projects no gate (see *The Walk Runs On
Detection*), and those changes land un-reconciled. The change-time
net cannot catch what was never handed to it, so the same backward pass runs
periodically — bound to the `retrospective` hook (`retrospective.md` →
Reflexive Scans At Retrospective) — as the net beneath the net. The carrier
makes that net's contents explicit: every cue still `open`, and every unraised
modification `mdllm cues` lists since the last retrospective, is this pass's
work list — answered here, each with its verdict recorded, so the period closes
with no question outstanding.

The two uses differ only in scope and cadence, not in kind: both freeze a
baseline, reconstruct the delta from history, walk the affected set, and seal.
The forward pass remains primary — the retrospective is the cost of reconciliation
*skipped*, not a licence to skip it; it is what makes the discipline robust to
the times the cue is missed, not a substitute for giving it.

## Enforcement

The split follows the framework's standard division of labour:

| Concern | Owner | Mechanism |
|---|---|---|
| The declared affected set is complete | Deterministic floor | `mdllm touchpoints <id>` (live), over the same edges the `relationships` + `provenance` indexes hold (`derived-index.md`, `provenance.md`) |
| Prose references the indexes miss | Deterministic floor (textual) | `mdllm touchpoints` literal tier + corpus grep for the thing's canonical name |
| Pinned dependents that are now behind | Deterministic floor | `mdllm provenance` Freshness check (Info) |
| The cue question waits until it is answered | Deterministic floor | `mdllm cues` — open `type: cue` things plus reasoned-from modifications since the newest retrospective that no cue covers; the same line in every session-start digest (*The Cue Persists*); `mdllm cues --raise` writes the open cue thing for every unraised modification — the raise is mechanical, the verdict never is |
| The walk runs where the change lands | Harness gate (where an adapter projects `pre-commit`) + **the agent** (the walk) + **the human** (the residue) | `mdllm cues --staged` behind the harness's own pre-tool hook: the agent's commit is refused while a definition surface changes with no walk on record; `--staged --raise` prefills the dependants as a checklist; the refusal names the native choice prompt for what the agent may not settle; an unattended run assimilates and files (*The Walk, Where The Change Lands*) |
| The answer carries a receipt | Floor (shape) + **the human** (verdict), or the framework agent citing the human's decision | `type: cue` — `verdict` from the two-value set and a `verdict_reason`; Error without them; `informed_by` pins the ruling that covers it. The verdict itself is never mechanised |
| A rule change leaves a supersede mark | Floor (shape) + agent (judgement) | `belief-revision.md` supersede protocol |
| Does each touch point still hold? | **Agent (semantic)** | `validate.thing.md` Layer 2 — the Walk |
| Is this change an inflection at all? | **The agent**, by walking — the verdict is the walk's outcome, not a permission asked before it | judgement over the prefilled checklist, within the four bounds |
| Which touchpoints need a ruling? | **The human driver** | the residue: a change of meaning, a contradiction, an irreversible — put through the harness's own prompt, overturnable by editing the cue |

The floor can guarantee the affected set is *complete* and *current*. It cannot
decide whether a dependent still holds, and it must not decide whether a change
is consequential — those are the semantic and the human layers respectively.
The floor's job here is to make the agent **unable to not see** the shape of
what a change disturbs; the judgement of what to do about it stays where it
belongs.

The Assimilate beat is exposed as a floor affordance twice over: `mdllm
touchpoints <id>` reports the complete declared inbound set (every reference
shape owned by the canonical structural registry, including provenance pins)
plus the literal textual references, computed fresh from the live corpus — not
from the committed indexes, because assimilation must be complete *and*
current — and `mdllm cues --staged --raise` writes the same two tiers into
the cue as the walk's checklist at the commit boundary. The tool assembles;
it never marks a line (see *The Walk Runs On Detection*). The spec mandates
the discipline of walking at the change, not the existence of the tool; the
tool is the affordance that makes the discipline cheap enough to be the
default.

The floor also asks the **cue question** without answering it
(`inflection-candidates-are-computable`): the pre-commit hook's index-view
`mdllm candidates` advisory reads Git's full A/M/D/R candidate set. A modified
thing that is reasoned-from asks whether its dependents still hold. An addition
asks whether its identity or claim duplicates/contradicts the corpus and whether
new exposure is intended. A deletion asks which dependents lose their target
and whether an exposed truth is being withdrawn. A rename asks whether identity
and path-sensitive references remain honest. The cue *verdict* remains the
driver's, and `touchpoints` remains invoked-never-hooked; what the floor
guarantees is that the truthful question existed at the exact candidate
boundary. Saying no to a named question is a decision, where not being asked was
drift. The question now also persists (*The Cue Persists*, above): the boundary
advisory is the moment it is asked; the carrier is where it waits.

## Relationship To Other Specs

- **thing.md** — the unit being reconciled; `linked_things` edges are the
  assimilation substrate.
- **validate.thing.md** — the Walk is its Layer 2 (semantic) validation, now
  given an explicit trigger and scope (the affected set) rather than an open
  "review everything."
- **provenance.md** — the reverse-provenance index and the Freshness check are
  the Assimilate beat's mechanical inputs; a rule-change-as-decision is what
  makes downstream staleness computable. Its Cross-Domain Imports section is
  the inbound edge: a `stale` or `diverged` import re-opens the quarantine and
  enters this pass as an external inflection (see *External Inflections*).
- **derived-index.md** — the `relationships` index is the other Assimilate input;
  reconciliation is one of the reflexive behaviours indexes exist to make cheap.
- **belief-revision.md** — the Seal beat records rule changes through the
  `supersedes`/`superseded-by` protocol.
- **git-workflow.md** — changes are reconciled and sealed at commit boundaries;
  the supersede mark and the revisions ride the same commit as the change.
- **`divergence-is-an-unrouted-decision`** — this spec is the **forward-cascade
  face** of that primitive: once the driver routes a divergence (the inflection),
  the four beats cascade its consequences. The Walk's three outcomes —
  consistent / revise / contradiction — are routing made operational.
