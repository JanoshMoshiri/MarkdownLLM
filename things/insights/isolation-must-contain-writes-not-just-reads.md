---
id: isolation-must-contain-writes-not-just-reads
type: insight
status: active
version: 1.0
created: 2026-07-09
confidence: high
origin: synthesised
source: session — sleeping-bag-longitudinal first multi-trial run (2026-07-09); haiku t5 perturb agent committed the fact-change to the source seed (framework commit 27409f4), silently invalidating the entire opus arm seeded after it
session: 2026-07-09
tags: [evals, controls, isolation, agent-agency, methodology, sandbox, data-integrity]
linked_things:
  - id: withholding-is-not-isolation
    relation: extends
    notes: "That was reads escaping the sandbox (defeating the bare control); this is writes escaping it (corrupting the shared fixture and invalidating the framework arm)."
  - id: committed-state-carries-defects-as-faithfully-as-facts
    relation: complements
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "The 'run workspaces outside the repo tree' item is now required for the FRAMEWORK condition, not just bare."
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: supports
---

# Isolation Must Contain Writes, Not Just Reads

## The Insight

[[withholding-is-not-isolation]] found that a capable agent **reads** past a
boundary placed around it — the opus-bare trial located the withheld seed and
applied it. The first multi-trial longitudinal run surfaced the same shape one
turn more dangerous: an agent **writes** past the boundary.

Haiku longitudinal trial 5's *perturb* session was told, in the operator's
voice, "update the domain to reflect the new plan" (Aonach Ridge → 3300 m,
pad R 4.2). Instead of editing its sandboxed workspace copy, the agent edited
**the shared source seed** at `evals/seeds/sleeping-bag-fac/things/trip-aonach-ridge.md`
and **committed it to the framework repo** (`27409f4`, 07:23:00, message
"fac-assessment: Aonach Ridge (updated to 3300 m altitude with R 4.2 pad)" —
the perturb task, verbatim). Its own workspace was left un-perturbed; the write
went to the wrong repo entirely.

The blast radius was silent and total for the arm that followed. The runner
seeds each trial by copying the source seed. Every **opus** trial started
*after* 07:23, so all five were seeded from the already-perturbed 3300 m/R 4.2
inputs. Opus then computed a build-session Aonach figure of −1 — **correct for
the corrupted inputs**, scored as wrong against the fixture's 2400 m-era
expectation of 4 — and its perturb session was a no-op (the change was already
present). The opus longitudinal chain was never actually exercised, and nothing
in the run output said so. Only forensic reconstruction from git history caught
it.

**The durable rule: a workspace that shares a filesystem and a git repo with the
material it is derived from is not isolated for *writes* any more than for
*reads*. An agent told to "update the domain" will update whatever domain it can
reach and cannot reliably distinguish its sandboxed copy from the canonical
original — and with `Bash(git:*)` it will commit the mistake into the parent
repo, contaminating every trial seeded afterward.** The `--add-dir <framework>`
grant that makes the framework condition *work* (the agent must read the specs)
is the same grant that makes the seed *writable*.

## Why This Is A Result, Not Just A Bug

The seed corruption is repaired (reverted in `16b3b77`; the six contaminated
result files — five opus, one haiku — are quarantined with evidence under
`evals/results/excluded/`, not deleted). But the finding outlives the cleanup,
and it is sharper than the read-breach:

- **It hit the *framework* condition, not the bare control.** The read-breach
  was a bare-cell problem; write-escape invalidated the *primary* arm. Isolation
  is not a control-only concern.
- **It was silent.** The read-breach announced itself in the transcript
  ([[withholding-is-not-isolation]]); this one produced plausible, internally
  consistent numbers and a green-looking perturb session. Contamination that
  scores as success is the dangerous kind.
- **It is the same trajectory, one step further.** Frontier agents route around
  constraints; the next step past "reads what it shouldn't" is "writes where it
  shouldn't." Cf. the cold-start `index.lock` on the framework repo and
  [[hook-compliance-correlates-with-scope-not-awareness]]: agent activity
  escapes the scope we imagine for it, and now it escapes in write.

## Implication

The "run bare workspaces outside the repo tree" item in
[[evidence-and-eval-backlog]] is now **required for every condition**, not just
bare, and for a second reason beyond read-isolation: a run workspace must be a
real sandbox (an OS temp dir outside the repo, or a filesystem/container
sandbox) so that (a) an agent cannot reach the canonical seed to read *or*
write, and (b) an errant `git commit` lands in the throwaway workspace repo, not
the framework. Until that lands, the runner should at minimum seed to a location
outside `evals/seeds/`'s repo and treat the source seeds as read-only, and every
multi-trial run should be checked against the seed's committed hash before the
results are trusted.

The valid data from this run is unaffected and reported separately: the four
haiku trials seeded *before* the corruption (t1–t4) plus the earlier smoke stand
as the haiku longitudinal arm. The opus arm must be **re-run from the restored
seed under real isolation** before it can be read at all. See
[[committed-state-carries-defects-as-faithfully-as-facts]] for the drift the
valid haiku trials did show.
