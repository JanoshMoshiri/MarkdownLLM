"""The estate's health, read by the floor — `mdllm estate-check --health`.

On 2026-10-24 a session measured fourteen workspaces by reasoning over them:
the share of commits that were maintenance, the age of the fired-trigger
backlog, how long since a retrospective, how much of the insight, conflict
and plan population was still open, how often a cue had been ruled
not-an-inflection, when the dispatcher last filed. Every one is a git or
frontmatter fact, and the floor's own rule — never re-perform a mechanical
check by reasoning — was broken because the floor had no surface that
performed it (`the-record-holds-unattended` Phase 3).

Doctrine, kept: stdout only, no persisted artifact, per repo, every figure
keyed to a same-builder source (git log, frontmatter, the trigger
evaluator, the sync module's digest read). No allow-list anywhere — a line
that could only stay quiet through one would be judgement in mechanical
clothing. Loud lines are marked, not hidden; this is a read the operator or
a retrospective asks for, never a line at t=0.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

from .model import TERMINAL_STATUSES, scan
from .sync import discover_repos, dispatch_silence
from .triggers import TriggerOutcome, evaluate_typed

# Paths a commit may touch and still be maintenance — derived, generated or
# tool-written surfaces, never authored content. A commit is maintenance
# when EVERY path it touched is one of these, or its message carries a
# maintenance prefix the git-workflow conventions reserve. A dotted
# top-level directory is a harness's or a tool's by convention, whichever
# harness it is; naming any of them here would make a neutral module
# vendor-aware.
_MAINTENANCE_PREFIXES = ("things/_index/", "things/cues/", "prompts/")
_MAINTENANCE_FILES = {"kernel.md", "AGENTS.md", ".markdownllm", "CHANGELOG.md"}
_MAINTENANCE_SUBJECTS = re.compile(r"^(refresh|reckon|index|kernel|regen|docs):", re.I)
_DATE_IN_TEXT = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _embedded_date(cond) -> dt.date | None:
    """First ISO date in a free-text trigger condition, or None — the same
    read the evaluator makes of a `time` condition."""
    if not isinstance(cond, str):
        return None
    m = _DATE_IN_TEXT.search(cond)
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None

# The tool's own terminal set, plus the reserved vocabularies' settled
# values for the three populations read here (insight: promoted; the rest
# are already in TERMINAL_STATUSES).
TERMINAL = set(TERMINAL_STATUSES) | {"promoted", "superseded", "retired", "answered"}

# Thresholds the specs already name; a line past one is marked `!`.
RETRO_INTERVAL_DAYS = 60          # validate.thing.md: no retrospective in 60 days
TRIGGER_AGE_DAYS = 30             # a fired trigger older than a month is a backlog
INSIGHTS_SINCE_RETRO = 20         # retrospective.md: volume trigger
CONFLICTS_SINCE_RETRO = 10        # retrospective.md: volume trigger
MAINTENANCE_SHARE = 0.25          # above a quarter, the tax is the work


def _is_maintenance(paths: list[str], subject: str) -> bool:
    if _MAINTENANCE_SUBJECTS.match(subject or ""):
        return True
    if not paths:
        return False
    return all(p in _MAINTENANCE_FILES or p.startswith(_MAINTENANCE_PREFIXES)
               or p.startswith(".")
               for p in paths)


def maintenance_share(root: Path, days: int, today: dt.date | None = None) -> dict | None:
    """{commits, maintenance, share} over the last `days`, or None without git."""
    today = today or dt.date.today()
    since = (today - dt.timedelta(days=days)).isoformat()
    out = subprocess.run(["git", "log", f"--since={since}", "--format=%x1e%cs%x1f%s",
                          "--name-only"], cwd=root, capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    if out.returncode != 0:
        return None
    commits = maint = 0
    for rec in out.stdout.split("\x1e"):
        rec = rec.strip()
        if not rec:
            continue
        head, _, rest = rec.partition("\n")
        subject = head.split("\x1f", 1)[1] if "\x1f" in head else ""
        paths = [p.strip() for p in rest.splitlines() if p.strip()]
        commits += 1
        if _is_maintenance(paths, subject):
            maint += 1
    return {"commits": commits, "maintenance": maint,
            "share": (maint / commits) if commits else 0.0}


def fired_backlog(root: Path, today: dt.date | None = None) -> dict:
    """{fired, oldest_days, over_month} from the trigger evaluator."""
    today = today or dt.date.today()
    ages = []
    fired = 0
    for r in evaluate_typed(root).results:
        if r.outcome is not TriggerOutcome.FIRED:
            continue
        fired += 1
        d = _embedded_date(r.condition)
        if d:
            ages.append((today - d).days)
    return {"fired": fired, "oldest_days": max(ages) if ages else None,
            "over_month": sum(1 for a in ages if a > TRIGGER_AGE_DAYS)}


def _date(v) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except (TypeError, ValueError):
        return None


def population(corpus, today: dt.date | None = None) -> dict:
    """Open ratios, cue precision, retrospective age — frontmatter facts."""
    today = today or dt.date.today()
    counts: dict[str, dict] = {}
    cues_answered = cues_not_infl = cues_open = 0
    last_retro: dt.date | None = None
    for t in corpus.things:
        typ = str(t.meta.get("type") or "")
        status = str(t.meta.get("status") or "")
        if typ in ("insight", "conflict", "plan"):
            c = counts.setdefault(typ, {"total": 0, "open": 0})
            c["total"] += 1
            if status not in TERMINAL:
                c["open"] += 1
        elif typ == "cue":
            if status == "answered":
                cues_answered += 1
                if str(t.meta.get("verdict") or "") == "not-inflection":
                    cues_not_infl += 1
            else:
                cues_open += 1
        elif typ == "retrospective":
            d = _date(t.meta.get("period_end")) or _date(t.meta.get("created"))
            if d and (last_retro is None or d > last_retro):
                last_retro = d
    since_retro = {"insights": 0, "conflicts": 0}
    if last_retro:
        for t in corpus.things:
            typ = str(t.meta.get("type") or "")
            d = _date(t.meta.get("created"))
            if d and d > last_retro:
                if typ == "insight":
                    since_retro["insights"] += 1
                elif typ == "conflict":
                    since_retro["conflicts"] += 1
    return {"counts": counts,
            "cues": {"answered": cues_answered, "not_inflection": cues_not_infl,
                     "open": cues_open},
            "retro_age": (today - last_retro).days if last_retro else None,
            "since_retro": since_retro}


def health(root: Path, today: dt.date | None = None) -> dict:
    """Every measurement for one repo, in one dict; rendering is separate so
    a test can read the figures without parsing prose."""
    root = Path(root).resolve()
    today = today or dt.date.today()
    corpus, _ = scan(root)
    return {
        "repo": root.name,
        "maintenance_30": maintenance_share(root, 30, today),
        "maintenance_90": maintenance_share(root, 90, today),
        "triggers": fired_backlog(root, today),
        "population": population(corpus, today),
        "dispatch": dispatch_silence([root], today=today),
    }


def _pct(x: float) -> str:
    return f"{round(x * 100)}%"


def render(h: dict) -> list[str]:
    """Lines for one repo. A `!` marks a figure past the threshold its spec
    names; nothing is hidden, nothing is ranked by opinion."""
    out = [f"### {h['repo']}"]
    for key, days in (("maintenance_30", 30), ("maintenance_90", 90)):
        m = h[key]
        if m is None:
            out.append(f"- maintenance share ({days}d): git history unreadable")
            continue
        mark = "!" if m["commits"] and m["share"] > MAINTENANCE_SHARE else "-"
        out.append(f"{mark} maintenance share ({days}d): {m['maintenance']}/{m['commits']} "
                   f"commits ({_pct(m['share'])}) touched only generated or "
                   f"tool-written surfaces")
    t = h["triggers"]
    mark = "!" if t["over_month"] else "-"
    oldest = f"oldest {t['oldest_days']}d" if t["oldest_days"] is not None else "no dated condition"
    out.append(f"{mark} fired triggers: {t['fired']} ({oldest}; {t['over_month']} older "
               f"than {TRIGGER_AGE_DAYS}d)")
    p = h["population"]
    ra = p["retro_age"]
    mark = "!" if ra is None or ra > RETRO_INTERVAL_DAYS else "-"
    out.append(f"{mark} last retrospective: "
               + (f"{ra}d ago" if ra is not None else "none on record")
               + (f"; since then {p['since_retro']['insights']} insights, "
                  f"{p['since_retro']['conflicts']} conflicts"
                  if ra is not None else ""))
    if ra is not None and (p["since_retro"]["insights"] > INSIGHTS_SINCE_RETRO
                           or p["since_retro"]["conflicts"] > CONFLICTS_SINCE_RETRO):
        out[-1] = "!" + out[-1][1:]
    for typ, label in (("insight", "insights active"), ("conflict", "conflicts open"),
                       ("plan", "plans open")):
        c = p["counts"].get(typ)
        if c:
            out.append(f"- {label}: {c['open']}/{c['total']} ({_pct(c['open'] / c['total'])})")
    cu = p["cues"]
    if cu["answered"] or cu["open"]:
        prec = (f"{cu['not_inflection']}/{cu['answered']} answered ruled "
                f"not-inflection ({_pct(cu['not_inflection'] / cu['answered'])})"
                if cu["answered"] else "none answered")
        out.append(f"- cues: {prec}; {cu['open']} open")
    d = h["dispatch"]
    if d:
        mark = "!" if d["silent"] else "-"
        out.append(f"{mark} dispatch: last digest {d['age']}d ago ({d['last']}; "
                   f"cadence observed {d['cadence']}d)"
                   + (" — silent" if d["silent"] else ""))
    return out


def cmd_estate_health(args) -> int:
    """`mdllm estate-check --health`: the same roots estate-check walks —
    named explicitly, or the local clones — and the health read instead of
    the membrane. Dispatched from the CLI, not from imports_check, so the
    membrane module never depends on this one."""
    if args.paths:
        roots = [Path(p).resolve() for p in args.paths]
    else:
        roots = discover_repos(Path(".").resolve())
        if not roots:
            print("estate-check: no local clones found to walk")
            return 0
    missing = [r for r in roots if not r.is_dir()]
    if missing:
        print("estate-check: not a directory: " + ", ".join(str(m) for m in missing))
        return 1
    print("\n".join(render_health(roots)))
    return 0


def render_health(roots: list[Path], today: dt.date | None = None) -> list[str]:
    lines = [f"## Estate Health — {len(roots)} repo(s); `!` marks a figure past the "
             f"threshold its spec names", ""]
    for r in roots:
        lines.extend(render(health(r, today)))
        lines.append("")
    lines.append("Every figure is a git or frontmatter fact, read now and kept "
                 "nowhere — this view is never an index. Maintenance = every path "
                 "generated or tool-written, or a refresh/reckon/index/kernel/docs "
                 "subject.")
    return lines
