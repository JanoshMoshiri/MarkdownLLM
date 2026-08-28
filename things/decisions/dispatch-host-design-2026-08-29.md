---
id: dispatch-host-design-2026-08-29
type: decision
status: made
version: 1.0
created: 2026-08-29
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [dispatcher, closed-loop, host, harness-agnostic, phase-2b, capability-survey]
linked_things:
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 2b's design, settled against a real host's measured capabilities rather than an assumed one. The installation grant itself remains the operator's."
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    relation: implements
    notes: "The payload command is this insight made mechanical: the corpus composes the launch text, the scheduler carries it, and no judgement lives outside the corpus."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: implements
    notes: "Decides emit-over-point: the tick hands the session the composed prompt text, never a path to read. A pointer is instruction; instruction is economised."
  - id: portability-claims-need-execution-tests
    relation: references
    notes: "Why the host was surveyed rather than assumed, and why the payload contract is proven on one host before being claimed for others."
  - id: coordination-claim-specification
    relation: implements
    notes: "The contention answer: the host's own sequential queue is one layer; an advisory claim on the worked repo is the estate-level layer, because a laptop session and a scheduled run share no scheduler."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "Unchanged: the run performs reversible work and files the rest. The host cannot push the release surface, which happens to align the machine with the doctrine."
---

# Decision: The Dispatch Host, Designed Against a Measured Machine

The operator commissioned a capability survey of the intended host — a
server-resident agent runtime that already carries several estate domains — and
supplied its answers on 2026-08-29. This decision records what the survey
settled and the design that follows. It is deliberately written from measured
facts: every claim below was evidenced by a command the host ran and showed.

## What the survey settled

- **Non-interactive execution exists and was proven.** The runtime takes a
  prompt as an argument, runs to completion, prints the final response to
  stdout, and exits 0. A live capability test was run and returned exactly.
- **The corpus tooling runs there.** Python 3.11 with PyYAML present in the
  runtime's own virtualenv; all six estate repositories already cloned; remote
  reads confirmed for every one.
- **The contract-delivery problem does not exist on this host.** The runtime
  loads `AGENTS.md` from the working directory as normal, even in one-shot
  mode, and the host has already exercised this — its dry-run workers ran with
  the domain directory as CWD and executed `estate-sync` then `session-start`
  against it. This is the failure that motivated the session gate on another
  harness; here it is absent by construction rather than by luck.
- **Scheduling exists at three layers** — the runtime's own cron gateway
  (ticking every 60s, with live jobs proven creatable by this account), system
  cron, and user timers.

## The three findings that shaped the design

**1. The host cannot push the framework root, and that is correct.** A
non-interactive push probe against the root failed for want of credentials,
while the same probe passed against all five domain repositories. This looks
like a gap and is actually the doctrine holding: the root is a release surface
declaring `autopush: false`, and its publication is the operator's deliberate
act. A host that *could* push it would be the anomaly.

The consequence is real, though: an estate-scoped run on this host would
accumulate unpushed root commits in a second clone, invisible to the operator's
machine. **The pilot is therefore scoped to one domain**, and any later
widening must answer what happens to root-scoped work before it widens.

**2. The run is turn-bounded and compression is on.** The configured ceiling is
120 agent turns, with automatic context compression enabled and no configured
model context length. A long multi-repository walk can therefore be compressed
mid-run — and compaction is not a session boundary in this framework. The stop
condition is consequently sized well inside the turn bound, and scope stays
narrow: a dispatch run that gets compressed is a run whose own record of what
it did is suspect.

**3. Runs can overlap, and the host says so itself.** Jobs carrying a working
directory are serialized by the host's own queue and a repeated job is skipped
while in flight — but two manually started processes are not coordinated, and
the host explicitly declined to treat its queue as sufficient. So the design
takes both layers: the job declares a working directory, **and** the dispatch
run takes an advisory claim on the repo it works, because the operator's laptop
session and the scheduled run share no scheduler and never will.

## The design

**Harness-agnostic by contract, not by adapter.** The framework composes the
launch text; the scheduler carries it. One new read-only surface —
`mdllm dispatch-payload` — prints the composed dispatch prompt for a named
scope, stop condition and launch context. Every host is then one line:

```
<runtime> --oneshot "$(python3 tools/mdllm.py dispatch-payload …)"
```

**Emit, never point.** The payload carries the prompt *text*. A tick that
handed over a path would be instructing rather than emitting, and instructed
content is economised — the failure mode the framework already measured on its
own contract. This also means the design does not depend on the host loading
anything automatically, which is what makes it portable to hosts where that is
not true.

**The digest is a committed thing, not a log file.** The host retains its own
run output — the latest fifty markdown files per job — which is transport and
backup, not record: it sits outside git, outside the estate, and rotates. The
digest the operator reads is committed into the corpus by the run itself, which
is also what gives the dead-man something durable to watch.

**Identity is preserved as the domain declares it.** The host commits to the
pilot domain under that domain's own agent identity, distinct from the
machine's general identity. That is an attributability property the regulated
domain wants, and the design must not flatten it.

## What stays the operator's

Registering the scheduled job is a permission-bearing installation — census
row 7, ratified 2026-08-28 — and remains the operator's single constructive
act. Nothing in this decision installs anything.

## What is claimed, and what is not

This design is proven-shaped for **one host**, on that host's own evidence. The
same payload contract is *expected* to serve the other harnesses because it
asks almost nothing of them, but that is a claim until each is exercised.
Recorded per `portability-claims-need-execution-tests`: a contract that runs
here has not thereby run anywhere else.
