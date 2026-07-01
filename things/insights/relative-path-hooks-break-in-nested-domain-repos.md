---
id: relative-path-hooks-break-in-nested-domain-repos
type: insight
status: active
version: 1.0
created: 2026-07-01
session: 2026-07-01
source: both
confidence: high
origin: stated
disposition: keep-active
disposition_reason: "Candidate settings-template fix (anchor hook script paths to $env:CLAUDE_PROJECT_DIR in both framework and scaffolded-domain templates). Held active until that template change is made or the pattern recurs."
tags: [hooks, cwd, nested-repo, harness, portability]
linked_things:
  - id: hook-enforcement-has-three-anchors
    relation: references
    notes: A git-fs / harness anchor detail — hook path resolution across nested repos.
---

# Relative-path hooks break when they fire against a nested domain repo

## The Insight

A framework checkout contains domains as **nested git repos**. That nesting creates a
working-directory ambiguity for hooks. When a `PostToolUse` (Write|Edit) hook fires against
a file *inside* a nested domain, the harness runs the hook with cwd set to the nested domain
directory (the nearest project), **not** the framework root. A hook whose command uses a
project-root-relative script path — `python tools/mdllm.py …` — then resolves that path
against the domain directory and fails: `domain/<x>/tools/mdllm.py` does not exist.

The scaffold-generated *domain* settings already dodge this by using `../../tools/mdllm.py`
(correct when the hook runs from the domain). But the *framework's own* `.claude/settings.json`
used a bare relative path and so broke the moment framework-session work touched a domain file.
The robust fix is to anchor the script path to the session project root rather than to cwd:
`python "$env:CLAUDE_PROJECT_DIR/tools/mdllm.py" …`, with an explicit `"shell"`. On Windows,
the powershell `$env:` form avoids the Git-Bash MSYS path-mangling that a bare
`$CLAUDE_PROJECT_DIR` in bash risks.

## Why It Matters

Any framework work done from the framework session that touches a domain file trips this, and
it is invisible until it errors — a silent papercut that erodes trust in the floor. The
general rule: **hook commands in a nested-repo layout must anchor paths to a stable root
(the project-dir env var), never to cwd.** That pattern belongs in the settings templates for
both the framework and scaffolded domains, so the robustness is the default rather than a
per-incident fix.

## Provenance

Hit and fixed 2026-07-01 while authoring the `agent-architect` domain from the framework
session: editing domain files fired the framework's `PostToolUse` validate hook with cwd at
the domain dir, and its relative `tools/mdllm.py` path failed. Diagnosed jointly with the
operator (who correctly read the cwd cause) and fixed by pinning to `$env:CLAUDE_PROJECT_DIR`
under powershell, verified live. `source: both`, `origin: stated`.
