# Changelog

All notable changes to the MarkdownLLM adapter for OpenClaw are recorded here.

## Unreleased

### Added

- Version-bounded OpenClaw 2026.9.3 hook plugin.
- Deterministic MarkdownLLM domain admission and session-start projection.
- Once-per-session-generation lifecycle gate with reset and compaction
  invalidation.
- Exact-session standing-watch bridge with unpublished/diverged-turn recovery.
- Owner-gated `/domain`, `/domain list` and `/domain open` commands that
  verify domain workspaces, reuse or create isolated Telegram topics, and
  persist topic-to-agent routing through OpenClaw's public config API.
- Public fixture, package fitness tests, managed-install smoke test and
  requirement-to-evidence matrix.

### Security

- No shell execution, private OpenClaw imports, direct session-store mutation
  or BookRite dependency.
