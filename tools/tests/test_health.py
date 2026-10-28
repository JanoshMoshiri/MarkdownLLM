"""`mdllm estate-check --health` — the estate's upkeep, backlog, cadence and
openness as figures the floor computes (the-record-holds-unattended
Phase 3). Every figure here was first produced by a session reasoning over
fourteen repositories on 2026-10-24; these tests pin what the floor says
instead."""

import datetime as _dt
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mdllm  # noqa: E402
from corpus_harness import _ns, _git_commit, thing_text, write  # noqa: E402

from markdownllm import health as H  # noqa: E402


def _repo(tmp_path):
    root = tmp_path / "ws"
    (root / "things").mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    return root


def test_maintenance_share_classifies_by_paths_and_subject(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/a.md", thing_text("id: a\ntype: plan\nstatus: in-progress\ncreated: 2026-10-01"))
    _git_commit(root, "plan: a")                               # authored
    write(root, "things/_index/schema.md", "# index\n")
    _git_commit(root, "index: schema rebuilt")                 # generated path + prefix
    write(root, "things/b.md", thing_text("id: b\ntype: plan\nstatus: in-progress\ncreated: 2026-10-01"))
    write(root, "things/_index/schema.md", "# index 2\n")
    _git_commit(root, "plan: b, with its index")               # mixed → authored
    write(root, "kernel.md", "# kernel\n")
    _git_commit(root, "regenerated")                           # generated file only
    m = H.maintenance_share(root, 30)
    assert m["commits"] == 4 and m["maintenance"] == 2 and abs(m["share"] - 0.5) < 1e-9


def test_population_reads_open_ratios_cue_precision_and_retrospective_age(tmp_path):
    root = _repo(tmp_path)
    today = _dt.date(2026, 10, 27)
    write(root, "things/i1.md", thing_text("id: i1\ntype: insight\nstatus: active\ncreated: 2026-09-01"))
    write(root, "things/i2.md", thing_text("id: i2\ntype: insight\nstatus: active\ncreated: 2026-10-20"))
    write(root, "things/i3.md", thing_text("id: i3\ntype: insight\nstatus: promoted\ncreated: 2026-08-01"))
    write(root, "things/c1.md", thing_text("id: c1\ntype: conflict\nstatus: open\ncreated: 2026-10-21\nparties: [i1, i2]"))
    write(root, "things/c2.md", thing_text("id: c2\ntype: conflict\nstatus: resolved\ncreated: 2026-07-01\nparties: [i1, i3]"))
    write(root, "things/p1.md", thing_text("id: p1\ntype: plan\nstatus: in-progress\ncreated: 2026-09-01"))
    write(root, "things/p2.md", thing_text("id: p2\ntype: plan\nstatus: completed\ncreated: 2026-09-01"))
    for n, verdict in (("1", "not-inflection"), ("2", "not-inflection"), ("3", "inflection")):
        write(root, f"things/cue{n}.md", thing_text(
            f"id: cue{n}\ntype: cue\nstatus: answered\ncreated: 2026-10-01\nsubject: i1\n"
            f"raised_at: abc\nverdict: {verdict}\nverdict_reason: r"))
    write(root, "things/cue4.md", thing_text(
        "id: cue4\ntype: cue\nstatus: open\ncreated: 2026-10-02\nsubject: i1\nraised_at: abc"))
    write(root, "things/r.md", thing_text(
        "id: r\ntype: retrospective\nstatus: complete\ncreated: 2026-10-15\n"
        "period_start: 2026-09-15\nperiod_end: 2026-10-15\ndomain: ws"))
    corpus, _ = mdllm.scan(root)
    p = H.population(corpus, today)
    assert p["counts"]["insight"] == {"total": 3, "open": 2}
    assert p["counts"]["conflict"] == {"total": 2, "open": 1}
    assert p["counts"]["plan"] == {"total": 2, "open": 1}
    assert p["cues"] == {"answered": 3, "not_inflection": 2, "open": 1}
    assert p["retro_age"] == 12
    assert p["since_retro"] == {"insights": 1, "conflicts": 1}   # i2 and c1 post-date it


def test_fired_backlog_counts_and_dates_from_the_evaluator(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/t.md", thing_text(
        "id: t\ntype: plan\nstatus: in-progress\ncreated: 2026-01-01\n"
        "triggers:\n  - type: time\n    condition: '2026-01-15 reached'\n    action: surface\n"))
    b = H.fired_backlog(root, _dt.date(2026, 10, 27))
    assert b["fired"] == 1 and b["oldest_days"] == 285 and b["over_month"] == 1


def test_render_marks_only_figures_past_their_thresholds():
    h = {"repo": "ws",
         "maintenance_30": {"commits": 10, "maintenance": 6, "share": 0.6},
         "maintenance_90": {"commits": 20, "maintenance": 2, "share": 0.1},
         "triggers": {"fired": 3, "oldest_days": 45, "over_month": 2},
         "population": {"counts": {"insight": {"total": 10, "open": 9}},
                        "cues": {"answered": 8, "not_inflection": 3, "open": 0},
                        "retro_age": 20, "since_retro": {"insights": 2, "conflicts": 0}},
         "dispatch": {"repo": "ws", "last": "2026-10-15", "age": 12, "cadence": 2, "silent": True}}
    lines = H.render(h)
    marked = [l for l in lines if l.startswith("!")]
    assert any("maintenance share (30d)" in l for l in marked)
    assert not any("maintenance share (90d)" in l for l in marked)
    assert any("fired triggers: 3" in l for l in marked)
    assert any("last retrospective: 20d ago" in l and l.startswith("-") for l in lines)
    assert any("insights active: 9/10 (90%)" in l for l in lines)
    assert any("3/8 answered ruled not-inflection (38%)" in l for l in lines)
    assert any("dispatch: last digest 12d ago" in l and "silent" in l for l in marked)


def test_estate_check_health_prints_per_repo_and_persists_nothing(tmp_path, capsys):
    root = _repo(tmp_path)
    write(root, "things/a.md", thing_text("id: a\ntype: plan\nstatus: in-progress\ncreated: 2026-10-01"))
    _git_commit(root, "plan: a")
    before = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if ".git" not in p.parts)
    rc = H.cmd_estate_health(_ns(paths=[str(root)], health=True))
    out = capsys.readouterr().out
    assert rc == 0 and "## Estate Health" in out and "### ws" in out
    assert "maintenance share (30d): 0/1" in out and "plans open: 1/1" in out
    assert "last retrospective: none on record" in out
    after = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if ".git" not in p.parts)
    assert before == after                                     # never an index
