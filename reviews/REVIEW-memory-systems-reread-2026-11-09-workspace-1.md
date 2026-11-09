---
id: review-memory-systems-reread-2026-11-09-workspace-1
type: artifact
status: evolving
authorship: model-session
version: 1.1
created: 2026-11-09
session: 2026-11-09
origin: synthesised
exposed: false
tags: [review, memory-systems, prior-art, problem-statement, continuity, evals, model-authored]
informed_by:
  - id: review-critical-comparison-2026-10-17-claude
    commit: b9bb9a716e928f446d8b9a99ae16b5b52ba605e8
  - id: limitations-guide
    commit: b9bb9a716e928f446d8b9a99ae16b5b52ba605e8
  - id: llm-driven-systems-manifesto
    commit: b9bb9a716e928f446d8b9a99ae16b5b52ba605e8
  - id: evidence-and-eval-backlog
    commit: b9bb9a716e928f446d8b9a99ae16b5b52ba605e8
linked_things:
  - id: review-critical-comparison-2026-10-17-claude
    relation: extends
    notes: "That review compared twelve systems on eleven dimensions, none of which was continuity of work; this reading adds that column, re-reads seven of the systems three weeks on, and reflects the result onto the framework's own problem statement rather than onto its novelty."
  - id: limitations-guide
    relation: informs
    notes: "Three of the guide's 'what the others do' facts moved between 2026-10-17 and 2026-11-08; the corrections are in §3 and the guide carries a dated pointer."
  - id: llm-driven-systems-manifesto
    relation: references
    notes: "The Accumulation section is the problem statement this reading measures the field against; the corollary section already demotes model-tier superiority, which §6 takes as given."
  - id: the-eval-question-is-which-surfaces-carry-the-weight-2026-11-08
    relation: informs
    notes: "§6 names the surfaces an ablation would move, now that the question is which part of the structure does the work."
  - id: eval-cycle
    relation: informs
    notes: "The moving-surfaces table gains a candidate row — the work-continuity layer — if the operator takes §6."
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "The backlog's purpose line still reads as evidence for the model-tier claim; §6 says what it would read as instead."
---

# Memory systems, reread — their problem against ours

**What this is.** A second reading of the agent-memory field, three weeks after
the critical comparison, made for one purpose the first reading did not serve.
The operator asked (2026-11-08) to "examine what features these things have,
what problems they're trying to solve, and then reflect that back and examine
what features do we have and what problems are we trying to resolve." The
first review ranked the framework's *novelty* against the field. This one
ranks the field's *problem statements* against the framework's, because the
operator's week inside a harness with no record under it had just shown that
the question the framework exists to answer is not the one the eval programme
was testing.

**Review status.** Model-authored, operator-requested, at commit
`b9bb9a716e928f446d8b9a99ae16b5b52ba605e8`. Sources were read on 2026-11-08 by two
research passes against primary documentation (official docs, changelogs,
release notes, engineering posts); every vendor number is marked as such; the
items that could not be verified from a primary source are listed at the end.
Facts here are the state of each product's *documentation* on that date, not
the state of its behaviour. The operator asked for the reading; asking does
not endorse the reflection in §4–§6, which is the agent's.

## 1. The problem statement this reading measures against

The operator's, on 2026-11-08, after a week in GitHub Copilot with no
MarkdownLLM workspace beneath it:

> From my experience through this process, the main aim for all this was a
> tool that enhanced one's ability to work over multiple sessions, over
> multiple days, weeks, months, years, on a specific set thing, or on many
> things within a specific set domain — and that this knowledge graph that
> builds itself through use as a fractal piece would become a domain graph.
> Even though I've had quite a big vision, that small beginnings piece of just
> what memory system is needed to be right, because that is essentially one of
> the foundations of the whole idea.

