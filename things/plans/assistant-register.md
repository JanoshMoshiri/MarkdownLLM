---
id: assistant-register
type: plan
status: in-progress
version: 1.0
created: 2026-07-28
priority: high
tags: [interface, register, orientation, session-start, onboarding, operator-experience]
linked_things:
  - id: interface-specification
    relation: extends
    notes: "interface.md specifies input routes and output types but never the response itself — the conversational turn. This plan closes that gap with a Response Register section."
  - id: tiered-loading-is-tiered-reading-applied-to-specs
    relation: implements
    notes: "Same generalisation move: the framework has tiered reading (depth matched to query); this adds tiered reporting (substance vs the agent's own housekeeping). Not a new idea — an existing principle applied to a new target."
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: informs
    notes: "Why prose alone cannot carry this: register has unbounded scope (every turn), so an interpretation-anchored rule decays. Drives the decision to harden the mechanical half in session-start's emitter."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: informs
    notes: "The register must expand, not compress, at human-decides moments — smooth assistant prose invites assent exactly where deliberation is owed."
  - id: operative-rules-are-a-small-fraction-of-spec-prose
    relation: references
    notes: "The register rule set must stay tersely stateable in a kernel block; if it cannot, it is not yet a rule."
---

# Assistant Register — the response is an output type, and it has been unspecified

## The finding

Operating any domain today produces responses dominated by the agent's own
housekeeping: floor state echoed when healthy, tier-loading narration, token
counts, sync mechanics, hook installation reports. The operator's actual loop —
*what have I got, what can I do, what's important, where do I go* — arrives
wrapped in machinery they never asked about. A second operator found this a
real barrier to entry (2026-07-28 session, non-author operator feedback — the
thing three independent reviews said the framework needed: a person who isn't
the author, watched).

Two diagnoses fell out of examining where the verbosity actually comes from:

1. **The tool is already quiet.** `session.py` is exception-disciplined:
   `_floor_status` returns None when healthy, verified-flips are silent when
   empty, kernel drift speaks only when drifted. The bulk of the noise is the
   *agent volunteering its own preparation narrative* — unspecified behaviour,
   neither required nor forbidden by any spec.
2. **The t=0 injection teaches the wrong register.** What `session-start`
   emits is jargon-shaped ("Floor: NOT INSTALLED", "Version: MISMATCH",
   "Domain kernel: DRIFT"). The agent's first turn largely paraphrases what
   the harness hands it, so it opens in that register and stays there. The
   injected ritual text is a register *anchor* — today anchoring the wrong
   register.

## The frame that survived deliberation

An earlier design — two registers, `operator` vs `engineer`, declared
per-domain — was considered and **rejected**. "Engineer mode" was honestly
just the current verbosity wearing a job title; no audience wants the floor
echoed at them. There is one good register. The real category boundary is not
audience but **domain substance vs the agent's own housekeeping**: kernel
drift is operator business in the framework repo because there the machinery
*is* the subject matter — same register, different substance. No flag, no
per-domain declaration, no `_schema.yaml` option.

The framing that holds: **an expert assistant, not an expert system.** An
expert system enumerates state and leaves the ordering to the human. An
assistant says what matters first, is accountable for that judgment, and can
always show its derivation.

## The register (the rule set — must stay this small)

1. **Report domain substance; never narrate your own preparation** unless it
   failed or was asked for.
2. **Speak on exception — silence means healthy.** (The tool already does
   this; the agent must match it.)
3. **Close with what is actionable**: what's open, what's first, one line of
   what the operator can ask for.
4. **Expand at human-decides moments.** The one place an assistant-register
   response gets *longer*: irreversible or consequential calls are slowed
   down and made explicit, never smoothed into a summary. Compression
   elsewhere buys deliberation here.
5. **"Show me why" must always work.** The derivation (which trigger fired,
   which due_date, which dependency) is retained and retrievable on demand —
   translation, never withholding. `_floor_status`'s own docstring is the
   cautionary precedent: a suppressed exception recreates the silent-loss
   failure that code exists to prevent.

## Design: harden the seed, floor the rest

