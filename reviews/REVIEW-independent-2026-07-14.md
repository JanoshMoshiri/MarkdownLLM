---
id: independent-review-2026-07-14-fable
type: artifact
status: stable
created: 2026-07-14
linked_things:
  - id: independent-review-2026-07-02-fable
    relation: extends
    notes: "Seventh independent review; first to read all nine live domains from their committed HEADs alongside the framework. Covers v3.17.4 @ c8dc778."
---

# Independent Review — MarkdownLLM v3.17.4 + the Domain Fleet

Full read from committed HEAD (`c8dc778`): all foundational specs, kernel,
AGENTS.md, `tools/mdllm.py` (3,425 lines) and its 103-test suite, evals
(fixtures, seeds, results including excluded), all insights/plans/decisions/
retrospectives, templates, adapters, docs, prior reviews — **and, for the
first time in a review, all nine live domains** read from their own HEADs:
regulated-qms, regulated-overview, regulated-engineering,
regulated-development, jmtm-software, code-architect, agent-architect,
property-ventures, eco-essentials. Reviewer: Claude (Fable), 2026-07-14.

## Verdict

The engineering question is settled. The floor is coherent, the corpus is
clean, the corrective loop demonstrably deletes as well as it builds, and —
new since review six — the framework's actual thesis finally has a direct
measurement: the longitudinal eval ran, and its honest result (within-session
drift resistance holds; the cross-session cascade dropped in 1 of 4 trials)
is the first real evidence for the claim the README leads with. Nine domains
are running real work on this substrate, including statutory filings and a
regulated QMS. This is no longer a promising system; it is a production
substrate with tenants.

The open risks are no longer mechanical. They are concentration risks: **one
human, one private language, and evidence behind a confidentiality wall.**
Every remaining high-leverage item on this list is a variant of one of those
three. The regulated QMS is the forcing function that can fix all three at
once — it introduces a second operator, it demands the regulator-lens
test ("understandable without the author in the room") be applied to the
framework's own surfaces, and it will produce the first disclosable record of
the substrate carrying weight. Treat the QMS deployment not as another tenant
but as the framework's externalisation event.

## What Is Very Well Engineered

**The floor's design signature.** Twenty-plus subcommands, one invariant:
detect mechanically, dispose semantically, never mutate domain state. The
admission criteria for floor checks — same-builder checkable, no suppression
lists, no judgement in mechanical clothing — are transferable engineering
principles, each paid for by a documented incident. The
`judgement-checks-need-a-suppression-list` revert (built, recognised,
deleted within a day, reasoning kept) remains the single best exhibit of the
project's engineering culture.

**Epistemic honesty as an operating property.** The longitudinal writeup is
the model case: the opus arm voided for seed corruption rather than
massaged, the contamination itself converted into a first-class finding
(`isolation-must-contain-writes-not-just-reads`), per-session results
reported instead of totals, and the standing haiku mis-keyed-link failure
reported against the framework rather than excused. Three claims (thesis /
utility / model-tier corollary) still kept deliberately apart in the
manifesto. Almost no published benchmark work is this honest.

**The division of labour is now lived, not just specified.** Reading the
domains confirms the specs describe real practice: regulated-qms's
`_schema.yaml` cites a QMS framework section for every rule it enforces
("zero mechanism was added in the encoding"); jmtm-software runs actual
filings with a conflict thing on a reverse-charge VAT question; the
session-end commits across domains are rich, honest, and reconstructable.
The fractal claim holds under inspection.

**The QMS encoding specifically.** This is the strongest domain work in the
fleet. §6.2 header block → frontmatter, §6.2 status vocabulary →
schema-enforced statuses, §3 register → derived, RTM → relationship graph,
Tier-4 evidence → `record-pointer` (keeping GDPR erasure and immutable git
history structurally apart). The dual-lineage conflict thing
(`qms-canonical-lineage-unresolved`) is precisely what a QMS should produce
when handed contradictory "approved" documents, and the split-of-authority
proposal (Drive keeps content, domain keeps the record) is well-sized — it
narrows the ratification ask to something a QA Lead can actually grant.

**Domain-kernel generated blocks.** Generating the operative sections of a
domain's AGENTS.md and drift-checking them in pre-commit solves the prose
dark region at the one surface every session reads. This is the entry-file
problem answered structurally rather than by exhortation.

**Credit where prior reviews demanded movement:** since 2026-07-02, all
twelve mechanical remediation items shipped (v3.17.4), examples walked to
current shape with a coherence guard, the stale trigger keys on git, the
longitudinal fixture was built *and run*, and the evidence backlog was
correctly reframed as operator-gated sessions rather than a perpetually
guilty backlog row. The loop is executing on its findings.

## Over-Engineered

**The insight corpus is a second spec layer with a private vocabulary.**
Sixty insights, sixteen `keep-active` razors, and a working language — the
floor, the Walk, the dark region, orient, faces of the primitive, razors —
that a reader must acquire before the corpus opens up. Each file is
individually justified; the aggregate is an onboarding wall. The razor index
(review five, queued for evidence session 1) remains undone and matters more
now that a second operator is imminent. Sharper version of the same point:
the framework's own regulator lens — *acceptable without the author in the
room* — is applied to every QMS artifact but not yet to the framework's own
entry surfaces. The second operator, an external assessor, or a future hire currently cannot
read this corpus without you in the room. That is the over-engineering that
costs, and it is prose density, not mechanism.

**Meta-gravity.** A large fraction of corpus and session effort is the
framework reasoning about itself — seven reviews in five weeks, insights
about insights, checks that check checks. The sixth review called review
saturation and was right. This should be the last independent review for a
while; the marginal finding rate has collapsed to periphery drift, and every
review session is a session not spent on the QMS or the evidence.

