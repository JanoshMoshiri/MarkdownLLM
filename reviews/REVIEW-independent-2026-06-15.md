---
id: independent-review-2026-06-15-cowork
type: artifact
status: stable
created: 2026-06-15
linked_things:
  - id: independent-review-2026-06-12-fable
    relation: extends
    notes: "Third independent review, three days after the second; reassesses maturity given evidence of real adoption and centres on the workflow-state gap"
  - id: framework-continuity-brief
    relation: references
    notes: "Action queue below maps onto the brief's parked gap-4 (workflow-state) and the concurrency thread"
  - id: framework-retrospective-2026-06
    relation: complements
    notes: "Extends the retrospective's What Should Change with a structural finding it did not yet hold: workflow run-state as a primitive"
---

# Independent Review — MarkdownLLM Framework v3.7.0 (HEAD da47a5a)

Third independent review. Full read of the operative core (manifesto, `thing.md`,
`kernel.md`, `AGENTS.md`, session-memory, continuity, belief-revision,
change-reconciliation), the framework's own self-knowledge (insights,
retrospectives, prior reviews, continuity brief), and the deterministic floor.
Verification run from HEAD: `mdllm validate .` clean across all three corpora
(58 + 6 + 12 things, 0 Errors / 0 Warnings / 0 Info), floor self-tests green
(36 passed, 1 skipped). This review also incorporates context supplied by the
author about real-world adoption that the repository itself does not — and cannot
— evidence; where a finding rests on that testimony rather than on the artifact,
it is marked. Reviewer: Claude (Cowork), 2026-06-15.

## Verdict

The intellectual spine is sound and load-bearing, not decorative. *"The notation
changed, not the primitives"* — treat an LLM-driven system as a program (data
structures in `thing.md`, instructions in prompts, control flow in hooks, git as
the state machine) and apply SOLID/Clean Architecture to *knowledge units* — is a
genuinely good frame, and the corpus holds to it with unusual discipline (the
decompose/compose cohesion rules, SRP-as-tier-promotion, the relation-vocabulary
prune from 35 to 13). This is well above the median spec-driven or agent-memory
project.

The maturity read has to be split, because the previous two reviews and my own
first pass made the same error: treating *"the proof is not in the repo"* as
*"the proof has not happened."* It has. The framework is in real production use,
and — on the author's account — at least one independent operator who is not the
author adopted it cold for their own domain and has carried that domain through to
a marketed MVP, sustaining use with no hand-holding. That is stronger evidence
than the staged cold-start eval still sitting at the top of the continuity queue:
a tool someone keeps using to ship something real, unobserved, outranks a test the
author designs and runs. **So the system is more mature than the artifact can
show.** What remains immature is the artifact's ability to *evidence and onboard* —
and that gap is itself the most important finding here (see The Meta-Risk).

One structural gap has now moved from theoretical to felt, and it is the highest-
value piece of work available: the framework has no first-class representation of a
**workflow run** — the state of a multi-stage, multi-session process instance as it
advances. It is the centre of this review.

---

## What Works Well

**The deterministic floor and the validate/semantic split** remain the single best
decision in the framework. Mechanical checks (structural, referential, schema) live
in `mdllm.py` and are enforced by the pre-commit hook; the agent is left only the
semantic judgment it is actually good at. This is the correction to the framework's
worst historical failure (a production domain silently violating the framework's own
strictest rule under honour-system validation), and it is what turns the whole thing
from aspiration into something with a spine that holds when an agent forgets.

**The epistemics are unusually sophisticated and genuinely used.** `confidence` /
`origin` / `verified`, the `origin: external` quarantine, and provenance pinning
decisions to git commits give the framework a trust-calibration layer most
agent-memory systems lack entirely. A quarantine model for untrusted external input
is rare and correct.

**The kernel is the best context-engineering move in the corpus.** Extracting
operative rules from rationale into a generated digest (26.5k → 5.3k Tier-0 tokens)
attacks the exact failure the framework's own data identified: hook compliance
correlates with *scope*, not awareness. Fixing a behavioural problem by reducing
load rather than adding rules is the disciplined move, and it is correctly applied
as generated-not-maintained (the same lesson as the CHANGELOG).

