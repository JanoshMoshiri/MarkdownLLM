---
id: independent-substrate-review-2026-08-20-codex
type: artifact
status: stable
version: 1.0
created: 2026-08-20
origin: synthesised
exposed: false
tags: [independent-review, codex, agent-system, architecture, adapters, transaction-integrity, specification-adherence, full-corpus]
linked_things:
  - id: independent-review-2026-08-11-codex
    relation: extends
    notes: "Re-tests the fifteen findings from the previous Codex review after 109 commits and records the new adapter, evidence, and session-adherence surfaces."
  - id: codex-substrate-review-response-2026-08-20
    relation: informs
    notes: "The response plan dispositions and sequences this review; the review remains the immutable test oracle for the later Claude assessment."
  - id: llm-driven-systems-manifesto
    relation: challenges
    notes: "Tests the manifesto's determinism, auditability, universality, self-hosting, prompt, truth, and consequence claims against the complete live substrate."
  - id: hook-enforcement-has-three-anchors
    relation: supports
    notes: "The index/worktree mismatch and adapter evidence independently confirm that an anchor names where a control can fire, not whether it guarded the intended bytes."
  - id: session-start-hardening
    relation: informs
    notes: "The adherence findings distinguish contract emission, receipt, reading, compliance, and outcome evidence; the four post-cutoff phases are reconciled in the addendum."
  - id: vendor-harness-adapter-foundation
    relation: informs
    notes: "Reviews the shared adapter ports, Claude Code and Codex projections, installer transaction, evidence gates, and remaining plan-shape debt."
  - id: cowork-adapter
    relation: informs
    notes: "Reviews the third adapter's assembly path, remote evidence, lifecycle parity, and acceptance boundary."
---

# Independent Agent-Substrate Review — Codex, 2026-08-20

## Commission And Disposition

The operator commissioned a full follow-on review of MarkdownLLM as an agent
system: every tracked file, the domain model and birth/management mechanisms,
the deterministic floor, the three harness adapters, the recent evidence and
tests, clean architecture and SOLID, specification adherence, and the manifesto.
The comparison point is `independent-review-2026-08-11-codex`.

This is a **stable point-in-time assessment**, not an accepted implementation
decision. `codex-substrate-review-response-2026-08-20` is the mutable response
plan. Keeping those roles separate gives the requested later Claude review a
fixed oracle: it can assess the implementation against this record without the
record changing to agree with the implementation.

Exposure decision: **no**. This is framework-estate review state; no downstream
domain should rest on it as served knowledge. A public release note may later
derive a deliberately smaller account from the completed work.

## Scope And Method

The review first froze and read the clean snapshot at `c86363382b1a66f7be7697410e5b1826c0ab1930`,
then reconciled every committed delta through
`43679e536f4d04351b5051a5cbc72ea9d73682ec` before capture.

- 481 tracked files at the reconciled cutoff
- 66,699 readable lines
- specifications, manifesto, guides, entry surfaces, prompts, templates,
  things, indexes, examples, reviews, plans, insights, evidence, eval fixtures
  and results, Python, PowerShell, shell, Git hooks, CI, packaging, and tests
- every textual file read end-to-end; the post-review delta inspected as both
  commits and final bytes
- history comparison from the previous review capture at `d7e9c2c`: 109
  commits, 171 files changed, 20,584 insertions, 1,138 deletions
- mechanical baseline at the reconciled cutoff: 232 framework things, 0
  Errors, 0 Warnings, 1 Info; both example corpora clean; coherence clean apart
  from four status-recency Infos; relationships and provenance indexes in sync
- current test baseline: 526 tests passed. The full run passed 523 and produced
  three failures solely because its temporary Git fixtures were placed beneath
  the real framework repository; those exact three passed when rerun in a true
  external temporary directory. The distinction and commands belong in the
  response plan's Phase 0 evidence rather than being silently called green.

One reconciliation commit (`a9028f8`) landed after the review cutoff and before
capture. It re-walked the dark region of session-start Phases 1–4, corrected two
stable-spec residues, and added a Phase 5 tripwire. It strengthens the adherence
work described below and does not close or invalidate a review finding.

