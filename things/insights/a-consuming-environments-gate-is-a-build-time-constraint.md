---
id: a-consuming-environments-gate-is-a-build-time-constraint
type: insight
status: active
version: 1.0
created: 2026-08-18
session: 2026-08-18
source: both
confidence: high
origin: inferred
tags: [adapters, bundles, build, install, harness, run-time-binding, cowork]
linked_things:
  - id: cowork-adapter
    relation: derived-from
    notes: "Two instances inside one session of that plan's Phase 3: CRLF bytes that would break `bash` on the Linux VM, and descriptions 57 and 220 characters over the harness's 500-character install limit. The second was found by an actual install failure in front of the operator."
  - id: an-environments-reachable-set-is-not-an-architecture
    relation: complements
    notes: "That insight: the consumer's environment decides what you can REACH, and the producer cannot test it from its own seat. This one: the consumer's environment also decides what it will ACCEPT, and those gates — unlike reachability — are knowable in advance and enforceable at build."
  - id: portability-claims-need-execution-tests
    relation: extends
    notes: "Execution tests prove the artifact runs where it was built. A run-time-bound artifact must additionally survive a gate it never reaches during any producer-side test: installation into the consuming harness."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "The install path is the extreme case — it executes exactly once per distribution, in an environment the producer's suite never enters, and its failure message is written for the operator rather than the author."
  - id: a-boundary-defect-is-visible-only-from-the-seat-that-did-not-build-it
    relation: complements
    notes: "Same blindness, different boundary: there a reviewing seat sees what the authoring seat cannot; here the consuming ENVIRONMENT sees it, and it reports in the least useful place — at install, to the operator, naming neither the file nor the fix."
---

# A consuming environment's gate is a build-time constraint

## The pattern, twice in one session

A run-time-bound artifact — an account-level bundle that assembles a
workspace after a session has started — must pass through gates the
producer's test suite never reaches. Building the framework's Cowork
bundle hit two in an afternoon:

- **Line endings.** The templates render `bootstrap.sh`, which runs under
  `bash` on a Linux VM. A Windows checkout would have stamped CRLF, and a
  CRLF shebang is `bad interpreter: /usr/bin/env bash^M`. Caught by
  reasoning before it shipped, not by a test that could have failed.
- **Description length.** The harness rejects a plugin whose manifest or
  skill `description` exceeds 500 characters. The rendered values were 557
  and 720. **This one was not caught** — it failed at install, in front of
  the operator, on the first attempt.

## Why the install gate is the worst place to learn

An install-time rejection is maximally distant from its cause in every
dimension that matters. It fires in an environment the author is not in,
at a moment the author is not present, with a message written for whoever
clicked install — naming neither the file, nor the field, nor the
template that produced it, nor the limit it exceeded. The operator's only
available action is to report the symptom back to the producer, which is
a full round trip to learn a fact the producer could have checked in
milliseconds.

And unlike a *reachability* constraint — which the producer genuinely
cannot evaluate from its own seat
(`an-environments-reachable-set-is-not-an-architecture`) — an acceptance
gate is **knowable in advance and cheap to assert**. Nothing about the
500-character limit required a VM to discover. It required only that
someone write it down where the build could read it.

## The rule

**Every constraint the consuming environment enforces at its gate should
become a refusal in the build, stated in the producer's own vocabulary.**
Not a warning — a refusal: a bundle that builds cleanly and installs
badly has simply relocated the failure onto the operator, which is the
one party who cannot fix it.

The refusal must carry what the install error cannot: the file, the
measured value, the overage, and the directory to change. This is the
same move the framework calls *moving a control rightward*, applied
across a distribution boundary rather than within a repo.

Two secondary lessons, both learned the same afternoon:

- **Measure what the consumer measures.** A YAML `description` folded
  across several source lines is still one string to the installer.
  Checking the first physical line would pass a bundle that fails.
- **Normalise what the consumer's platform will reinterpret.** The
  mechanism hash had to normalise line endings too, or a Windows-built
  stamp would false-STALE against the Linux VM's own recomputation — the
  guard against drift becoming a source of it.

## The standing consequence

A harness that binds at run time will keep meeting gates its author
cannot see, because the whole point of the class is that the artifact
travels somewhere the producer does not run. Each such gate found is
permanent knowledge, and its home is the vendor adapter — a vendor limit
belongs beside the vendor's other facts, so a future bundle harness
declares its own rather than inheriting one that was never about it.

Expect more of these. The right reflex on the next install failure is not
"fix the value" but **"which build-time refusal would have caught this,
and why was it not there?"**