**Spine — Option 2 (git-fs/tool anchor):** rewrite what `cmd_session_start`
emits, as the default (not a `--brief` variant — two renderings drift).
Assistant-shaped output: what's open ranked by what mechanics honestly know
(`due_date` proximity, `priority` where set, fired triggers first), exceptions
in plain language with the ask attached ("Safety checks aren't switched on in
this copy — run `mdllm install-hook .`"), healthy states silent or one word.
The tool must not fake judgment it lacks: mechanical ordering only; genuine
sequencing stays with the agent. Fix the seed and the agent's cheapest
behaviour becomes the correct one — mechanical, zero-decay, every harness
with an adapter.

**Floor — Option 1 (interpretation anchor):** a short **Response Register**
section in `interface.md` (closing its acknowledged gap: things and
deliverables are specified; the response never was) carrying the five rules
above in a `<!-- kernel -->` block → `kernel.md` via `mdllm kernel` →
every domain's managed block via `domain-kernel`. This covers what only the
model can do: holding the register through mid-session events, the
human-decides expansion, answering "show me why".

**Rejected — Option 3 (bound per-domain prompt):** opt-in means the operator
who most needs it gets it only if someone bound it first; and it fails the
restraint rule (a prompt should be tighter than the prose it replaces).

## Phases

- [ ] **Phase 0 — Test drive (before any spec changes).** Prototype the new
  `session-start` output shape and trial the register live: one session on
  this repo, one on a live operating domain (QMS is the natural candidate —
  it is where the pain was felt). The operator judges: does orientation
  answer *what have I got / what's first / where do I go* without translation?
  Does "show me why" hold up? Findings feed Phase 1; the rule set may shrink
  or shift before it is sealed into a spec. Prototype may live on a branch or
  as uncommitted working state — this phase deliberately precedes the
  inflection.
- [ ] **Phase 1 — Declare the inflection; spec the register.** Response
  Register section in `interface.md` + kernel block; `mdllm kernel` regen.
- [ ] **Phase 2 — Reshape the emitter.** `session.py`: assistant-shaped
  default output per the design above; mechanical ranking in
  `_orient_forward` (fired triggers, then due-date proximity, then priority;
  alphabetical only as final tiebreak); exceptions in plain language with the
  remedy attached.
- [ ] **Phase 3 — Propagate.** `domain-kernel` managed-block content updated;
  refresh across estate domains as each next opens (normal refresh cadence,
  not a sweep).
- [ ] **Phase 4 — Walk the dark region.** `mdllm coherence`, then the
  prose-only residue: AGENTS.md tier table and catalog, `docs/framework-map.md`,
  operator-guide and first-hour (both speak to exactly this audience and
  must describe the new orientation shape).
- [ ] **Phase 5 — Watch it decay (or not).** The register's known weakness is
  unbounded scope on an interpretation floor. After a few weeks of sessions:
  does the register hold mid-session? Does the human-decides expansion
  actually happen? Candidate retrospective material; possible insight either
  way.

## Open questions carried into Phase 0

- Does mechanical ranking in the emitter feel like guidance or like the tool
  overreaching? (The expert-system trap wearing assistant clothes.)
- Where does the affordance line ("you can also ask me to…") live — emitter,
  register rule, or both?
- Is one line of session-start output enough for a healthy quiet domain, or
  does an empty brief feel broken to a newcomer?

## Phase 0 findings — first drive, 2026-08-01 (this repo + the live QMS domain)

**The prototype worked; the register did not hold.** The emitter reshape did
what the design asked (ranked attention, plain-language exceptions, silence
when healthy — branch `phase0/assistant-register`, `--assistant`), and the
drive surfaced two real defects (fired triggers filtered through the open-loop
set; git subjects decoded with the locale codepage). But when the agent then
*reported* the drive — same session, plan and register freshly read — the
report itself violated the register: a derivation dump the operator read twice
and could not digest. Asked to restate, the agent produced four labeled
buckets, one plain sentence each, and it landed immediately. Same work, same
model, same session; the only variable was response shape. The register's
Phase 5 decay question arrived in Phase 0, with a lived instance on the
register's own author-session.

**Rule 5 gains its missing corollary.** "Show me why must always work" implies
its inverse: *if the derivation is retrievable on demand, it is withheld by
default.* The failed report handed over the whole chain unasked. Every fault
in it follows from that one error.

**The operator's frame, adopted:** the communication channel *is* the system's
interface. Not a report about the system — the system, as far as the operator
can see. A framework whose responses cannot be digested is a capable engine
behind an unusable screen; the interface quality gates whether any of the
rest matters. (Operator, 2026-08-01, verbatim intent: open a domain, ask
questions, and every turn from session start to close comes back clean.)

### Where the register predictably fails

Decay is not uniform. It clusters at moments where the cheapest completion
opposes the rule — name the moments and the unbounded-scope problem becomes
a bounded list:

1. **Reporting after substantial work** (lived, above): context is full of
   derivation; serializing it is the path of least resistance.
2. **Mixed findings**: bugs + design questions + status collapse into
   chronology — order-of-discovery masquerading as order-of-importance.
3. **Mid-session injections**: sync reports, hook output, harness reminders
   hand the agent housekeeping text; paraphrasing it back is the t=0 anchor
   problem recurring at t=n.
4. **A small question after big work**: the answer arrives wrapped in
   accumulated context instead of standing alone.
5. **Human-decides under momentum**: the inverse failure — when everything
   else is being compressed, the consequential call gets compressed too,
   exactly where rule 4 demands expansion.
6. **Self-correction mid-response** (added from leg 2): the agent catches its
   own error and narrates the catch. The operator needs the corrected fact;
   the arrival at it is derivation, and shipping it spends the operator's
   attention on the agent's process at the exact moment they are re-reading
   to find out what is true.

### The counter-evidence was already in the repo

The commit-message register has never decayed. `action: description of the
domain state change` — written hundreds of times across this history without
drift, by the same models that let the response register slip in one turn.
The difference: it is a **named format with a fixed shape**, sitting at a
mechanical boundary, practiced at every commit — not a style to be held but
a form to be filled. Formats hold where styles decay, because conformance to
a named shape is checkable, including by the agent against its own draft.

### Options for holding it (the framework's own three anchors, again)

- **Option B — name the shape (interpretation, format-strength). The spine.**
  The response becomes a tiny named format, peer to the commit format:
  *what changed → what needs you → what's next*; buckets, three or four at
  most; one plain sentence each, in the operator's nouns; the single thing
  that matters last; everything else held until asked. Specified in
  interface.md beside the five rules — the rules say why, the format says how.
- **Option C — stop duplicating the derivation channel (git-fs, already
  built). What makes B cheap.** The framework already mandates the full
  derivation into commit messages; git log is the event stream. The failed
  report was largely a restatement of what its own commit already recorded.
  Doctrine: if it is in the commit, reference it, never repeat it. The
  response's job is only what needs the operator.
- **Option A — re-anchor at the failure moment (harness-session). Optional
  hardening.** The seed anchors turn one; the failure list above says where
  anchors are missing. A harness adapter re-injects one register line at
  report-shaped moments (e.g. post-commit). Per-harness, never the
  difference between working and not — same status as every adapter.

Recommendation carried to the operator: B as spine, C as doctrine, A as
optional hardening — the anchor pattern the framework already trusts.

### Scenario evidence (two lived, two played)

- **S1 — report after substantial work** (lived, failed then recovered):
  the drive report above. The recovered form is the B format, discovered
  under correction before it was named.
- **S2 — human-decides moment** (lived, held): the same session opened on a
  DIVERGED repo; the response stated that a decision was owed, gave the one
  command, and stopped. Rule 4 survives when the moment is discrete and
  mechanical — the risk is momentum, not ignorance (failure moment 5).
- **S3 — small question after big work** (played): "did the tests pass?" —
  drift shape recaps the flake investigation; register shape: "Yes — 161.
  One flaked once under load; passed isolated and on re-run." One sentence,
  derivation on request.
- **S4 — mid-session exception** (played): validation rejects a write —
  drift shape narrates the debugging journey; register shape names the
  exception and the ask: "The schema rejects `review_date` on this type —
  extend the schema, or move the date? Your call either way."

### Phase adjustments from the drive

Phase 0 gains a second leg: a **working QMS session run under the B format
end to end**, judged per-turn — does every turn, session start to close,
answer *what needs you* in digestible shape? Tuning is expected; this is not
a one-pass plan (operator, 2026-08-01). Phase 1's input shifts accordingly:
interface.md carries the five rules (rule 5 with its corollary) **and the
named format**, with the kernel block staying small; Phase 2 is unchanged;
the failure-moment list is the checklist Phase 5 watches against.

## Leg 2 — drive card (prepared 2026-08-06, framework root)

Leg 2 runs in the live QMS domain, in an operator session opened for real
work. Preparing it surfaced one defect and closed one gap.

**The defect: the drive could not have driven anything.** QMS's
`.claude/settings.json` binds `SessionStart` to `mdllm session-start .` with
no `--assistant`. Every QMS session to date — including the one leg 2 was
about to run in — received the *legacy status dump*, not the prototype. A
Phase 0 prototype behind a flag is reachable only where something passes the
flag, and nothing did. Generalises past this plan: **an opt-in prototype is
un-driven by default, and "we tested it" is the claim most likely to be
false about it.** Candidate insight if leg 2 confirms the shape.

**The gap closed: the seed carried the rules but not the format.** The Phase 0
finding was that *styles decay where named shapes hold* — yet `_REGISTER_SEED`
emitted only the five rules, which is a style. Driving leg 2 on that seed
would have re-run leg 1 and reproduced leg 1's failure. The seed now carries
Option B (the named shape: *what changed → what needs you → what's next*,
three or four buckets, one plain sentence each, the ask last) and Option C as
doctrine (if a commit records it, reference it, never restate it), with rule
4's override stated as the one part that gets longer. Still Phase 0: prototype
text behind the flag, no spec change, no inflection declared.

**To run the drive:**

- Mid-session re-anchor (no config change):
  `python ../../tools/mdllm.py session-start . --assistant`
- For subsequent sessions, add `--assistant` to the QMS `SessionStart` hook.
  Operator's repo, operator's call — deliberately not changed from here.

**What to log per turn** (the answer to open question 3 and to Phase 5's decay
question comes from this log or from nowhere):

1. Which failure moment was in play, if any — the numbered list above (report
   after big work · mixed findings · mid-session injection · small question
   after big work · human-decides under momentum).
2. Did the turn fill the shape, or narrate? One word.
3. Did you want more than you got? If yes, *what* — grounds (D2) or the full
   working (D3)? This is `response-depth-control`'s evidence, gathered free.
4. Would you have set a dial, or just asked? Open question 3 lives here.

## Phase 0 findings — leg 2, 2026-08-06 (a live operating domain)

All specifics below are abstracted to shape. The drive ran in a private
domain; nothing identifying it, its people, or its documents belongs in this
repo (framework-privacy-boundary).

**Verdict: the shape holds; the delivery needed tuning.** Operator, on the
drive: the orientation did its job and read as *domain-operation oriented*
rather than as machinery. This is the first leg to pass on substance. What
failed was legibility, and it failed the same way leg 1 did.

**The lived correction.** Mid-session the operator asked, once, for plain
English — verbatim intent: *stop going from one reference to one date to
another*. The reply that followed was immediately right: headings that named
a subject in plain words and carried a verdict, short causal sentences, and a
genuine close naming the one item decaying fastest. Same session, same model,
same facts; the only variable was again response shape.

### The three delivery defects, named

1. **An identifier stood in for a noun.** "In the operator's nouns" was read
   as *the domain's filing codes*. The operator thinks in the subject; the
   register was answering in the index key. The recovered reply proved the
   point by naming three controls in plain words where the failed one had
   listed five identifiers — same facts, one of them readable. Rule: name the
   thing before its identifier; never an identifier where a name would do.
2. **The buckets were borrowed from the tool.** Headings echoed the emitter's
   own ranking (overdue / due-within-N-days). That is how the floor *sorts*,
   not how the operator *decides* — failure moment 3 arriving at t=0 rather
   than mid-session, because the orientation output is itself the injection
   being paraphrased. The recovered headings each named a subject and carried
   its verdict before the body was read. Rule: headings carry the verdict,
   never a bare topic and never the tool's sort order.
3. **Self-correction was narrated three times.** New failure moment 6 above.

### The guard the format was missing

Operator's constraint, adopted: **things important to domain operation must
not be tidied away by the shape.** Compression applies to the telling, never
to the substance — a fact bearing on how the domain runs survives every
shape, and a bucket it will not fit is a wrong bucket, not a reason to drop
it. Without this, the format is one step from a register that reads
beautifully and omits the thing that mattered — the failure mode that would
discredit the whole plan.

### The omission — the guard was already being violated, by the emitter

Asked what had gone missing, the operator named one thing without hesitation:
**the work they had left in a plan.** They had to ask for it — *didn't we have
a plan about something?* Traced, it was not a response-format failure at all.
Three compounding causes, all in the emitter:

1. **The handoff was truncated by design.** Carried-forward work lives in the
   session-end commit — the framework's own doctrine puts the handoff in the
   event stream, and there is no `continuity-brief` in practice. The assistant
   renderer cut that subject to 110 chars, with a comment justifying it:
   *answers none of the operator's four questions*. It answers the first one.
   Brevity deleted the handoff and left a rationale in its place.
2. **The detail was in the body, not the subject.** The first fix read `%s`
   and would have reproduced the omission — domains that write a short
   session-end subject carry the whole carried-forward list in `%b`.
3. **Underway was indistinguishable from untouched.** Anything without a
   fired trigger or a near due date fell into a flat row of bare ids. A plan
   mid-execution and a plan never begun rendered identically, because the
   ranking knows only *waiting*, never *underway*.

**The generalisation, and it is the sharpest thing the drive produced:** the
orientation ranks by **maturity of waiting** and has no concept of **work in
motion**. Everything mechanically legible about urgency is a date or a
trigger; a half-finished plan emits neither. So the artefact most certain to
be asked about at session start was the one the emitter was least able to see.

This is also the operator's guard arriving as a lived instance, one turn after
it was adopted — and arriving from the direction nobody was watching. The
compression that dropped it was not the agent's prose. It was the tool's, and
it had been there since the prototype was written.

Fixed behind the flag: a **Where you left off** section carrying the last
handoff's subject *and* body (capped, with the command to read it whole),
placed before the ranking because the operator's loop opens at *what have I
got*; and **Also open** grouped by the domain's own status vocabulary, so
underway and unstarted stop rendering alike. No semantics invented — whatever
the domain declared is what shows.

**Phase note:** this is Phase 2 work (reshape the emitter) surfacing inside
Phase 0. Taken now rather than deferred, because leaving it would have run
the next pass with a known hole and produced evidence about a format that was
not the thing failing.

### What held, and should not be touched

- **Batched decisions before writing.** Four discrete calls surfaced together,
  each with its finding attached, before any file was changed. Rule 4 working
  as designed, and a pattern worth naming in Phase 1.
- **Rule 4 on a security exposure.** A credential exposed in the transcript
  was surfaced plainly with the only real remedy, and kept short. Third lived
  confirmation that rule 4 survives when the moment is discrete (S2, S4).

### The pattern this plan is circling — candidate insight

Twice now, across two legs: the correct shape is produced **reliably on
request and never once unprompted**. Leg 1 — dense report, operator asks,
four clean buckets. Leg 2 — dense report, operator asks, verdict-carrying
headings. A behaviour a model performs on demand but never by default is a
**format gap, not a capability gap**: nothing needs teaching, something needs
*naming*. This is the strongest available argument for Option B over any
amount of rule prose, and it generalises past the response register to every
interpretation-anchored rule the framework holds.

Pairs with the leg-2 preparation finding (an opt-in prototype is un-driven by
default). Both are candidate insights; neither is harvested yet — Phase 1
decides whether they are one thing or two.

### Seed changes made (still Phase 0, still behind the flag)

Name-before-identifier · headings carry the verdict · corrections are silent ·
compression is of the telling, never the substance. Second pass runs on the
tuned seed.