This is the manifesto's Accumulation section in the operator's voice: *a
thought taken partway is kept whole… so that a later purpose its author never
had can pick it up*; *the record must hold while nobody attends*; *the read
across the record is made by the structure, not by the operator's spare
attention*. The unit of concern is **work on a domain over time** — what is
open, what was decided and why, what depends on what, what is due — not facts
about a user or a codebase. That distinction is the whole of this review.

## 2. Eight problem statements, side by side

What each system says it is for, what it stores, and — the column the first
review did not draw — whether a new session learns *where the work got to*.
Sources are in the two survey tables filed with this review's session and
cited in the critical comparison; vendor wording is quoted where it is short.

| System | What it says it solves | Unit of memory | Does a new session know where the work got to? |
|---|---|---|---|
| **Mem0** | "Stateless agents, repeated instructions, and zero personalization across sessions"; "context that persists" | Extracted text facts about the user, scoped by user/agent/run; a JSON-schema User Profile | No. Facts and a profile; no open-work primitive |
| **Zep / Graphiti** | "Handle changing information" — a real-time temporal knowledge graph; "the unified context layer for enterprise data" | Episodes → typed entities → bi-temporal fact edges | No. Per-user graph across threads plus summaries; facts only |
| **Letta** | "Machines that learn… remember everything, learn continuously"; memory is "a core responsibility of the agent harness" | Markdown files with frontmatter in a git repo (MemFS); root files always in context | Partly. Resumes the last conversation; `/init` reviews prior sessions; whatever the agent wrote — no reserved field for it |
| **Claude Code** | "Each session begins with a fresh context window"; CLAUDE.md is your instructions, auto memory is Claude's notes on your corrections — "context, not enforced configuration" | Markdown: instruction files plus a per-repo memory directory with a four-value `type` | Partly. `type: project` is "ongoing work, deadlines, and decisions Claude can't derive from the code or git history" — one of four note types, loaded on demand |
| **Codex** | "Carry useful context from earlier work into future work"; "a helpful recall layer, not… rules that must always apply" | Background-extracted summaries of past chats plus "supporting evidence", per machine | No. Summaries of what was said; `codex resume` for the transcript |
| **Copilot Memory** | "Learn and retain useful details about your repositories"; the hard part "is keeping stored knowledge valid as code changes, not retrieval" | Server-side typed facts about the repository, each cited to code; user preferences cited to your words | No. Durable facts; CLI checkpoints are a separate mechanism |
| **Hermes Agent** | "Bounded, curated memory that persists across sessions"; small durable facts always in context, procedures in skills | Two plain-text files (2,200 and 1,375 characters) per profile; skills; a full-text session index | No. "Completed work" is listed as save-worthy; `/journey` is a timeline; no open-task model |
| **MarkdownLLM** | Nothing a later session relies on changes silently; the record as what training is for a model | Typed records with declared schema, status, relations, dates and triggers, in git | Yes — by construction. `status` on every record, `plan` and `workflow-run` with a stage cursor, triggers with dates, and a session-start digest that *computes* open loops, stalls, fired triggers and unanswered questions from the record |

Two readings of that last column. First, it is empty for the field: seven
systems, and the two that touch it do so with a free-form note the agent may
or may not have written. Second, that emptiness is not a gap the vendors
missed — it is a different problem. Every problem statement in the first
column is about **persistence of facts** (about a person, a codebase, an
enterprise) across sessions. None is about **continuity of work**. The
framework's problem statement is the second thing, and the operator's week
without it was the first-hand measurement of what the first thing does not
give you: a capable model, well-stocked with facts, that still had to be told
every morning where yesterday ended.

## 3. What moved between 2026-10-17 and 2026-11-08

The critical comparison's "is it still true" findings stand in shape; three
of the facts under them have moved, and one convergence has become general.

