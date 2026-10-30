---
description: Watch — arm this seat's doorbell in the background so Claude Code rises when the other seat's turn lands; `/watch <role> <definition> [run]`. The Claude Code half of the wake channel (standing-watch.md → Harness bindings).
allowed-tools: Bash(sh *), Bash(mdllm *), Bash(python *), Bash(pwsh *), Bash(powershell *)
---

**Why this is a command.** The standing watch (`mdllm watch`) detects the
other seat's turn and exits 0 on yours; what *rises* on that exit is the
harness's act, and until 2026-10-30 Claude Code had no recorded binding for
it. The loop definitions said "hold the blocking watch inside your turn",
which in Claude Code dies at the tool timeout, so the record shows turns
picked up "through the operator's chat prompt, not an automatic wake". This
command is the binding: the watch runs as a **background** command, which
Claude Code keeps running across turns and re-invokes you on when it exits.
Never run it in the foreground.

Arguments: `$ARGUMENTS` — `<role> <definition> [run]`, this seat's actor
name, the loop definition's id, and optionally the `workflow-run` the
conversation is scoped to.

## Arm

Run the watch **in the background** (the Bash tool's `run_in_background`),
from the workspace root, through the launch route the entry file names:

```
mdllm watch . --role <role> --definition <definition> [--run <run>] --exit-on-wake
```

Before arming, confirm the seat is declared (`mdllm seat .`): the watch
rings a declared seat only for its own unpublished commits, and tells an
undeclared one it cannot narrow whose turn never left. Then tell the operator
in one line what is armed and against which ref, and end your turn. The
watch's startup line (`watching … as [role] … silence means nothing moved`)
is the receipt; `already watching … (pid N)` with exit 3 means another
instance holds this role in this clone — do nothing.

## Rise

When the background command exits, the harness re-invokes you with its
output. Read the exit code before anything else:

| Exit | Meaning | What you do |
|---|---|---|
| `0` | Your turn: a thing moved to a stage this role acts at, or your own turn never left | Take the turn as the loop definition says — read the thing **at the remote head**, do the work, move the token, commit, publish — then **re-arm** with the same command, in the background, before ending the turn |
| `3` | Another instance of this role is already watching | Nothing. The other instance is the watch |
| `1` | A poll failed in `--once` mode | Report the line; re-arm |
| `2` | Refused to arm | Fix the declaration it names; do not retry blindly |

A `not your turn [role]` line means the checkout holds another party's
unpublished commit: say so to the operator and leave it; the watch stays
armed. A `WATCHER BLIND` line is a finding, not quiet: report it.

## What this never does

It never advances a turn, never merges, and never grants authority: a wake
is a doorbell, and the ticket or thing it rang for carries a request, never
an approval. The irreversible still goes to the human seat. Never substitute
a scheduled heartbeat for the watch (`standing-watch.md` → What This
Refuses: the one tried hung once and blocked every run for twenty-three
hours).
