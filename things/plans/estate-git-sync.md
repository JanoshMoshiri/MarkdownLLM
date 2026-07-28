---
id: estate-git-sync
type: plan
status: completed
version: 1.1
created: 2026-07-28
priority: high
tags: [estate, git, sync, session-start, multi-machine, floor]
linked_things:
  - id: divergence-is-an-unrouted-decision
    relation: implements
    notes: "The ff-only rule is this insight mechanised: the tool transports, never resolves — a non-ff state is reported as a decision owed, not merged"
  - id: source-behind-mirror-is-still-a-consumer-side-read
    relation: references
    notes: "Same design lens: no new operator-axis machinery — the walk is a batch of per-repo reads any session could make alone"
  - id: git-workflow-specification
    relation: extends
    notes: "Extends commit-is-real across the machine axis: the commit makes state real on one machine; publication makes it real to the estate"
  - id: orchestration-specification
    relation: extends
    notes: "New hard hook session-start:estate-sync; sharpens (does not violate) the no-live-fetch doctrine"
  - id: operator-gated-work-is-scheduled-on-the-operators-calendar
    relation: references
    notes: "The felt gap: manual fetch/pull on every machine switch is operator toil the floor can carry"
---

# Estate Git Sync — session-start fetch/pull across the machine axis

The operator now works the same domains from more than one machine (local +
cloud Cowork), with collaborators coming. Orientation reads committed state —
velocity, triggers, verified flips, the audit all read `git log` — but in a
multi-machine estate, committed state partly lives on the remote. A session
that orients without fetching is orienting from a stale event stream. So
session-start sync is an **orientation-correctness requirement**, not a
convenience — which is why it belongs in the floor rather than in the
operator's fingers.

**The spine (named, not invented):** the commit makes state real *on one
machine*; publication (push/fetch) makes it real *to the estate* — and
orientation reads the estate. Zero new primitives: this extends
git-workflow.md's commit-is-real principle across the machine axis.

## Design decisions (settled with the operator, 2026-07-28)

1. **`git pull --ff-only`, never a bare pull.** Fast-forward = transport of
   already-committed state; silently safe. Non-ff = both machines committed
   since last sync = `divergence-is-an-unrouted-decision`: report
   `DIVERGED (+a/+b)`, take no action, route the resolution to the operator.
   Never auto-merge, never reset, never force-anything (history is sacred).