**The self-knowledge is exceptional.** The `things/insights/` corpus, retrospectives
that open by indicting the framework, and two prior independent reviews already in
the tree mean the framework is not fooling itself about where it is weak. That
property is rare and is what lets a review like this be blunt rather than gentle —
most of what follows, the framework already half-knows.

---

## The Central Finding — Workflow Run-State Is a Missing Primitive

### The gap

The framework models **knowledge state** richly — insights, conflicts, continuity,
decisions, provenance, belief revision. It barely models **workflow state**.
Workflows exist only as *definitions* (prose in `*-workflow.skill.md`); there is no
representation of a workflow *run*. The continuity brief records this honestly as
"gap 4," parked, lean-Option-A, "watch for the pain before speccing."

The pain has arrived. In a real domain running a long-running, multi-session,
multi-stage workflow, the run-state of a given instance is reconstructed by hand
each session — reading the continuity brief and the worklog, then walking the
related things to infer "where is this case." That cost exists *because there is no
authoritative per-instance run-state object.* The state is smeared across a
singleton document (`continuity.md`, one-per-domain, mutable, lean-by-design) and a
pile of things.

### Why this is the same defect as the concurrency problem

These are not two roadmap items; they are one defect seen from two angles. The
nearest thing the framework has to run-state is `continuity.md` — and it is the
*least* concurrency-safe object in the design: a single-writer singleton that becomes
a merge-conflict magnet and a lost-update hazard the moment two operators run two
sessions. Decompose run-state into one first-class thing **per instance** and both
problems move at once: status is *read*, not reconstructed; and two operators working
two different instances now touch two different files, which git merges without
thought. Only same-instance contention remains — rare, small, and addressable with a
lightweight visible claim rather than a lock.

This reorders the continuity brief's stated priorities. Solving "concurrency" as a
separate workstream around the current singleton hardens the wrong object. The
run-state primitive *is* the bulk of the concurrency solution.

### Is it actually a primitive? (running the framework's own razor)

The framework nearly minted a primitive once that was really a half-applied
discipline (`insight-consolidation` → composition). So the test is not "is it
useful" but "what about it is irreducible to what already exists."

**Reducible — and therefore to be inherited, not reinvented:** it is a thing
(`thing.md`); it accrues decisions with pinned inputs (`provenance` + `type:
decision`); it commits at stage transitions (`git-workflow.md` meaning boundaries);
and — load-bearing — **a run is the *instance* of a workflow *definition*, which is a
template/instance pair the decomposition section already governs** (`template-for` /
`instance-of`, `derived-from`). The framework already has the vocabulary for exactly
this relationship.

**Irreducibly new — and therefore what earns primitive status:** (1) the **cursor** —
`current_stage`, a pointer into an externally-defined, possibly-looping sequence;
`status` models a thing's *own* lifecycle and cannot carry "position N in a process
defined elsewhere" without meaning two different things across domains (a cohesion
violation). (2) a **coordination claim** — a visible "who holds this instance right
now," which nothing in the framework expresses because nothing has needed to. (3) a
**per-instance resume point** — continuity does this at domain granularity; nothing
does it per-run.

**Verdict: yes, a primitive — but a narrow one.** The proof it is genuine is how
little it adds: three or four fields plus a body convention; everything else
inherited. If a draft of this grows large, it has smuggled in things that already
exist. This mirrors composition's "four lines, not a new mechanism" signature.

The author's own framing settles a secondary question correctly: a primitive being
undeployed in a domain does not make it not-primitive — it is exactly how the
framework already treats `conflict`, `retrospective`, and `index`. "Spec when
foreseeable, deploy when felt" is the statement that primitives are *available*, not
mandatory. A recipe domain never minting a workflow run is no different from its
never minting a conflict.

### The reframe that keeps it on the spine

Do not introduce this as a free-standing invention. Introduce it as **the
decomposition principle applied to processes.** Today, workflow definitions violate
that principle — the skeleton lives as prose in a skill and the instance does not
exist at all, so run-state smears. Workflow-state is *finishing* the decomposition:
separate the definition (`template-for`) from the run (`instance-of`); the
cursor / claim / resume are what the instance side legitimately needs that no prior
instance-thing did. Framed this way it passes the razor — not "the notation
changed," but a discipline the framework already preaches, applied to a kind of
thing it had not yet applied it to.

