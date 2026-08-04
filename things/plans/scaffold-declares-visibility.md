---
id: scaffold-declares-visibility
type: plan
status: not-started
version: 1.1
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
- ~~**Externally-audited repos need one too** — a QMS domain may be read by an
  auditor, which is a disclosure surface even though the repo is private.~~
  **Withdrawn same day — the premise was wrong.** See *An auditor is not a
  disclosure surface* below.
- **Private, single-party repos mostly do not** — several domains hold work
  that only ever reaches people already inside the confidence, and there is no
  boundary for a term to cross.

So the file's contents are not a constant: they are a function of who can see
the repo, and nothing at birth has ever captured that.

## An auditor is not a disclosure surface (operator, 2026-08-04)

The triage above originally counted an externally-audited repo as needing a
disclosure vocabulary. The operator withdrew that on the same day, and the
correction is worth more than the claim was:

> **An auditor is an *authorised* reader.** Reviewing a QMS requires exactly
> the identifiers a disclosure list would block — who signed a document, which
> project it belongs to, which legal entity it concerns, which partner or
> third party is involved. Blocking those terms in that repo would be blocking
> the audit.

The boundary governs **unauthorised** eyes. Visibility and authorisation are
different axes, and conflating them produces protection aimed at people who
are entitled to see. The regulated deployment therefore needs **no disclosure
vocabulary today**, and its single-term file is correct rather than a gap.

**What would change it:** the domain begins holding a genuinely different data
class — patient-identifiable data and questionnaire responses are the named
trigger — or it starts feeding a *disclosable package* whose readers are not
the auditor (`boundary-disclosure-check` anticipated that second case). Either
event earns the vocabulary; neither has happened.

## The distinction this surfaced — and why it does not become structure

`.boundary-terms` is doing **two different jobs** under one name, and they have
different scopes:

1. **Disclosure vocabulary** — names, clients, internal identifiers. Genuinely
   visibility-dependent; pointless in a private single-party repo.
2. **Commit hygiene** — the AI-attribution trailer. Wanted in *every* repo
   regardless of visibility, for reasons that have nothing to do with
   disclosure: it is noise in a permanent record.

Conflating them is why the second job went unserved for eleven domains — it was
riding in a file whose whole framing is "declare what must not leak", which
reads as *not applicable* to a private repo.

**The operator ruled against splitting the file (2026-08-04), and the reasoning
holds.** Job 2 has a population of exactly one — the attribution trailer — and
in the estate's whole history no other commit-hygiene term has ever been
wanted: *"everything else has always been disclosure-scoped."* Building a
structural separation for a category with one member is a mechanism where a
ruling suffices, and the framework already knows which of those is cheaper.

So the distinction stays **explanatory, not structural**. It is why the eleven
skips happened; it is not a thing to build. One list stands, and the entire fix
is that scaffold seeds the one line rather than leaving it to be noticed —
which on its own would have prevented every skip.

## What is actually left to build

After both rulings, the substance is small — and that is the finding, not a
disappointment. Most of what this plan started as was answered by reasoning
rather than by code.

**The one certain change.** Scaffold seeds the commit-hygiene block into every
new `.boundary-terms`, unconditionally, no question asked and no visibility
input required. One line in the template. It would have prevented all eleven
skips on its own.

**The parked consideration.** Whether birth should capture the domain's
**visibility** at all — the operator raised it and asked that it not be
forgotten, while noting it is a different session's work. Its value is now
narrower than when this plan opened: only a genuinely public repo clearly needs
a disclosure vocabulary, private repos do not, and audited repos do not either
(authorised readers). Whether that leaves enough for scaffold to ask about is
itself the open question. If visibility is captured, the further question is
whether it belongs in AGENTS.md frontmatter as a declared fact other surfaces
can read, rather than only in a local gitignored file.

**Not to be built:** a file split (ruled against), and a running
inertness sensor (ruled against on 2026-08-04, before either).

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