- **Background consolidation is now everywhere.** Letta's dreaming (March)
  was the first; by November it has company: **Mem0 Dream** (Platform, August,
  updated September — Supersede and Merge "always on", a daily/weekly
  Synthesis pass), **Codex's Phase 2 "global consolidation"** sub-agent ("no
  approvals, no network, local write access only"), and **Copilot Dreaming**
  (public preview 2026-10-28 — "removes duplicate memories and corrects
  outdated guidance", and proposes pull requests to `copilot-instructions.md`,
  `AGENTS.md`, `CLAUDE.md` and skills). Four vendors now run a model over the
  memory while nobody is watching. None asks before it edits; Copilot's run
  output is "not a complete activity history" and has no undo.
- **Write-time approval gates are appearing — off by default.** Hermes added
  `memory.write_approval` (2026-06-19, default false) and then made protected
  files — `AGENTS.md`, skills, memory stores — *always* require approval
  (2026-08-31), against prompt injection. Copilot "may ask you to approve
  storing a memory" in the app and interactive CLI, not in the cloud agent.
  Zep's Agent Skills (2026-11-05) offer opt-in "member review" of versions.
  The field is adding a human gate; it is adding it at *write* time, on
  *security* grounds, and the default is open.
- **Mem0's add-only retreat has a sequel.** The April position — "nothing is
  overwritten", staleness "left to the application" — now has Dream's
  Supersede retiring facts into labelled history. Mem0's own evaluation page
  still says "Knowledge update remains the hardest category for an additive,
  ADD-only architecture", and its state-of-memory post calls staleness in
  high-relevance memories "a harder, open problem."
- **Copilot's expiry moved.** The guide's "28 days idle" is the January and
  March changelog; the current concept page reads a **90-day default,
  configurable 7–180 days** by organisation, upvotes resetting the clock
  (the date of the change is unverified). Memory went GA on paid plans on
  2026-10-28 with a vendor adherence figure of 93%.
- **Codex grew a memory of its own.** Not in the first review's matrix: a
  two-phase background pipeline (per-thread extraction after six idle hours,
  then consolidation), markdown files under a per-machine git-baseline
  directory, usage-driven decay (`max_unused_days` 30), explicit "supporting
  evidence" per memory, and an import path for other agents' memories
  (v2 default from 0.165.0, 2026-10-27). Off by default.
- **Claude Code added a `modified` stamp** to every auto-memory file
  (2.1.214, July) "so Claude can see how current the fact is", and
  `/doctor prompt-audit` (2.1.283, September) that proposes edits and
  "changes nothing until you ask." The "may pick one arbitrarily" sentence
  is still in the docs.

The direction the first review named — files, git, verification at some
boundary, a human somewhere — has continued. The parts it named as the
framework's own remain its own: no surveyed system refuses a *change to
something others depend on* until the dependants are walked; no surveyed
system keeps the *question* as a record until a human answers it; no surveyed
system pins a *decision* to the commits it was read from. Codex's git baseline
and Copilot's citations are the nearest approaches, and both are provenance
of *facts*, not of *rulings*.

## 4. Reflecting it back — our features against our problem

The operator's instruction was to reflect the field's features onto ours.
Done honestly, the map is not "what we have that they lack" but "which of our
features answers the problem in §1, and which the field also answers." The
table takes the framework's surfaces one at a time.

