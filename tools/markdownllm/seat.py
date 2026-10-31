"""`mdllm seat` — the seat: one agent, in one clone, on one framework, under
one git identity (seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15).

The live record (read 2026-10-14) showed that three of the four largest
causes of agent-to-agent trouble were seats nothing checked: two clones on
different framework versions rewriting one generated block in turns; two
agents in one working copy colliding on the git index; and turns committed
in a clone and never published, invisible to their addressee for hours. All
of it was invisible in the record because every agent committed under the
operator's git identity.

A seat is declared in the clone, never in the corpus — clones share a corpus
and a seat is a property of one of them — as clone-local git config, the way
`mdllm.sync` and `mdllm.publication` already are:

    mdllm.seat.name      the actor name the workspace's loops know it by
    mdllm.seat.agent     the harness or product that sits there (free text)
    mdllm.seat.declared  the date it was declared
    user.name / user.email   set to the seat, so every commit says who sat

The floor reads it: the session-start digest says which seat this clone is
and whether a turn it committed never left; doctor warns when a workspace
that runs loops has an undeclared seat. The floor never declares a seat —
only the agent arriving in the clone can know who it is.

The stall ring (the-seat Phase 7, 2026-10-30). The second-largest cause —
turns that never left, 35 and 13 hours unseen — was named at the next
session start, which is when somebody arrives, and the record of every
attempt says the intervention it then took was the costliest of all. So the
same read now rings: a commit unpublished, or an open ticket unanswered, for
longer than a declared window is a *stalled turn*, printed as an attention
line at session start and in estate-sync, and `--stall-exit` returns 5 so a
scheduled task can wake the operator on the code alone — the shape Phase 2
of the-record-holds-unattended gave the dispatcher's silence.

Two thresholds, both declared. The first cut set the window at twelve
hours from the failures on record, and the operator corrected it the same
day: the turns that wait half a day are the ones the loop has finished and
nobody closed, and the ones that need attending are an hour apart or less.
The busiest workspace's tickets said the same (783 turn gaps on 87 tickets,
2026-09-25 to 10-30): a reply from the other seat arrives in a median of
five minutes, 90% within about an hour, 95% within four. So the *window*
(`STALL_HOURS`, 1h) rings on a conversation that has gone quiet while it
was alive, and the *ceiling* (`ABANDON_HOURS`, 24h) stops ringing: a ticket
open past it is reported once as abandoned — close it or reopen it — never
rung about, because a ring that fires on every forgotten ticket teaches the
operator to ignore the ring. A clone may declare both in local config
(`mdllm.seat.stall-hours`, `mdllm.seat.abandon-hours`); flags override.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

from .model import load_schema

SEAT_KEYS = ("mdllm.seat.name", "mdllm.seat.agent", "mdllm.seat.declared")

# The stall window and the abandonment ceiling, in hours. One hour is past
# the 90th percentile of healthy replies on the busiest workspace's record;
# a day is past everything the record shows a live conversation doing.
STALL_HOURS = 1.0
ABANDON_HOURS = 24.0
_CFG_STALL = "mdllm.seat.stall-hours"
_CFG_ABANDON = "mdllm.seat.abandon-hours"

# The turn budget: the number of turns a conversation may take before the
# floor says so. The exogenous stop an agent inside a loop never asks for
# (an-agent-in-a-loop-optimises-the-loop-not-the-goal), made a line at
# session start rather than a question the operator must remember. The
# operator set the number on 2026-10-31: "120 sounds like a good number".
# A ticket may declare its own `turn_budget` (declare the field in the
# schema's known_fields); a clone may set `mdllm.seat.turn-budget`.
TURN_BUDGET = 120
_CFG_BUDGET = "mdllm.seat.turn-budget"
_FM_BUDGET_RE = re.compile(r"^\s*turn_budget:\s*['\"]?(\d+)")

# Tickets by name, the way the dispatch read finds digests: the template
# names them `ticket-<item>`, so a seat read pays for a handful of
# frontmatter heads and never a corpus walk.
_TICKET_GLOB = "things/**/ticket*.md"
_FM_TYPE_RE = re.compile(r"^\s*type:\s*['\"]?ticket\b")
_FM_STATUS_RE = re.compile(r"^\s*status:\s*['\"]?([^'\"\s#]+)")
_FM_ID_RE = re.compile(r"^\s*id:\s*['\"]?([^'\"\s#]+)")


def _run(repo: Path, *args: str, timeout: int = 20):
    try:
        return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout)
    except Exception:
        return None


def read_seat(repo: Path) -> dict:
    """{name, agent, declared, user_name, user_email} from the clone's local
    config, one git spawn; empty strings for what is not set."""
    out = {"name": "", "agent": "", "declared": "", "user_name": "", "user_email": ""}
    r = _run(repo, "config", "--local", "--get-regexp", r"^(mdllm\.seat\.|user\.)")
    if r is None or r.returncode not in (0, 1):
        return out
    for line in (r.stdout or "").splitlines():
        key, _, value = line.partition(" ")
        key = key.strip().lower()
        value = value.strip()
        if key == "mdllm.seat.name":
            out["name"] = value
        elif key == "mdllm.seat.agent":
            out["agent"] = value
        elif key == "mdllm.seat.declared":
            out["declared"] = value
        elif key == "user.name":
            out["user_name"] = value
        elif key == "user.email":
            out["user_email"] = value
    return out


def unpublished(repo: Path, now: dt.datetime | None = None) -> tuple[int, float] | None:
    """(count, hours since the oldest) of commits on the checked-out branch
    that its upstream does not have — a turn that never left. None when the
    branch has no upstream or git cannot say. One git spawn."""
    # A rev-list over the unpublished range only: bounded by the turns that
    # never left, never by the corpus (session start's walk budget holds).
    r = _run(repo, "rev-list", "--timestamp", "@{upstream}..HEAD")
    if r is None or r.returncode != 0:
        return None
    stamps = [int(ln.split()[0]) for ln in (r.stdout or "").splitlines()
              if ln.split() and ln.split()[0].isdigit()]
    if not stamps:
        return 0, 0.0
    now = now or dt.datetime.now(dt.timezone.utc)
    oldest = dt.datetime.fromtimestamp(min(stamps), dt.timezone.utc)
    return len(stamps), max(0.0, (now - oldest).total_seconds() / 3600)


def stall_thresholds(repo: Path, stall_hours: float | None = None,
                     abandon_hours: float | None = None) -> tuple[float, float]:
    """(window, ceiling) in hours: an explicit argument, else the clone's
    local config, else the defaults. The ceiling is never below the window."""
    cfg = {}
    cfg = _seat_config(repo)
    window = stall_hours if stall_hours is not None else cfg.get(_CFG_STALL, STALL_HOURS)
    ceiling = abandon_hours if abandon_hours is not None else cfg.get(_CFG_ABANDON, ABANDON_HOURS)
    return float(window), max(float(ceiling), float(window))


def _seat_config(repo: Path) -> dict:
    """The clone's numeric seat settings, one git spawn."""
    cfg: dict = {}
    r = _run(repo, "config", "--local", "--get-regexp",
             r"^mdllm\.seat\.(stall-hours|abandon-hours|turn-budget)$")
    if r is not None and r.returncode in (0, 1):
        for line in (r.stdout or "").splitlines():
            key, _, value = line.partition(" ")
            try:
                cfg[key.strip().lower()] = float(value.strip())
            except ValueError:
                continue
    return cfg


