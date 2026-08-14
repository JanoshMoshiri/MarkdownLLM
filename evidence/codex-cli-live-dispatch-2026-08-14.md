---
id: codex-cli-live-dispatch-2026-08-14
type: artifact
status: stable
created: 2026-08-14
tags: [codex, codex-cli, windows, phase-6, execution-evidence, git-floor]
---

# Codex CLI Live Dispatch — 2026-08-14

**Verified on the stated Windows Codex CLI surface.** This is a live,
automatically dispatched probe, not a direct `harness-event` invocation.

## Tested surface

| Fact | Observed value |
|---|---|
| Harness | Codex CLI 0.147.0 (`exec` session) |
| Platform | Microsoft Windows 11 Pro 10.0.26200 (build 26200) |
| Repository HEAD at session start | `5a76fb1632bbd93e6cc39d0b18d3f63635887f56` |
| Project configuration | `.codex/hooks.json` SHA-256 `a68be54142e7acbe9d268ef8895baab25cda0b3cef800870c4e8258186b66461` |
| Trust path | Normal CLI hook-trust policy; no `--dangerously-bypass-hook-trust` was supplied |

## Automatic dispatch evidence

The CLI session started with the trusted project layer and created the
hash-bound SessionStart attestation at `2026-08-14T19:40:41.666820+00:00`:

```text
harness=codex
capability=session-start
source=codex-project-hook
outcome=passed
detail=estate-sync=0, session-start=0
definition_hash=sha256:758054d6fae6f79165d9f4f09a156c4f76f3410b53b0408121f9e9bf20fa95fb
```

For the PostToolUse probe, the first `apply_patch` deliberately created this
artifact without `created`. Codex CLI then injected the hook output into the
agent turn:

```text
[steps: validate=1]
[validate: exit 1]
- codex-cli-live-dispatch-2026-08-14: missing required field `created`
```

The matching Codex project-hook attestation was automatic and contemporaneous
(`2026-08-14T19:41:39.533532+00:00`), with `outcome=failed` and
`detail=validate=1`. The failed outcome is the expected controlled invalid
write result; it demonstrates delivery of advisory validation feedback rather
than a configuration-only claim.

## Repair and Git floor

The repair itself automatically produced a passing PostToolUse attestation at
`2026-08-14T19:43:09.274000+00:00`: `source=codex-project-hook`,
`outcome=passed`, and `detail=validate=0`, bound to
`sha256:c55c7ef73426b01c59599f9c1fde850dc61a8ac31399c5cc1907e6cb05307cdc`.
Ordinary framework validation then passed with no errors or warnings. The
ordinary Git commit that follows establishes the Git-floor half. No plan,
existing tracked file, or lifecycle hook was changed, and no lifecycle command
was run manually.

## Scope

This verifies Codex CLI on this Windows framework-root surface only. It does
not claim the nested-domain, Desktop, POSIX, `resume`, `clear`, or `compact`
surfaces.
