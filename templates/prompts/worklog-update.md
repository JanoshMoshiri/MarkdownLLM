---
id: worklog-update
type: prompt
status: stable
version: 2.0
created: 2026-05-28
inputs:
  - name: current-date
    description: "Today's date — for confirming the regenerated session heading"
outputs:
  - name: regenerated-worklog
    description: "WORKLOG.md regenerated from the commit stream and committed"
bound_to:
  - hook: session-end
linked_things:
  - id: orchestration-specification
    relation: implements
  - id: session-memory-specification
    relation: complements
---

# Worklog Update

## Purpose

At the end of a session, regenerate `WORKLOG.md` so it reflects the session's
commits. The WORKLOG is a **generated** artifact — `mdllm worklog` derives it
from the commit stream (sessions delimited by `session-end:` commits; full
detail lives in `git log`). It is never hand-edited. This prompt is the
session-end reminder to regenerate it, not an instruction to author it.

The WORKLOG records what happened, not what's still live — the continuity brief
(`session-end-continuity`) carries forward state; this is the retrospective
index over the commit history.

## Reasoning Template

### 1. Commit The Session's Work First

The WORKLOG is generated *from commits*, so anything not yet committed will not
appear in it. Ensure the session's work is committed following
`git-workflow.md` conventions — including a `session-end:` commit if this is the
end of a working session (that is the delimiter `mdllm worklog` splits sessions
on).

### 2. Regenerate

Run the floor:

```sh
mdllm worklog --write
```

This rewrites `WORKLOG.md` in place from `HEAD`. The system name and id are read
from the local `AGENTS.md`, so the same command is correct in the framework and
in any domain repo.

### 3. Commit The Regenerated WORKLOG

Commit the regenerated `WORKLOG.md`. (Because it is derived, a future floor
check may treat a stale WORKLOG as drift the way `kernel --check` and
`index check` do — until then, regenerating it here is what keeps it honest.)

## What Not To Do

- **Do not hand-edit `WORKLOG.md`.** The narrative detail belongs in the commit
  messages it is generated from. If an entry reads poorly, fix the commit
  message convention, not the generated file.
- **Do not duplicate the continuity brief.** Live state is the continuity
  brief's job; this is history.