def turn_budget(repo: Path, explicit: int | None = None) -> int:
    """The clone's default budget: an explicit argument, else local config,
    else TURN_BUDGET. A ticket's own `turn_budget` overrides per ticket."""
    if explicit is not None:
        return max(1, int(explicit))
    cfg = _seat_config(repo)
    if _CFG_BUDGET in cfg:
        return max(1, int(cfg[_CFG_BUDGET]))
    return TURN_BUDGET


def declares_tickets(repo: Path) -> bool:
    """Does this workspace run agent-to-agent loops? The ticket type is the
    carrier every such loop uses (standing-watch.md -> The Ticket)."""
    try:
        schema = load_schema(repo)
    except Exception:
        return False
    types = schema.get("types") if isinstance(schema, dict) else None
    return isinstance(types, dict) and "ticket" in types


def _terminal_ticket_statuses(repo: Path) -> set:
    try:
        schema = load_schema(repo)
    except Exception:
        return {"closed"}
    types = schema.get("types") if isinstance(schema, dict) else None
    ticket = types.get("ticket") if isinstance(types, dict) else None
    terminal = ticket.get("terminal_statuses") if isinstance(ticket, dict) else None
    return {str(s) for s in terminal} if terminal else {"closed"}


def _hours_since_last_commit(repo: Path, path: Path, now: dt.datetime) -> float | None:
    """Hours since the commit that last touched `path`; None when it has
    never been committed (a turn written and not yet taken)."""
    rel = path.resolve().relative_to(repo.resolve()).as_posix()
    r = _run(repo, "log", "-1", "--format=%ct", "--", rel)
    if r is None or r.returncode != 0 or not (r.stdout or "").strip().isdigit():
        return None
    stamp = dt.datetime.fromtimestamp(int(r.stdout.strip()), dt.timezone.utc)
    return max(0.0, (now - stamp).total_seconds() / 3600)


