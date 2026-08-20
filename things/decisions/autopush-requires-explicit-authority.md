---
id: autopush-requires-explicit-authority
type: decision
status: made
created: 2026-08-20
session: 2026-08-20
decided_by: human
confidence: high
informed_by:
  - id: independent-substrate-review-2026-08-20-codex
    commit: 27b95e739f78cad6fa609cee7b1359897ccf40ae
  - id: codex-substrate-review-response-2026-08-20
    commit: 27b95e739f78cad6fa609cee7b1359897ccf40ae
linked_things:
  - id: autopush-moves-the-deliberate-act
    relation: supersedes
    notes: "Keeps declaration-level automation but reverses the unsafe default: silence and malformed policy grant no send authority."
  - id: git-workflow-specification
    relation: informs
  - id: orchestration-specification
    relation: informs
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
---

# Decision: autopush requires explicit authority

## Context

The prior rule moved publication authority from each push into repository
configuration, but made a missing or malformed declaration mean “publish.” The
independent substrate review identified that as fail-open authorization for a
send: an agent, parser failure, old domain, or partial scaffold could acquire
publication authority without anyone affirmatively granting it.

The operator accepted the review as requirements and the response plan as the
design on 2026-08-20. The plan explicitly stated that this acceptance decides
the open policy question in favour of default deny.

## Options

- Keep default-on and rely on repositories to opt out.
- Require literal `git.autopush: true`, with every other state off.
- Remove standing automation and require a human instruction for every push.

## Decision

Keep standing, declaration-level automation, but require affirmative authority.
Only the YAML boolean `true` at `git.autopush` enables the post-commit send.
False, absence, malformed YAML, non-boolean values, and unreadable policy are
off. `doctor` explains the effective state. A human may still authorize an
individual push explicitly where standing authority is off.

This supersedes only the default direction of
`autopush-moves-the-deliberate-act`; it preserves that decision’s useful move
from repetitive ceremony to configuration and preserves its no-force,
bounded, divergence-reporting mechanics.

## Consequences

- New domains must declare their publication choice; scaffolded domains that
  choose estate publication carry literal `true`.
- Existing domains with no declaration stop publishing until deliberately
  migrated.
- Parse failure is safe: it can create publication debt, never an accidental
  send.
- The framework root remains explicitly false and this remediation is not
  published automatically.
