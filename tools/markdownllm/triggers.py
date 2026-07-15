"""Trigger evaluation — time, dependency, and threshold conditions.

Relationship triggers and `blocked_duration` need change history the floor
does not keep; they are reported as not-mechanically-evaluable rather than
silently skipped. Includes the deadline horizon scan over every non-terminal
date-bearing thing.
"""

from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

from .model import ISO_RE, TERMINAL_STATUSES, scan


def cmd_triggers(args) -> int:
    root = Path(args.path).resolve()
    corpus, _ = scan(root)
    today = dt.date.today()
    by_id = corpus.by_id()
    hits: list[str] = []
    skipped: list[str] = []

    def as_date(v):
        if isinstance(v, dt.datetime):
            return v.date()
        if isinstance(v, dt.date):
            return v
        if isinstance(v, str) and ISO_RE.match(v):
            return dt.date.fromisoformat(v[:10])
        return None

    def last_activity(path: Path) -> dt.date:
        # Staleness keys on the commit stream, not mtime: mtime is clone-local
        # noise (a fresh checkout resets it, a stray touch renews it) while
        # git history is the domain's actual activity record (review 5 drift
        # item; thing-lifecycle's last_active-from-git is the same fact).
        # mtime is the fallback for untracked files / no git.
        try:
            out = subprocess.run(
                ["git", "log", "-1", "--format=%cs", "--", str(path)],
                cwd=root, capture_output=True, text=True, check=True).stdout.strip()
            if out:
                return dt.date.fromisoformat(out)
        except Exception:
            pass
        return dt.date.fromtimestamp(path.stat().st_mtime)

    for t in corpus.things:
        meta, name = t.meta, t.id or t.path.name
        status = str(meta.get("status", ""))
        for tr in meta.get("triggers") or []:
            if not isinstance(tr, dict):
                continue
            ttype, cond, action = tr.get("type"), tr.get("condition"), tr.get("action")
            if ttype == "time":
                if cond == "due_date_passed":
                    due = as_date(meta.get("due_date"))
                    if due and due < today and status not in TERMINAL_STATUSES:
                        hits.append(f"{name}: due_date {due} passed "
                                    f"({(today - due).days}d ago) -> {action}")
                elif cond == "review_date_reached":
                    rd = as_date(meta.get("review_date"))
                    if rd and rd <= today:
                        hits.append(f"{name}: review_date {rd} reached -> {action}")
                elif cond == "stale":
                    thresh = str(tr.get("threshold", "30d")).rstrip("d")
                    last = last_activity(t.path)
                    if (today - last).days > int(thresh):
                        hits.append(f"{name}: unmodified {(today - last).days}d "
                                    f"(threshold {thresh}d) -> {action}")
            elif ttype == "dependency":
                watch = tr.get("watch") or []
                watch = watch if isinstance(watch, list) else [watch]
                value = tr.get("value")
                if tr.get("on") == "status_changed_to" and value:
                    states = [str(by_id[w].meta.get("status")) for w in watch if w in by_id]
                    if states and all(s == str(value) for s in states):
                        hits.append(f"{name}: all watched ({', '.join(watch)}) are "
                                    f"`{value}` -> {action}")
            elif ttype == "threshold":
                if cond == "subtasks_complete":
                    subs = [e.get("id") for e in meta.get("linked_things") or []
                            if isinstance(e, dict) and e.get("relation") == "subtask"]
                    if subs and all(str(by_id[s].meta.get("status")) in TERMINAL_STATUSES
                                    for s in subs if s in by_id):
                        hits.append(f"{name}: all subtasks complete -> {action}")
                elif cond == "blocked_duration":
                    skipped.append(f"{name}: `blocked_duration` needs status history "
                                   f"(evaluate via git log) — left to the agent")
            elif ttype == "relationship":
                # Watching another thing's field change needs event history the
                # floor doesn't keep — same honesty line as blocked_duration,
                # not silence (review 6, finding 3: the no-silent-default law
                # violated in miniature by the tool that enforces it).
                skipped.append(f"{name}: `relationship` trigger "
                               f"(on: {tr.get('on', '?')}, watch: {tr.get('watch', '?')}) "
                               f"needs change history — left to the agent")
            else:
                skipped.append(f"{name}: unrecognised trigger type `{ttype}` — "
                               f"not evaluated")

    # Deadline scan: every non-terminal date-bearing thing, triggers or not.
    horizon: list[tuple[int, str]] = []
    for t in corpus.things:
        meta, name = t.meta, t.id or t.path.name
        due = as_date(meta.get("due_date"))
        if due and str(meta.get("status", "")) not in TERMINAL_STATUSES:
            days = (due - today).days
            if days < 0 and not meta.get("triggers"):
                hits.append(f"{name}: OVERDUE by {-days}d (due {due}, no trigger declared)")
            elif 0 <= days <= 30:
                hits.append(f"{name}: due in {days}d ({due})")
            elif days > 30:
                horizon.append((days, f"{name}: due {due} ({days}d out)"))

    print(f"## Trigger Evaluation — {root}  ({today})\n")
    if hits:
        for h in hits:
            print(f"- {h}")
    else:
        print("No trigger conditions currently true.")
    if horizon:
        print("\n### Horizon (beyond 30 days)")
        for _, line in sorted(horizon):
            print(f"- {line}")
    if skipped:
        print("\n### Not mechanically evaluable")
        for s in skipped:
            print(f"- {s}")
    return 0
