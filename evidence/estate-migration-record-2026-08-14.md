---
id: estate-migration-record-2026-08-14
type: artifact
status: stable
created: 2026-08-14
tags: [harness, adapters, migration, estate, phase-8, execution-evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "The Phase 8 rollout, executed: every domain moved onto the 5R.2 projection after the mechanism was verified on both platforms."
  - id: claude-gate-5r3-acceptance-2026-08-13
    relation: derived-from
    notes: "The refresh mechanism accepted there is what this record exercises across the live estate."
  - id: assistant-register-does-not-graduate
    relation: implements
    notes: "The one extended domain migrated by removing the extension that decision retired, not by overriding the refusal that protected it."
---

# Estate migration record — all thirteen domains

Every domain moved onto the Phase 5R.2 one-handler projection on 2026-08-14,
in a deliberate risk order, each verified by a real Claude Code session
before the next was touched. The mechanism was verified on Windows and Linux
*before* it touched a live domain — the precondition the plan set at 5R.2.

## Order and outcome

| # | Domain | Decision | Verified |
|---|---|---|---|
| 1 | code-architect | create | ✅ |
| 2 | agent-architect | refresh (first true legacy replacement) | ✅ |
| 3 | a domain in daily use | refresh (first actively-used domain) | ✅ |
| 4–10 | seven further domains | refresh | ✅ |
| 11 | property-ventures | create | ✅ |
| 12 | eco-essentials | **merge** | ✅ |
| 13 | the regulated deployment | refresh, after extension removal | ✅ |

The escalation was the operator's: a create first, then a low-risk legacy
refresh, then a domain in daily use, and only then the remainder. Each of the
first three was verified before the next began, so a failure would have
stopped the sequence rather than propagating through it.

## What verification meant

Not exit codes. For every domain: a real session, its harness transcript
read, and the mechanical result line confirmed —

```
[steps: estate-sync=0, session-start=0]
```

Every legacy refresh produced the identical diff: **4 insertions, 6
deletions**, confined to the hooks region. Nothing outside it changed in any
domain.

## The three that were not uniform

**eco-essentials** was a `merge`, not a refresh: it carried `permissions` and
no hooks, so the hooks member was added beside them and the existing
permission survived byte-intact. Its `.gitignore` had excluded `.claude`
wholesale since the domain was a Copilot workspace being trialled with
Claude — a stale reason, narrowed to `settings.local.json` so the adapter now
ships with the repo like every other domain.

**One domain has no remote**, so it committed without publishing. Correct,
not a failure.

**The regulated deployment** carried a `--assistant` command tail. Ordinary
and explicit refresh both refused it: a local extension makes ownership
mixed, and the tool will not infer a migration across an operator's own edit.
The refusal was resolved by *removing the extension* — which
[[assistant-register-does-not-graduate]] had just retired — not by
overriding the guard. Once removed, the fragment matched `legacy-v1` exactly
and migrated like the rest.

That sequence is the mechanism working as designed: the operator's caution
and the tool's refusal reached the same answer independently, and the
migration only proceeded once the ambiguity was genuinely gone.

## Version seal

All thirteen domains were then sealed from v3.30.0/v3.30.1 to **v3.31.0**.
The judgement was made once, centrally, and is recorded in each commit: both
intervening releases are framework-internal (review-loop findings, spec
contradictions, doctrine), introduce no domain-facing capability, and the
domain-kernel managed blocks were already in sync. There was nothing to adopt
semantically, so sealing states a true fact rather than rubber-stamping one.

## Known residue

Two of the largest domains truncate their orientation at the 2200-character
lifecycle output cap, losing version drift, velocity and open loops while
keeping the triggers line. Recorded separately in
`lifecycle-output-truncation-2026-08-14` and returned to the owner of that
seam; it is not a migration defect and predates the migration on any domain
large enough to hit it.

## Not claimed

Codex projections were not installed in any domain — this is the Claude
lifecycle only. No domain's content, schema, skills or permissions were
touched. macOS remains designed-for.
