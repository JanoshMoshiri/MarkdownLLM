---
id: limitations-guide
type: guide
status: draft
version: 1.0
created: 2026-10-18
tags: [limitations, positioning, when-not-to-use, prior-art, memory-systems]
linked_things:
  - id: review-critical-comparison-2026-10-17-claude
    relation: derived-from
    notes: "Every competitor fact and every weakness here is that review's finding, cited to its sources; this file is the answer four earlier reviews asked for and the corpus never made."
  - id: scalability-guide
    relation: references
    notes: "The measured range: comfortable to 200–300 records in one workspace; the guide's own limit near 1,000."
  - id: evidence-and-eval-backlog
    relation: references
    notes: "The two measurements that would turn the central claim from a hypothesis into a result."
  - id: operator-guide
    relation: complements
    notes: "The operator guide says what the tooling carries for you; this file says when not to pick up the tooling at all."
  - id: glossary
    relation: complements
    notes: "The vocabulary this file avoids is translated there."
---

# Limitations — when not to use this, and why not just a notes folder

This file exists because four commissioned reviews between June and October
2026 asked the same question and the repository never answered it in one
place: *why not just `CLAUDE.md` plus a notes folder?* The honest answer has
two halves. For most people, most of the time, the notes folder is right. What
follows is the smaller set of situations where it is not, the list of
situations where this framework is the wrong tool, and what the other systems
in this field actually do about the one question this framework is built
around.

## When not to use this

- **High-volume transactional data.** Every record is a file and every
  change is a commit. Thousands of writes an hour belong in a database.
- **Many concurrent writers.** Coordination is by publication to a git
  remote and by advisory claims with a lease — read and respected, never a
  lock. Two agents taking turns works; twenty people editing at once does not.
- **Sub-second latency.** There is no index and no search by design: a broad
  question is answered by scanning frontmatter. At roughly 560 records,
  `mdllm validate` takes about 27 seconds on one machine. If you need an
  answer before the next keystroke, this is not the layer that gives it.
- **Genuinely relational queries.** "Every record linked to X whose status
  changed in the last month, grouped by owner" is a query. Git and YAML can
  hold the data; they cannot serve the join.
- **Corpora past the measured range.** The framework's own guide says one
  workspace is comfortable to 200–300 records and that near 1,000 the
  approach — full model reasoning over unindexed files — should be
  reconsidered. The largest live workspace is about 555 records. Anything
  that says "10 to 10,000" elsewhere in this repository was the claim before
  the measurement; the guide is the measured document.
- **Interfaces without a filesystem.** A chat window that cannot read and
  write files cannot run this at all.
- **Anyone who wants contradictions settled automatically.** The framework
  routes "is this still true" to a human on purpose: forty years of
  belief-revision theory say the general case cannot be automated, and the
  model-only resolvers in the field are retreating from it. If you want a
  system that quietly decides, pick one that does.
- **Teams who will not accept a refused commit.** The pre-commit gate
  protects the record and repels the newcomer in the same motion. The one
  non-author operator onboarded so far lost ninety minutes to the vocabulary
  (hence the [glossary](glossary.md)). Expect that cost.

## Why not `CLAUDE.md` plus a notes folder

For one person, one project, and memory that only needs to last a few weeks:
use the notes folder. It is cheaper, it is what the harness vendors ship, and
nothing here will beat it on speed.

The folder fails in one specific way, and it fails silently. Suppose a
workspace holds a rule others reason from — a VAT threshold, an escalation
route in a procedure, a definition of "done" for a stage — and seven other
notes were written against it. The rule changes. In a notes folder nothing
knows that the seven exist. The agent reads whichever note it opens, and the
harness documentation is candid about what happens when notes disagree: it
"may pick one arbitrarily". With the floor installed, the rule is a
*definition surface*: the commit that changes it is refused until the seven
dependants have been read and each one marked as still holding, revised, or
needing a human's ruling; the question persists as a file until that record
exists; the human rules on the one the agent may not settle; and the ruling is
committed. That is the whole difference. It costs a file per question and a
slower commit, and it is only worth paying when the record will be reasoned
from for longer than anyone will remember writing it.

## What the others do about "is it still true"

The field does not leave the question open; it answers it in ways this
framework deliberately does not. Facts as read on 2026-10-17 and 2026-10-18,
with sources in the [critical comparison](../reviews/REVIEW-critical-comparison-2026-10-17-claude.md):

- **Mem0** mechanised the question in 2025 as a model choosing add, update,
  delete or no-op against similar memories — and in April 2026 retreated to
  single-pass, add-only extraction, "nothing is overwritten", with staleness
  "left to application-layer decisions".
- **Zep / Graphiti** keeps every fact bi-temporal: when it was true in the
  world and when the system knew it. New information invalidates old facts
  rather than deleting them. The decision is the model's; no human step.
- **Letta** rebuilt memory in 2026 as git-backed markdown with background
  "dreaming" passes that consolidate and update memory and, in its own words,
  do not ask for approval.
- **Claude Code** treats `CLAUDE.md` and its auto-memory as advisory context;
  when files contradict, the model "may pick one arbitrarily", and
  `/doctor prompt-audit` proposes fixes without recording the question.
- **GitHub Copilot Memory** stores each repository fact with a code citation
  and re-verifies the citation against the current branch before use; memories
  expire after 28 days idle.
- **Karpathy's LLM wiki** has a lint step the user invokes that reports
  "contradictions between pages, stale claims that newer sources have
  superseded", and forgets the report.
- **Hermes Agent** keeps a 2,200-character memory page the agent rewrites
  itself and skills it patches as it uses them; nothing validates or versions
  a write, and the one independent benchmark names replacing outdated state
  as its weakest step.

What this framework does, and no surveyed system does, is refuse to let a
model settle that question silently: the walk, the persisted cue, the pinned
decision, the human residue. What it does not do, and several of them do:
retrieve at scale, model when a fact was true as distinct from when it was
recorded, run without a filesystem, or consolidate in the background without
asking.

## What is not yet known

- **Whether structure beats scale.** The framework's central hypothesis — a
  smaller model with this structure matching a larger one without it — rests
  on one evaluation whose reasoning core saturated. It is a hypothesis.
- **Whether the coherence claim holds over time.** The longitudinal
  measurement — seeded definition changes and contradictions across many
  sessions, this framework against a plain notes folder, detection rate and
  false positives — is designed and not yet run.
- **Whether anyone else can run it.** All evidence of the mechanisms in use
  comes from one author's estate. No independent operator has scaffolded a
  workspace from the public repository alone and reached a validated commit on
  record.
- **Whether the reconciliation cue pays for itself.** Of the first 173 cues,
  78% were ruled "not an inflection". That is the mechanism's precision until
  its trigger is narrowed.

If any of these matter to your decision, wait for the measurement or run it
yourself — the fixtures are in `evals/`.