def _open_tickets(repo: Path) -> list[dict]:
    """Every open ticket by name: {path, id, status, turn_budget}. A ticket in
    a terminal status owes nothing and is skipped."""
    terminal = _terminal_ticket_statuses(repo)
    out: list[dict] = []
    for path in sorted(repo.glob(_TICKET_GLOB)):
        try:
            head = path.read_text(encoding="utf-8", errors="replace")[:4000]
        except OSError:
            continue
        if not head.startswith("---"):
            continue
        front = head.split("\n---", 1)[0]
        is_ticket = False
        status = ""
        tid = path.stem
        budget = None
        for line in front.splitlines():
            if _FM_TYPE_RE.match(line):
                is_ticket = True
            m = _FM_STATUS_RE.match(line)
            if m:
                status = m.group(1)
            m = _FM_ID_RE.match(line)
            if m:
                tid = m.group(1)
            m = _FM_BUDGET_RE.match(line)
            if m:
                budget = int(m.group(1))
        if not is_ticket or not status or status in terminal:
            continue
        out.append({"path": path, "id": tid, "status": status, "turn_budget": budget})
    return out


def ticket_stalls(repo: Path, seat_name: str = "", now: dt.datetime | None = None,
                  stall_hours: float = STALL_HOURS) -> list[dict]:
    """Open tickets whose last turn is older than the window: {id, status,
    hours, owed_here}. `owed_here` is true when the addressee is this clone's
    seat — the stall is ours to end; otherwise another seat has not risen.
    The caller splits the result at the ceiling into stalled and abandoned."""
    now = now or dt.datetime.now(dt.timezone.utc)
    out: list[dict] = []
    for t in _open_tickets(repo):
        hours = _hours_since_last_commit(repo, t["path"], now)
        if hours is None or hours <= stall_hours:
            continue
        out.append({"id": t["id"], "status": t["status"], "hours": hours,
                    "owed_here": bool(seat_name) and t["status"] == seat_name})
    return out


def _turns_taken(repo: Path, path: Path) -> int | None:
    """The turns a ticket has taken: the commits that touched it. None when
    it has never been committed."""
    rel = path.resolve().relative_to(repo.resolve()).as_posix()
    r = _run(repo, "rev-list", "--count", "HEAD", "--", rel)
    if r is None or r.returncode != 0 or not (r.stdout or "").strip().isdigit():
        return None
    return int(r.stdout.strip())


def ticket_budgets(repo: Path, default_budget: int = TURN_BUDGET) -> list[dict]:
    """Open tickets at or past their turn budget: {id, status, turns, budget}.
    The budget is the ticket's own `turn_budget` when it declares one, else
    the clone's default. Counted from the record — every commit that touched
    the ticket is a turn — so the number is the floor's, not a counter an
    agent maintains."""
    out: list[dict] = []
    for t in _open_tickets(repo):
        turns = _turns_taken(repo, t["path"])
        if turns is None:
            continue
        budget = t["turn_budget"] or default_budget
        if turns >= budget:
            out.append({"id": t["id"], "status": t["status"], "turns": turns,
                        "budget": budget})
    return out


def _age(hours: float) -> str:
    if hours < 1:
        return f"{hours * 60:.0f}m"
    if hours < 48:
        return f"{hours:.0f}h"
    return f"{hours / 24:.0f}d"


