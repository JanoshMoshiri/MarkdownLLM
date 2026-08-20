"""session-start digest signals (session-start-hardening Phase 3): weekly
velocity trend buckets, floor-computed stall lines, and the self-answering
armed-trigger heuristic. Every emitted cue is a pull-router — these are the
computable cores of the orientation walk the five-run baseline showed not
happening unprompted.

Run: python -m pytest tools/tests/test_digest_signals.py -q
"""

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402


def _ns(**kw):
    defaults = {"contract": False}
    defaults.update(kw)
    return argparse.Namespace(**defaults)


def _git(root: Path, *args, date: str | None = None) -> None:
    env = None
    if date:
        env = {**os.environ,
               "GIT_AUTHOR_DATE": f"{date}T12:00:00",
               "GIT_COMMITTER_DATE": f"{date}T12:00:00"}
    subprocess.run(["git", *args], cwd=root, check=True, env=env,
                   capture_output=True)


def _repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@t")
    _git(root, "config", "user.name", "t")
    return root


def _thing(root: Path, rel: str, front: str, date: str) -> None:
    p = root / "things" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\n{front}---\n# T\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", f"create: {rel}", date=date)


def _days_ago(n: int) -> str:
    return (dt.date.today() - dt.timedelta(days=n)).isoformat()


def test_velocity_trend_buckets_show_deceleration(tmp_path, capsys,
                                                  monkeypatch):
    """A flat 30-day total masked an 85 → 16 → 9 deceleration; the weekly
    buckets cannot mask it."""
    monkeypatch.delenv("MDLLM_LIFECYCLE_CHANNEL", raising=False)
    root = _repo(tmp_path)
    for i, back in enumerate((24, 23, 22)):
        _thing(root, f"old{i}.md",
               f"id: old{i}\ntype: note\nstatus: in-progress\n"
               f"created: 2026-07-01\n", _days_ago(back))
    _thing(root, "fresh.md",
           "id: fresh\ntype: note\nstatus: in-progress\ncreated: 2026-08-01\n",
           _days_ago(1))
    mdllm.cmd_session_start(_ns(path=str(root)))
    out = capsys.readouterr().out
    assert "Weekly commits to `things/` (oldest→newest): 3 · 0 · 0 · 1." in out


def test_stall_line_names_critical_work_and_spares_knowledge(
        tmp_path, capsys, monkeypatch):
    """Critical/high non-terminal work past the 21-day line is named per
    thing; knowledge types (insights) and fresh work stay out of the cue."""
    monkeypatch.delenv("MDLLM_LIFECYCLE_CHANNEL", raising=False)
    root = _repo(tmp_path)
    _thing(root, "stalled-plan.md",
           "id: stalled-plan\ntype: plan\nstatus: in-progress\n"
           "priority: critical\ncreated: 2026-07-01\n", _days_ago(30))
    _thing(root, "old-insight.md",
           "id: old-insight\ntype: insight\nstatus: active\n"
           "priority: high\ncreated: 2026-07-01\n", _days_ago(30))
    _thing(root, "fresh-plan.md",
           "id: fresh-plan\ntype: plan\nstatus: in-progress\n"
           "priority: critical\ncreated: 2026-08-01\n", _days_ago(2))
    mdllm.cmd_session_start(_ns(path=str(root)))
    out = capsys.readouterr().out
    assert "Stalled past the 21-day line (1):" in out
    assert "`stalled-plan` (critical, in-progress) untouched 30d" in out
    stall_block = out.split("Stalled past the 21-day line")[1] \
                     .split("- **")[0]
    assert "old-insight" not in stall_block
    assert "fresh-plan" not in stall_block


def test_self_answering_armed_trigger_is_cued(tmp_path, capsys, monkeypatch):
    """An armed future-dated trigger whose action text already answers its
    condition is cued as a heuristic; a healthily conditioned trigger with a
    real check in its action stays silent."""
    monkeypatch.delenv("MDLLM_LIFECYCLE_CHANNEL", raising=False)
    root = _repo(tmp_path)
    far = (dt.date.today() + dt.timedelta(days=200)).isoformat()
    near = (dt.date.today() + dt.timedelta(days=10)).isoformat()
    _thing(root, "answered.md",
           "id: answered\ntype: plan\nstatus: in-progress\n"
           "created: 2026-08-01\n"
           "triggers:\n"
           f"  - type: time\n    condition: '{far} reached'\n"
           "    action: 'Both remedies are spent; do not re-ask either.'\n",
           _days_ago(1))
    _thing(root, "healthy.md",
           "id: healthy\ntype: plan\nstatus: in-progress\n"
           "created: 2026-08-01\n"
           "triggers:\n"
           f"  - type: time\n    condition: '{near} reached'\n"
           "    action: 'Check whether the submission artifact exists.'\n",
           _days_ago(1))
    mdllm.cmd_session_start(_ns(path=str(root)))
    out = capsys.readouterr().out
    assert "Self-answering armed triggers (1):" in out
    assert "answered: armed for" in out
    assert "healthy: armed" not in out


def test_triggers_cli_prints_self_answering_section(tmp_path, capsys):
    root = _repo(tmp_path)
    far = (dt.date.today() + dt.timedelta(days=90)).isoformat()
    _thing(root, "armed.md",
           "id: armed\ntype: plan\nstatus: in-progress\ncreated: 2026-08-01\n"
           "triggers:\n"
           f"  - type: time\n    condition: '{far} reached'\n"
           "    action: 'It already issued; do not re-ask.'\n",
           _days_ago(1))
    mdllm.cmd_triggers(_ns(path=str(root)))
    out = capsys.readouterr().out
    assert "### Self-answering armed triggers (heuristic)" in out
    assert "armed: armed for" in out