The review deliberately separates four facts that agent systems often blur:

1. a specification exists;
2. the specification was delivered;
3. the model read and applied it;
4. the resulting state or outcome complies.

Evidence of one is not promoted into evidence of the next.

## Executive Assessment

MarkdownLLM is now a credible, self-describing agent substrate with an unusually
good conceptual core, readable implementation, strong correction culture, and
real multi-harness evidence. The three-layer domain model, mechanical/semantic
division, Git-backed state, tiered loading, thing graph, provenance, quarantine,
and adapter ports belong together. I would keep that architecture.

The limiting seam is no longer the absence of agent-system concepts. It is
**transaction integrity**: several deterministic claims are evaluated against
bytes adjacent to, but not identical with, the bytes being committed, served,
executed, or attested. Horizontally, the system has become sophisticated across
Claude Code, Codex, and Cowork. Vertically, the path from specification to exact
state transition is still uneven.

The shortest accurate description remains:

> A deterministic state and validation substrate around probabilistic
> reasoning — with the transaction boundary not yet consistently pinned to one
> immutable repository view.

That is a strong proposition. It is also narrower than several surviving public
claims.

## What Has Materially Improved Since The 2026-08-11 Review

### 1. The adapter layer is now real architecture

The old review encountered an in-flight extraction. The current substrate has
accepted ports, registry-driven projections, pure render/inspect separation,
runtime resolution shared across harnesses, transactional preflight/apply for
project adapter installation, diagnostic facts that avoid promoting presence
into operation, and evidence gates that distinguish designed-for from verified.

This is clean-architecture progress, not just vendor support. The domain core no
longer needs to know Claude or Codex configuration shapes. The installer is also
the best transaction design currently in the repository and should be reused as
the pattern for scaffold and hook installation.

### 2. Specification-adherence work has found the right problem

The recent five-run, multi-model evidence rejected the comforting assumption
that instructions are read because they are present. `session-start-hardening`
correctly moved toward emission, integrity marks, a receipt file for truncated
channels, mechanically computed orientation signals, and an explicitly invoked
judgement residue.

The four commits after the initial review cutoff improve this further:

- the read prerequisite moved upstream into the operative kernel;
- direct session-start channels emit the kernel with an integrity trailer;
- budgeted lifecycle channels defer loudly with line count and digest;
- velocity trend, stall lines, and self-answering trigger cues became computed;
- the deep orientation residue became an invoked bound prompt;
- the Tier-0 obligation was removed from the economy rule agents had used to
  excuse skipping it.

This is exactly the right empirical posture: observe omission, change delivery,
then re-test. It does **not** yet prove that received text was read or followed;
the plan should preserve that boundary rather than invent a compliance token.

### 3. Evidence discipline is now one of the substrate's strengths

The estate keeps failures, partial results, model/build attribution, seat-swapped
reviews, real shell probes, and narrowed claims. The Cowork remote leg was graded
PARTIAL rather than rhetorically upgraded. Codex approval and permission
behaviour was tested in the actual managed shell. The system revises its own
claims when a stronger probe disagrees.

### 4. Domain creation is richer and safer in several dimensions

Scaffolds now create isolated repositories, schema, entry pointers, selected
adapter projections, runtime-resolving hooks, a strict session gate, private
boundary terms, and a first validated commit. Domain refresh, estate sync,
publication debt, import quarantine, and derived indexes form a coherent
management story. These are substantial improvements over a template copier.

### 5. The deterministic floor has broadened without swallowing judgement

Field registration, terminal-status ownership, quarantine flips, calculation
checks, relationship/provenance indexes, cue candidates, estate freshness, and
orientation signals generally respect the mechanical-versus-semantic boundary.
The framework has often resisted turning semantic residue into noisy pseudo-
determinism. That restraint should remain.

## Finding Disposition Against The Previous Review