### How to bring it into being

1. **It is two things, and the harder one is the definition.** For `current_stage`
   to mean anything mechanically, the *definition* must stop being prose and become
   structured — its stages enumerable as data. And a real pipeline is rarely linear:
   iteration loops and backward/forward passes make it a graph with cycles, so the
   definition must express *allowed transitions*, not a sequence. Keep it minimal via
   the framework's own division of labour: the **floor** checks the cheap mechanical
   fact (`current_stage` ∈ the definition's stage set); the **agent** judges the
   semantic one (was this a legal move given the loops). Do not push cyclic-traversal
   legality into the floor — that is Layer 2, and forcing it mechanical is how this
   spec would bloat.

2. **Do not duplicate what git already holds.** Resist a `stage_history` array — the
   history of `current_stage` changes *is* the commit log ("git is the event
   stream"). Frontmatter holds the present cursor; git holds the path; the body holds
   the resume narrative; accrued decisions are `linked_things` to `type: decision`
   things (provenance already does this). Keep that discipline and the run thing stays
   tiny — the tell that the primitive is clean.

3. **Mature it on the ladder the framework already has.** Capture the originating
   idea as a `type: insight` now; write the spec as **`draft`**, extending `thing.md`
   and complementing `interface.md` (a run produces deliverables on hand-off),
   `git-workflow.md` (stage transition = checkpoint boundary), and `provenance.md`;
   exercise it on the real domain before promoting past draft; let the `mdllm` hook
   (validate `current_stage` ∈ definition stages) land *when felt*, after the
   discipline has run.

One call to make deliberately rather than drift into: **reserve it, or document it
as a domain pattern first?** The case for reserving is specific — fixed semantics are
wanted by any mechanism that must read `current_stage` from outside the domain
(cross-domain hand-off to a downstream consumer is the test, and that consumer
already exists in practice). That is the same test that reserved `decision` and
`index`. Lean reserve-but-draft.

---

## Coherence Gaps (beyond workflow-state)

**Cross-domain linking is promised by the manifesto and specified nowhere.** The
manifesto repeatedly says domains can reference each other; domains are isolated,
gitignored, separate-id-space repos with no cross-reference spec. This was a vision/
architecture incoherence in the prior review; it is now also a *felt* one, because a
real workflow run produces deliverables that become another domain's inputs — a
cross-domain hand-off the framework cannot yet describe. Spec it or stop promising
it.

**The central small-model hypothesis is still narrowly untested.** Evidence of real
adoption proves *the framework delivers value to others* — it does not prove the
specific claim that a *smaller* model with structure beats a *larger* one without it.
That claim still rests on one eval whose reasoning core saturated. Keep the two
claims distinct: utility is now well-evidenced; the model-tier superiority is not.

---

## Over-Engineered

**Tracking-surface proliferation.** Six surfaces for one repo (git log, WORKLOG,
CHANGELOG, REVIEWLOG, continuity, insights), and the framework's own insight records
that they have drifted from reality twice. The WORKLOG (~115KB of *hand-maintained*
prose) is the worst offender and is precisely what the framework's own
generate-or-validate-or-delete principle condemns. The CHANGELOG is generated; the
WORKLOG should be generated from git or cut. It is the largest file in the repo and
is a liability, not an asset.

**The corpus is at risk of outgrowing what it manages, by a mechanism the framework
named itself** — "each failure mode answered with new prose machinery… the corrective
loop amplifies the disease." That pattern is still running: the newest spec
(`change-reconciliation.md`) is elegant — the fractal four-beat pass, the dark-region
tiering, the human-cues-the-inflection reframe are real contributions — but it is a
`draft` with *zero real runs* ("never run; first real test next session") carrying
high implementation detail, including retrospective-reconciliation sub-modes, for a
pass nobody has exercised once. "Spec when foreseeable" licenses the spec; it does
not license polishing sub-modes ahead of the first run.

---

## Under-Engineered

**Concurrency / multi-writer.** Two real collisions are already on record, and the
model is "single-writer-by-convention." As soon as more than one operator shares a
domain, this bites. Most of it is dissolved by the run-state decomposition above
(different instances → different files); the residue (same-instance contention) wants
a *visible advisory claim* — a committed `held_by` / lease field the agent reads and
respects — not a distributed lock. General principle worth recording for the day a
domain needs true runtime concurrency: **keep git as the system of record** (it is
the audit trail, and for any domain with compliance stakes that is a feature, not
overhead); if a separate coordination layer is ever introduced to handle concurrent
writes, treat it strictly as coordination and checkpoint its state back into a
committed run-state thing at every meaning boundary. The durable schema is the
contract; design it once and both a purely-local domain and any future coordinated
deployment share it without diverging.

**Upstream framework-version propagation.** The framework has the *downward* check
(is this domain behind its framework? — `session-start:version-check`). It lacks the
*upward* one (is this framework behind its published source?). Today operators must
coordinate updates manually before a session. The fix is the same primitive one hop
up the chain: at session start, compare the local framework against its published
source and surface a "you are N versions behind — update before this session?"
prompt. Make it **advisory, cached, non-blocking** — a hard network call at session
start is exactly the `portability-claims-need-execution-tests` trap in a harness with
no network. Lowest-effort, highest-coordination-value item on the list; grab it
independent of everything else.

**Domain refresh is not mechanised.** Domains sit one to five versions behind a
framework that versions daily; most of a refresh is re-copying a few boilerplate
blocks (scaffold-adjacent), yet it is still manual. Drift compounds per domain. This
wants an `mdllm refresh` before there are many domains, not after.

**Status truthfulness.** Several `stable` specs change week to week (`thing.md` is
`stable` and changed the day of this review). By the framework's own checklist
("status reflects reality"), much of the `stable` core is really `evolving`. The
author has acknowledged this and owns the call; the fix is cheap relabelling, and it
matters because the framework asks *domains* to trust those labels.

---

## The Meta-Risk (the most important finding)

The framework's strongest evidence — independent adoption, sustained real-world use,
a downstream product — lives in places the artifact cannot reference. A cold
evaluator (this review an hour before the author supplied context; a prospective
adopter; a sceptical colleague) sees a self-referential spec corpus that has
apparently never touched a real problem. A framework whose whole ethos is
*transparent, auditable, self-describing* currently makes the case for its own
maturity by word of mouth.

This is fixable without exposing anything private, and it is probably the
highest-ROI documentation work available: a sanitised validation record. The
independent cold-start written up as the eval it actually was — problem, incumbent
tool displaced, what broke, what was fixed, that it sustained to a marketed MVP — and
any real multi-stage workflow abstracted to its *shape* (the stage graph, which
primitives carried which load, what was missing) with all domain-specific content
stripped. One such document would change what every future cold evaluator concludes.

---

## Action Queue (prioritised)

1. **Design the `workflow-state` primitive** — the run as `instance-of` a structured
   workflow *definition*; minimal fields (`current_stage`, coordination claim,
   definition pointer), resume in the body, no `stage_history`; floor checks
   stage-membership, agent judges transition legality. Draft spec + definition
   template + a filled generic run instance. Decouples from "finish defining the
   workflow," because what a *run is* is independent of how many stages exist.
2. **Add the upstream framework-staleness check** — advisory, cached, non-blocking.
   Cheapest coordination win.
3. **Decompose run-state per instance and add the advisory lease** — most of the
   concurrency problem dissolves here, ahead of any heavier mechanism.
4. **Publish a sanitised validation record** — close the meta-risk.
5. **Generate-or-kill the WORKLOG**; relabel the `stable` core to `evolving`.
6. **Spec cross-domain hand-off**, or remove the manifesto's promise of it.
7. **Mechanise domain refresh** before domain count grows.
8. **Get model-tier data**, or demote the small-model claim from spine to footnote.

The throughline: the work has shifted from *proving* the framework to *harvesting*
from where it is already proven. The live domains are generating exactly the
empirical signal the specs need, and almost none of it is flowing back. The most
framework-faithful next move — by its own "deploy when felt" razor — is to let the
real, felt needs (run-state, concurrency, refresh) author the next specs, rather than
adding machinery ahead of need.
