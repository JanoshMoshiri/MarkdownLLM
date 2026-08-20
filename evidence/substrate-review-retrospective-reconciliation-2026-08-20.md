---
id: substrate-review-retrospective-reconciliation-2026-08-20
type: artifact
status: stable
version: 1.0
created: 2026-08-20
origin: synthesised
exposed: false
tags: [review-response, retrospective-reconciliation, dark-region, semantic-validation, evidence]
linked_things:
  - id: independent-substrate-review-2026-08-20-codex
    relation: derived-from
    notes: "The review whose implementation was retrospectively declared an inflection."
  - id: independent-review-2026-08-11-codex
    relation: references
    notes: "The preceding Codex review supplied the comparison baseline and several still-relevant claim boundaries."
  - id: codex-substrate-review-response-2026-08-20
    relation: documents
    notes: "Records the retrospective semantic pass after the local implementation closeout."
  - id: substrate-review-implementation-evidence-2026-08-20
    relation: extends
    notes: "Adds whole-corpus semantic reconciliation to the implementation and test evidence."
  - id: change-reconciliation-specification
    relation: implements
    notes: "Runs the retrospective Cue, Assimilate, Walk, and Seal beats over the implementation range."
---

# Substrate Review Implementation — Retrospective Reconciliation

## Cue And Frozen Scope

The operator retrospectively declared the 2026-08-20 substrate-review
implementation a consequential inflection. The original response design at
`27b95e739f78cad6fa609cee7b1359897ccf40ae` is the pre-implementation baseline;
the completed local closeout at
`97a4f4149f2af38f7117fd018dfa69b31d53dbd7` is the frozen post-implementation
baseline. `mdllm session-start . --assert-head` accepted that full SHA
immediately before the first reconciliation write.

The range contains five commits, 121 changed paths, 10,906 insertions, and
4,580 deletions. It spans code, specifications, plans, insights, public prose,
templates, examples, evidence, installers, CI, and generated indexes. The
working tree was clean before the pass. Historical reviews, old changelog
entries, and the body of a superseded decision remain historical evidence;
the Walk changes only surfaces that still present themselves as current truth.

## Assimilate — Declared And Literal Reach

The changed root-corpus authorities were inventoried from the Git range, then
read through the live structural-reference registry rather than a hand-kept
field list. Twenty-five changed semantic targets produced **297 declared-edge
observations** and **116 literal-reference observations**. Those figures are
target-wise observations, not deduplicated source counts: one source can
legitimately appear under several changed authorities. The changed
`session-end-continuity` template is outside the root thing scan and was walked
separately through its AGENTS, command-template, Copilot-template, plan, and
insight references.

The initial Walk exposed nine unchanged authorities whose prose still carried
pre-v3.33 concepts. Their own touchpoint expansion added 52 declared and 21
literal target-wise observations:

- `deterministic-calculation`
- `hook-enforcement-has-three-anchors`
- `session-start-loses-to-the-first-request`
- `emitted-content-is-read-instructed-content-is-economised`
- `premature-publish-manufactures-discipline-eroding-urgency`
- `estate-cadence-cluster`
- `cowork-integrity-estate-sweep`
- `cross-domain-readiness-is-a-shared-signal-not-a-producer-push`
- `mcp-domain-server-design`

The mechanical baseline was independently clean before revision: framework and
example validation, coherence, immutable provenance, and relationship/provenance
index checks reported no blocking drift.

## Walk — Whole Corpus And Dark Region

The full root corpus was walked at broad-reading depth (238 thing identities at
the frozen closeout baseline, types, statuses, paths, and body heading
structures), followed by full-body
reads for the changed authorities, every live surface implicated by the review
concepts, and every source that the dark-region pass identified as potentially
current. The two example corpora were handled as separate id-spaces: their
changed AGENTS/skills and compliance examples were read from the Git delta and
retained because they now distinguish policy, mechanism, evidence, and human
legal judgement. Non-corpus surfaces—README, templates, installers, CI, CLI
descriptions, and reference guides—were searched and walked separately.

The conceptual pass used the review's actual seams rather than retired file
names: repository-view currency; exact candidate commits; transaction and hook
authority; publication default-deny; strict YAML and structural-reference
ownership; eval and decimal integrity; workflow/trigger totality; session
emission versus receipt/read/application/outcome; external execution trust;
MCP provenance; adapter capability evidence; supply-chain pins; and template
birth claims.

Three dispositions were applied:

- **consistent** — the implementation, current specification, and dependent
  prose still agree; no edit;
- **revise** — a live/current surface carried a pre-inflection claim; corrected
  below;
- **historical** — the statement is accurate evidence of the former state and
  is explicitly bounded by status, an erratum, or a new current-doctrine note;
  it is not rewritten into fake foresight.

No live contradiction thing was required: every discovered tension was stale
restatement, not two simultaneously defended rules.

## Revisions From The Walk