2. **Bounded and degrading, never blocking.** `GIT_TERMINAL_PROMPT=0` +
   per-repo timeout. Offline / auth-failure / timeout → one advisory line
   ("orienting from last-fetched state") and the session proceeds. This
   *sharpens* rather than violates orchestration.md's no-live-fetch doctrine:
   what that rule actually forbids is orientation **requiring** a network
   call to complete. Both spec passages are amended to draw the line
   explicitly (a required network call stays forbidden; a bounded
   degrade-gracefully attempt that improves orientation when the network
   exists is the hook's job).
3. **`session-start` stays read-only.** The ritual emitter documents itself
   "Read-only; safe on every session" — sync mutates the working tree, so it
   is its **own command**, ordered *before* `session-start` in the harness
   SessionStart adapter (two commands). Interpretation anchor in prose;
   harness adapter is the hardening, exactly like `session-start:version-check`.
4. **Discovery is legitimate here — the estate-check guardrail does not
   transfer.** `estate-check` refuses discovery because its objects are
   *membrane reads* and a config/registry would become a producer→consumer
   map. `estate-sync`'s objects are **repos and their own remotes** — a
   filesystem walk for `.git` dirs (root + immediate children of `domain/`
   and `domains/`) reveals nothing `ls` doesn't and touches no membrane.
   Batching-never-an-index still binds: stdout-only, ephemeral, nothing
   persisted. Explicit paths accepted as override. The code comment states
   this distinction so a future session doesn't "fix" it into consistency.
5. **Push discipline untouched, made visible.** The tool never pushes
   (git-workflow.md: push is always the human's deliberate act). The
   session-end ritual gains a **publication-debt** step — `estate-sync
   --status` (no network; cached tracking refs) listing `ahead +n (unpushed)`
   per repo — so the other machine's next pull finds everything, without the
   operator having to remember. Cloud sessions keep their push-per-commit
   standing instruction (spin-up-domain); the asymmetry is now surfaced
   instead of silent.
6. **Membrane chaining stays deliberate.** If sync moved any domain, print
   one advisory line suggesting `mdllm estate-check <moved roots>` — pulled
   source commits can flip consumers stale/diverged. Never auto-run.
7. **`git.autopush` per-domain config: held.** The multi-user need is real
   but not yet felt; deploy-when-felt. When a collaborator exists, add it as
   the mirror of `git.autocommit` (declared discipline per domain rather than
   implicit per harness), plus PR flow on shared repos.

## Eventuality table (every state a repo can be in at session start)

| State | Behaviour |
|---|---|
| Remote ahead, ff possible | pull, `synced (+n)` |
| Local ahead only | `ahead +n (unpushed)` — no action; this is the publication-debt signal |
| Both moved | `DIVERGED (+a/+b)` — no action, decision owed |
| Force-pushed remote | surfaces as DIVERGED; never reset |
| Offline / DNS / timeout | `offline` — orient from last-fetched state, proceed |
| Auth would prompt | `GIT_TERMINAL_PROMPT=0` → `auth-failed`, proceed |
| Dirty working tree | fetch yes, pull skipped, `dirty` — never eat uncommitted work |
| Merge/rebase in progress | skipped, reported |
| No remote | `local-only` — legitimate; the remote has always been the human's step |
| No upstream / detached HEAD / unborn branch | reported, skipped |

Worst outcome of any row: orient from slightly stale state *and be told so* —
strictly better than today's silent staleness. None block.

## Phases

1. **Spec: git-workflow.md** — machine-axis section (ff-only inbound,
   divergence routed, publication debt; push discipline unchanged) + one
   kernel-block line.
2. **Spec: orchestration.md** — hard hook 4 `session-start:estate-sync`
   (anchor `interpretation`, hardened by harness adapter); amend the two
   no-live-fetch passages; kernel block updated.
3. **Floor:** `mdllm estate-sync` (`tools/markdownllm/sync.py`) + `--status`
   offline mode; cli wiring; self-tests against local `file://` remotes
   covering the eventuality table.
4. **Wiring:** `.claude/settings.json` SessionStart two-step; AGENTS.md
   hard-hook prose; `end-session.md` publication-debt step.
5. **Docs:** operator-guide "Running More Than One Domain" machine-axis
   paragraph; framework-map subcommand count + View 3 node.
6. **Seal v3.22.0:** CHANGELOG, sentinel trio, kernel regen, validate +
   coherence + full suite; close this plan with outcome.

## Candidate insight (harvest at session end if it survives the build)

`an-unpushed-commit-is-invisible-to-the-estate` — commit-is-real has a scope
qualifier the single-machine era never exposed: real-here vs real-everywhere.
The publication-debt report is that qualifier made visible.

## Outcome

Shipped as v3.22.0, all six phases, one session (2026-07-28). The build
followed the settled decisions without deviation. Proof points from the
session itself:

- **The felt gap, caught on contact:** the first live `estate-sync` run
  fast-forwarded two genuinely stale local domains (+2 and +3 behind their
  remotes from cloud sessions) — exactly the manual-fetch toil that motivated
  the plan, found and closed by the tool's first execution.
- **The floor defended the build twice while it was being built:** the
  pre-commit hook blocked the git-workflow.md commit until the kernel was
  regenerated with it, and the commit-msg boundary hook blocked a floor
  commit whose message named private domains (rewritten with substitutions).
- **`--status` proved honest at zero distance:** its first run reported the
  only publication debt as this session's own unpushed framework commits.

Wired on all three surfaces (Claude Code SessionStart adapter, AGENTS.md
interpretation block, generated domain session-start kernel step 0 — domains
inherit through the refresh channel). 8 self-tests (151 total), incl.
never-pushes and no-merge-commit proofs. Deferred as designed: `git.autopush`
per-domain config waits for a real collaborator (deploy-when-felt).
