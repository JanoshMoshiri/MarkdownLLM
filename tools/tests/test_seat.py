"""The seat (seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15;
the-seat Phases 1 and 2): `mdllm seat` declares who sits in a clone, the
digest says so and names a turn that never left, and a clone whose framework
is behind the one that generated a workspace's blocks refuses to regenerate
them and reads the difference as *behind*, never drift.

Run: python -m pytest tools/tests/test_seat.py -q
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_harness import _sync_git, thing_text, write  # noqa: E402

FW = Path(__file__).resolve().parents[2]


def _commit(root: Path, msg: str, day: str = "2026-10-15", from_config: bool = False) -> str:
    env = {**os.environ, "GIT_AUTHOR_DATE": f"{day}T12:00:00",
           "GIT_COMMITTER_DATE": f"{day}T12:00:00"}
    if from_config:  # let the clone's own user.name/email speak, not the harness's env
        for k in ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME",
                  "GIT_COMMITTER_EMAIL"):
            env.pop(k, None)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=root, check=True, env=env)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                          text=True).stdout.strip()


def _repo(tmp_path: Path, name: str = "ws") -> Path:
    root = tmp_path / name
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    write(root, "things/a.md", thing_text("id: a\ntype: task\nstatus: in-progress\ncreated: 2026-10-01"))
    _commit(root, "seed")
    return root


# ------------------------------------------------------------------ the seat

def test_set_declares_the_seat_and_the_clone_identity_locally(tmp_path):
    from markdownllm.seat import read_seat, set_seat
    root = _repo(tmp_path)
    before_global = subprocess.run(["git", "config", "--global", "--get", "user.name"],
                                   capture_output=True, text=True).stdout.strip()
    writes = set_seat(root, "codex", "codex-cli", today=dt.date(2026, 10, 15))
    assert writes["user.name"] == "codex" and writes["user.email"] == "codex@seat.local"
    seat = read_seat(root)
    assert seat == {"name": "codex", "agent": "codex-cli", "declared": "2026-10-15",
                    "user_name": "codex", "user_email": "codex@seat.local"}
    # Clone-local: the global identity is untouched.
    after_global = subprocess.run(["git", "config", "--global", "--get", "user.name"],
                                  capture_output=True, text=True).stdout.strip()
    assert after_global == before_global
    # And the next commit in this clone carries the seat.
    write(root, "things/b.md", thing_text("id: b\ntype: task\nstatus: in-progress\ncreated: 2026-10-01"))
    _commit(root, "a turn", from_config=True)
    author = subprocess.run(["git", "log", "-1", "--format=%an <%ae>"], cwd=root,
                            capture_output=True, text=True).stdout.strip()
    assert author == "codex <codex@seat.local>"


def test_a_seat_name_is_one_word(tmp_path):
    import pytest
    from markdownllm.seat import set_seat
    root = _repo(tmp_path)
    for bad in ("", "  ", "two words"):
        with pytest.raises(ValueError):
            set_seat(root, bad, "x")


def test_clear_withdraws_the_declaration_but_keeps_the_identity(tmp_path):
    from markdownllm.seat import clear_seat, read_seat, set_seat
    root = _repo(tmp_path)
    set_seat(root, "claude", "claude-code")
    clear_seat(root)
    seat = read_seat(root)
    assert seat["name"] == "" and seat["agent"] == "" and seat["declared"] == ""
    assert seat["user_name"] == "claude"


def test_unpublished_counts_the_turns_the_upstream_lacks(tmp_path):
    from markdownllm.seat import unpublished
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
    root = _repo(tmp_path)
    assert unpublished(root) is None  # no upstream yet
    subprocess.run(["git", "remote", "add", "origin", str(origin)], cwd=root, check=True)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                            capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "push", "-q", "-u", "origin", branch], cwd=root, check=True)
    assert unpublished(root) == (0, 0.0)
    write(root, "things/b.md", thing_text("id: b\ntype: task\nstatus: in-progress\ncreated: 2026-10-01"))
    _commit(root, "a turn that never left", "2026-10-14")
    n, hours = unpublished(root, now=dt.datetime(2026, 10, 15, 1, 0, tzinfo=dt.timezone.utc))
    assert n == 1 and 12 <= hours <= 14


def test_seat_line_names_the_seat_or_asks_for_one(tmp_path):
    from markdownllm.seat import seat_line, set_seat
    root = _repo(tmp_path)
    line = seat_line(root, loops=True)
    assert line.startswith("- **Seat: undeclared**")
    assert "cannot tell them apart" in line and "mdllm seat . --set" in line
    assert seat_line(root, loops=False).startswith("- **Seat: undeclared**")
    assert "cannot tell them apart" not in seat_line(root, loops=False)
    set_seat(root, "haze", "hermes", today=dt.date(2026, 10, 15))
    line = seat_line(root)
    assert line.startswith("- **Seat:** haze (hermes), declared 2026-10-15")
    assert "no upstream" in line


def test_session_start_carries_the_seat_line(tmp_path, capsys):
    import yaml
    from markdownllm.session import cmd_session_start
    root = _repo(tmp_path)
    write(root, "things/_schema.yaml", yaml.safe_dump({
        "schema_version": 1, "domain": "x",
        "types": {"task": {"statuses": ["in-progress", "done"]},
                  "ticket": {"statuses": ["a", "b", "closed"], "terminal_statuses": ["closed"]}}},
        sort_keys=False))
    _commit(root, "schema")
    assert cmd_session_start(argparse.Namespace(path=str(root))) == 0
    out = capsys.readouterr().out
    assert "**Seat: undeclared**" in out and "cannot tell them apart" in out


def test_seat_cli_reads_sets_and_refuses(tmp_path, capsys):
    from markdownllm.seat import cmd_seat
    root = _repo(tmp_path)
    assert cmd_seat(argparse.Namespace(path=str(root), set=None, agent="", email=None,
                                       clear=False)) == 0
    assert "Seat: undeclared" in capsys.readouterr().out
    assert cmd_seat(argparse.Namespace(path=str(root), set="codex", agent="codex-cli",
                                       email=None, clear=False)) == 0
    assert "seat declared" in capsys.readouterr().out
    assert cmd_seat(argparse.Namespace(path=str(root), set="two words", agent="",
                                       email=None, clear=False)) == 2
    assert cmd_seat(argparse.Namespace(path=str(tmp_path / "nowhere"), set=None,
                                       agent="", email=None, clear=False)) == 2


# ------------------------------------------------------------- the guard

def _framework(tmp_path: Path) -> Path:
    """A tiny framework clone: a sentinel and a git history to be behind."""
    fw = tmp_path / "fw"
    (fw / "tools").mkdir(parents=True)
    _sync_git(fw, "init", "-q")
    (fw / ".markdownllm").write_text("version: 3.47.0\n", encoding="utf-8")
    _commit(fw, "release 3.47.0")
    return fw


def _workspace(tmp_path: Path, fw: Path, seen: str = "3.47.0") -> Path:
    ws = tmp_path / "fw" / "domain" / "ws"
    (ws / "things").mkdir(parents=True)
    _sync_git(ws, "init", "-q")
    write(ws, "AGENTS.md",
          f"---\nid: ws-agent\nframework_root: ../..\nframework_version_seen: {seen}\n---\n"
          "# WS\n\n<!-- generated:types -->\nold\n<!-- /generated:types -->\n")
    write(ws, "things/_schema.yaml", "schema_version: 1\ndomain: ws\ntypes:\n  task:\n    statuses: [open]\n")
    _commit(ws, "seed")
    return ws


def _meta(ws: Path) -> dict:
    from markdownllm.model import parse_frontmatter
    meta, _, _ = parse_frontmatter((ws / "AGENTS.md").read_text(encoding="utf-8"))
    return meta or {}


def test_a_clone_at_the_generating_commit_or_after_may_regenerate(tmp_path):
    from markdownllm.domain_kernel import (framework_head, kernel_source_check,
                                           set_kernel_source)
    fw = _framework(tmp_path)
    ws = _workspace(tmp_path, fw)
    assert kernel_source_check(ws, _meta(ws)) == ("ok", "")  # nothing recorded yet
    text = set_kernel_source((ws / "AGENTS.md").read_text(encoding="utf-8"), ws, _meta(ws))
    assert f"framework_kernel_from: {framework_head(fw)}" in text
    (ws / "AGENTS.md").write_text(text, encoding="utf-8")
    assert kernel_source_check(ws, _meta(ws)) == ("ok", "")  # same commit
    (fw / "tools" / "x").write_text("later\n", encoding="utf-8")
    _commit(fw, "a later framework commit")
    assert kernel_source_check(ws, _meta(ws)) == ("ok", "")  # descends from it


def test_a_clone_behind_the_generating_commit_refuses_and_is_not_drift(tmp_path, capsys):
    from markdownllm.domain_kernel import (cmd_domain_kernel, framework_head,
                                           kernel_source_check, set_kernel_source)
    fw = _framework(tmp_path)
    ws = _workspace(tmp_path, fw)
    old_head = framework_head(fw)
    (fw / "tools" / "x").write_text("later\n", encoding="utf-8")
    _commit(fw, "the newer framework")
    text = set_kernel_source((ws / "AGENTS.md").read_text(encoding="utf-8"), ws, _meta(ws))
    (ws / "AGENTS.md").write_text(text, encoding="utf-8")
    # Now this clone's framework goes back to the older commit.
    subprocess.run(["git", "checkout", "-q", old_head], cwd=fw, check=True)
    state, why = kernel_source_check(ws, _meta(ws))
    assert state == "behind" and "pull the framework" in why
    assert cmd_domain_kernel(argparse.Namespace(path=str(ws), check=False)) == 1
    assert "refused — behind" in capsys.readouterr().out
    assert "old" in (ws / "AGENTS.md").read_text(encoding="utf-8")  # the block stands
    assert cmd_domain_kernel(argparse.Namespace(path=str(ws), check=True)) == 0
    assert "BEHIND" in capsys.readouterr().out


def test_a_clone_on_an_older_version_than_the_workspace_adopted_refuses(tmp_path):
    from markdownllm.domain_kernel import kernel_source_check
    fw = _framework(tmp_path)
    ws = _workspace(tmp_path, fw, seen="3.48.0")
    state, why = kernel_source_check(ws, _meta(ws))
    assert state == "behind" and "adopted framework 3.48.0" in why


def test_a_generating_commit_this_clone_lacks_refuses_as_unknown(tmp_path):
    from markdownllm.domain_kernel import kernel_source_check
    fw = _framework(tmp_path)
    ws = _workspace(tmp_path, fw)
    text = (ws / "AGENTS.md").read_text(encoding="utf-8").replace(
        "framework_version_seen: 3.47.0",
        "framework_version_seen: 3.47.0\nframework_kernel_from: " + "f" * 40)
    (ws / "AGENTS.md").write_text(text, encoding="utf-8")
    state, why = kernel_source_check(ws, _meta(ws))
    assert state == "unknown" and "does not have" in why


def test_coherence_reads_behind_as_info_not_error(tmp_path):
    from markdownllm.coherence import coherence_findings
    from markdownllm.domain_kernel import framework_head, set_kernel_source
    from markdownllm.model import SEV_ERROR, SEV_INFO
    fw = _framework(tmp_path)
    ws = _workspace(tmp_path, fw)
    old_head = framework_head(fw)
    (fw / "tools" / "x").write_text("later\n", encoding="utf-8")
    _commit(fw, "the newer framework")
    (ws / "AGENTS.md").write_text(set_kernel_source(
        (ws / "AGENTS.md").read_text(encoding="utf-8"), ws, _meta(ws)), encoding="utf-8")
    subprocess.run(["git", "checkout", "-q", old_head], cwd=fw, check=True)
    findings = coherence_findings(ws, 15)
    kernel = [f for f in findings if "domain-kernel" in f.message]
    assert kernel and all(f.severity == SEV_INFO for f in kernel)
    assert not [f for f in kernel if f.severity == SEV_ERROR]


# ------------------------------------------------------------- the stall ring

def _ticket_repo(tmp_path: Path) -> Path:
    import yaml
    root = _repo(tmp_path)
    write(root, "things/_schema.yaml", yaml.safe_dump({
        "schema_version": 1, "domain": "x",
        "types": {"task": {"statuses": ["in-progress", "done"]},
                  "ticket": {"statuses": ["claude", "codex", "closed"],
                             "terminal_statuses": ["closed"]}}}, sort_keys=False))
    _commit(root, "schema")
    return root


def _ticket(root: Path, item: str, addressee: str, when: str) -> None:
    """A ticket turn committed at `when`, an ISO UTC instant such as
    2026-10-15T06:00:00+0000, so the test's clock and git's agree."""
    write(root, f"things/tickets/ticket-{item}.md", thing_text(
        f"id: ticket-{item}\ntype: ticket\nstatus: {addressee}\ncreated: {when[:10]}",
        "# Ticket\n\nthe current message.\n"))
    env = {**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", f"ticket: {item} -> {addressee}"],
                   cwd=root, check=True, env=env)


def _ago(hours: float) -> str:
    when = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)
    return when.strftime("%Y-%m-%dT%H:%M:%S+0000")


def test_turn_stalls_reads_open_tickets_against_the_window_and_the_ceiling(tmp_path):
    # the-seat, the ring: an open ticket quiet for longer than the window and
    # no longer than the ceiling has stalled -- owed here when its addressee is
    # this seat, awaiting the other seat otherwise. Past the ceiling it is
    # abandoned, reported and never rung. Closed tickets owe nothing; fresh
    # ones wait. The window is one hour: the busiest workspace's replies
    # arrive in a median of five minutes and 90% within about an hour.
    from markdownllm.seat import set_seat, stall_lines, turn_stalls
    root = _ticket_repo(tmp_path)
    set_seat(root, "codex", "codex-cli", today=dt.date(2026, 10, 15))
    _ticket(root, "mine", "codex", "2026-10-15T06:00:00+0000")      # 7h: stalled, owed here
    _ticket(root, "theirs", "claude", "2026-10-15T05:00:00+0000")   # 8h: stalled, awaiting
    _ticket(root, "done", "closed", "2026-10-13T12:00:00+0000")     # closed: nothing owed
    _ticket(root, "fresh", "codex", "2026-10-15T12:30:00+0000")     # 30m: waiting
    _ticket(root, "old", "claude", "2026-10-13T12:00:00+0000")      # 49h: abandoned
    now = dt.datetime(2026, 10, 15, 13, 0, tzinfo=dt.timezone.utc)
    info = turn_stalls(root, now=now)
    assert info["stall_hours"] == 1.0 and info["abandon_hours"] == 24.0
    by_id = {t["id"]: t for t in info["tickets"]}
    assert set(by_id) == {"ticket-mine", "ticket-theirs"}
    assert by_id["ticket-mine"]["owed_here"] and not by_id["ticket-theirs"]["owed_here"]
    assert [t["id"] for t in info["abandoned"]] == ["ticket-old"]
    assert info["stalled"] and info["seat"] == "codex"
    lines = stall_lines(info)
    assert any("`ticket-mine` owed by this seat for 7h" in ln for ln in lines)
    assert any("`ticket-theirs` awaiting `claude` for 8h" in ln for ln in lines)
    assert any(ln.startswith("- tickets abandoned (1, the oldest 2d quiet")
               and "`ticket-old`" in ln for ln in lines)
    assert all("window 1h" in ln for ln in lines if "turn stalled" in ln)
    # A wider window than the live turns: only the abandoned line remains, and
    # nothing rings.
    info = turn_stalls(root, now=now, stall_hours=10)
    assert not info["stalled"] and info["abandoned"]
    # The clone may declare its own thresholds: a 9h window and a 100h ceiling
    # make the 7h and 8h turns wait and bring the 49h ticket back as stalled.
    subprocess.run(["git", "config", "--local", "mdllm.seat.stall-hours", "9"],
                   cwd=root, check=True)
    subprocess.run(["git", "config", "--local", "mdllm.seat.abandon-hours", "100"],
                   cwd=root, check=True)
    info = turn_stalls(root, now=now)
    assert info["stall_hours"] == 9.0 and info["abandon_hours"] == 100.0
    assert [t["id"] for t in info["tickets"]] == ["ticket-old"] and not info["abandoned"]
    # A workspace with no ticket type has no turns to stall.
    plain = _repo(tmp_path, "plain")
    assert turn_stalls(plain, now=now)["tickets"] == []


def test_seat_stall_exit_rings_only_when_a_turn_has_stalled(tmp_path, capsys):
    from markdownllm.seat import cmd_seat, set_seat
    root = _ticket_repo(tmp_path)
    set_seat(root, "codex", "codex-cli")
    ns = argparse.Namespace(path=str(root), set=None, clear=False,
                            stall_exit=True, stall_hours=None, abandon_hours=None)
    assert cmd_seat(ns) == 0                       # nothing open: no ring
    assert "turn stalled" not in capsys.readouterr().out
    _ticket(root, "forgotten", "codex", _ago(72))  # abandoned: reported, never rings
    assert cmd_seat(ns) == 0
    out = capsys.readouterr().out
    assert "tickets abandoned (1" in out and "turn stalled" not in out
    _ticket(root, "waiting", "codex", _ago(3))     # stalled: the ring
    assert cmd_seat(ns) == 5
    out = capsys.readouterr().out
    assert "turn stalled: `ticket-waiting` owed by this seat for 3h" in out
    ns.stall_exit = False
    assert cmd_seat(ns) == 0                       # the line prints either way
    assert "turn stalled" in capsys.readouterr().out


def test_session_start_carries_the_stall_line(tmp_path, capsys):
    from markdownllm.session import cmd_session_start
    root = _ticket_repo(tmp_path)
    _ticket(root, "unanswered", "claude", _ago(3))
    assert cmd_session_start(argparse.Namespace(path=str(root))) == 0
    out = capsys.readouterr().out
    assert "turn stalled: `ticket-unanswered` awaiting `claude` for 3h" in out
