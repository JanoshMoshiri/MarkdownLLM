---
id: task-book-fitter
type: task
status: blocked
priority: medium
created: 2026-05-24
parent: project-kitchen-renovation
dependencies: [task-choose-worktop]
tags: [home, renovation]
triggers:
  - type: dependency
    on: status_changed_to
    watch: [task-choose-worktop]
    value: completed
    action: "worktop chosen — book Howell Joinery for the fitting week"
---

# Book Fitter

## What to Do

Confirm a fitting week with Howell Joinery once the worktop order date is
known. They asked for two weeks' notice.

## Why It Matters

The fitting date anchors the whole back end of the project. Booking too early
risks a kitchen with no worktop; too late risks missing the August deadline.

## Success Criteria

A confirmed week in the contractor's calendar, in writing.

## Current State

Blocked, correctly: the `dependencies` field carries the sequencing, and the
dependency trigger above tells the next session to surface this task the
moment `task-choose-worktop` completes. No "dependency thing" exists — fields
express sequencing; things are for content.