| Surface | Dark-region finding | Reconciled current truth |
|---|---|---|
| `AGENTS.md` | The Tier-2 catalog still said the agent judges workflow transition legality. | The floor checks membership and declared prior→candidate edges; the agent judges transition merit. |
| `README.md` | Vendor replacement and Obsidian compatibility were stated more strongly than their evidence. | The contract is vendor-neutral while product compatibility is build-specific; Obsidian remains an explicitly unrun compatibility test. |
| `docs/calculation-reference.md` | The guide said YAML destroyed authored decimal scale and `10.00 + 5.50` printed `15.5`. | Strict loading preserves the authored lexeme and scale; the exact result is `15.50`. |
| `deterministic-calculation` | The live plan omitted strict non-evaluation blocking and the v3.33 lexical follow-on. | Default non-evaluation warns, strict mode errors, and the plan records the exact-decimal closure without falsely closing its domain-adoption gate. |
| `hook-enforcement-has-three-anchors` | A promoted insight still called interpretation sufficient for correctness. | Interpretation is the portable probabilistic fallback; receipt, reading, application, and outcome require evidence. |
| `session-start-loses-to-the-first-request` | Session-start was framed as the sole exception to interpretation sufficiency and injection as performing the ritual. | The case falsified the broad claim; machinery delivers content/state while semantic orientation remains invoked judgement. |
| `emitted-content-is-read-instructed-content-is-economised` | It still said the overcoming plan had not been written. | Local hardening is implemented; fresh exact-build behavioural evidence still owns the insight's dismissal condition. |
| `cowork-integrity-estate-sweep` | A completed historical plan still presented timestamp+HEAD attestation as the live fail-safe. | A current-boundary notice records contract fingerprints, integrity-aware delivery, and the five non-promotable assurance states. |
| `estate-cadence-cluster` | The completed plan's default-on ruling could be mistaken for current publication policy. | Its historical body stays intact behind a notice and edge to the superseding literal-true-only decision. |
| `premature-publish-manufactures-discipline-eroding-urgency` | “The agent commits; the operator publishes” excluded standing authority already decided by the human. | The agent never self-authorises; literal standing true or a specific one-shot instruction are the two human authority forms. |
| `cross-domain-readiness-is-a-shared-signal-not-a-producer-push` | Protocol neutrality was promoted into an unearned claim that products read the face identically. | MCP is a vendor-neutral wire contract; each product/build earns discovery, receipt, and application claims separately. |
| `mcp-domain-server-design` | The draft called the MCP process boundary itself the trust boundary and described HEAD-stamped resources. | Transport grants no authority or sandbox; clone-local exact-config trust governs execution, and committed pins name the immutable served bytes while drafts are explicit. |

## Historical Surfaces Deliberately Preserved

- `CHANGELOG.md` continues to say v3.27 was default-on because that is the truth
  of that release, not current guidance.
- `autopush-moves-the-deliberate-act` remains `status: superseded`; its body
  records the decision that actually governed before 2026-08-20.
- Both Codex reviews retain their original open/partial findings. Their value is
  as immutable assessment baselines, not mutable dashboards.
- Older acceptance artifacts retain the exact product/build observations they
  recorded. The v3.33 capability matrix and implementation evidence bound what
  may be promoted from them.

## Dated Provenance Inputs Dispositioned

`mdllm provenance` reported its informational dated-input set and each decision
was read against the newer input rather than treated as mechanically resolved:

| Decision | Walk outcome |
|---|---|
| `autopush-requires-explicit-authority` | **consistent** — completion/compaction of the response plan does not change the operator-approved default-deny design pinned from its original version. |
| `decision-status-vocabulary-domain-owned` | **consistent** — the current schema and specifications still implement domain-owned vocabularies with fixed reserved-type exceptions. |
| `divergence-primitive-promotion` | **consistent** — later edits preserve the constitutional recognition and add no sixth mechanism. |
| `live-eval-scope-bounded-to-claude` | **consistent** — the compacted adapter plan and capability matrix still keep deterministic eval separate from the Claude-scoped live runner. |
| `phase-3-run-domain-task-reverted` | **consistent** — the v3.33 trust clarification strengthens, rather than reopens, the removal of the unsandboxed live-agent surface. |
| `substrate-reconciliation-2026-08-09` | **consistent, historically bounded** — its one-owner/derive-restatements rule governs this pass; its cited default-on publication state is superseded history, not current policy. |

## Seal Boundary And Residuals

This record does not grant publication, external trust, credentials, or release
authority. It also does not convert local tests into live Claude, Codex, Cowork,
hosted-CI, Obsidian, or independent-review evidence. Those remain with the
owners already named in the implementation evidence and completed response
plan.

The revised corpus regenerated both deployed derived indexes; the kernel was
already current. Worktree validation passed for 239 framework things and the
6/14 example corpora with no Errors or Warnings; coherence and provenance
reported information only. The full integrated suite passed **682 tests in
2964.27 seconds** (the sole warning was the restricted workspace refusing
pytest's optional cache write). The remaining seal is the exact-index checks
and installed frozen-index hook at commit time. The containing commit is
intentionally resolved from Git history rather than embedded
self-referentially here.
