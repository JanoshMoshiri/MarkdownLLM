---
id: claude-entry-surface-unprovisioned-for-no-adapter-domains
type: conflict
status: resolved
created: 2026-08-16
session: 2026-08-16
resolution: both-valid
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
  - id: claude-no-adapter-entry-probe-2026-08-17
    relation: references
    notes: "The observation that closed it: a first-hand differential probe pair proving the provisioned pointer delivers the entry file at t=0, and that its removal leaves no automatic surface at all."
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

## Chosen path — option 1, decided by the operator 2026-08-16

> "You'd expect any prerequisite files to be generated even if redundant,
> because you don't know what vendor the person's gonna use."

The alternative considered and rejected was detecting the harness and emitting
`CLAUDE.md` *instead of* `AGENTS.md` — rejected because it makes domains
non-interchangeable between harnesses, which is the property the whole entry
surface exists to hold.

**Implemented the same day.** `templates/entry/` now holds the entry pointers
and `scaffold` writes every one of them in every selection, `none` included.
The pointer is core surface, reserved against adapter projection, and carries
no content of its own — it routes to `AGENTS.md` and says so. Which pointers
exist is data in the template directory, never a vendor name in neutral code,
so the architecture fitness gate still passes.

**The estate followed, by explicit instruction.** All thirteen domains now
carry a tracked pointer that imports the entry file. The sweep found that the
four domains which already had one carried prose rather than an import, and
that `eco-essentials` had ignored the file since a session concluded it was
redundant duplication — the same reasoning this conflict overturns. Both were
corrected without discarding operator text.

**Left open deliberately.** The provisioning contradiction is gone, but that
the pointer actually causes the entry file to auto-load has not yet been
observed in a live session — the CLI on this host cannot authenticate. This
conflict flips to resolved when that observation exists, and not before: a fix
believed to work is the thing this framework refuses to call verified.

**2026-08-17 partial observation — the mechanism works at the framework
root.** A live authenticated Claude Code session on this host (this clone,
framework root as workspace) received the checked-in `CLAUDE.md` pointer as
project instructions at t=0, with its `@AGENTS.md` import expanded inline —
the full entry file was in model context before any tool call. That is the
pointer→entry-file auto-load this conflict waits on, observed for the root's
pointer. What remains for the flip is the same observation in a *scaffolded
domain opened directly as its own workspace* — the estate's thirteen pointers
use the same filename and import mechanism, but same-mechanism is an
inference, and the Phase 6 leg exists precisely to replace that inference
with a run.

## Resolution — 2026-08-17, both positions valid

**Closed by the operator on first-hand differential evidence**
(`claude-no-adapter-entry-probe-2026-08-17`). Two `--harness none` scaffolds
outside the estate tree, identical but for the entry pointer, each opened by
the real CLI with the same prompt: the pointer-bearing domain had its
`AGENTS.md` in context before any tool call; the pointer-removed control
reported *"No project files are in my context"*. The flip condition this
conflict declared — that the pointer causing auto-load be **watched**, in a
scaffolded domain opened directly as its own workspace, not inferred from
same-mechanism — is met, and met more strongly than asked: proven by removal
as well as by presence.

**`both-valid`, and the distinction is the resolution.** Neither position was
wrong; they were about different things and the clash was real only while a
provisioning gap made them incompatible in practice.

- Position A — *adapters are optional hardening* — holds. All four floor legs
  ran adapter-free in the probe, and the entry surface survived the adapter's
  absence because it was never adapter-owned.
- Position B — *Claude's automatic route runs through a wrapper file* — holds,
  and is now load-bearing rather than incidental: the control proves the route
  does not exist without it.

What reconciles them is the boundary the finding forced into the open: the
entry pointer is **core surface, not adapter surface**. `templates/entry/`
owns it, every harness selection writes it, no adapter may claim it. Once it
sits on the correct side of that line, "removing the adapter leaves
interpretation intact" and "Claude discovers a domain through a wrapper" are
simply both true.

**What the closure does not cover**, recorded so it is not read wider than it
is: the tested surface is Claude Code CLI 2.1.233 headless on Windows; the
expanded-inherited case at the framework root (an operator approving the
external-import dialog) remains untested by construction, with the corrected
root wrapper written for it; and the frontmatter-delivery boundary the probe
surfaced is carried separately as
`an-injected-file-arrives-without-its-frontmatter`.

## Resolution paths (option 1 chosen; the others recorded as considered)

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
