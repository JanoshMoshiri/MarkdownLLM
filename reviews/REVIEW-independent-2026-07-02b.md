---
id: independent-review-2026-07-02b-cowork-fable
type: artifact
status: stable
created: 2026-07-02
linked_things:
  - id: independent-review-2026-07-02-fable
    relation: extends
    notes: "Sixth independent review, same day and same version as the fifth; independently read, then cross-verified against it. Adds six new mechanical findings the fifth did not hold."
---

# Independent Review — MarkdownLLM Framework v3.17.3 (second sitting)

Full read of every tracked file at HEAD `b940f82`: all foundational specs,
kernel, AGENTS.md, `tools/mdllm.py` (3,277 lines) and its test suite, all
insights, plans, decisions, the conflict, all retrospectives, the five prior
reviews, all templates and prompts, adapters, installers, CI, evidence/, both
examples, and the evals (README, fixtures, seeds, committed results).
**Reviewer: Claude (Fable model), running in Anthropic Cowork, 2026-07-02.**

Disclosure: a full Fable review of this same version
(`REVIEW-independent-2026-07-02.md`) was committed earlier the same day. This
review was formed from an independent read first, then cross-checked against
it. Its six drift findings were all independently verified as real (including
one instance it did not list: the `instance-of` residue also survives in
`examples/life-manager/things/home-renovation-process.md`'s body). What
follows agrees where it agrees, pushes differently on the strategic read, and
adds six new mechanical findings.

## Verdict

From the v2.9→3.0 reference point, the transformation is close to complete,
and it is better than what the transformation plan promised. v3.0 built a
floor; v3.17 built a *culture around* the floor. The thing that most
distinguishes this codebase now is not any mechanism — it is that the
corrective loop **deletes as readily as it builds**: WORKLOG retired for
circular duplication, `continuity.md` dissolved into the graph, two
orchestration prompts removed, the MCP live-agent surface built and reverted
in full, and the retired-vocabulary check reverted within twenty-four hours
because it needed a suppression list — with the razor that killed it kept as
a reusable gate. Almost no software project can build a mechanism, recognise
it is judgement in mechanical clothing, and remove it without losing the
reasoning. This one does it routinely.

The structural weakness is equally clear, and it is not a mechanism: the
framework has become systematically better at work the loop can generate
internally (coherence, floor checks, specs) than work it cannot (external
evidence, the longitudinal eval, the periphery nobody lives in). Every review
since June 11 ranked the sanitised validation record first; `evidence/` still
contains a README and a template, and `evidence-and-eval-backlog` sits at
`not-started`. The strategic section below reads that pattern slightly
differently than the fifth review does.

## What Is Genuinely Excellent

**The floor's design signature is consistent across all 20 subcommands** —
detect mechanically, dispose semantically, never mutate domain state.
`touchpoints`/`cascade` as an explicit inbound/outbound pair, `coherence`
self-scoping by presence of the sentinel, `doctor` execution-testing rather
than existence-testing (including hook *body freshness*), `scaffold` exiting
non-zero on partial birth, `imports-check` reporting "unreachable = freshness
unknown" rather than a silent "fresh". That consistency is what makes "never
re-perform a mechanical check by reasoning" a safe rule rather than a hope.
The test suite deserves specific praise: tests encode design *rationale* in
comments (the terminal-source-doesn't-confer-liveness case, the
reports-doesn't-apply case), and the code carries real-world scar tissue —
Windows Store python stubs, cp1252 em-dash mangling, npm `.CMD` shim quoting.
This is a tool that has actually been run.

**The insight lifecycle is the first agent-memory design this reviewer has
seen with a real retirement mechanism.** Graph-keyed liveness (an inbound
edge from a non-terminal thing), the floor orphan check, `keep-active`
requiring a stated reason, the end-session disposition brake paired with
capture. The fade-class diagnosis — insights rot because their end-of-life is
a fade, not an event — is exactly right and transferable well beyond this
project.

**The epistemics remain best-in-class.** Three claims kept apart (thesis /
utility / model-tier corollary); excluded eval trials preserved as evidence;
the opus-bare control leak kept as a *finding* (`withholding-is-not-isolation`)
rather than deleted; the premature-publish incident recorded symmetrically.
`sleeping-bag-fac` is a genuinely well-designed discriminator — an unleakable
fictional rule with per-trap trips, including the hammock inversion that
discriminates on direction, not magnitude — and the honest reading (structure
decided the figures; scale decided only the convention) is the right one.

**The kernel / domain-kernel / orient arc is coherent context engineering.**
One idea — generate the operative surface, drift-check it against the same
builder, never hand-maintain — applied three times: spec corpus → `kernel.md`,
entry file → managed blocks, forward state → the orient view. The v3.15
diagnosis behind it (`session-start-loses-to-the-first-request` is structural,
not model-tier) is one of the sharpest insights in the corpus.

**The razor corpus is becoming the transferable product.**
Discovered-not-authored; same-builder checkability as the floor gate;
suppression-list-means-judgement; existence ≠ currency;
repeated-drift-promotes-a-fact; hard-invariants-encode-a-semantic-assumption;
recoverability-not-frequency as the safety axis. Each is paid for by a
documented incident. These generalise; they are what a future reader will
quote.

## New Findings (verified against HEAD)

1. **The generated domain-kernel block references a subcommand that does not
   exist.** `_dk_session_start` (`tools/mdllm.py:1908`) emits
   "`mdllm session-start` / `mdllm orient`" — there is no `orient`
   subcommand. Every scaffolded domain is born with an instruction pointing at
   a phantom command, and no drift check can ever catch it, because the check
   compares against the same builder that is wrong. The corpus's own insight —
   `a-same-builder-check-is-blind-to-a-self-contradictory-builder`, written
   three days earlier — predicts precisely this failure. A small bug and a
   perfect exhibit.

2. **MCP egress leaks producer-local ids through `informed_by` and
   `parties`.** `_MCP_INTERNAL_GRAPH` strips `linked_things`, `dependencies`,
   `blocks`, `parent`, `definition`, `triggers` — but not `informed_by`
   (decision pins) or `parties` (conflicts). An exposed decision ships pins
   naming things in the producer's id-space: exactly the leak
   `a-crossing-thing-carries-its-producers-private-graph` closed, one field
   over.

3. **`mdllm triggers` silently ignores relationship triggers.** The spec
   defines four trigger types; the tool evaluates time/dependency/threshold
   and reports `blocked_duration` as "not mechanically evaluable" — but a
   `type: relationship` trigger is skipped with no line in the report at all.
   A domain declaring one gets silence, not the honest "left to the agent"
   note the tool gives elsewhere. The no-silent-default law, violated in
   miniature by the tool that enforces it.

4. **The kernel token figure has drifted, hand-maintained, again.**
   `AGENTS.md:79` and `framework-discovery.md:89` say ~1.6k; the README and
   the 06d retrospective corrected to ~2.1k. Third occurrence of the exact
   class (`repeated-drift-promotes-a-fact-into-the-floor` says twice =
   promote): a number derivable from `mdllm tokens` restated in prose.

5. **The guide teaches two contradictory birth paths.**
   `domain-specification-guide.md` §Setup Steps says `mdllm scaffold` does the
   whole sequence; the same file's "Getting Started: Step-by-Step" (Step 1)
   still teaches manual `mkdir` + `git init`, and CONTRIBUTING teaches a third
   manual variant. The eval data says agents drop mechanical birth steps when
   hand-rolling — the guide still offers the hand-roll path alongside the fix.

6. **The TIERS↔catalog coherence check is one-directional.** It verifies
   every `foundational_specs` entry has a TIERS row; it does not verify every
   TIERS row is in the catalog (`thing-lifecycle.md` is in TIERS but not in
   `.markdownllm`). Given `directional-graph-reads-come-in-inbound-outbound-pairs`
   is a named razor, the check should have its mirror.

None of these is severe. What is notable is *where* they cluster:
generated-content correctness at birth, egress completeness, and prose
restatements of mechanical facts — the exact tiers the framework's model says
drift hides in. The model keeps being right about its own failure modes,
which is the strongest kind of validation the corpus offers.

## Over-Engineered

**Narrative redundancy is the new tracking-surface proliferation.** WORKLOG
was retired for circular duplication, but the *story* of each change still
lives in four or five places: the spec's rationale prose, the CHANGELOG
paragraph, the insight, the plan, the retrospective. The
continuity-dissolution story is told at length in `session-memory.md`,
CHANGELOG 3.17.0, the dissolve plan, the orient insight, and the template's
retirement banner. Mechanical drift between them is impossible (they are all
prose), which means `coherence` cannot help — this is pure read-cost and
semantic-drift surface. `operative-rules-are-a-small-fraction-of-spec-prose`
measured 7% operative; the same measurement applied to the whole corpus would
be sobering. The fifth review's razor-index suggestion addresses one slice;
the general question is whether rationale should live once (the insight) and
be pointed at, rather than re-narrated per surface.

**The session-start ritual is growing back what the kernel cut.** Seven steps
before the first response: kernel load, orient read, two-direction version
check, orientation + staleness check, velocity, triggers, attention. Each is
individually justified; together they are a fixed tax on every session of
every domain, including a ten-thing life manager. The framework's own
root-cause analysis (hook compliance correlates with scope) argues for *less*
standing obligation, not more, and mechanical injection does not repeal that —
it moves the load from recall to attention. Consider making the
orientation/velocity/trigger steps proportional-by-default, with skipping
legitimate for small or quiet domains.

**`mdllm.py` at 3,277 lines now contains an MCP server *and* client inside
the validator.** The single-file constraint was a portability virtue at 800
lines. The framework applies SRP to 60-line specs and exempts its largest
artifact; the internal seams are clean, so this is a watch-item, not urgent —
but the MCP transport is the natural first extraction when it moves.

**Agreed with the fifth review, not re-argued:** prompt frontmatter
`inputs:`/`outputs:` is residue of the deleted chain-validation;
`thing-lifecycle.md` is a 473-line draft rotting against the live tool (its
`last_active`-from-git definition now contradicts the mtime-based `stale`
trigger); ~15 keep-active razors are approaching a second spec layer.

## Under-Engineered

The carried queue is real and correctly ordered, so briefly: the **sanitised
validation record** (cheapest, highest-leverage, every reviewer's #1 for
three weeks); the **longitudinal eval** — the README *leads* with "is any of
it still true after hundreds of sessions" and no eval has ever tested a
second session, let alone a hundredth; **bare-control isolation**;
**read-side quarantine** (sharper now that MCP imports arrive by construction
— `verified: true` is still a flag any agent can write, and unverified
content still enters context at full depth); **schema migration**;
**limitations.md** and the "why not CLAUDE.md + a notes folder" answer, which
the corpus could win and never makes.

One addition: **the Obsidian claim is untested.** The README promises "a
domain is a valid Obsidian vault, so the human GUI comes for free" — nothing
in the corpus validates this (wikilink conventions, `_index` handling,
frontmatter rendering). It is a portability claim, and
`portability-claims-need-execution-tests` is the framework's own law.

## The Strategic Read

The fifth review frames the evidence gap as an unrouted divergence and says
"route it." This review pushes one step further, because the pattern has a
simpler explanation nobody has stated plainly: **the framework-agent loop can
only produce artifacts the agent can produce, and every artifact the evidence
needs requires the operator** — a disclosure decision, a session with the
real adoption story, a multi-session eval run on the operator's machine. The
loop does not keep "choosing" mechanism over evidence; the mechanism work is
the only work the loop can complete without the operator doing something only
the operator can do. So the fix is not prioritisation prose — it is
recognising that the top three backlog items are *operator tasks with agent
support*, not agent tasks with operator sign-off. Schedule the human, not the
agent. One session for the validation record (the template exists; the shape
is a redacted workflow-definition; it is dictation, not design). One evening
for the longitudinal fixture (the sleeping-bag rule is reusable; build →
perturb → resume is three prompts and the assertion engine already exists).

The second strategic observation: **review saturation.** This is the sixth
full review in twenty-one days, and the 06-12 review already predicted the
marginal-information decay. The genuinely new findings above are real but
small — a phantom subcommand, two unstripped fields, a silent trigger skip.
The instrument is nearly exhausted against this corpus. The next unit of real
information cannot come from another read; it comes from the longitudinal
eval, a second human, or a second harness. This should be the last review
until one of those exists.

## Priority Recommendations

1. **The operator-gated evidence pair** — validation record, then the
   longitudinal fixture — framed as operator sessions, not backlog rows.
2. **A small mechanical pass:** the `mdllm orient` phantom,
   `informed_by`/`parties` egress stripping, relationship-trigger honesty in
   the `triggers` report, the 1.6k/2.1k figure, the six drift items from the
   fifth review, and the guide's duplicate birth path.
3. **Refresh the examples to v3.17 shape** and add the example-staleness
   coherence check (same-builder: the sentinel — it qualifies).
4. **Decide the root-AGENTS.md kernel question and the razor-index question
   together** — both are "apply the discipline to yourself."
5. **Then stop reviewing and point the instrument outward.**

The honest summary: at v2.9 this was an elegant idea with an honour-system
core that had just been caught failing. At v3.17.3 it is the most internally
coherent self-describing system this reviewer has read — floor enforced,
memory with retirement, epistemics that survive audit, and a corrective loop
that deletes on principle. What it still is not, and what no amount of
further internal excellence will make it, is *externally evidenced*. The
machine is finished enough. The proof is the work now.