| Framework surface | The problem it answers (in §1's terms) | Who else answers it |
|---|---|---|
| Typed records with a declared `_schema.yaml`; `linked_things`, `dependencies` with reserved relations | *The graph that builds itself through use becomes a domain graph* — the type system is the domain's, the relations are walked both ways | **Zep** alone has user-declared entity and edge types (Pydantic/Zod, enterprise data). Mem0 removed its graph ("connections are inferred, not typed"); Letta, Claude Code, Codex, Hermes have no types or relations between memories |
| `status` on every record; `plan` phases; `workflow-run` with `current_stage`; the open-loops line of the digest | *Work over sessions, days, weeks, months* — what is in flight is a property of the record, not a note someone remembered to write | **Nobody**, as a computed property. Claude Code's `type: project` and Letta's free-form files are the closest; both depend on the agent having written it |
| Triggers with dates; the fired-triggers line | *Dates the operator declared still reaching them when they arrive* | **Nobody**. The field has expiry (Copilot, Codex decay, Mem0 `expiration_date`) — dates that make memory *go away*, not dates that bring work *back* |
| The session-start digest (`mdllm session-start`): version, velocity, open loops, conflicts, cues, fired triggers, reckoning — computed from the record and emitted | *A session arrives knowing where the work got to* — the thing the Copilot week lacked | **Nobody** computes one. Codex injects summaries of past chats; Hermes injects two frozen files; Claude Code injects the first 200 lines of an index; Letta loads root files. All inject *what was written*; none derives *what is open* |
| The cue, the walk, the gate; `type: conflict`, `supersedes`/`contradicts` | *Nothing a later session relies on changes silently* | **Nobody** at the change boundary (the first review's finding, unchanged). Zep invalidates facts bi-temporally by model; Copilot re-verifies against code at read time; four vendors now consolidate in the background without asking |
| `type: decision` with `informed_by` pinned to commits; the reverse index | *Why* — the reasons arrive with the record instead of being inferred afterwards | **Nobody** for decisions. Zep has per-fact episode provenance; Copilot per-fact citations; Codex "supporting evidence" per memory; Letta commit history. Provenance of facts is now common; provenance of rulings is not |
| The reckoning: an actor disposes at a session boundary; `--close` before a `session-end:` commit | *The record must hold while nobody attends… cost nothing to set down and nothing to pick up* | The field disposes **automatically**: Copilot 90-day expiry and downvotes, Codex 30-day unused decay, Mem0 Dream, Letta dreaming, Hermes's curator. Same need, opposite allocation |
| `type: insight`; `*.skill.md`; `type: example` | *Generative knowledge that survives the session* | **Everyone**, and arguably better: Hermes's self-authored, self-patched `SKILL.md` in an open standard; Letta's agent-owned skills; Zep's compiled Agent Skills with per-step citations; Codex's `skills/` under memories |
| The kernel; tiered loading | *A contract the processor reads before it acts* | **Everyone**: CLAUDE.md/AGENTS.md hierarchies, Hermes's three skill tiers, Letta's root-files-always-in-context. Standard |
| Git as the substrate; the seat; publication as the turn | *Many sessions, more than one machine, one record* | **Letta** (MemFS, Cloud-synced, shared repos), **Codex** (git baseline, per machine, not synced). Shared, *typed*, multi-seat records: nobody |

Read down the middle column and the pattern is plain. The rows where the
framework stands alone are exactly the rows that answer **continuity of
work** — status as a property, dates that return, a computed "where did we
get to", a change that cannot pass silently, a ruling pinned to its inputs.
The rows where the field matches or beats the framework are the rows about
**persistence of knowledge** — skills, lessons, the loaded contract, the
substrate. That is the same split as §2's last column, seen from the inside.

## 5. What the field has that the framework does not

The first review's list stands and has grown; it is restated because a
reflection that omits it is advocacy.

- **Retrieval at scale.** Hybrid search in Mem0 and Zep; Hermes's full-text
  session index at ~20 ms with no model call; Zep v4's bounded subgraphs with
  a `truncated` flag "so an agent cannot mistake a partial neighborhood for a
  complete one." The framework scans frontmatter and reads files.
- **Validity as distinct from knowledge.** Zep's two timelines — when a fact
  was true in the world and when the system learned it. The framework's
  `status`/`stale`/`supersedes` conflates them.
- **Background upkeep.** Four systems tidy while nobody is present. The
  framework's reckoning needs an actor at a session boundary; its standing
  watch observes but does not tidy.
- **Zero setup and presence.** Every harness memory is on by default or one
  toggle away, in the tool the person already uses; Hermes meets the user in
  Telegram, Discord, Slack, WhatsApp, Signal and email. The framework needs a
  scaffold, a floor install, and a vocabulary.
- **Portability of memory between agents.** Codex imports other agents'
  memories; Hermes runs eight external providers; Mem0 ships plugins for
  Claude Code, Cursor, Codex and OpenClaw. The framework's record is portable
  by being plain files in git, and by nothing else.
- **Adoption and independent measurement.** Unchanged from the first review:
  the systems with the least governance have the users; the framework has one
  estate and one partner operator.

## 6. What this does to the eval question

On 2026-11-08 the operator ruled that the question to answer is no longer
whether a smaller model with structure beats a larger one without — the
manifesto already calls that "a secondary, still-open hypothesis… re-proving
it adds little" — but **what in the structure does the work**
(`the-eval-question-is-which-surfaces-carry-the-weight-2026-11-08`). This
reading supplies the first answer worth testing.

The features the field does *not* have cluster on one layer: the one that
makes a record *about work* rather than *about facts* — `status` and stage
cursors, dated triggers, the computed digest, the change gate, the pinned
ruling. The features the field *does* have — skills, lessons, a loaded
contract, files in git — are the ones a bare-but-journalled arm would carry
too. So the ablation the `eval-cycle` definition is built for has a natural
first cut:

- **Hold constant** the model, the fixture, the facts available, and the
  knowledge layer (skills, insights, the kernel) — give every arm those.
- **Move one surface at a time** in the work-continuity layer: a seed whose
  records carry `status` and stage cursors against one whose records do not;
  a session start that emits the computed digest against one that injects
  the same files verbatim; a change gate on against off.
- **Measure** what the Copilot week felt: re-establishment (how much of the
  read set is re-deriving what the record already settled), wrong turns
  (actions taken against a superseded or stale record), and whether the
  session acts on the open loop the record names without being told.

The pre-registered prediction that follows from §4, written before any run:
**the digest surface carries more of the weight than the schema surface** —
a session that is told what is open, by computation, re-establishes less and
acts on the right thing sooner than one that has typed records but must
derive the open set itself. If the read set and the changed-set figures do not
move when the digest is removed, the "where did we get to" story is wrong,
and this review's reflection falls with it. That is a cycle for
`run-eval-cycle-0` to be followed by, not a conclusion.

Nothing in this section is built. The runner has no digest-off arm and no
status-stripped seed; the `eval-cycle` moving-surfaces table does not yet
name the work-continuity layer as a surface; the backlog's purpose line still
reads as evidence for the model-tier claim. Those are three edits the operator
has not yet asked for, listed so that the next session finds them here rather
than re-deriving them.

*2026-11-09, later the same day:* the operator asked for the three edits and
they are made — `eval-cycle` 1.1 carries the work-continuity row,
`run-eval-cycle-0` 1.1 re-plans its cycles over it, and the backlog's 2.4
paragraph states the new purpose. The runner work named above is still not
done, and is now listed as each cycle's pre-work where the cycle sits.

## Unverified, and what this reading is not

Could not be confirmed from a primary source on 2026-11-08: Codex's injection
token budget and its EEA/UK/CH default; the date Copilot's expiry moved from
28 to 90 days and any organisation-instruction character limit; any official
Hermes memory benchmark (none found — the circulating "52.8 → 66.5%" figure is
a LangChain harness experiment, not Hermes memory); OpenMemory's 2026 status;
the date Letta's V1 server was archived; the openai.com "Codex for (almost)
everything" post (403 on fetch). Every benchmark figure above is a vendor's
own and is marked so; the first review's finding that the benchmark column is
unusable for comparison is unchanged.

This is one reading by one model session on one day. It is not a cold review,
not a usability test of any product, and not evidence that the framework's
work-continuity layer *works* — only that no surveyed system has one. The
operator's week in Copilot is one person's experience, recorded here because
it is what prompted the question, not as a measurement.
