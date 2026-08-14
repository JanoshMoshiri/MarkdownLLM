---
id: assistant-register-does-not-graduate
type: decision
status: made
created: 2026-08-14
session: 2026-08-14
decided_by: human
confidence: high
linked_things:
  - id: assistant-register
    relation: informs
    notes: "Phase 0's exit question, answered: the register does not become the default rendering. Phases 1-5 do not run."
  - id: field-report-2026-08-13-domain-session
    relation: derived-from
    notes: "The field report rated the register 'genuinely good' in live use — the observation this decision reinterprets once a second vendor supplied the control."
---

# The assistant register does not graduate

Phase 0 of [[assistant-register]] was a test drive with one exit question:
does the register become the default session-start rendering? The operator
answered it on 2026-08-14: **no.** Phases 1–5 do not run, and the
`--assistant` prototype is retired rather than promoted.

## What changed the answer

The register looked good in live use, and the 2026-08-13 field report said
so. What that observation lacked was a control: every session judging it was
a Claude session.

Running the same domain through a second vendor supplied one. Codex produced
the output the operator wanted **without** the register. The operator's
reading:

> Claude likes to talk a lot, so I got very verbose output. GPT is not so
> talkative.

So the register's apparent value was **confounded with one vendor's
verbosity**. It was compensating for a Claude trait, and being credited for
a quality the rendering did not supply.

## The structural reason, which outlives the measurement

Even if the register were purely beneficial for Claude, its delivery
mechanism is wrong. The rendering was selected by a **command-line flag in
the domain's project hook** — one configuration, serving whichever vendor
opens that domain. There is no vendor dimension in it, and there should not
be: the hook is the domain's contract with *any* agent.

Imposing one vendor's compensation on every agent that opens the domain
inverts the vendor-neutrality the substrate is built on. As the operator put
it: it *"invalidates the whole thing."* A rendering that exists to smooth one
model's habits belongs to that model's side of the boundary, not to shared
domain configuration.

## What was done

The extension was removed from the one domain carrying it, which turned a
refused mixed-ownership fragment into an exact `legacy-v1` match and let that
domain migrate with the rest of the estate.

## Residual

The `--assistant` code path still exists in `session.py`, labelled a Phase 0
prototype. It is now unreferenced by any domain and is removal work, not a
supported surface. Removing it — and the register-seed text it renders —
closes the prototype properly; leaving it is dead weight behind a flag.

## What this does not decide

Nothing here says the register's *content* was wrong. Where-you-left-off,
ranked attention, open loops and conflicts were all rated useful. The
finding is about **who chooses a rendering, and on whose behalf** — not about
what a good orientation contains. If a future rendering change is wanted, it
belongs in the one shared emitter for every vendor, not in a per-domain flag.
