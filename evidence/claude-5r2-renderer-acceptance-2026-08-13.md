---
id: claude-5r2-renderer-acceptance-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [harness, adapters, claude-code, phase-5r, renderer, execution-evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Phase 5R.2 renderer/launch acceptance at ba96d73. Earns designed-for only; Phase 6 owns the automatic-dispatch record that earns verified-on."
  - id: claude-phase5r0-matrix-completion-2026-08-13
    relation: derived-from
    notes: "The sh-dialect carrier and CLAUDE_PROJECT_DIR anchoring implemented here were determined by that live dispatch matrix."
  - id: code-architect-governs-substrate-code
    relation: implements
    notes: "First code work under the operator's direction that code-architect principles govern substrate code."
---

# Claude 5R.2 renderer acceptance — one handler, ordered runner, live

The Claude-owned projection replacement, executed against real Claude Code
rather than reasoned about. Commit `ba96d73`; full suite **443 passed**.

Per the v1.10 amendment this record earns **designed-for**: it proves the
renderer and launch seam work when Claude dispatches them. Phase 6 owns the
independently witnessed automatic-dispatch record that earns `verified-on`.

## What changed

| Before (legacy-v1) | After (5R.2) |
|---|---|
| two SessionStart handlers, one per step | **one** handler per moment |
| ordering implied by handler order (never guaranteed — Claude runs matching handlers in parallel) | ordering owned by the neutral lifecycle runner |
| `python ../../tools/mdllm.py <op> .` — cwd-dependent, bare-name Python | sh via the **shared** launcher; root from `${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}` |
| no timeout declared (vendor default inherited) | explicit `"timeout": 120` |
| no output port; raw CLI stdout | `LifecycleOutputPort` — Claude's documented envelope |
| `trust=not-applicable` | `trust=unknown` + detail (the surface was never modelled, not absent) |

## Live evidence — Claude Code CLI 2.1.229, Windows 11, fresh scaffold

**Ordered session-start, in one handler.** The transcript carries exactly
**one** `hook_success` for `SessionStart:startup`, whose stdout is Claude's
envelope containing both steps in order:

```
[steps: estate-sync=0, session-start=0]
[estate-sync: exit 0]  ## Estate Sync — <probe domain> (1 repo(s)) …
[session-start: exit 0] # MarkdownLLM — Session Start …
```

Ordering is now a property of the runner's output, not of a schema promise
the harness never made.

**Passing post-write is silent — and provably fired.** A valid `Write`
produced *no* PostToolUse attachment. Absence alone is ambiguous (quiet and
never-fired look identical), so the hash-bound attestation settles it:

```
claude-code/post-write: … currency=current; execution=passed
execution evidence: source=claude-code-project-hook;
                    observed_at=2026-08-13T08:24:49Z; definition_current=true
execution detail: validate=0
```

**Failing post-write is advisory, never enforcing.** A deliberately invalid
thing (missing `created`) produced a `PostToolUse:Write` attachment carrying
`[steps: validate=1] [validate: exit 1] ## Validation Report …`. The tool
action was not blocked and the session continued — the Git pre-commit hook
remains the whole enforcement boundary.

**Floor commit.** After removing the broken thing, `git commit` in the
scaffolded domain passed the pre-commit floor (exit 0) under
`session_gate: strict`, the attestation having been minted by the real
SessionStart event rather than by hand.

## Inspector states

`ManagedFragment` gains `legacy_id`, with the invariant that a recognised
legacy fragment is never also current:

| Estate shape | `current` | `legacy_id` |
|---|---|---|
| 5R.2 projection | `True` | `None` |
| scaffolded pre-5R.2 form | `False` | `legacy-v1` |
| legacy **+ local `--assistant`** | `False` | `None` — recognition withheld |
| unknown stale | `False` | `None` |

Row three is the load-bearing one. Recognition is withheld over mixed
ownership so migration can never be inferred across an operator's own edit,
while the extension is still *reported* rather than flattened into silence.

Consequently every shape in the live estate is now `known-legacy`, and a
plain install **refuses** where it previously no-op'd. The tests assert the
refusal is enforced at apply time, not merely advertised at preflight:
applying a refused plan raises and leaves the bytes hash-identical.

## Goldens

`settings.json.legacy-v1.golden` freezes the historical bytes as immutable
recognition input. The current golden carries `{rel_fw}` **and**
`{hash_*}` placeholders, because the definition hash is path-derived; the
test substitutes them from the adapter's own `_definition_hash`. That
asserts the invariant worth having: an installed handler carries exactly the
hash its renderer would produce, so a stale handler cannot mint current
attestation evidence.

## Not claimed

Automatic-dispatch `verified-on` (Phase 6), POSIX live dispatch (needs a
native Linux Node + Claude Code), non-`startup` SessionStart sources, and
Copilot compatibility — which stays a separate claim with its own contract
and execution record. No existing domain was migrated; no `.claude`
artifact outside the throwaway probe was modified.
