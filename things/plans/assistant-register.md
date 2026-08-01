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
