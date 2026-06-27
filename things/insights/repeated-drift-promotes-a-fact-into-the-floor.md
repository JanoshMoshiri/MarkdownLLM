---
id: repeated-drift-promotes-a-fact-into-the-floor
type: insight
status: active
disposition: keep-active
disposition_reason: "Standing razor for when a recurring drift has earned hardening into the deterministic floor."
version: 1.1
created: 2026-06-24
session: 2026-06-24
source: both
confidence: high
origin: synthesised
tags: [coherence, drift, dark-region, floor, design-principle, framework-map]
linked_things:
  - id: prose-references-are-mechanically-checkable
    relation: extends
  - id: tracking-artifacts-can-drift-from-reality
    relation: references
  - id: framework-retrospective-2026-06d
    relation: references
---

# Repeated Drift Promotes a Fact Into the Floor

## The Insight

The framework-map's *"N mechanical subcommands"* count is a prose mirror of a
mechanical fact (`mdllm --help`). It has now drifted from reality more than once
— the 23→25 spec-count drift the v3.12.0 `coherence` work already cited as
motivation, and 15→17 caught this session. A hand-maintained number that restates
something the tool can compute will drift *every* time the tool changes and the
prose is not updated in the same commit.

The rule that falls out is a **trigger for when to spend a floor check**: not on
first drift (cheap to fix by hand, and the change-reconciliation edge-walk catches
it), but on **recurrence**. One drift is an accident; a *second* drift of the same
prose-mirrored fact is a missing check announcing itself. At that point you stop
maintaining the fact by discipline and move it into the floor — here, a `coherence`
dark-region check comparing the asserted integer against the live `--help` list.

This is `prose-references-are-mechanically-checkable` generalised from *references*
to *derived summaries* — counts, lists, tallies. The dark region has a mechanical
half wherever the prose asserts something the corpus already knows.

## Why It Matters

It keeps the floor **sized to demonstrated failure, not anticipated failure** —
the framework's standing discipline. A `coherence` check is justified by recurrence
you can point to, not by a preemptive hunch that something *might* drift. So the
heuristic is cheap to apply and self-limiting: most prose facts never drift twice
and never earn a check. `coherence` already owns kernel / index / catalog freshness;
the framework-map subcommand count is the next member of that family, and its
build is small (parse the asserted count, diff against `mdllm --help`).

## Context

Surfaced 2026-06-24 in retrospective `framework-retrospective-2026-06d`, whose
reconciliation pass caught the 15→17 drift — the second recorded instance. Left as
the retrospective's open recommendation #2 and captured here as the durable rule
plus the concrete next build. Not yet implemented; the operator chose to record it
and move the actual `coherence` work to a later session.
