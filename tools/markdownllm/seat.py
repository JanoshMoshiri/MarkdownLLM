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
of the-record-holds-unattended gave the dispatcher's silence. The window is
declared, not inferred: turns inside a conversation are minutes apart and a
cadence read would ring on every coffee break; the failures on record were
half a day and more.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

from .model import load_schema

SEAT_KEYS = ("mdllm.seat.name", "mdllm.seat.agent", "mdllm.seat.declared")

# The stall window, in hours. Half a day: the shortest unseen turn on the
# 2026-10-14 evidence read was 13 hours, and no healthy conversation on
# record waited that long for a reply.
STALL_HOURS = 12.0

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


def ticket_stalls(repo: Path, seat_name: str = "", now: dt.datetime | None = None,
                  stall_hours: float = STALL_HOURS) -> list[dict]:
    """Open tickets whose last turn is older than the window: {id, status,
    hours, owed_here}. `owed_here` is true when the addressee is this clone's
    seat — the stall is ours to end; otherwise another seat has not risen.
    A ticket in a terminal status owes nothing and is skipped."""
    now = now or dt.datetime.now(dt.timezone.utc)
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
        for line in front.splitlines():
            if _FM_TYPE_RE.match(line):
                is_ticket = True
            m = _FM_STATUS_RE.match(line)
            if m:
                status = m.group(1)
            m = _FM_ID_RE.match(line)
            if m:
                tid = m.group(1)
        if not is_ticket or not status or status in terminal:
            continue
        hours = _hours_since_last_commit(repo, path, now)
        if hours is None or hours <= stall_hours:
            continue
        out.append({"id": tid, "status": status, "hours": hours,
                    "owed_here": bool(seat_name) and status == seat_name})
    return out


def turn_stalls(repo: Path, now: dt.datetime | None = None,
                stall_hours: float = STALL_HOURS, *, seat: dict | None = None,
                up: tuple[int, float] | None | bool = False) -> dict:
    """The stall read: {seat, unpublished, tickets, stall_hours, stalled}.
    `seat` and `up` may be passed in by a caller that already read them, so
    the digest pays its two git spawns once."""
    now = now or dt.datetime.now(dt.timezone.utc)
    seat = seat if seat is not None else read_seat(repo)
    if up is False:
        up = unpublished(repo, now)
    left_stalled = bool(up and up[0] and up[1] > stall_hours)
    tickets = (ticket_stalls(repo, seat["name"], now, stall_hours)
               if declares_tickets(repo) else [])
    return {"seat": seat["name"], "unpublished": up, "tickets": tickets,
            "stall_hours": stall_hours, "stalled": left_stalled or bool(tickets)}


def stall_lines(info: dict) -> list[str]:
    """Attention lines for the stall read; empty when nothing has stalled."""
    lines: list[str] = []
    window = f"{info['stall_hours']:g}h"
    up = info["unpublished"]
    if up and up[0] and up[1] > info["stall_hours"]:
        lines.append(f"- turn stalled: {up[0]} commit(s) unpublished for {up[1]:.0f}h "
                     f"(window {window}) — the addressee cannot see this turn; "
                     f"push it, or say in the record why it waits")
    for t in info["tickets"]:
        who = ("owed by this seat" if t["owed_here"]
               else f"awaiting `{t['status']}`")
        lines.append(f"- turn stalled: `{t['id']}` {who} for {t['hours']:.0f}h "
                     f"(window {window}) — a conversation nobody has risen to; "
                     f"the watch did not ring, or rang and nobody rose "
                     f"(the-seat -> the ring)")
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


def seat_lines(repo: Path, *, loops: bool = False,
               stall_hours: float = STALL_HOURS) -> list[str]:
    """The seat line followed by any stall lines, reading the seat and the
    unpublished range once."""
    seat = read_seat(repo)
    up = unpublished(repo)
    lines = [seat_line(repo, loops=loops, seat=seat, up=up)]
    lines.extend(stall_lines(turn_stalls(repo, stall_hours=stall_hours, seat=seat, up=up)))
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
    stall_hours = float(getattr(args, "stall_hours", None) or STALL_HOURS)
    print(f"## Seat — {repo}")
    seat = read_seat(repo)
    up = unpublished(repo)
    print(seat_line(repo, loops=True, seat=seat, up=up))
    info = turn_stalls(repo, stall_hours=stall_hours, seat=seat, up=up)
    for line in stall_lines(info):
        print(line)
    if getattr(args, "stall_exit", False) and info["stalled"]:
        # The ring: a scheduled task that runs this with --stall-exit can
        # wake the operator on the code alone, the way estate-sync
        # --silence-exit does for the dispatcher.
        return 5
    return 0
