---
id: claude-platform-surface-narrowed
type: decision
status: made
created: 2026-08-13
session: 2026-08-13
decided_by: human
confidence: high
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: informs
    notes: "Resolves the Gate 5R.0 open question (complete the POSIX matrix vs narrow the surface): narrow now. 5R.1 is unblocked; the plan's 5R.0 gate text should absorb this scope when its owner next amends it."
  - id: claude-phase5r0-matrix-completion-2026-08-13
    relation: derived-from
    notes: "The evidence that reduced the choice to POSIX-only: exec form observed, no-bash fallback proven unreachable wherever Git for Windows is present, sh-dialect shell form determined as the single portable carrier."
---

# Claude platform surface: verified-on narrows to Windows + Git for Windows

> **Narrowing lifted for Linux, 2026-08-14 — the trigger below fired as
> written.** `posix-live-dispatch-record-2026-08-14` supplies the real POSIX
> dispatch record: native Linux Claude Code, hooks launched under `sh`,
> parallel handlers confirmed, and a full lifecycle on a scaffolded domain
> (ordered session-start, quiet pass, advisory failure, floor commit).
> **Linux is verified-on.** No amendment was required — promotion happened
> by evidence, exactly as this decision specified. macOS remains
> designed-for: reported working in practice by a second operator, but with
> no recorded execution evidence.

The operator resolved the Gate 5R.0 remainder (2026-08-13): do not block
Phase 5R.1 on a POSIX execution record.

**Decision.** The Claude Code *verified-on* surface is **Windows with Git for
Windows present** — the surface the 5R.0 evidence actually executed. POSIX
dispatch remains **designed-for** on the strength of the sh-dialect argument
(identical shell-form bytes run natively on POSIX; Claude self-locates Git
Bash on Windows), not verified-on. The no-Git-Bash PowerShell fallback stays
a named, unverifiable branch outside the supported claim.

**What lifts the narrowing.** A real POSIX dispatch record — the probe
projects are self-contained and reusable — lands as its own evidence
artifact whenever a POSIX host exists (WSL install or a macOS/Linux
machine). Promotion to verified-on happens then, by evidence, not by
amendment.

**Why.** Blocking shared launch-seam repair (5R.1) on an operator system
change (WSL install) buys little: the portable-form determination is already
made from live dispatch, and the seam's sh dialect is the same bytes POSIX
would run. Narrow claims with named residue beat broad claims with silent
assumptions — the same rule that reopened this gate in the first place.
