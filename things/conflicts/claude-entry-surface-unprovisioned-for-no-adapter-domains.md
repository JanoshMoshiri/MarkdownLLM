---
id: claude-entry-surface-unprovisioned-for-no-adapter-domains
type: conflict
status: open
created: 2026-08-16
session: 2026-08-16
parties:
  - interface-specification
  - vendor-harness-adapter-foundation
confidence: high
origin: stated
linked_things:
  - id: interface-specification
    relation: references
    notes: "Declares the Claude Code route as CLAUDE.md → AGENTS.md with discovery 'Automatic'."
  - id: vendor-harness-adapter-foundation
    relation: references
    notes: "Requirement 3 and the completion criteria assert that removing the adapter leaves AGENTS.md interpretation intact."
  - id: framework-discovery-specification
    relation: references
    notes: "Owns entry-file discovery; it addresses how a domain finds the framework, not how a harness finds the domain's entry file."
  - id: claude-phase6-no-adapter-and-root-2026-08-16
    relation: references
    notes: "The Phase 6 record that surfaced the clash while attempting the Claude disposable no-adapter proof."
---

# Claude's Automatic Entry Surface Is Not Provisioned for Scaffolded Domains

## The Clash

The framework claims that a domain works with no harness adapter, and it
separately claims that Claude Code discovers a domain automatically. For a
scaffolded domain on Claude Code, both cannot currently be true: the file that
carries Claude's automatic discovery is written by no scaffold mode.

## Position A — the adapter is optional hardening

`vendor-harness-adapter-foundation` requirement 3: *"Removing `.claude/` or
`.codex/` must leave AGENTS.md interpretation and the Git floor intact."* Its
completion criteria repeat it: *"the substrate and every domain remain usable
with no harness adapter."* `orchestration.md` makes the same commitment through
the anchor model — `interpretation` is the portable floor, and adapters are
optional `harness-session` hardening that must never be the difference between
working and not.

## Position B — Claude's automatic route runs through a wrapper file

`interface-specification` lists the Claude Code route as *"CLAUDE.md at root
references AGENTS.md"*, discovery **Automatic** — unlike the Codex, Cursor,
Windsurf and Gemini rows, which read `AGENTS.md` directly. README's vendor
setup says the installer writes that `CLAUDE.md` wrapper, and tells a
hand-cloner to add one.

## What the estate actually contains

- `mdllm scaffold` writes `AGENTS.md` and never `CLAUDE.md` — verified by
  creating both a `--harness none` and a `--harness claude` scaffold and
  comparing: neither contains the wrapper.
- Only `install.ps1` / `install.sh` write it, and only at a framework clone
  root. It is optional there and absent on this clone.
- Nine of thirteen live domains have no `CLAUDE.md`; four do.
- On Claude Code 2.1.229 at this framework root, the root `AGENTS.md` was never
  auto-loaded: its prose first entered the harness transcript inside a
  deliberate read ten minutes after SessionStart. The only automatic framework
  state at session start came from the adapter's SessionStart hook.

## Why it matters

For Claude Code specifically, removing the adapter from a scaffolded domain
removes the *only* automatic route the harness had. The interpretation anchor
still works when an agent is told to read `AGENTS.md` — but "told to" is not
what "Automatic" claims, and it is not what the Codex degradation record
proved on its side. This blocks an honest Claude equivalent of the Phase 6
adapter-optionality leg.

## Resolution paths (not yet chosen — operator's call)

1. **Provision the wrapper in scaffold**, in every harness mode including
   `none`, since it is an entry-surface projection rather than adapter
   hardening. Cheapest, and it makes the two positions consistent.
2. **Provision it only in Claude-selecting modes**, and narrow the
   adapter-optionality claim for Claude to "interpretation is available, not
   automatic".
3. **Verify whether the current product reads `AGENTS.md` natively** on other
   builds or surfaces, and if it does, correct `interface.md` and README
   instead of the scaffold.

Option 1 or 3 would close the Phase 6 leg; option 2 narrows the claim rather
than closing it. A scaffold behaviour change is a product decision and belongs
with the operator.
