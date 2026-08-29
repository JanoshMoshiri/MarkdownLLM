---
id: dispatch-digest-home-2026-08-29
type: decision
status: made
version: 1.0
created: 2026-08-29
decided_by: Phase 2b build session, under the operator's delegated build authority
confidence: high
origin: stated
tags: [dispatcher, closed-loop, digest, dead-man, phase-2b, regulated-corpus]
informed_by:
  - id: dispatch-host-design-2026-08-29
    commit: c964b2ebf607dc233b8cd4ea358e274335e08a63
linked_things:
  - id: dispatch-host-design-2026-08-29
    relation: extends
    notes: "That decision named the digest a committed thing and left its home unsettled — its own finding 1 (the host cannot push the root) is what forces the answer."
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 2b: the digest is what makes silence a report rather than an absence, which is the desired state's own honesty clause."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: implements
    notes: "The decisive argument against the root: a dead-man reading an invisible digest fires on every healthy run, and a check that always fires is worse than no check."
  - id: coordination-claim-specification
    relation: implements
    notes: "The digest doubles as the run's advisory claim on the repo — opened held, closed released — which is the only cross-machine signal between the host's queue and the operator's laptop."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "The run may not declare a type in a domain it is only visiting. A vocabulary change to a regulated corpus is the domain's act; an unattended run that self-declares it has taken an authority nobody granted."
---

# Decision: The Dispatch Digest Lands In The Worked Repo

`dispatch-host-design-2026-08-29` ruled that the digest is a committed thing
rather than a log file, and deliberately left *which repo* open. The capability
survey had created a real tension, and both horns are genuine.

## The two candidates

**The framework root.** Dispatch is estate machinery; the root is where estate
machinery lives; and a root digest keeps run metadata out of a regulated
corpus that has a strict test about what may enter it. Natural, tidy, and — on
this host — broken. The survey's finding 1 is that the host **cannot push the
root**, correctly: the root declares `autopush: false` because its publication
is the operator's deliberate act. A digest committed to the host's root clone
is therefore invisible from the operator's machine until the operator pushes a
clone they never work in. Unpushed root commits would simply accumulate.

**The worked repo.** Pushes fine, is visible the same morning, and is where
the run's effects already landed. The objection is real: the pilot is a
regulated corpus, and dispatch-run metadata is not its subject matter.

## The ruling: the worked repo

Three arguments, in order of weight.

1. **A record the operator cannot see is not a record.** The digest exists to
   make silence a report. On this host a root digest makes silence *look* like
   a report while being unreadable — the worst of the three states, because it
   also disarms the dead-man that reads the digest's existence. And it does not
   merely disarm it: the dead-man would fire on every healthy run, which is the
   failure mode `a-check-that-always-fires-teaches-the-operator-to-ignore-it`
   names exactly.
2. **The regulated objection inverts on inspection.** A run that writes into a
   regulated corpus and leaves no record *inside* it is the worse regulatory
   posture, not the better one: attributability wants the automated activity
   recorded where it happened, under the identity that performed it — which
   the host design already preserves. The corpus's boundary test is not "no
   metadata"; it is "nothing undeclared". Declaration is the mechanism the
   framework already provides for exactly this.
3. **Declaration keeps the authority where it belongs.** The digest is a
   declared `type: dispatch-digest` in the worked repo's own `_schema.yaml`.
   The dispatch run **may not add that declaration itself** — a vocabulary
   change to a domain is that domain's act, and an unattended visiting session
   granting itself new vocabulary is precisely the move the framework's own
   consequence law forbids. So an undeclared repo is a repo dispatch does not
   write to: the run prints its digest to stdout, reports the missing
   declaration as the single blocker, and works nothing there.

## What the digest is, and is not

Small and pointer-shaped. Frontmatter: the claim (`held_by` / `held_until`),
the launch context, the scope, the stop reason. Body: loops run, items queued
per seat, breakage or "none", publication debt. `status: in-flight` while the
run holds the repo, `filed` when it closes.

The host retains the latest fifty run files per job outside git, rotating.
That is **transport and backup, not record** — it sits outside the estate, it
expires, and nothing validates it. The committed digest is the record, and it
must never become a copy of the transcript.

## The digest doubles as the claim

The run opens the digest before it works the repo, holding it under
`held_by`/`held_until`, and closes it after. One artifact then serves three
purposes: the advisory claim the host design requires (because the operator's
laptop and the scheduled run share no scheduler), the run's record, and the
dead-man's target. A digest left `in-flight` with a live lease is itself the
report that a run died mid-work — the failure state is legible without any
additional mechanism.

The claim's honest limit is the one `coordination-claim.md` already states: it
is advisory, not a lock, and it only coordinates if the other side reads it.
The operator's laptop session does not take claims, so the practical guard in
that direction remains the dispatch prompt's step 2 — a dirty tree means
another session may be live, and the repo is skipped.

## The dead-man, and what it does not cover

Armed as a dated trigger at the framework root, on
`closed-loop-operating-state`. It fires when no dispatch digest has been filed
within its window — dispatcher silence is otherwise indistinguishable from a
dispatcher with nothing to do.

**Its coverage is genuinely partial, and this decision says so rather than
implying more.** A dead-man that only a dispatch session reads is useless: the
case it exists for is the case where no dispatch session runs. So its realistic
reader for the pilot is the operator's ordinary session-start orientation at
the framework root, which surfaces fired triggers on every session the operator
opens. That means:

- Coverage tracks the operator's own session cadence. An operator who does not
  open a session for a fortnight does not learn for a fortnight.
- The trigger is at the root; the digest is in the worked repo. Nothing
  mechanically joins them today — the check is "has a digest been filed", and
  answering it is a read the surfaced trigger *asks for*, not one the floor
  performs. This is the chase pattern the dispatch prompt already names, and it
  is proven at this radius; it is not a monitor.
- Anything stronger — a heartbeat the host itself watches, or a root-side
  mechanical check over domain digests — is a real capability and is not built.
  Claiming it here would be exactly the overstatement the closed-loop plan's
  honesty clauses forbid.

The pilot's evidence should settle whether the chase is enough. If a dispatcher
death goes unnoticed past its window during the pilot, that is a finding, and
the finding is the argument for the stronger mechanism.

## What the build stops short of

Registering the job is the operator's single constructive act — census row 7,
ratified — and nothing here installs anything. The shape of what gets
registered, so the operator is choosing rather than composing:

- **working directory**: the framework root, so the host's own queue
  serializes dispatch runs against each other (survey finding 3) and the
  runtime loads the root's entry file the way it already does;
- **command**: `<runtime> --oneshot "$(python3 tools/mdllm.py dispatch-payload . --scope domain/<pilot> --stop-condition '<stop>' --launch-context '<job id and cadence>')"`;
- **stop condition**: sized well inside the host's 120-turn bound and stated
  as work, not time — one repo's fired list, then stop. A run that gets
  compressed mid-way is a run whose own record of what it did is suspect
  (survey finding 2);
- **the pilot repo's prerequisite**: `dispatch-digest` declared in its
  `_schema.yaml`, by that domain, before dispatch can file anything in it.

The command is one line on every host because the composition is inside the
corpus and read-only. That is the whole of the harness-agnostic claim, and it
is a claim until each further host is exercised
(`portability-claims-need-execution-tests`).
