# Claude dispatch probe — live-harness evidence apparatus

<!-- A human-facing README (skipped by `mdllm validate`, like every README.md). -->

Apparatus for Phase 5R.0 of `vendor-harness-adapter-foundation`: establishing
by **real harness dispatch** — never by reading a schema — how Claude Code
launches a hook on a given platform.

It answers, per platform: which shell (if any) executes the command, whether
handlers in one matcher group run in parallel, how argv boundaries survive,
what cwd and project-root environment the hook receives, whether stdin
carries the event payload, and whether the harness-owned transcript can be
correlated with the record.

Committed rather than improvised so both agents rerun the *identical* fixture
on different hosts — the standard the PowerShell 5.1 red fixture set.

## Run it

```
python install.py <scratch-dir> --form shell --handlers 2
cd "<scratch-dir>/probe dir" && claude -p "Reply with exactly: OK"
```

Then read `records/*.json`. Repeat with `--form exec` in a *separate* target
directory to keep records unambiguous.

The model turn may fail (expired CLI auth, no credit) without harming the
evidence — hook dispatch happens before the model call. What matters is that
`records/` fills and the harness transcript names the same `session_id`.

## Reading a record

| Field | Establishes |
|---|---|
| `parent_chain` | the real launcher — `bash.exe` means shell form ran under Git Bash; a bare harness parent means exec form is shell-free |
| `start_epoch` / `end_epoch` | overlap between two handlers = parallel dispatch (the probe holds 3s to make this visible) |
| `argv` | quoting/expansion layers; awkward members in exec form are deliberate |
| `cwd`, `CLAUDE_PROJECT_DIR` | working directory and project-root spelling (forward vs back slash differs by form) |
| `stdin` | event payload incl. `transcript_path` — the correlation key |
| `SHELL`, `MSYSTEM`, `COMSPEC` | environment corroboration for the launcher |

## Discipline

- The probe is **inert**: never invokes the framework, writes only inside its
  own project, always exits 0.
- It proves *dispatch*, not correctness. Running `probe.py` by hand proves
  nothing about the harness — only a real event, correlated with the
  harness's own transcript, is dispatch evidence.
- Records are host-specific and may contain local paths: treat them as
  working material and publish only what a written evidence artifact quotes,
  under this directory's disclosure discipline.
- No host path is committed here; `install.py` computes them at run time.

## Records to date

| Platform | Form | Artifact |
|---|---|---|
| Windows 11 + Git for Windows | shell, 2 handlers | `claude-phase5r0-red-acceptance-2026-08-12` |
| Windows 11 + Git for Windows | exec; no-Git-Bash attempt | `claude-phase5r0-matrix-completion-2026-08-13` |
| POSIX (WSL/Linux/macOS) | shell + exec | *pending — promotes POSIX from designed-for to verified-on per `claude-platform-surface-narrowed`* |
