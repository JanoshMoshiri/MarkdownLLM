---
id: scaffold-declares-visibility
type: plan
status: not-started
version: 1.0
created: 2026-08-04
priority: medium
tags: [scaffold, boundary, disclosure, birth, visibility, floor]
linked_things:
  - id: boundary-disclosure-check
    relation: extends
    notes: "That plan built the check and shipped it into every domain. This one addresses what it could not: the check is armed by a LOCAL file the scaffold ships empty, so eleven domains ran an installed, inert control for weeks."
  - id: agents-drop-mechanical-birth-steps-not-semantic-ones
    relation: informs
    notes: "The same class again. Filling the terms file is a semantic step left to the operator at birth, and eleven of thirteen births skipped it — not through carelessness, but because nothing at birth asked."
  - id: hook-enforcement-has-three-anchors
    relation: references
    notes: "The precise diagnosis: the git-fs anchor was installed everywhere and starved of input everywhere, so enforcement silently degraded to the interpretation anchor — which is exactly as skippable as no hook at all."
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: references
    notes: "Eleven of thirteen domains is well past the second occurrence. The promotion the operator ruled for is at BIRTH, not as a running sensor — see The Ruling below."
---

# Scaffold Takes Visibility Into Account At Birth

## The finding (2026-08-04)

An AI-attribution trailer kept reaching commit messages across the estate
despite a standing rule against it and a commit-msg hook installed in all
thirteen domains. The cause was not the framework version and not old commits:

**Eleven of thirteen domains had a `.boundary-terms` containing zero active
terms** — the scaffold's comment-only stub, never filled in. The stub says so
in its own text (*"Empty = the boundary check no-ops"*), so every one of those
domains ran a fully installed, entirely inert disclosure boundary.

The evidence is an unusually clean natural experiment:

| Repo | Term loaded | Last trailer | Still committing |
|---|---|---|---|
| `code-architect` | yes | 2026-06-30 | yes, weeks after |
| the regulated deployment | yes | 2026-07-10 | yes, weeks after |
| an overview domain | **no** | **2026-08-04** | that same day |
| framework root | yes | never — 0 of 406 | — |

Where the vocabulary is loaded the trailer stops dead and stays stopped. Where
it is absent it continued to the day of the finding. Estate-wide: 122 of 502
commits carry it, and the only repo with a populated file has none.

## The ruling (operator, 2026-08-04)

**No running sensor.** A "boundary installed but inert" check was offered and
declined. An empty terms file is a legitimate state for a domain with nothing
to protect, so the check would be Info-level noise across most of the estate —
and the framework already knows what a check that fires on healthy state does
to an operator's attention.

**Birth is the right place.** The gap is not that inertness goes undetected
later; it is that nothing at birth ever asks what this domain's boundary
is. A question asked once, at scaffold time, replaces a sensor that would ask
forever.

**Visibility is the missing input.** The operator's own triage, recorded
because it is the design input this plan needs:

- **Public repos genuinely need a disclosure vocabulary** — the framework root
  is public, and it is the one repo where the boundary is load-bearing.
- **Externally-audited repos need one too** — a QMS domain may be read by an
  auditor, which is a disclosure surface even though the repo is private.
- **Private, single-party repos mostly do not** — several domains hold work
  that only ever reaches people already inside the confidence, and there is no
  boundary for a term to cross.

So the file's contents are not a constant: they are a function of who can see
the repo, and nothing at birth has ever captured that.

## The distinction this surfaced

`.boundary-terms` is currently doing **two different jobs** under one name, and
they have different scopes:

1. **Disclosure vocabulary** — names, clients, internal identifiers. Genuinely
   visibility-dependent; pointless in a private single-party repo.
2. **Commit hygiene** — the AI-attribution trailer. Wanted in *every* repo
   regardless of visibility, for reasons that have nothing to do with
   disclosure: it is noise in a permanent record.

Conflating them is why the second job went unserved for eleven domains — it was
riding in a file whose whole framing is "declare what must not leak", which
reads as *not applicable* to a private repo. Whether these should separate (a
scaffold-seeded universal block plus an operator-authored disclosure section)
is the first design question this plan has to answer.

## Sketch (not a design — that is this plan's work)

- Scaffold asks, or accepts as an argument, the new domain's **visibility**
  (public / externally-audited / private).
- The generated `.boundary-terms` is seeded accordingly: the universal commit-
  hygiene block always, plus a prompt for disclosure vocabulary when visibility
  implies one — rather than a stub that reads the same in every case.
- Consider whether visibility belongs in the domain's AGENTS.md frontmatter as
  a declared fact other surfaces can read, rather than living only in a local
  gitignored file.
- Consider what `doctor` should say at first run in a domain whose visibility
  implies a vocabulary that is still empty — a birth-adjacent probe the
  operator opts into, not a standing estate sensor.

## Interim state

The eleven stub files were given the commit-hygiene block by hand on
2026-08-04 and execution-tested: a trailer-bearing message is now blocked in
each, and a clean message still passes. That closes the immediate annoyance and
deliberately does **not** close this plan — a hand-applied fix across eleven
local files is precisely the birth-time gap restated, and the next domain
scaffolded will be born with the same empty stub.

**Known consequence, accepted:** `mdllm boundary --history` will now report
historical trailer commits in those repos (47 in one domain alone) and stay red
there. That is the same trap the framework root's own terms file documents from
2026-07-28. The staged and commit-message paths — the ones that block — are
unaffected; only the on-demand full-archive audit is noisy, and only about
history that cannot be changed without rewriting published commits.
