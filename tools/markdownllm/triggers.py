"""Trigger evaluation — time, dependency, and threshold conditions.

Relationship triggers and `blocked_duration` need change history the floor
does not keep; they are reported as not-mechanically-evaluable rather than
silently skipped. Includes the deadline horizon scan over every non-terminal
date-bearing thing.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

from .model import ISO_RE, is_terminal, scan

_DATE_IN_TEXT = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _embedded_date(cond):
    """First ISO date appearing anywhere in a free-text condition, or None."""
    if not isinstance(cond, str):
        return None
    m = _DATE_IN_TEXT.search(cond)
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None


# Lazy membrane reads for `type: import` triggers — crossed at most once per
# evaluation run, and only if such a trigger exists. Cleared at the start of
# every evaluate() so each run reads live state.
_MEMBRANE_CACHE: dict = {}


def _import_states(root: Path) -> dict | None:
    key = ("states", str(root))
    if key not in _MEMBRANE_CACHE:
        try:
            from .imports_check import imports_freshness
            _MEMBRANE_CACHE[key] = {r["id"]: r["state"]
                                    for r in imports_freshness(root)}
        except Exception:
            _MEMBRANE_CACHE[key] = None
    return _MEMBRANE_CACHE[key]


def _porch_coverage(root: Path) -> list | None:
    key = ("porch", str(root))
    if key not in _MEMBRANE_CACHE:
        try:
            from .imports_check import face_coverage
            _MEMBRANE_CACHE[key] = face_coverage(root)
        except Exception:
            _MEMBRANE_CACHE[key] = None
    return _MEMBRANE_CACHE[key]


def evaluate(root: Path) -> tuple[list[str], list[tuple[int, str]], list[str]]:
    """One domain's trigger evaluation: (hits, horizon, skipped)."""
    _MEMBRANE_CACHE.clear()
    corpus, _ = scan(root)
    today = dt.date.today()
    by_id = corpus.by_id()
    hits: list[str] = []
    skipped: list[str] = []
    horizon: list[tuple[int, str]] = []

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
            if ttype in ("time", "date"):
                # `date` is accepted as an alias of `time` — domains write it
                # naturally, and it is one character of drift away from a
                # silently dead control (estate audit FW-1).
                if cond == "due_date_passed":
                    due = as_date(meta.get("due_date"))
                    if due and due < today and not is_terminal(corpus.schema, meta):
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
                else:
                    # Free-text time condition. Recover a date if the condition
                    # names one; otherwise say so instead of falling through
                    # silently (the else below is on TYPE, so it never fires
                    # here — the no-silent-default law, same bug class as the
                    # `relationship` branch one screen down).
                    d = _embedded_date(cond)
                    if d is None:
                        skipped.append(f"{name}: time condition {cond!r} names no "
                                       f"parseable date - left to the agent")
                    elif d <= today and not is_terminal(corpus.schema, meta):
                        hits.append(f"{name}: time condition {cond!r} - date {d} "
                                    f"reached ({(today - d).days}d ago) -> {action}")
                    elif d <= today:
                        pass  # fired, but the thing is already settled
                    elif (d - today).days <= 30:
                        hits.append(f"{name}: time condition {cond!r} - fires in "
                                    f"{(d - today).days}d ({d}) -> {action}")
                    else:
                        horizon.append(((d - today).days,
                                        f"{name}: time condition {cond!r} fires {d} "
                                        f"({(d - today).days}d out)"))
            elif ttype == "dependency":
                watch = tr.get("watch") or []
                watch = watch if isinstance(watch, list) else [watch]
                value = tr.get("value")
                if tr.get("on") == "status_changed_to" and value and watch:
                    states = [str(by_id[w].meta.get("status")) for w in watch if w in by_id]
                    if states and all(s == str(value) for s in states):
                        hits.append(f"{name}: all watched ({', '.join(watch)}) are "
                                    f"`{value}` -> {action}")
                else:
                    # A dependency trigger outside the evaluable shape used to
                    # fall through in silence — the no-silent-default law
                    # violated by the evaluator itself (and masked for months
                    # by the YAML `on:`-is-True key bug parse_frontmatter now
                    # normalizes). Prose conditions route to the agent; a
                    # shapeless declaration is named as such.
                    if tr.get("condition"):
                        skipped.append(f"{name}: dependency trigger with prose "
                                       f"condition {tr.get('condition')!r} — "
                                       f"left to the agent")
                    else:
                        skipped.append(f"{name}: dependency trigger not in the "
                                       f"evaluable shape (`on: status_changed_to` "
                                       f"+ `watch` + `value`) — never fires as "
                                       f"declared")
            elif ttype == "threshold":
                if cond == "subtasks_complete":
                    subs = [e.get("id") for e in meta.get("linked_things") or []
                            if isinstance(e, dict) and e.get("relation") == "subtask"]
                    if subs and all(is_terminal(corpus.schema, by_id[s].meta)
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
            elif ttype == "import":
                # Keyed to the state imports-check computes — a live,
                # consumer-side face read (trigger-specification.md ->
                # Import-based). Lazy: the membrane is crossed at most once
                # per evaluation run, and only if an import trigger exists.
                icond = tr.get("condition") or "state_is"
                if icond == "state_is":
                    states = _import_states(root)
                    if states is None:
                        skipped.append(f"{name}: import trigger — imports "
                                       f"machinery unavailable, state unknown")
                        continue
                    watch = tr.get("watch") or list(states)
                    watch = watch if isinstance(watch, list) else [watch]
                    values = tr.get("value") or ["stale", "diverged", "withdrawn"]
                    values = [str(v) for v in
                              (values if isinstance(values, list) else [values])]
                    unknown = [w for w in watch if w not in states]
                    for w in unknown:
                        skipped.append(f"{name}: import trigger watches `{w}` "
                                       f"but no such import exists here")
                    fired = {w: states[w] for w in watch
                             if w in states and states[w] in values}
                    for w, s in fired.items():
                        hits.append(f"{name}: import `{w}` is {s} -> {action}")
                elif icond == "porch_offers_unimported":
                    cov = _porch_coverage(root)
                    if cov is None:
                        skipped.append(f"{name}: import trigger — face "
                                       f"coverage unavailable")
                        continue
                    src_filter = tr.get("source")
                    for c in cov:
                        if src_filter and c["source"] != str(src_filter):
                            continue
                        if c["state"] == "unreachable":
                            skipped.append(f"{name}: face `{c['source']}` "
                                           f"unreachable — offering unknown")
                        elif (c["offered"] or 0) > c["imported"]:
                            hits.append(f"{name}: face `{c['source']}` offers "
                                        f"{c['offered']}, imported "
                                        f"{c['imported']} -> {action}")
                else:
                    skipped.append(f"{name}: import trigger condition "
                                   f"{icond!r} is not one the floor knows "
                                   f"(state_is, porch_offers_unimported)")
            else:
                skipped.append(f"{name}: unrecognised trigger type `{ttype}` — "
                               f"not evaluated")

    # Deadline scan: every non-terminal date-bearing thing, triggers or not.
    # OVERDUE is never suppressed by a declared trigger — the more carefully
    # authored thing must not get less warning (estate audit FW-1).
    for t in corpus.things:
        meta, name = t.meta, t.id or t.path.name
        due = as_date(meta.get("due_date"))
        if due and not is_terminal(corpus.schema, meta):
            days = (due - today).days
            if days < 0:
                note = "" if meta.get("triggers") else ", no trigger declared"
                hits.append(f"{name}: OVERDUE by {-days}d (due {due}{note})")
            elif 0 <= days <= 30:
                hits.append(f"{name}: due in {days}d ({due})")
            elif days > 30:
                horizon.append((days, f"{name}: due {due} ({days}d out)"))

    return hits, horizon, skipped


def _print_evaluation(hits, horizon, skipped) -> None:
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


def cmd_triggers(args) -> int:
    root = Path(args.path).resolve()
    today = dt.date.today()

    if getattr(args, "estate", False):
        # Operator-axis batch over per-domain evaluations — the estate
        # attention sweep. Roots come from the same local-clone walk
        # estate-sync uses (repos-not-membranes: a filesystem fact, not an
        # estate manifest). Ephemeral roll-up, never an index. Run after
        # `estate-sync` — the sweep is only as honest as the clones are
        # fresh (an-unpulled-checkout-orients-on-a-past-domain).
        from .sync import discover_repos
        repos = discover_repos(root)
        if not repos:
            print(f"triggers --estate: no local clones under {root}")
            return 0
        print(f"## Estate Trigger Sweep — {len(repos)} local clone(s) walked "
              f"({today})\nA filesystem fact, not an estate manifest; "
              f"sync before sweeping.\n")
        total_hits = 0
        rollup = []
        for repo in repos:
            hits, horizon, skipped = evaluate(repo)
            # Retrospective debt joins the sweep (estate-cadence-cluster
            # Phase 2): per-domain the v3.24.0 sensor fires as scatter across
            # thirteen validates; here it lands as one picture in the one
            # sweep the operator's estate loop already reads. Quiet when
            # healthy — the sensor's own young/dormant gates hold.
            retro = ""
            try:
                from .model import scan as _scan
                from .validation import retrospective_findings as _retro
                _corpus, _ = _scan(repo)
                rf = _retro(repo, _corpus)
                if rf:
                    retro = rf[0].message.split(" — ")[0].split(" (")[0]
            except Exception:
                pass
            rollup.append((repo.name, len(hits), len(skipped), retro))
            total_hits += len(hits)
            print(f"### {repo.name}")
            _print_evaluation(hits, horizon, skipped)
            print()
        print("### Roll-up")
        overdue = 0
        for name, nh, ns, retro in rollup:
            line = f"- {name}: {nh} fired, {ns} not mechanically evaluable"
            if retro:
                line += f" — RETROSPECTIVE DEBT: {retro}"
                overdue += 1
            print(line)
        tailbits = [f"{total_hits} trigger(s) fired across the walk"]
        if overdue:
            tailbits.append(f"{overdue} domain(s) owe a retrospective")
        print(f"\n{'; '.join(tailbits)}. Ephemeral — never an index.")
        return 0

    hits, horizon, skipped = evaluate(root)
    print(f"## Trigger Evaluation — {root}  ({today})\n")
    _print_evaluation(hits, horizon, skipped)
    return 0