| Previous finding | Current disposition | Assessment |
|---|---|---|
| 1. Pre-commit validates worktree, not index | **Open — critical** | The hook still invokes filesystem scanning. The candidate bytes Git will commit are not the validation source. |
| 2. No consistent read snapshot | **Open — high** | Long reads and most commands still scan mutable paths; no repository-view port or base-commit concurrency check exists. |
| 3. Autopush fails open | **Open — high, now doctrinally explicit** | Missing/malformed config still means publish. This is no longer accidental prose drift; it is a deliberate estate-cadence rule that conflicts with the consequence principle and therefore needs an explicit operator decision to reverse. |
| 4. Scaffold/hook installation not transactional | **Open — high** | Adapter installation now supplies a good transaction pattern, but legacy hook installation still overwrites hooks and scaffold can commit unrelated staged outer state. |
| 5. MCP provenance can stamp the wrong bytes | **Open — high** | MCP still scans live things and attaches a path-derived commit; dirty content can carry a provenance claim it did not come from. |
| 6. Structural graph lists drift | **Open — high** | `CORE_FIELDS`, validators, indexes, touchpoints, egress, candidates, and trigger checks still encode overlapping reference knowledge separately. |
| 7. Duplicate YAML keys accepted | **Open — high** | Multiple `yaml.safe_load` call sites remain; duplicate keys can still collapse silently. |
| 8. Eval can succeed on failed evidence | **Open — high** | Scan findings, full validation, process return, agent error semantics, final exit status, provenance pins, and run-id uniqueness remain incomplete. |
| 9. Calculation strictness loopholes | **Open — high in financial domains** | Float lexemes can lose precision before Decimal conversion; strict non-evaluability remains a Warning; excluded inputs are not always loud. |
| 10. Workflow transition legality agent-owned | **Open — medium-high** | Stage membership is enforced; machine-readable old→new transition legality is still intentionally left to Layer 2. |
| 11. Trigger evaluation partial/unsafe | **Partly improved — medium-high** | Silent branches are fewer and history cues improved, but malformed stale thresholds can still raise, absent subtasks can still be ignored, and evaluation is not a total typed result. |
| 12. Session attestation SHA unused | **Partly improved — high semantics** | Kernel outcome tokens and integrity facts were added. Freshness still cannot establish receipt, reading, compliance, or whether the relevant contract changed without a content-level comparison. |
| 13. External integration trust boundary | **Open — now critical** | The automatic session-start/trigger path can reach imports freshness, which can execute repository-declared MCP commands or send configured HTTP headers. Reachability increased faster than the trust boundary. |
| 14. Birth-surface defects/overclaims | **Partly improved — medium** | Many concrete template issues were repaired, but templates are not yet validated by instantiation as a first-class corpus and examples still need policy/enforcement/evidence distinctions. |
| 15. Supply-chain hardening | **Open — medium-high** | Moving-branch pipe installers, unpinned dependencies/action references, and executable hook installation remain below the framework's stated trust ambition. |

The important comparison is not “fifteen old bugs still exist.” Several have
been narrowed, and the adapter work created reusable repair patterns. The
important comparison is that the **same five seams** still explain almost all
open findings: repository state view, authority/transaction, canonical
definition, evidence semantics, and claim vocabulary.

## New And Newly-Severe Findings

### A. Critical: automatic orientation can cross a repository-supplied execution boundary

`session._fired_by_thing` evaluates triggers. Import triggers call
`imports_check`, which reads `.mcp.json`. A stdio entry executes its configured
`command` and arguments; an HTTP entry can contact an arbitrary HTTP(S) URL,
send configured headers, and read an unbounded body. This means an apparently
read-only session-start path can execute repository-selected code or disclose
configured credentials before the operator has trusted that repository state.

The fix is a local, uncommittable trust decision pinned to the exact server
configuration hash, default deny on automatic paths, explicit network/command
authorization, bounded response reads, redaction, and protocol-correct MCP
initialisation. “The operator wired `.mcp.json` once” is not enough when the file
itself can change in Git.

### B. High: contract assurance currently conflates five states

