---
id: claude-no-adapter-entry-probe-2026-08-17
type: artifact
status: stable
created: 2026-08-17
tags: [claude-code, windows, phase-6, execution-evidence, adapter-optionality, entry-surface, first-hand]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Closes the Phase 6 Claude no-adapter checkbox first-hand: differential A/B entry proof plus all four floor legs in one fresh out-of-estate probe pair."
  - id: claude-phase6-no-adapter-and-root-2026-08-16
    relation: extends
    notes: "Supplies the interpretation leg that record could not run — its precondition was unprovisioned then, and the CLI could not authenticate; both are resolved here."
  - id: claude-entry-surface-unprovisioned-for-no-adapter-domains
    relation: references
    notes: "The flip-condition observation, now first-hand and differential: pointer present → entry file in context at t=0; pointer removed → no automatic entry surface at all. Disposition stays with the operator."
  - id: claude-domain-entry-pointer-observation-2026-08-17
    relation: complements
    notes: "Same day, other end of the telescope: that record is relayed evidence from an adapter-carrying live domain; this one is first-hand evidence from adapter-less disposable probes."
---

# Claude no-adapter entry probe — 2026-08-17 (first-hand, differential)

**The leg the 2026-08-16 record could not run, run.** Two `--harness none`
domains were scaffolded out of the estate tree, identical except that one had
its entry pointer removed through the floor. The real Claude Code CLI was then
opened in each, same prompt verbatim, no tools permitted. The domain with the
pointer had its `AGENTS.md` in model context before the first tool call; the
domain without it had **nothing** — the product's own words: *"No project
files are in my context."* The pointer, and nothing else, is Claude's
automatic entry surface, and with it provisioned a no-adapter domain has one.

## Tested surface

| Fact | Value |
|---|---|
| Harness | Claude Code CLI **2.1.233**, headless (`-p`), one turn, no tools |
| Platform | Windows 11 Pro 10.0.26200 |
| Framework HEAD | `5ec0a58` (wrapper fix `09200dd` included; scaffolds born v3.31.0) |
| Probe location | `Temp/mdllm-entry/` — outside the framework worktree; ancestry checked free of `CLAUDE.md` up to the drive root; no user-level `~/.claude/CLAUDE.md` exists |
| probe-a (pointer present) | scaffold commit `c4f951c`; `CLAUDE.md` SHA-256 `411ee61d…7a48b85`; `AGENTS.md` SHA-256 `5baeef4e…5cb214` |
| probe-b (pointer removed) | scaffold `3b5f9c0`; removal committed through the floor at `ceeaa4e` |
| Session A | `12637da3-d68e-4236-9aa0-45412fc7fecb`, 17.1 s, 1 turn, no error |
| Session B | `6c3302d5-bf5b-4082-b4d4-f686e7615020`, 7.8 s, 1 turn, no error |
| Absent in both probes throughout | `.claude/`, `.codex/`, `.git/mdllm-harness-attest` — no adapter, and no harness attestation was ever minted |

Both sessions received the identical prompt (list every project file whose
contents are already in context, quoting first headings; state the `name:`
field from `AGENTS.md` or say it is absent — answer from context only, no
tools). `git status` in probe-a was captured before and after its session and
is byte-identical: the session read nothing and wrote nothing.

## The differential

| | probe-a (pointer) | probe-b (no pointer) |
|---|---|---|
| Project files reported in context at t=0 | `CLAUDE.md` (*"# Probe A — harness entry pointer"*) then `AGENTS.md` (*"# Probe A Agent"*, full body) | **none** — *"Nothing from … probe-b has been read into this conversation"* |
| Fallback sentence | correctly declined — content was present | *"AGENTS.md is not in my context."* — verbatim |
| Automatic entry surface | present, via the pointer's `@AGENTS.md` import | absent, by construction |

Probe-b is the executed negative the 2026-08-16 record could only assert
structurally: on this harness, without the wrapper there is no automatic
route in at all. Probe-a is the same scaffold plus one three-line pointer,
and the entry file arrived before any tool ran.

## Floor legs, re-closed first-hand in the same fixture (probe-a)

| Leg | Act | Result |
|---|---|---|
| A | valid thing, commit **before** any ritual | **blocked** — `_session-gate` Error naming the remedy; HEAD unchanged at `c4f951c` |
| B | interpretation-prescribed `session-start`, resolved through the scaffolded `framework_root` (`../../../../../Projects/MarkdownLLM`) | exit 0; Tier-0 contract emitted; `.git/mdllm-attest` written |
| C | same commit again | **passed** — `3a6f175` |
| D | thing omitting `created` | **blocked** — Error names the exact field; HEAD unchanged |
| E | repaired thing | **passed** — `7ddcbd6` |

All four legs of the Codex degradation record now have first-hand Claude
equivalents in a single fixture: automatic entry (the differential above),
strict gate load-bearing before the ritual, valid commit through the floor,
invalid commit blocked.

## A new fact the probe surfaced: frontmatter is not delivered

The injected `AGENTS.md` copy begins at its first heading. Session A reported
this precisely, refused to guess the `name:` value, and reasoned correctly
that frontmatter exists on disk but was not injected. Implication, recorded
rather than acted on: anything the agent must know at t=0 belongs in the
entry file's **body** — frontmatter (`framework_root`, git config,
`framework_version_seen`) reaches the agent only when it reads the file with
a tool, which the Tier-0 ritual has it do anyway. Consistent with the
documented stripping of non-loading content from memory files; not a defect,
but a boundary future entry-surface design should know.

## Limits

- One surface: headless `-p` on CLI 2.1.233/Windows. The interactive desktop
  surface was exercised the same day in the (adapter-carrying) live domain
  sessions of the companion record; the memory-injection mechanism is the
  same documented one, but this record claims only what it ran.
- The sessions are product-dispatched memory injection, not hook dispatch —
  there is no adapter here, which is the point. Harness-owned transcripts for
  both session ids live under the product's project store.
- **Fixtures disposed 2026-08-17 after operator review.** Before deletion both
  repositories were confirmed to have clean worktrees, no remotes, and logs
  matching the hashes quoted above exactly — nothing unrecorded, nothing
  published. The probe commit hashes are therefore **no longer resolvable in
  any repository**, the same convention the Codex and 2026-08-16 Claude
  records follow for their own fixtures. What survives them: this record, and
  the two harness-owned session transcripts (`12637da3`, `6c3302d5`) in the
  product's project store.
- **The conflict was closed on this evidence**, by the operator, the same day:
  `resolution: both-valid` — the entry pointer is core surface rather than
  adapter surface, and once it sits on that side of the line, adapter
  optionality and Claude's wrapper route are both true at once.
