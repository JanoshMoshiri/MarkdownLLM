---
id: cue-public-docs-face-build-2026-09-24
type: cue
status: answered
version: 1.0
created: 2026-09-24
subject: public-docs-face-build
raised_at: 446155b8936ef32de98af6d713d77a8700f4b4a2
raised_by: "floor — mdllm cues --raise"
verdict: inflection
verdict_reason: "Phases 1-3 changed how the public docs are kept and where they live: toolbox generated and map views gated, the site switched on, and the selector ruled link-out; each walked in its own commit."
informed_by:
  - id: public-docs-face-is-derived-not-restated
    commit: 35aae16b2c185b6aa2d63c20d8eabae8d9432f28
  - id: public-face-links-out-not-hosts-2026-09-22
    commit: dc66a7dafcc7a475c60474fcdea852bbe220f3c6
tags: [cue, raised-mechanically]
---

# Cue: `public-docs-face-build` was modified — inflection?

## The Change
Raised by the floor on 2026-09-24: `public-docs-face-build` is reasoned-from (3 inbound edge(s)) and
was modified in 7 commit(s) since the baseline 2026-09-13 — latest
2026-09-22 (`446155b`) — with no cue covering the change. `mdllm touchpoints
public-docs-face-build` lists what depends on it; `git log -p 446155b` shows what moved.
The raise is mechanical (`inflection-candidates-are-computable`); the
verdict never is (`unattended-cue-carrier-2026-09-12`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
**Inflection.** Seven modifications, one arc. Phase 1 (`fda4fa8`, `f29c96e`) changed the maintenance rule of the two surfaces it touched — the toolbox generated, the map's views gated — and was walked in its own commit: two cues answered `inflection` on the guide and the map, and `AGENTS.md`'s residue sentence rewritten. Phase 2 (`632cd4c`, `e4a1358`, `cdcdb36`, `446155b`) put the face on the internet, and its renderer defects were fixed in the shape the drift gate keeps. Phase 3 (`dc66a7d`) settled the selector as link-out, on the operator's ruling; the README was walked in the same commit. What remains is Phase 4, the human digest, which is a decision and not a walk.

*Answered by citation under `framework-agent-closes-settled-cues-2026-09-13`; the operator may overturn it by editing the verdict.*
