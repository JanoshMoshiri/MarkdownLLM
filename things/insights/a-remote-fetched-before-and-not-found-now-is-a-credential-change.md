---
id: a-remote-fetched-before-and-not-found-now-is-a-credential-change
type: insight
status: active
version: 1.0
created: 2026-09-12
session: 2026-09-12
source: both
confidence: high
origin: inferred
disposition: keep-active
disposition_reason: "A diagnostic heuristic awaiting its mechanism: estate-sync's `undiagnosed` bucket could name the credential case by checking whether the remote-tracking ref already exists. Promoted when that check lands; dismissed if a 'not found' on a previously-fetched remote turns out to have another common cause in practice."
tags: [estate-sync, git, credentials, diagnostics, multi-account, machine-axis]
linked_things:
  - id: git-workflow-specification
    relation: informs
    notes: "The Machine Axis: estate-sync degrades to 'fetch-failed — undiagnosed' on this case; the diagnosis is available from state git already holds."
  - id: a-check-run-where-it-cannot-see-mints-a-false-finding
    relation: supports
    notes: "Same family — the tool reports absence when what it observed was invisibility."
---

# A remote that was fetched before and is "not found" now is a credential change, not a missing repository

## The Insight

A Git host answers a request for a private repository the presented
credential cannot see with **"Repository not found"** — the same words it
uses for a repository that does not exist. On a machine with more than one
account, a change of the *active* credential therefore makes every private
remote owned by the other account vanish, all at once, in a way that reads
as eleven repositories having been deleted. The distinguishing fact is
already on disk: a remote-tracking ref (`refs/remotes/origin/main`) exists
only because a fetch once succeeded. **"Not found" on a remote that has a
tracking ref is a credential change until proven otherwise.**

## Why It Matters

- `mdllm estate-sync` reports this case as `fetch-failed — undiagnosed
  (remote: Repository not found.) — orienting from last-fetched state`, and
  it said so for eleven of fifteen repositories on 2026-09-12. The report
  was true and the diagnosis was one `git rev-parse origin/main` away. A
  bucket named *undiagnosed* that could diagnose is the shape
  `a-check-run-where-it-cannot-see-mints-a-false-finding` warns about,
  one step milder: it does not mint a false finding, it withholds a true
  one.
- The cost is real on a multi-account machine: the estate's remotes all
  lived under one account while the default active account was the other,
  so every unattended sync would have reported the same eleven failures
  indefinitely, and an operator reading "not found" reaches for
  re-authentication or worse before reaching for `gh auth status`.
- It generalises past GitHub: any host that conflates *absent* and
  *invisible* in one message needs the client to keep the distinction,
  and the client can, from what it already fetched.

## Context

The operator asked for a fetch-and-pull because "we're not in line with
head." The framework root was fine (ahead, not behind); eleven domain
remotes failed with "Repository not found." All were reachable the moment
the other logged-in account was made active. The operator then ruled that
account the standing default. The session's own memory holds the machine
specifics; this insight holds the diagnostic.
