---
id: boundary-disclosure-check
type: plan
status: completed
version: 1.0
created: 2026-07-27
priority: high
tags: [floor, boundary, disclosure, regulated, hooks]
linked_things:
  - id: mechanical-coherence-checks-backlog
    relation: complements
    notes: "Same family — a mechanical check replacing an honour-system discipline — but big enough to be its own plan"
  - id: independent-review-2026-07-14-fable
    relation: implements
    notes: "The review's confidentiality-wall finding: regulated deployments hold evidence that must not cross into disclosable surfaces"
  - id: provenance-specification
    relation: extends
    notes: "Quarantine governs what may come IN unverified; the boundary governs what may go OUT at all"
---

# Disclosure-Boundary Check

A repo declares, in a **local, gitignored** file, terms that must never cross
its disclosure boundary — client names, personal names, internal identifiers.
The floor blocks any commit whose staged content or commit message contains
one. Regulated deployments need this mechanically: a QMS domain feeding a
disclosable package cannot rely on authors remembering which vocabulary is
internal, and the framework's own history shows the honour system failing
twice on exactly this surface.

## The invariant

**The public repo ships the capability, never the vocabulary.** Not the
terms, not hashed terms (short-string hashes are dictionary-recoverable — a
hashed denylist *is* the denylist), not match counts in any committed
artifact. Enforcement is local by construction: CI finds no terms file and
no-ops silently. This inverts the floor's usual hardening direction — every
other check gets stronger moving rightward toward CI; this one must never
reach CI at all, because the knowledge it checks against is exactly the
knowledge that must not be published.

## Design

- **`.boundary-terms`** at the repo root, gitignored, one term per line.
  Case-insensitive literal substring match. `#` comments. Optional
  `term ==> replacement` names the approved substitute, so the block message
  teaches the alias at the moment of violation.
- **`mdllm boundary`** — one routine, three surfaces: staged additions +
  staged filenames (pre-commit), the commit message (commit-msg hook — a
  surface the pre-commit floor structurally cannot see; both prior incidents
  lived there), and `--history` for a full-archive audit before any
  publication event. Findings go to the console only, never to a file.
- **Self-guard:** before scanning anything, error if the terms file is
  itself tracked. The mechanism protecting the boundary must not become the
  leak.
- **Hooks:** `install-hook` grows a `commit-msg` hook alongside pre-commit;
  the pre-commit hook runs the boundary check first (fail fast, cheapest
  check, clearest message).
- **Scaffold seeding:** a new domain is born with its own placeholder
  `.boundary-terms` (per-repo boundaries — a domain's disclosure surface is
  its own), and its name is appended to the framework root's terms file:
  private-by-default at birth, deleted from the list only by operator
  decision.
- **No bypass flag.** A false positive is fixed by editing the local terms
  file — operator judgment, recorded nowhere public. Consistent with the
  never-`--no-verify` rule.

## Phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Plan (this thing) | done |
| 2 | `boundary` module + CLI + framework-map | done |
| 3 | commit-msg hook + pre-commit integration | done |
| 4 | Scaffold seeding + template + .gitignore | done |
| 5 | Floor self-tests | done |
| 6 | Close: backlog cross-link, CHANGELOG, version | done |

## Outcome

Shipped as v3.20.0. `mdllm boundary` covers staged additions, staged
filenames, commit messages, and `--history`; `install-hook` writes both
hooks; `scaffold` seeds per-repo terms files and registers the newborn
domain in the framework's own. 9 self-tests (131 total). The commit-msg
surface — where both prior honour-system failures actually lived — is now
mechanically observed. The invariant held in the build itself: no term,
count, or example of real vocabulary appears in any committed artifact,
and the self-guard makes tracking the terms file a blocked commit.
