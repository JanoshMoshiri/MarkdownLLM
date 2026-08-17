---
id: claude-phase6-no-adapter-and-root-2026-08-16
type: artifact
status: stable
created: 2026-08-16
tags: [claude-code, windows, phase-6, execution-evidence, git-floor, adapter-optionality]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Claude-owned Phase 6 evidence: the automatic framework-root lifecycle record after the Gate 6R refresh, and the disposable no-adapter floor proof with its one unestablished leg."
  - id: codex-phase6-post-6r-acceptance-2026-08-16
    relation: complements
    notes: "The Codex half of the same Phase 6 split. Neither agent self-certifies the other harness; this record supplies only the Claude side."
  - id: claude-gate-6r-acceptance-2026-08-16
    relation: extends
    notes: "Gate 6R proved bounded output on the largest nested domain; this record repeats the automatic lifecycle at the framework root itself."
  - id: claude-entry-surface-unprovisioned-for-no-adapter-domains
    relation: references
    notes: "The finding this record produced: Claude's automatic entry route needs a CLAUDE.md wrapper that no scaffold mode writes."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Every claim below is asserted from a harness-owned transcript record or a contract-bearing side effect, never from exit zero."
---

# Claude Phase 6 — framework root and disposable no-adapter — 2026-08-16

**Two records, one negative finding.** The framework-root automatic lifecycle
record is complete and closes its checkbox. The disposable no-adapter proof
closes its floor legs and *fails* its interpretation leg — not for want of
running it, but because the precondition it depends on is not provisioned by
any scaffold mode on this harness.

## Tested surface

| Fact | Value |
|---|---|
| Harness | Claude Code **2.1.229** |
| Platform | Windows 11 Pro 10.0.26200 |
| Framework root HEAD at session start | `de035d3ef41c4cd75a6c367070d6077881db8720` |
| Session / transcript id | `aedc0d0b-d095-487b-ab60-bc4c129ee88e` |
| `.claude/settings.json` SHA-256 | `2232dd0c79bef65deb4b0e0e42fdcbbe871b78a6177e75cd5be1081f84bce264` |
| `.claude/settings.local.json` SHA-256 (operator-owned, read only) | `5c1dd0cbe158a132c442cd79022670f1b252abf407d5279c26f04f3d8e241a72` |
| SessionStart definition | `sha256:df8e8f5f9422754302552bfdbed1d12692c961b8dd244045bf13f0a2a65b4e2a` |
| PostToolUse definition | `sha256:36fd9fc6350291fea06d6d5cfbd9ca0d0bce7571a7e5bdb9eb80af2097d64da2` |

The root artifacts are the ones the operator approved and refreshed at Gate 6R;
`doctor` reports `currency=current`, `legacy-id=none` for both moments, so this
is not a reuse of the 5R.2 launch probe and not a legacy record.

## Framework root — automatic SessionStart

Dispatched by the product. Neither `session-start` nor `harness-event` was
invoked by hand at any point before the record below was captured.

| Fact | Value |
|---|---|
| Transcript record | `hook_success` / `SessionStart:startup` |
| Harness timestamp | `2026-08-16T17:25:28.237Z` |
| Attestation `observed_at` | `2026-08-16T17:25:28.203365+00:00` |
| Correlation window | **34 ms** |
| Emitted context | **2015 / 2200 characters** |
| SHA-256 of emitted context | `742e43fd9d4513d82a90769c1e0c8250b70dd23deac7ce9c611546681035fd10` |
| cwd / branch | framework root / `main` |

Content assertions against the emitted text, not against the exit code:

| Assertion | Result |
|---|---|
| within the 2,200-character envelope | PASS (2015) |
| both step labels present | PASS |
| both return codes present | PASS (`estate-sync=0, session-start=0`) |
| represents estate state | PASS (14 repos walked) |
| contains Version | PASS |
| contains Velocity | PASS |
| contains Open loops | PASS (12) |
| contains Triggers | PASS |
| elision marked explicitly | PASS (`[truncated]` inside the estate listing) |
| `definition_current=true` | PASS |
| `execution=passed` | PASS |

**Claude's transcript names the normalized source.** The hook record is
`SessionStart:startup`, not an undifferentiated event. This is a genuine
asymmetry with the Codex record, whose attestation schema does not carry the
source at all.

### A second source, observed the same day

Later that evening the same session was resumed, and the hook fired again on
its own as `SessionStart:resume` — `2026-08-16T22:33:12.833Z`, attestation 30 ms
away at `22:33:12.803813+00:00`, same definition hash, `estate-sync=0,
session-start=0`. Emitted context **2042 / 2200 characters**, again carrying
both step labels and return codes, estate state, Version, Velocity, Open loops,
Triggers, and explicit elision — plus an Open conflicts section that had not
existed at startup, because the finding recorded below had become a live thing
in between. Orientation surfaced it without being asked to.