def turn_stalls(repo: Path, now: dt.datetime | None = None,
                stall_hours: float | None = None, abandon_hours: float | None = None,
                budget: int | None = None, *, seat: dict | None = None,
                up: tuple[int, float] | None | bool = False) -> dict:
    """The stall read: {seat, unpublished, tickets, abandoned, over_budget,
    stall_hours, abandon_hours, turn_budget, stalled}. `tickets` are open
    tickets quiet for longer than the window and no longer than the ceiling
    — a live conversation that has stopped, which is what rings. `abandoned`
    are open tickets quiet past the ceiling — a loop that finished and was
    never closed, reported and never rung. `over_budget` are open tickets at
    or past their turn budget — the loop optimising the loop, which rings.
    `seat` and `up` may be passed in by a caller that already read them, so
    the digest pays its two git spawns once."""
    now = now or dt.datetime.now(dt.timezone.utc)
    window, ceiling = stall_thresholds(repo, stall_hours, abandon_hours)
    default_budget = turn_budget(repo, budget)
    seat = seat if seat is not None else read_seat(repo)
    if up is False:
        up = unpublished(repo, now)
    left_stalled = bool(up and up[0] and up[1] > window)
    loops = declares_tickets(repo)
    quiet = ticket_stalls(repo, seat["name"], now, window) if loops else []
    over = ticket_budgets(repo, default_budget) if loops else []
    tickets = [t for t in quiet if t["hours"] <= ceiling]
    abandoned = [t for t in quiet if t["hours"] > ceiling]
    return {"seat": seat["name"], "unpublished": up, "tickets": tickets,
            "abandoned": abandoned, "over_budget": over,
            "stall_hours": window, "abandon_hours": ceiling,
            "turn_budget": default_budget,
            "stalled": left_stalled or bool(tickets) or bool(over)}


def stall_lines(info: dict) -> list[str]:
    """Attention lines for the stall read; empty when nothing has stalled
    or been abandoned."""
    lines: list[str] = []
    window = f"{info['stall_hours']:g}h"
    up = info["unpublished"]
    if up and up[0] and up[1] > info["stall_hours"]:
        lines.append(f"- turn stalled: {up[0]} commit(s) unpublished for {_age(up[1])} "
                     f"(window {window}) — the addressee cannot see this turn; "
                     f"push it, or say in the record why it waits")
    for t in info["tickets"]:
        who = ("owed by this seat" if t["owed_here"]
               else f"awaiting `{t['status']}`")
        lines.append(f"- turn stalled: `{t['id']}` {who} for {_age(t['hours'])} "
                     f"(window {window}) — a live conversation has stopped; "
                     f"the watch did not ring, or rang and nobody rose "
                     f"(the-seat -> the ring)")
    for t in info.get("over_budget") or []:
        lines.append(f"- turn budget reached: `{t['id']}` at {t['turns']} turns "
                     f"(budget {t['budget']}; addressee `{t['status']}`) — a "
                     f"conversation this long is the loop optimising the loop, not "
                     f"the goal; conclude it, split the item, or raise the budget "
                     f"deliberately (`turn_budget` on the ticket, or "
                     f"`mdllm.seat.turn-budget` in the clone) "
                     f"(an-agent-in-a-loop-optimises-the-loop-not-the-goal)")
    if info.get("abandoned"):
        ids = ", ".join(f"`{t['id']}`" for t in info["abandoned"])
        oldest = max(t["hours"] for t in info["abandoned"])
        lines.append(f"- tickets abandoned ({len(info['abandoned'])}, the oldest "
                     f"{_age(oldest)} quiet; ceiling {info['abandon_hours']:g}h): {ids} — "
                     f"open past the ceiling, so the loop finished and nobody closed "
                     f"it, or it was forgotten; close or reopen, this never rings")
    return lines


