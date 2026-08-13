---
id: claude-gate-5r4-acceptance-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [harness, adapters, phase-5r, acceptance-gate, execution-evidence, timeout]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Claude-side acceptance of Gate 5R.4 at 42877f3: mechanism accepted; one live defect returned as blocking for Phase 6."
  - id: framework-root-tracks-both-adapters
    relation: implements
    notes: "The operator decision is now executed: .codex/hooks.json is rerendered and tracked, and the root .claude projection is migrated."
  - id: claude-gate-5r3-acceptance-2026-08-13
    relation: derived-from
    notes: "5R.3's refresh mechanism is what made this root migration possible; this record exercises it on the root itself."
---

# Claude acceptance — Gate 5R.4 at `42877f3`

**Mechanism accepted. One live defect returned, blocking for Phase 6.**

Every 5R.4 claim was independently re-derived. The suite matches
(**456 passed**, external pytest base, per the handoff's instruction). The
reconciliation itself is correct. But firing a real session at the newly
reconciled root exposed a lifecycle budget defect that makes the framework
root's own orientation truncate.

## Verified claims

| Claim | Independent result |
|---|---|
| root projections refreshed atomically | working tree fully clean |
| `.codex/hooks.json` tracked | confirmed via `git ls-files` |
| both adapters current | `currency=current`, `launch-currency=current`, `legacy-id=none` |
| old attestations invalidated | see below |
| execution honestly `untested` | both harnesses, both moments |
| no nested domain migrated | all 13 nested repositories clean |
| post-refresh dry run | exactly two `NO-OP` decisions |
| scaffold matrix | 15 passed |
| complete suite | 456 passed (external base) |
| **operator permissions preserved** | byte-identical across the refresh |

**Attestation invalidation, demonstrated on my own evidence.** The
attestations minted by the Phase 5R.2 live run (07:39–07:40Z) now report
`definition_current=false` — *"stale execution attestation ignored: managed
definition changed"* — so execution reports `untested` rather than
inheriting them. Old evidence cannot certify a new definition; the
placeholder-hash design holds against the very records that would most
plausibly have leaked through.

## Returned defect — the reconciled root truncates its own orientation

A real Claude session against the reconciled root produced one correctly
ordered handler, and then:

```
[steps: estate-sync=0, session-start=124]
[session-start: exit 124]  step timed out after 25.0s
```

Measured directly on this host:

| Step | Actual | Budget | Margin |
|---|---|---|---|
| `estate-sync` | 59.8s | 75s | +15.2s |
| `session-start` | **36.1s** | **25s** | **−11.1s (exceeds by 45%)** |
| combined | 95.9s | 105s total | +9.1s |

**Consequence.** On the framework root a session now begins with estate-sync
output but **no orientation** — version, velocity, open loops and triggers
are all lost. The hook still exits 0, so the loss is quiet by design
(`surface-and-continue`): the operator sees a truncation note, and the model
simply never receives the Tier-0 report the session-start contract promises.

**Attribution.** Not caused by 5R.4's reconciliation. The per-step budgets
were set in 5R.1, and the legacy projection had no per-step timeout at all,
so the root only became subject to them when 5R.4 migrated it. 5R.4 is the
commit that makes the defect live, not the commit that introduced it.

**Why it was not fixed here.** `LIFECYCLE_BINDINGS` is a neutral port. The
standing rule is that an acceptance pass does not alter neutral ports
opportunistically, so this is returned rather than patched.

**The design question inside it.** A single constant cannot serve both
scales: 25s is generous for a small domain and wrong for the largest. Even
raising it to ~45s leaves roughly 9s of total headroom, which one slow
network fetch consumes — `estate-sync` is already at 59.8s of its 75s.
Options worth weighing rather than a value to pick blindly: raise the
per-step budget; make the remaining budget flow to later steps; move the
per-repo sync bound inside `estate-sync`; or treat orientation as
non-truncatable and let it borrow from the total.

**Blocking scope.** Phase 6 records `verified-on` evidence. Certifying a
root that silently drops its orientation would place a false claim in the
record, so this must be resolved before Phase 6 execution evidence is
gathered — it does not block accepting the 5R.4 mechanism itself.

## Incidental observation

`cmd_scaffold` exits 1 with an unhelpful error when the target path is long
enough to hit the Windows path limit (a ~150-character pytest base was
sufficient here; a 39-character base passes all 15 scaffold tests).
Pre-existing and unrelated to 5R.4, recorded so it is not rediscovered as a
phantom regression.

## Not claimed

Execution remains `untested` for both harnesses at the current definitions —
correctly, since no real event has run against them since the refresh (the
session described above ran against the reconciled Claude projection and is
reported here as a defect observation, not as `verified-on` evidence). The
`/hooks` trust boundary remains CLI-specific and human-observed.