`startup` and `resume` are therefore both observed on this surface. `clear` and
`compact` remain unobserved and unclaimed.

**What the resume does *not* establish.** Claude Code replays a resumed
session's context rather than re-reading project memory, so a resume cannot
test whether an entry pointer is auto-loaded. That question needs a fresh
session, and it is the one thing still outstanding below.

## Framework root — automatic PostToolUse

| Step | Observation |
|---|---|
| Invalid write (frontmatter thing omitting `created`) | `hook_success` / `PostToolUse:Write` at `2026-08-16T17:33:06.541Z`, 602 characters: `[steps: validate=1]`, `[validate: exit 1]`, naming ``missing required field `created` `` |
| Enforcement | **advisory only** — the write was not reverted or blocked; the Git floor remained the sole enforcement boundary |
| Repair (add `created`) | **quiet** — no additional context attached to the transcript |
| Proof the quiet run happened | the post-write attestation moved to `2026-08-16T17:33:19.366688+00:00`, `detail=validate=0`, `outcome=passed`, same definition hash |
| Probe disposal | file deleted; worktree clean before any commit |

Silence is the contract for a successful post-write, so the attestation — not
the absence of output — is what evidences the run.

## Disposable no-adapter repository — Claude-owned floor proof

An out-of-estate disposable domain was created with
`mdllm scaffold <path> --harness none`, outside the framework worktree so the
fixture could not inherit the parent `.git` floor.

Absent by inspection immediately after scaffold: `.claude/`, `.codex/`,
`.git/mdllm-harness-attest`, `CLAUDE.md`. Present: `AGENTS.md`, the domain
skills and prompts, and the installed `pre-commit` hook. Scaffold commit
`a3967cadee8973a2e632115dae32f02b97bd78de`.

| Leg | Act | Result |
|---|---|---|
| A | valid thing, commit **before** any session-start attestation | **blocked**, exit 1, `_session-gate` Error naming the remedy; HEAD unchanged |
| B | the interpretation-prescribed `python {framework_root}/tools/mdllm.py session-start .`, resolved through the relative `framework_root` declared in the scaffolded `AGENTS.md` | exit 0; emitted the Tier-0 contract plus version, velocity and open loops; wrote `.git/mdllm-attest` at `2026-08-16T17:31:21.487917+00:00` |
| C | same valid thing, commit again | **passed** — `83eec633c3637b40fe30c8c2ff417a12660965a5` |
| D | thing omitting `created`, commit | **blocked**, exit 1, Error names the exact field; HEAD unchanged |
| E | repaired thing, commit | **passed** — `5c16ea8b7c7c7a83abeea94807a7a8a27e79597b` |

`.git/mdllm-harness-attest` was never created at any point: with no adapter
there is no harness event to attest, and the tool did not invent one. Leg A is
additional to the Codex record — it proves the strict gate is load-bearing
before the ritual, not merely satisfied after it. The fixture was deleted
after capture.

**Three of the four legs the Codex record established are therefore
established for Claude too:** the interpretation-prescribed session start can
set the strict gate, a valid commit passes the floor, and an invalid commit is
blocked.

## The fourth leg is not established, and the reason is structural

Codex's record could assert "AGENTS interpretation remains automatic" because
Codex auto-discovers `AGENTS.md`. On Claude Code that route is different, and
the difference is documented in this repository: `interface.md` lists the
Claude Code route as "CLAUDE.md at root references AGENTS.md", and README's
vendor setup says the *installer* writes a `CLAUDE.md` wrapper containing
`@AGENTS.md`.

Three checks, all mechanical:

1. **No scaffold mode writes that wrapper.** `--harness none` and
   `--harness claude` scaffolds were both created and compared: neither
   contains `CLAUDE.md`. Only `install.ps1` / `install.sh` write one, and only
   at a framework clone root.
2. **The framework root here has no `CLAUDE.md` either** — the installer's file
   is optional and absent on this clone. Nine of the thirteen live domains also
   lack it.
3. **The entry file was consequently never auto-loaded in this session.** The
   root `AGENTS.md` prose first appears in the harness-owned transcript at
   `2026-08-16T17:35:33Z` — inside a tool result from a deliberate read, ten
   minutes after SessionStart — and nowhere before it. The only framework state
   delivered automatically at session start was the adapter's SessionStart
   injection.

The disposable repository is in exactly the structural condition point 3
describes. So the leg is not merely unrun: as scaffolded, a `--harness none`
domain has **no automatic Claude entry surface at all**, and removing the
adapter removes the only automatic route the harness had.

