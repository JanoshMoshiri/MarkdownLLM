---
id: assistant-register
type: plan
status: not-started
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
