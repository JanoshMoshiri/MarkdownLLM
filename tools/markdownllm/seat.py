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
"""

from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

SEAT_KEYS = ("mdllm.seat.name", "mdllm.seat.agent", "mdllm.seat.declared")


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


def seat_line(repo: Path, *, loops: bool = False) -> str:
    """The digest's line. `loops` says the workspace runs agent-to-agent
    loops (a ticket type, a definition with actors), which is when an
    undeclared seat costs something."""
    seat = read_seat(repo)
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
    print(seat_line(repo, loops=True))
    return 0