That is recorded as a finding, not as an executed negative — see *Failures*
below for what was actually attempted. The finding is carried forward as
`claude-entry-surface-unprovisioned-for-no-adapter-domains`.

## What was done about it, the same day

The operator chose to provision the pointer rather than narrow the claim, on
the grounds that scaffold cannot know which harness will be opened and a
redundant three-line file costs nothing next to an undiscoverable domain. The
alternative — detect the harness and emit `CLAUDE.md` *instead of* `AGENTS.md` —
was rejected for destroying interchangeability between harnesses.

`templates/entry/` now holds the entry pointers and scaffold writes every one
of them in every selection, `none` included, reserved as core so no adapter can
claim the filename. The vendor name lives in the template's filename, not in
neutral code, so the architecture fitness gate still passes; adding a pointer
for a future harness is a file, not a code change. The framework root — which
had none, and whose missing pointer is what made this session blind to its own
`AGENTS.md` — received the same pointer the installers write.

**The estate was then swept, on the operator's explicit instruction** — which is
what requirement 4 actually forbids doing *silently*, not what it forbids doing.
All thirteen domains now carry a tracked pointer that imports the entry file.
Two things the sweep exposed:

- The four domains that already had a `CLAUDE.md` carried **prose only** — "read
  `AGENTS.md` first" — which instructs the agent rather than inlining the file.
  Better than nothing, and it is why those four were never blind, but weaker
  than the import. Their existing text was kept and the import appended.
- `eco-essentials` had `CLAUDE.md` in `.gitignore`, added by commit `89b1e49`
  ("consolidate CLAUDE.md into AGENTS.md, untrack ignored files") — a past
  session reasoning that the pointer was redundant duplication. That is exactly
  the belief this finding overturns, so the ignore was removed and the reversal
  named in the commit.

This closes the *provisioning* half. It does not close the leg: that the
pointer causes the entry file to auto-load has still not been watched happen.

### Verification of the fix

| Check | Result |
|---|---|
| Focused suite (scaffold selection + architecture fitness) | **20 passed** |
| Complete suite, external basetemp | **466 passed** (465 before, plus the new entry-pointer test) |
| `validate .` | 203 things + 6 + 14 across the two example corpora, 0 errors / 0 warnings / 0 info |
| `coherence .` | no issues found |
| `git diff --check` | clean |
| Estate after the sweep | 13/13 domains carry a tracked pointer that imports; 12 published through their own autopush, one has no remote and stayed local |

One failure worth recording rather than hiding: the first complete run reported
2 failed / 464 passed, both `FileNotFoundError` on ~230-character paths. The
cause was the basetemp, not the change — it sat inside an already deeply nested
session scratchpad and the scaffold fixtures crossed Windows' 260-character
limit. Rerunning from a short path cleared both without touching a test, which
is the same discipline the Codex record applied to the mirror-image error
(basetemp *inside* the repository, inheriting the parent Git floor): correct the
environment, never edit production to make the error disappear.

## Failures and limits, recorded

- **A live Claude Code session was not opened in the disposable repository.**
  Two attempts were made from this host with the real CLI (2.1.229) with cwd
  set to the probe repo. Both terminated before any model turn:
  session `2a517166-b349-4642-8cf4-1f9bf7f22f12`, `apiKeySource: none`,
  result `Failed to authenticate: OAuth session expired and could not be
  refreshed`; a second attempt supplying an external key returned
  `Invalid API key`. The carried-forward constraint from Gate 5R.1 — live
  Claude runs require a re-authenticated CLI — still stands. The structural
  finding above does not depend on that failure, and the failure does not
  establish the finding.
- Point 3 is one surface: Claude Code 2.1.229 on Windows, this clone, this
  session. It is not a claim about every Claude Code build or about whether
  the product reads `AGENTS.md` natively elsewhere.
- macOS and POSIX remain `designed-for` for the Claude projection; nothing here
  changes `claude-platform-surface-narrowed`.
- `clear` and `compact` SessionStart sources remain unobserved (`startup` and
  `resume` are both recorded above).
- GitHub Copilot remains separately untested; shared `.claude` bytes are not
  Copilot evidence.
- The disposable fixtures were deleted after capture, so the commit hashes
  quoted above are no longer resolvable in any repository — the same convention
  the Codex record follows for its own fixture. The harness-owned session
  transcripts do survive under the harness's project store, including the
  failed-authentication probe cited above.
- The framework root's adapter artifacts were read and hashed, never modified.
  The estate sweep that followed wrote one pointer file per domain and, in one
  case, removed a `.gitignore` line; no adapter, permission or settings byte was
  touched anywhere.