The new emission work is valuable, but the vocabulary must remain exact:

| State | What can establish it |
|---|---|
| Emitted | producer-side execution record |
| Received whole | channel integrity marker or full receipt bytes |
| Read | behavioural probe or explicit model action; never inferred from receipt |
| Applied | evidence in the resulting reasoning/state change |
| Outcome compliant | independent validation against the specification |

A timestamp plus kernel digest proves neither reading nor adherence. The system
should store these as different evidence classes and resist a single
“session-compliant” flag.

### C. High: Cowork assembly does not run the lifecycle it claims to run

The Cowork assembler reuses a clone by fetching, then later prints an
`estate-sync` heading while performing another fetch. It does not call the
shared sync service and does not fast-forward the reused clone. It also imports
private helpers from other modules. A remote clone can therefore orient from a
stale checked-out branch while the handoff says sync ran mechanically.

Route assembly through public application services used by every harness. The
same lifecycle name must mean the same operation and result type everywhere.

### D. Medium-high: the forward-work surfaces have exceeded agent-readable shape

`vendor-harness-adapter-foundation.md` is 2,021 lines, `cowork-adapter.md` is
536, and `session-start-hardening.md` is 303. The longest plan mixes active
work, amendments, evidence, historical handoffs, and closed phase detail.
Humans can search it; an agent under context pressure cannot reliably distinguish
operative residue from history.

This is a cohesion problem in the domain layer, not merely long prose. A plan
should hold forward state and acceptance; completed evidence belongs in stable
artifacts and Git. The remediation should compact these without destroying
their audit trail.

### E. Medium: adapter correctness is ahead of adapter product clarity

The registry and ports are stronger than the user-facing support matrix. A
harness can be supported at several different levels: entry discovery, config
rendering, lifecycle dispatch, runtime execution, write feedback, and live
acceptance. One compatibility word hides those distinctions. Publish a
capability matrix with exact builds and evidence links; do not turn “adapter
exists” into “all specification adherence is enforced.”

## Clean Architecture And SOLID Assessment

| Principle | Assessment | Evidence |
|---|---|---|
| Single responsibility | **Strong in specs and newer adapter ports; mixed in legacy services** | Things usually have one reason to change. Renderer/inspector/runner/install roles are separated. `scaffold.py`, `adapter_install.py`, `assemble.py`, and the 2,021-line adapter plan carry multiple temporal or operational responsibilities. |
| Open/closed | **Strong and improving** | Registry-driven adapters allow a new harness without editing domain logic. Trigger kinds and structural reference fields remain branch/list driven rather than registered capabilities. |
| Liskov substitution | **Good at the adapter boundary** | Shared adapter consumers mostly depend on declared ports and typed results. Cowork's not-applicable project projection is modelled rather than faked. Private imports in assemble weaken substitution. |
| Interface segregation | **Good** | Render, inspect, diagnostics, lifecycle, install, and evidence concerns are separately visible. The next needed segregation is repository read view and external trust authorization. |
| Dependency inversion | **Good horizontally, weak vertically** | Vendor implementations depend inward on neutral ports. Core parsing, validation, MCP, workflow, and hooks still depend directly on live `Path`/Git/process details rather than repository, trust, and transaction ports. |

The next architectural work should therefore add only three substantial ports:

1. `RepositoryView` — worktree, index candidate, or immutable commit;
2. `ExternalTrustPolicy` — whether exact repository-supplied command/network
   configuration may execute in this clone;
3. `RepositoryTransaction` — staged-state isolation, hooks-dir resolution,
   apply/rollback, and explicit external-effect boundaries.

Everything else in the plan should become a consumer of those ports, not a new
parallel framework.

## Domain System Review

### What is complete and coherent

- one thing = one identity/reason to change;
- domain-owned lifecycle vocabularies with reserved framework types;
- explicit hard dependencies versus soft relationships;
- graph-connected session memory rather than chat-summary persistence;
- conflicts, decisions, provenance pins, quarantine, workflows, claims, and
  indexes as durable state;
