---
id: claude-gate-5r5-acceptance-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [harness, adapters, phase-5r, acceptance-gate, execution-evidence, timeout]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Claude-side acceptance of Gate 5R.5 at d59f7af (implementation 244fdfe). Releases Phase 6."
  - id: claude-gate-5r4-acceptance-2026-08-13
    relation: derived-from
    notes: "Closes the orientation-truncation defect returned at 5R.4; the same root, same session-start step, now completing."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Acceptance was designed against this insight: exit zero, hook_success, and a generic attestation were all explicitly ruled insufficient — only the emitted orientation content counts."
---

# Claude acceptance — Gate 5R.5 at `d59f7af`

**Accepted. Phase 6 is released.**

The 5R.4 defect is closed: the framework root's own session now completes
its orientation instead of truncating it. Acceptance deliberately refused
the weak signals — exit zero, `hook_success`, and a generic attestation each
prove only that something ran, which is precisely the failure mode this
phase existed to fix.

## The fix, and why it is the right shape

`LifecycleStep.protected_seconds` replaces a hard per-step timeout. It is a
**floor, not a cap**: preceding steps must leave at least this much budget,
but once a step is current it may consume budget its predecessors did not
use, while the binding's total deadline stays absolute. Invariants are
enforced at construction — positive budgets, non-empty steps, a reserve that
leaves application time, and protected budgets that cannot exceed the
application budget.

This is the "flow unused budget to later steps" option rather than raising a
constant. A raised constant would have re-broken at the next corpus size;
this makes orientation's budget a function of what the fetch actually used.

## Acceptance evidence — a real automatic root session

Native `powershell.exe` 5.1.26100.9168 · Windows 11 26200 · Claude Code CLI
2.1.229 · framework root at `d59f7af`.

**1. The unchanged PS 5.1 reproduction stays green.** 2 passed — the shared
launcher and Codex hook fixtures accepted red on 2026-08-12 remain fixed.

**2. Both steps succeeded.** The transcript's `hook_success` carries:

```
[steps: estate-sync=0, session-start=0]
```

`session-start=0`, not the `124` recorded at 5R.4. Same root, same step,
same corpus.

**3. Orientation was actually emitted** — content, not merely a zero exit:

```
- **Version:** framework root (v3.31.0) — not a downstream domain…
- **Velocity:** last `things/` change 39 minutes ago (…); 144 commit(s) in 30d
- **Open loops (13):** forward work still in flight —
- **Triggers:** none currently true.
```

All four elements present with live values. This is the criterion the 5R.4
failure would have passed on a weaker test: the hook exited 0 there too.

**4. A fresh session-gate attestation.** Before: `11:53:08Z` pinned to
`42877f3`. After: `14:58:29Z` pinned to `d59f7af` — refreshed by the real
event and bound to current HEAD.

**5. Transcript correlated with the current definition hash.**

```
claude-code/session-start: currency=current; launch-currency=current;
                           execution=passed
execution evidence: source=claude-code-project-hook;
                    observed_at=2026-08-13T14:58:29.676681+00:00;
                    definition_current=true
execution detail: estate-sync=0, session-start=0
```

The attestation timestamp and the harness event agree to within a second,
and `definition_current=true` binds the record to the definition installed
now — not to an earlier one.

**Honest counter-evidence in the same report.** `post-write` remains
`execution=untested` with `definition_current=false` — *"stale execution
attestation ignored: managed definition changed"* — because 5R.5 changed that
definition too and no write has fired against it since. The diagnostic
refuses to let one moment's success cover another's silence.

## Boundary and estate

- Native PS 5.1 reproduction unchanged and green.
- The nested code-architect repository carries a second captured contract,
  `lifecycle-budget-allocation-boundary`, alongside the 5R.3 one — the
  code-architect direction continues to be honoured in the capture
  direction, not merely the consuming one.
- That repository's operator-owned `.claude/settings.local.json` is
  untouched; its working tree is clean.
- Nothing pushed. Publication remains the operator's deliberate act.

## What this releases, and what it does not

Phase 6 is released. It is the phase that earns `verified-on`, and its
evidence design should inherit this acceptance's standard: assert the side
effect a contract depends on, never the fact that a command ran.

Still outstanding and unchanged by this gate: POSIX live dispatch (needs a
natively installed Node and Claude Code in the Linux host), non-`startup`
SessionStart sources, and Copilot compatibility as a separately evidenced
claim.
