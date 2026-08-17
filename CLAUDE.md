---
name: MarkdownLLM
description: Definition-driven framework — agents reason within domains you define
---

# MarkdownLLM — Claude Code Instructions

This is the **framework root's** entry pointer. It is read from two
positions, and it routes each differently:

- **Your workspace is this directory** → the framework's entry file is
  imported below and governs the session.
- **This file arrived inherited from a parent directory** — your workspace
  is a domain nested under this framework → your workspace's own
  `CLAUDE.md` → `AGENTS.md` governs. Do not read or follow the framework
  root's `AGENTS.md`, whether or not the import below expanded: it is the
  framework repo's entry file, not your domain's.

@AGENTS.md
