---
id: framework-triggers-index
type: index
status: live
index_of: triggers
created: 2026-08-30
generated: 2026-08-30T18:34:31
generated_from: HEAD@67d7816
coverage: 7
framework_version: 3.37.0
---

# Triggers Index — framework

## closed-loop-operating-state
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-09-05 reached, action=Dead-man on the dispatcher. Check whether a dispatch digest has been filed in the pilot repo within the window; if none has, the loop is silent and silence is not health — establish whether the job was never registered, was registered and never fired, or fired and died mid-run (a digest left in-flight with a live claim says the third). Re-date this trigger to the next window once answered. Coverage is honestly partial: this fires into the operator's own session-start orientation at the framework root, so it is read at the operator's session cadence and not before — the chase pattern, not a monitor (dispatch-digest-home-2026-08-29).

## estate-retrospective-synthesis-2026-08
- status: evolving  due_date: —
- trigger: type=time, condition=2026-09-10 reached, action=Defer to `operator-queue-2026-08-28`, which now carries this synthesis's undischarged rows and chases the same date — report only what is unique to this artifact: whether the regulated cluster's formal estate retrospective (chased 2026-09-03 in its vantage domain) ran and consumed this synthesis as its layer-below input, and whether the standing aggregation read (row 6) has been ruled. Do not double-chase the rows the queue holds.

## estate-workflow-derivation
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-09-10 reached, action=The MVP was met 2026-08-28, so this fires on the residuals, not the gate. Report whether the two stale mirrors (residual 2) have been re-synced and re-flipped by the operator — nothing mechanical will detect them while imports-check coverage is 0/101 and 0/43 — and whether the three recorded process gaps have been ruled by their domains. Re-conditioned from the original MVP chase, which its own outcome answered.

## framework-retrospective-2026-08b
- status: completed  due_date: —
- trigger: type=time, condition=2026-08-27 reached, action=Chase: if the 2026-08b retrospective has not been written, surface the wait itself — the debt is now three weeks past its own volume and milestone triggers

## operator-queue-2026-08-28
- status: evolving  due_date: —
- trigger: type=time, condition=2026-09-10 reached, action=If this queue has not been ruled, report which tier-1 rows remain open and what each is blocking. The queue idles at the operator's seat by design; an undated idle is the drift the estate already learned to chase.

## watertight-membrane-sprint-2026-08-30
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-09-05 reached, action=If Phase A/B operator gates (verified flips, trust grants) are still unruled, surface them alongside the dispatcher dead-man — the same date, deliberately: both are the closed loop waiting on its human seats.

## workflow-reconciliation-precedes-new-definitions
- status: made  due_date: —
- trigger: type=time, condition=2026-09-10 reached, action=If the derivation shape is still unsettled, surface this decision at the operator's ratification sitting — the quality-loop plan and any new framework-level workflow-definition wait on it, and an undated human wait is the drift the estate learned to chase.

