---
id: an-injected-file-arrives-without-its-frontmatter
type: insight
status: active
session: 2026-08-17
created: 2026-08-17
tags: [entry-surface, harness, context-loading, claude-code, frontmatter]
confidence: high
origin: stated
linked_things:
  - id: claude-no-adapter-entry-probe-2026-08-17
    relation: derived-from
    notes: "The probe that surfaced it: the session reported the injected AGENTS.md beginning at its first heading, and refused to state a frontmatter field it could not see."
  - id: interface-specification
    relation: informs
    notes: "The entry route delivers a body, not a file. Anything the I/O layer expects an agent to know before its first tool call must live in prose."
  - id: framework-discovery-specification
    relation: informs
    notes: "framework_root is frontmatter, so it reaches the agent by reading — not by arriving. Discovery survives because the Tier-0 ritual reads the file anyway."
---

# An Injected File Arrives Without Its Frontmatter

A harness that auto-loads an entry file delivers its **body**. The YAML
frontmatter is stripped on the way in. Observed 2026-08-17 on Claude Code
2.1.233: a scaffolded domain's `AGENTS.md`, reaching the session through its
`CLAUDE.md` pointer, began at `# … Agent` — the session could quote the
heading, could not state the `name:` value, and correctly declined to guess
it, reasoning that the frontmatter existed on disk but had not been injected.

This is not a defect and nothing here needs repairing. It is a boundary
between two things the framework has been treating as one: *what the agent is
handed* and *what the file contains*. Injection hands over prose. Reading
hands over the file.

**Why it currently costs nothing.** Every frontmatter field the framework
relies on early — `framework_root`, `git.autocommit`, `framework_version_seen`
— is consumed by machinery that reads the file with a tool, or by the Tier-0
ritual which opens it regardless. The probe's own floor legs resolved
`framework_root` correctly precisely because the interpretation path *reads*.
So the gap is real and presently harmless.

**Where it would bite.** Any future design that expects an instruction to be
*in force at t=0* by putting it in frontmatter — a flag that suppresses a
behaviour, a declared mode, a routing rule expressed as a field. That
instruction would be silently absent in exactly the sessions it was written
for, and absent in the way this framework finds hardest to see: the file
looks correct on disk, validates clean, and the failure appears only as
behaviour that never happened. Compare
[[a-missing-contract-degrades-to-semantic-drift-not-breakage]] — same shape,
different cause.

**The rule that follows:** anything the agent must know *before its first tool
call* belongs in the entry file's body. Frontmatter is for the floor and for
readers, not for the arriving session.

There is a second-order point worth keeping. The pointer's value was never
that it carries content — it deliberately carries none
([[the-cheapest-fix-is-the-one-that-adds-no-mechanism]]) — but that it causes
a body to arrive. A pointer routes; a body instructs; frontmatter configures.
Three roles that look like one file until a harness separates them for you.