**Residual ceremony.** Prompt frontmatter still carries typed
`inputs:`/`outputs:` nothing consumes (flagged twice before). The
hard/soft × anchor two-axis hook taxonomy is correct but subtle enough that
the spec warns against conflating the axes three separate times — a sign the
model is one notch more complex than any consumer of it needs. And
`thing-lifecycle.md` — properly evicted from TIERS now — is still ~470 lines
of draft drifting against the live tool; trim it to a design skeleton or
reconcile it.

**`mdllm.py` at 3,425 lines.** Validator, eval harness that spawns headless
agents, MCP server *and* client, scaffolder, three generators — one file,
many reasons to change. The single-file portability argument weakened the
day the test suite began importing it as a module. Not urgent; the seams are
clean; but the framework applies SRP to 60-line specs and exempts its
largest artifact, and every review now says so.

**Small placement inconsistency:** plans live in two homes —
`things/plans/` and `docs/plans/` (where `mcp-domain-server.md` is a
`type: specification` outside the spec root). Mechanically valid, cognitively
untidy; pick one home.

## Under-Engineered — Ranked for the QMS Deployment

1. **The `verified` flip is the QMS's load-bearing control and it is an
   honour-system flag.** Quarantine (`origin: external` / AI-drafted ⇒
   `verified: false`) is your stated no-shadow-AI control, but
   `verified: true` is frontmatter any agent can write, and nothing
   constrains *reading* unverified content into context. Floor-shaped fixes
   exist and are cheap: Error (or at least Warning) when `verified` flips in
   the same commit that created the thing; require the flip commit to name
   the human verifier (your own ALCOA "attributable" lens, mechanised);
   surface every flip at session start. Before the second operator ratifies anything, this
   gap should be closed — an inspector will find it in minutes, because it
   is exactly what they are trained to look for.

2. **The Drive↔register reconciliation check must exist before
   ratification.** The split-of-authority proposal is right, but its
   enforcement — the mechanical sync check against Drive revision metadata —
   is marked "under discussion, not yet proposed." Without it, the register's
   authority rests on the same behavioural discipline your own risk review
   identifies as the thing that fails first ("manual controls fail
   behaviourally before they fail technically"). This check is
   same-builder-checkable (Drive revision API vs register frontmatter) and
   is therefore floor-shaped by your own admission criteria. Build it with
   the proposal, not after.

3. **The second operator has never existed.** Every domain in the fleet has
   been operated by one person. The QMS makes the second operator a consumer and approver
   of domain output; nothing — not the docs, not the claim convention, not
   the working-tree contention note in `coordination-claim.md` — has been
   exercised by a second human. The second operator's onboarding is simultaneously the
   real cold-start eval, the disclosable evidence artifact every review has
   asked for, and the bus-factor mitigation. Design it as all three:
   observe, don't help; record it; sanitise and publish what you can.

4. **Fleet drift is real and nothing sweeps it.** property-ventures sits at
   `framework_version_seen: 2.9` with retired artifacts (`continuity.md`,
   `WORKLOG.md`) still live; eco-essentials at 3.14. The refresh hook only
   fires when a domain is *opened*, so dormant domains rot silently — the
   periphery problem again, one level up. A framework-side fleet report
   (`doctor` walking `domain/` and listing each repo's seen-version and last
   commit) is cheap, same-builder-checkable, and would have surfaced both.

5. **The two operator-gated evidence items, still.** The sanitised
   validation record (one sitting, template exists) and the opus
   longitudinal arm re-run under real workspace isolation (outside the repo
   tree — now required for the framework condition too, per the seed
   corruption). The v2.0 reframe correctly put these on your calendar rather
   than the agent's backlog; the calendar now has to actually contain them.

6. **Schema migration remains unspecified** — rename a status, retire a
   field, re-baseline a vocabulary over an existing corpus. Carried since
   June 11, and about to stop being theoretical: the second operator's weekend SOP rewrite
   plus kickoff regeneration is exactly a vocabulary re-baseline over a live
   corpus.

7. **Binary deliverables in domain git.** regulated-development carries
   ~20 `.docx`/`.pdf` outputs in-repo. Consistent with `interface.md`
   (deliverables in `outputs/`), fine at this scale — but opaque to diff,
   unboundedly growing, and about to live inside what becomes controlled
   company storage. Your own Drive-canonical + pointer pattern is the
   answer; state a policy before ratification fixes the current shape in
   place.

## Where To Focus, Where To Stop

**Focus:** the QMS ratification package as one unit — verified-flip
enforcement, the Drive sync check, the Annex-11 system description
(QMS-AUTO-001), and the split-of-authority decision — then the second operator as
second operator (onboarding = cold-start eval = evidence), then the two
operator-gated evidence sessions. Everything on that list either closes a
control gap an inspector would find or converts private proof into
disclosable proof.

**Stop (for now):** new framework primitives — the mechanism inventory
already exceeds what nine domains consume; further independent reviews —
saturation was called correctly; growth of the standing-razor population
without the index; MCP expansion beyond the read-only face; token-cost
tuning. None of these move the three concentration risks.

## Closing

The honest summary: the machine is built and it is good — better than the
overwhelming majority of solo-built systems I have seen, and honest about
itself to a degree that is rarer still. What it has not yet survived is
*another person*. The private language, the single operator, the
undisclosable evidence — all three are the same finding wearing different
files. The QMS deployment puts a second human, a regulator's eyes, and a
hard deadline in front of the framework at once. That is not a risk to the
framework; it is the missing half of its validation. Point everything at it.