- generated indexes as disposable caches with rebuild-and-diff validation;
- nested repository isolation and framework discovery/refresh;
- mechanical floor versus semantic judgement;
- exposure as an explicit per-thing membrane decision;
- Git history as accepted-state event stream and useful telemetry;
- “deploy when felt” as a guard against premature primitives.

### What remains incomplete

- exact repository-view semantics at commit, serve, and long-read boundaries;
- optimistic concurrency for an agent writing after its base commit moved;
- transition legality where both prior state and allowed graph are mechanical;
- complete structural-reference ownership;
- transactional domain birth and hook coexistence;
- a trust ceremony for executable/networked project configuration;
- first-class template instantiation validation;
- a compact forward-work representation that agents can load without consuming
  the context needed to perform it.

### What I would not change

I would not replace Markdown/YAML/Git with a database-centric runtime, turn the
thing graph into a mandatory ontology engine, mechanise semantic judgement,
make adapters necessary for correctness, introduce an event bus for prompt
bindings, or add always-on autonomous agents. Those changes would discard the
framework's best property: inspectable supplementary structure that improves a
human-led reasoning system without pretending to replace the human.

I would also keep the manifesto's central thesis, the mechanical/semantic split,
the three-layer domain shape, tiered loading, examples as inductive teaching,
and explicit evidence of failed hypotheses. The remediation is a hardening and
claim-precision programme, not a conceptual rewrite.

## Manifesto And Claim Review

The manifesto works best when it describes a design discipline. It overreaches
when it converts that discipline into empirical or universal guarantees.

Retain:

- definition-driven rather than chat-residue-driven systems;
- persistent, inspectable, versioned domain state;
- elegant constraint as a testable efficiency hypothesis;
- human authority over irreversible consequence;
- self-description and dogfooding as serious evidence;
- probabilistic reasoning inside deterministic structural boundaries.

Narrow:

- Git is **accepted recorded state**, not truth;
- inspectable history is an audit aid, not a complete reasoning trace;
- self-hosting demonstrates reflexivity, not universality;
- definitions are still instructions/prompts in the broad technical sense;
- Markdown and executable behaviour are connected by a stochastic interpreter,
  not literally one artifact;
- “any LLM” becomes a portability ambition bounded by named harness evidence;
- “everything is a thing” applies to managed domain knowledge, not every code,
  config, evidence, and release artifact in the repository;
- “no black boxes” cannot describe vendor models or harnesses the project does
  not control;
- consequence is a useful authority principle, not a theorem that removes the
  need for ordinary prospective risk analysis.

## Priority Order

1. Gate repository-supplied MCP command/network execution behind exact local
   trust; automatic read paths default deny.
2. Build `RepositoryView`; make pre-commit validation index-native and MCP
   serving commit-native.
3. Transactionalise hook installation and scaffold; make publication
   authorization fail closed if the operator approves reversing the recent
   default-on doctrine.
4. Finish session-start evidence semantics and route Cowork through the same
   lifecycle services as Claude Code and Codex.
5. Introduce one strict YAML loader and one structural-reference registry.
6. Make trigger, workflow, calculation, and eval semantics total at their
   mechanical boundaries.
7. Validate templates through instantiation and harden the install/release
   supply chain.
8. Reconcile manifesto, README, operator docs, and compatibility claims.
9. Re-run live acceptance in all three harnesses, then give this record and the
   implementation evidence to Claude for an independent closeout.

## Overall Verdict

The project is worth continuing. The conceptual substrate is stronger than the
remaining defects, and recent work shows the team responds to evidence rather
than defending claims. The risk is not that MarkdownLLM lacks another primitive.
The risk is that sophisticated specifications and adapters create confidence
faster than the exact transaction boundary can justify it.

The next milestone should therefore be **transaction-integrity complete**:
every deterministic statement names the immutable bytes, authority, execution
boundary, and evidence level it actually proves. Once that is true, the three
adapters become evidence of one coherent agent system rather than three good
projections over a partially ambiguous core.
