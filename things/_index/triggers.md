---
id: framework-triggers-index
type: index
status: live
index_of: triggers
created: 2026-10-08
generated: 2026-10-08T23:57:47
generated_from: HEAD@ff7e8d6
coverage: 8
framework_version: 3.47.0
---

# Triggers Index — framework

## closed-loop-operating-state
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-10-21 reached, action=Answered 2026-10-08: yes. The tick was re-registered on the operator's machine on 2026-09-23 and has filed digests in two workspaces, on 2026-10-04 and 2026-10-07 (runs 2 to 5 on the 7th), last result 0; run 3 worked a fired trigger end to end. The question for this window: do digests keep landing at the daily cadence, and has the workspace one run skipped as DIVERGED been routed? A tick never merges. Earlier: re-dated 2026-09-15 after its first answer (Phase 4: the tick had been deliberately retired, not lost). The question now is whether the tick has been re-registered on the operator's own host and has filed a digest. Dead-man on the dispatcher. Check whether a dispatch digest has been filed in the pilot repo within the window; if none has, the loop is silent and silence is not health — establish whether the job was never registered, was registered and never fired, or fired and died mid-run (a digest left in-flight with a live claim says the third). Re-date this trigger to the next window once answered. Coverage is honestly partial: this fires into the operator's own session-start orientation at the framework root, so it is read at the operator's session cadence and not before — the chase pattern, not a monitor (dispatch-digest-home-2026-08-29).

## estate-retrospective-synthesis-2026-08
- status: evolving  due_date: —
- trigger: type=time, condition=2026-10-13 reached, action=Answered 2026-10-08, half: the regulated cluster's estate retrospective ran in its vantage domain on 2026-09-17. Row 6, the standing aggregation read, is unruled; since 2026-10-05 `mdllm reckon` aggregates disposition per workspace, which is the per-repo half of that read. Re-dated to the framework retrospective's chase, which is the reader for both. Earlier: defer to `operator-queue-2026-08-28`, which now carries this synthesis's undischarged rows and chases the same date — report only what is unique to this artifact: whether the regulated cluster's formal estate retrospective (chased 2026-09-03 in its vantage domain) ran and consumed this synthesis as its layer-below input, and whether the standing aggregation read (row 6) has been ruled. Do not double-chase the rows the queue holds.

## estate-workflow-derivation
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-10-21 reached, action=Answered 2026-10-08, re-conditioned: the residual 'process gaps ruled by their domains' now has a floor read. `mdllm workflows --emergent` names each workspace's enacted process and the unbound definition that already describes it (`workflows-emerge-from-use-2026-10-07`), and the reckoning hands it to the domain agent. Ask at this date: has a workspace bound or written one, and have the two stale mirrors been re-synced? Earlier: the MVP was met 2026-08-28, so this fires on the residuals, not the gate. Report whether the two stale mirrors (residual 2) have been re-synced and re-flipped by the operator — nothing mechanical will detect them while imports-check coverage is 0/101 and 0/43 — and whether the three recorded process gaps have been ruled by their domains. Re-conditioned from the original MVP chase, which its own outcome answered.

## framework-retrospective-2026-09
- status: complete  due_date: —
- trigger: type=time, condition=2026-10-13 reached, action=Retrospective chase (thirty days from period_end 2026-09-13; retrospective-cadence-is-a-dated-chase-2026-09-13). If things/ moved since 2026-09-13: run the mechanical scans now, offer the ritual as this session's first item, or — unattended — draft it and file the rulings to the seat. If nothing moved: re-date this chase. Either way, the retrospective that answers it disarms this trigger and arms its own.

## operator-seat-and-harness-native-onramp
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-10-22 reached, action=Acted 2026-10-08 at the-reckoning Phase 3's close: Phase 5 still has no account recorded, so the operator was asked for it in one line. If none is recorded by this date, ask once more in one line; never rewrite first-hour.md without it. Earlier: answered 2026-09-23: the operator put this arc first (birth arc — onramp, guided scaffold, first-hour rewrite as one piece) ahead of the eval evening. It starts from his own account of how scaffolding a domain actually goes, which he said he would give. If Phase 5 still has no account recorded, ask for it in one line — do not rewrite first-hour.md without it.
- trigger: type=time, condition=2026-10-10 reached, action=Re-dated 2026-09-26 after its first answer (onramp first — see Sequencing). Chase: has the Codex cloud route produced a first-hand record, and has Phase 2's silent bootstrap been started for any route? If neither moved, surface the wait plainly and ask whether the eval backlog should take the slot instead.

## substrate-native-a2a
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-10-10 reached, action=Has Phase 4 run one real writer/reviewer turn through `mdllm watch` in the engineering domain? If not, establish which: the command was never armed, was armed and never woke, or woke and the turn was hand-relayed anyway. The third is the interesting failure — it would mean the doorbell rings and nobody rises, which is a seat problem and not a channel problem. Re-date once answered.

## the-reckoning
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-10-19 reached, action=surface, note=Two weeks: has one attended session ended through the reckoning, and has one tick drafted one? If neither, the actor is the problem, not the command.

## workflows-emerge-from-use
- status: in-progress  due_date: —
- trigger: type=time, condition=2026-10-21 reached, action=surface, note=Two weeks: has a workflow emerged in a live workspace, and has the agent followed one when working on its carrier type? If neither, the actor is the problem.