def seat_line(repo: Path, *, loops: bool = False, seat: dict | None = None,
              up: tuple[int, float] | None | bool = False) -> str:
    """The digest's line. `loops` says the workspace runs agent-to-agent
    loops (a ticket type, a definition with actors), which is when an
    undeclared seat costs something."""
    seat = seat if seat is not None else read_seat(repo)
    if up is False:
        up = unpublished(repo)
    if up is None:
        left = "no upstream — nothing published from this branch"
    elif up[0] == 0:
        left = "nothing unpublished"
    else:
        n, hours = up
        age = f"{hours:.0f}h" if hours >= 1 else f"{hours * 60:.0f}m"
        left = (f"{n} commit(s) unpublished, the oldest {age} ago — a turn that "
                "never left; pull, merge, push before taking another")
    if seat["name"]:
        who = seat["name"] + (f" ({seat['agent']})" if seat["agent"] else "")
        return f"- **Seat:** {who}, declared {seat['declared'] or '?'} · {left}"
    identity = seat["user_name"] or "(no local user.name)"
    tail = (" — every seat in this workspace commits under the operator's name "
            "and the record cannot tell them apart; declare yours: "
            "`mdllm seat . --set <actor> --agent <harness>`" if loops else
            " — declare one when this clone takes turns in a loop: "
            "`mdllm seat . --set <actor> --agent <harness>`")
    return f"- **Seat: undeclared** — this clone commits as {identity}{tail} · {left}"


def seat_lines(repo: Path, *, loops: bool = False) -> list[str]:
    """The seat line followed by any stall lines, reading the seat and the
    unpublished range once. Thresholds come from the clone's config or the
    defaults."""
    seat = read_seat(repo)
    up = unpublished(repo)
    lines = [seat_line(repo, loops=loops, seat=seat, up=up)]
    lines.extend(stall_lines(turn_stalls(repo, seat=seat, up=up)))
    return lines


def set_seat(repo: Path, name: str, agent: str, email: str | None = None,
             today: dt.date | None = None) -> dict:
    """Declare the seat: the three mdllm.seat keys and the git identity, all
    clone-local. Returns what was written. Raises ValueError on a bad name."""
    name = (name or "").strip()
    if not name or any(ch.isspace() for ch in name):
        raise ValueError("a seat name is one word — the actor name the loops use")
    agent = (agent or "").strip()
    email = (email or "").strip() or f"{name}@seat.local"
    today = today or dt.date.today()
    writes = {
        "mdllm.seat.name": name,
        "mdllm.seat.agent": agent,
        "mdllm.seat.declared": today.isoformat(),
        "user.name": name,
        "user.email": email,
    }
    for key, value in writes.items():
        r = _run(repo, "config", "--local", key, value)
        if r is None or r.returncode != 0:
            raise ValueError(f"git could not write {key} in {repo}: "
                             f"{(r.stderr if r else '').strip() or 'timeout'}")
    return writes


def clear_seat(repo: Path) -> None:
    for key in SEAT_KEYS:
        _run(repo, "config", "--local", "--unset", key)


def cmd_seat(args) -> int:
    repo = Path(args.path).resolve()
    if _run(repo, "rev-parse", "--git-dir") is None or \
            _run(repo, "rev-parse", "--git-dir").returncode != 0:
        print(f"mdllm: seat — {repo} is not a git repository")
        return 2
    if getattr(args, "set", None):
        try:
            writes = set_seat(repo, args.set, getattr(args, "agent", "") or "",
                              getattr(args, "email", None))
        except ValueError as exc:
            print(f"mdllm: seat set — {exc}")
            return 2
        print(f"seat declared in {repo}: {writes['mdllm.seat.name']}"
              + (f" ({writes['mdllm.seat.agent']})" if writes["mdllm.seat.agent"] else "")
              + f" — commits from this clone now carry `{writes['user.name']} "
              f"<{writes['user.email']}>`; the git identity is clone-local and "
              "nothing outside this clone changed")
        return 0
    if getattr(args, "clear", False):
        clear_seat(repo)
        print(f"seat cleared in {repo} (user.name/user.email left as they are)")
        return 0
    print(f"## Seat — {repo}")
    seat = read_seat(repo)
    up = unpublished(repo)
    print(seat_line(repo, loops=True, seat=seat, up=up))
    info = turn_stalls(repo, stall_hours=getattr(args, "stall_hours", None),
                       abandon_hours=getattr(args, "abandon_hours", None),
                       budget=getattr(args, "turn_budget", None),
                       seat=seat, up=up)
    for line in stall_lines(info):
        print(line)
    if getattr(args, "stall_exit", False) and info["stalled"]:
        # The ring: a scheduled task that runs this with --stall-exit can
        # wake the operator on the code alone, the way estate-sync
        # --silence-exit does for the dispatcher.
        return 5
    return 0
