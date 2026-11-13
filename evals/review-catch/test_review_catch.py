"""Tests for the review-catch runner and scorer. Nothing is launched."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import run_reviews as rr  # noqa: E402
import score_reviews as sr  # noqa: E402

# Two real commits in this repo that touch tools/.
C_ITEM = "9f0cc58ce63168642381af315547ed8ba746da0b"
C_CONTROL = "c502b0c599993ee43cf53681b4335f154e823727"
FAKE_FIX = "5767e0b87565b17db9884edff0888d872b7a65f7"


def make_set(tmp_path: Path) -> Path:
    s = {"schema": 1, "repo_head": "83ad75d" + "0" * 33, "entries": [
        {"id": "r001", "kind": "item", "commit": C_ITEM, "files": ["tools/x.py"], "changed_lines": 1,
         "defects": [{"fix": FAKE_FIX, "file": "tools/markdownllm/x.py", "ranges": [[100, 110]],
                      "found_by_keywords": ["review"]}]},
        {"id": "r002", "kind": "control", "commit": C_CONTROL, "files": ["tools/y.py"],
         "changed_lines": 1, "defects": []}]}
    p = tmp_path / "set.json"
    p.write_text(json.dumps(s), encoding="utf-8")
    return p


def args_for(set_path, arm, tmp_path, **kw):
    ns = argparse.Namespace(set=str(set_path), arm=arm, model="test-model-id", trial=1,
                            out=str(tmp_path / "out"), entries=None, timeout=5, dry_run=False)
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


# ---------------------------------------------------------------- prompts

def test_prompt_hashes_are_frozen_lf_values():
    assert hashlib.sha256(rr.lf_bytes(rr.PROMPTS["blind"])).hexdigest() == \
        "9c3a82ecde6b5f9cce40eb8221ac67a2aca274fc926d7ca15c6de3c9ad0ebd9c"
    assert hashlib.sha256(rr.lf_bytes(rr.PROMPTS["message"])).hexdigest() == \
        "8c00ed5643c5f87eda73890d91f27f49b35360c59a1294d3963cbbdb1c1d7b7f"


def test_set_sha_is_over_lf_bytes(tmp_path):
    lf = b'{"schema": 1,\n "repo_head": "x",\n "entries": []}\n'
    (tmp_path / "lf.json").write_bytes(lf)
    (tmp_path / "crlf.json").write_bytes(lf.replace(b"\n", b"\r\n"))
    sha = hashlib.sha256(lf).hexdigest()
    assert rr.load_set(tmp_path / "lf.json")[1] == sha == rr.load_set(tmp_path / "crlf.json")[1]
    assert hashlib.sha256(sr.lf_bytes(tmp_path / "crlf.json")).hexdigest() == sha


# ---------------------------------------------------------------- work folder

@pytest.mark.parametrize("variant", ["blind", "message"])
def test_work_folder_contents_and_leak_check(tmp_path, variant):
    set_path = make_set(tmp_path)
    s, _ = rr.load_set(set_path)
    e = s["entries"][0]
    folder = rr.build_work_folder(e, variant, tmp_path / "w" / "r001")
    names = {p.name for p in folder.iterdir()}
    expected = {"tools", "CHANGE.diff"} | ({"COMMIT_MESSAGE.txt"} if variant == "message" else set())
    assert names == expected
    assert not list(folder.rglob(".git"))
    assert (folder / "CHANGE.diff").read_bytes().startswith(b"diff --git a/tools/")
    rr.assert_no_leak(folder, variant, e, s)  # passes on a clean folder
    all_bytes = b"".join(p.read_bytes() for p in folder.rglob("*") if p.is_file())
    assert C_ITEM.encode() not in all_bytes and FAKE_FIX[:7].encode() not in all_bytes


def test_leak_check_refuses_extra_file_message_in_blind_and_ids(tmp_path):
    s, _ = rr.load_set(make_set(tmp_path))
    e = s["entries"][0]
    folder = rr.build_work_folder(e, "message", tmp_path / "w" / "r001")
    with pytest.raises(AssertionError, match="top level"):
        rr.assert_no_leak(folder, "blind", e, s)  # blind arm must not carry the message
    folder = rr.build_work_folder(e, "blind", tmp_path / "w" / "r001")
    (folder / "tools" / "note.txt").write_text("see r002 and fix " + FAKE_FIX[:7], encoding="utf-8")
    with pytest.raises(AssertionError) as exc:
        rr.assert_no_leak(folder, "blind", e, s)
    assert "entry id r002" in str(exc.value) and "sha prefix" in str(exc.value)
    folder = rr.build_work_folder(e, "blind", tmp_path / "w" / "r001")
    (folder / "set.json").write_text("{}", encoding="utf-8")
    with pytest.raises(AssertionError):
        rr.assert_no_leak(folder, "blind", e, s)


def test_work_folder_refuses_repo_descendant():
    s = {"commit": C_ITEM}
    with pytest.raises(ValueError):
        rr.build_work_folder(s, "blind", rr.REPO / "evals" / "runs" / "x")


def test_dry_run_launches_nothing(tmp_path, capsys, monkeypatch):
    set_path = make_set(tmp_path)
    monkeypatch.setattr(rr, "launch", lambda *a, **k: pytest.fail("launched"))
    for arm in rr.ARMS:
        assert rr.run_arm(args_for(set_path, arm, tmp_path, dry_run=True), work_root=tmp_path / "w") == 0
    out = capsys.readouterr().out
    assert "--sandbox read-only" in out and "--safe-mode" in out
    assert not (tmp_path / "out").exists()


# ---------------------------------------------------------------- JSON extraction

F = {"file": "tools/a.py", "line_start": 3, "line_end": 4, "claim": "breaks", "confidence": "high"}


def test_extract_clean():
    r = rr.extract_findings(json.dumps({"findings": [F]}))
    assert r["ok"] and r["offered"] == 1 and r["findings"][0]["file"] == "tools/a.py"


def test_extract_fenced_and_prose_before():
    text = "I looked.\n```json\n" + json.dumps({"findings": [F, F]}) + "\n```"
    r = rr.extract_findings(text)
    assert r["ok"] and r["offered"] == 2 and not r["trailing_text"]


def test_extract_trailing_prose_and_earlier_objects():
    text = 'first {"x": 1} then ' + json.dumps({"findings": [F]}) + "\nHope this helps."
    r = rr.extract_findings(text)
    assert r["ok"] and r["trailing_text"]


def test_extract_last_object_wins():
    text = json.dumps({"findings": [F]}) + ' and finally {"note": "done"}'
    assert not rr.extract_findings(text)["ok"]


def test_extract_six_keeps_five():
    r = rr.extract_findings(json.dumps({"findings": [F] * 6}))
    assert r["ok"] and r["offered"] == 6 and len(r["findings"]) == 5


def test_extract_empty_findings_is_valid():
    r = rr.extract_findings('{"findings": []}')
    assert r["ok"] and r["findings"] == []


@pytest.mark.parametrize("text", ["", "no json here", "{broken", '{"findings": "none"}',
                                  json.dumps({"findings": [{"file": "a", "line_start": "3",
                                                            "line_end": 4, "claim": "c"}]}),
                                  json.dumps({"findings": [{"file": "a", "line_start": 3,
                                                            "line_end": 4}]})])
def test_extract_garbage_is_void(text):
    r = rr.extract_findings(text)
    assert not r["ok"] and r["reason"]


# ---------------------------------------------------------------- geometry

D = {"file": "tools/m/x.py", "ranges": [[100, 110]]}


def f(ls, le, file="tools/m/x.py"):
    return {"file": file, "line_start": ls, "line_end": le, "claim": "c"}


def test_hit_overlap_and_widening():
    assert sr.classify(f(105, 105), D) == "hit"
    assert sr.classify(f(111, 115), D) == "hit"
    assert sr.classify(f(115, 120), D) == "hit"   # gap 5: widened by 5 still overlaps
    assert sr.classify(f(90, 94), D) == "near"    # gap 6: 94 widened is 99
    assert sr.classify(f(116, 120), D) == "near"  # gap 6


def test_widening_boundaries_exact():
    assert sr.classify(f(95, 95), D) == "hit"     # 95+5 = 100
    assert sr.classify(f(94, 94), D) == "near"    # 94+5 = 99
    assert sr.classify(f(140, 150), D) == "near"  # gap 30
    assert sr.classify(f(141, 150), D) == "miss"  # gap 31
    assert sr.classify(f(105, 105, "tools/m/y.py"), D) == "miss"


def test_path_normalisation_and_reversed_range():
    assert sr.classify(f(108, 102, ".\\tools\\m\\x.py"), D) == "hit"
    assert sr.classify(f(105, 105, "./tools/m/x.py"), D) == "hit"


def test_majority_rule():
    assert sr.majority(2, 3) and not sr.majority(1, 2) and sr.majority(1, 1) and not sr.majority(0, 0)


def test_mcnemar_hand_computed():
    # b=1, c=7: n=8, P(X<=1) = (1 + 8)/256; two-sided = 18/256
    assert sr.mcnemar_exact(1, 7) == pytest.approx(18 / 256)
    assert sr.mcnemar_exact(0, 0) == 1.0
    assert sr.mcnemar_exact(3, 3) == 1.0


# ---------------------------------------------------------------- scoring end to end

def result_file(tmp_path, name, set_sha, arm="claude-blind", trial=1, findings=None,
                complete=True, prompt_sha="p" * 64):
    r = {"schema": 1, "arm": arm, "vendor": arm.split("-")[0], "model_requested": "m",
         "prompt_sha256": prompt_sha, "set_sha256": set_sha, "trial": trial, "complete": complete,
         "reviews": [{"entry": "r001", "findings": findings or [], "void": False},
                     {"entry": "r002", "findings": [], "void": False}]}
    p = tmp_path / name
    p.write_text(json.dumps(r), encoding="utf-8")
    return p


def test_refuses_mismatched_set_hash_and_incomplete(tmp_path):
    set_path = make_set(tmp_path)
    _, sha = rr.load_set(set_path)
    res = tmp_path / "res"
    res.mkdir()
    result_file(res, "a.json", sha)
    result_file(res, "b.json", "0" * 64, trial=2)
    result_file(res, "c.json", sha, trial=3, complete=False)
    groups, skipped = sr.load_results([str(res)], sha)
    assert sum(len(g) for g in groups.values()) == 1
    assert any("b.json" in s and "set sha256" in s for s in skipped)
    assert any("c.json" in s and "incomplete" in s for s in skipped)


def test_prompt_hashes_never_pooled(tmp_path):
    set_path = make_set(tmp_path)
    _, sha = rr.load_set(set_path)
    res = tmp_path / "res"
    res.mkdir()
    result_file(res, "a.json", sha, trial=1, prompt_sha="a" * 64)
    result_file(res, "b.json", sha, trial=2, prompt_sha="b" * 64)
    groups, _ = sr.load_results([str(res)], sha)
    assert len(groups) == 2


def test_score_near_emit_and_rulings(tmp_path, capsys):
    set_path = make_set(tmp_path)
    _, sha = rr.load_set(set_path)
    res = tmp_path / "res"
    res.mkdir()
    near_f = {"file": "tools/markdownllm/x.py", "line_start": 125, "line_end": 126, "claim": "off by one"}
    hit_f = {"file": "tools/markdownllm/x.py", "line_start": 108, "line_end": 108, "claim": "bad"}
    result_file(res, "t1.json", sha, trial=1, findings=[near_f])
    result_file(res, "t2.json", sha, trial=2, findings=[hit_f])
    result_file(res, "t3.json", sha, trial=3, findings=[])
    result_file(res, "x1.json", sha, arm="codex-blind", trial=1, findings=[hit_f])
    emit = tmp_path / "near.md"
    assert sr.main(["--set", str(set_path), "--results", str(res), "--emit-near", str(emit)]) == 0
    text = emit.read_text(encoding="utf-8")
    for word in ("claude", "codex", "trial", "blind"):
        assert word not in text.lower().replace("near misses to rule on", "")
    keymap = json.loads((tmp_path / "near.key.json").read_text(encoding="utf-8"))
    (key,) = keymap
    assert keymap[key]["arm"] == "claude-blind"
    out1 = capsys.readouterr().out
    assert "1/3" in out1  # claude: caught in 1 of 3 trials before ruling
    rulings = tmp_path / "rulings.txt"
    rulings.write_text(f"{key}: hit\n", encoding="utf-8")
    sr.main(["--set", str(set_path), "--results", str(res), "--near-rulings", str(rulings)])
    out2 = capsys.readouterr().out
    assert "2/3" in out2 and "McNemar" in out2


# ---------------------------------------------------------------- void handling

def claude_reply(text):
    ev = {"type": "result", "subtype": "success", "is_error": False, "result": text,
          "total_cost_usd": 0.01, "num_turns": 2, "modelUsage": {"test-model-id": {}}}
    return json.dumps(ev)


def fake_launcher(replies):
    calls = []

    def launcher(cmd, cwd, stdin, timeout):
        calls.append(cmd)
        out, code = replies[min(len(calls) - 1, len(replies) - 1)]
        return {"stdout": out, "stderr": "", "exit_code": code, "timed_out": False,
                "started": "s", "ended": "e", "seconds": 0.1}
    launcher.calls = calls
    return launcher


def test_two_consecutive_voids_stop_the_arm(tmp_path):
    set_path = make_set(tmp_path)
    launcher = fake_launcher([("garbage", 1)])
    code = rr.run_arm(args_for(set_path, "claude-blind", tmp_path), launcher=launcher,
                      base_cmd=["fake-claude"], work_root=tmp_path / "w")
    assert code != 0 and len(launcher.calls) == 2
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    assert data["complete"] is False and "two consecutive" in data["stopped"]
    assert data["reviews"][0]["void"] and data["reviews"][0]["raw_final_message"]
    text = res.read_text(encoding="utf-8")
    assert '"kind"' not in text and FAKE_FIX not in text and '"defects"' not in text


def test_void_is_retried_once_then_run_completes(tmp_path):
    set_path = make_set(tmp_path)
    good = claude_reply("Done.\n" + json.dumps({"findings": [F]}))
    launcher = fake_launcher([("garbage", 1), (good, 0), (good, 0)])
    code = rr.run_arm(args_for(set_path, "claude-message", tmp_path), launcher=launcher,
                      base_cmd=["fake-claude"], work_root=tmp_path / "w")
    assert code == 0 and len(launcher.calls) == 3
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    assert data["complete"] and data["models_observed"] == ["test-model-id"]
    assert data["reviews"][0]["retries"] == 1 and not data["reviews"][0]["void"]
    assert data["totals"]["cost_usd"] == pytest.approx(0.02)
    assert data["hashes_over"].startswith("LF")


def test_timeout_voids(tmp_path):
    set_path = make_set(tmp_path)

    def launcher(cmd, cwd, stdin, timeout):
        return {"stdout": claude_reply('{"findings": []}'), "stderr": "", "exit_code": 1,
                "timed_out": True, "started": "s", "ended": "e", "seconds": 5}
    code = rr.run_arm(args_for(set_path, "claude-blind", tmp_path), launcher=launcher,
                      base_cmd=["fake-claude"], work_root=tmp_path / "w")
    assert code != 0


# ---------------------------------------------------------------- reach outside the folder

def claude_stream(tool_uses, final):
    lines = [json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": n, "input": i} for n, i in tool_uses]}})]
    lines.append(claude_reply(final))
    return "\n".join(lines)


def test_claude_reach_rules(tmp_path):
    folder = tmp_path / "w" / "r001"
    folder.mkdir(parents=True)
    outside_file = str(tmp_path / "elsewhere" / "x.py")
    assert rr.claude_reach("Read", {"file_path": outside_file}, folder)
    assert rr.claude_reach("Read", {"file_path": "tools/markdownllm/watch.py"}, folder) == []
    assert rr.claude_reach("Read", {"file_path": str(folder / "CHANGE.diff")}, folder) == []
    assert rr.claude_reach("Read", {"file_path": "../r002/CHANGE.diff"}, folder)
    assert rr.claude_reach("Glob", {"pattern": "C:/**/*.py"}, folder)
    assert rr.claude_reach("Glob", {"pattern": "../**/*.py"}, folder)
    assert rr.claude_reach("Glob", {"pattern": "tools/**/*.py"}, folder) == []
    assert rr.claude_reach("Grep", {"pattern": "a..b", "glob": "*.py"}, folder) == []
    assert rr.claude_reach("Grep", {"pattern": "x", "glob": "/etc/*"}, folder)


def test_claude_outside_read_voids_review(tmp_path):
    folder = tmp_path / "w" / "r001"
    folder.mkdir(parents=True)
    good = json.dumps({"findings": []})
    run = {"stdout": claude_stream([("Read", {"file_path": str(tmp_path / "x.py")})], good),
           "stderr": "", "exit_code": 0, "timed_out": False, "started": "s", "ended": "e",
           "seconds": 1}
    rec = rr.review_once("claude", ["fake"], "m", "p", folder, tmp_path, 5,
                         launcher=lambda *a: run)
    assert rec["void"] and rec["void_reason"] == "reached outside the work folder"
    assert rec["outside_reach"]
    run["stdout"] = claude_stream([("Read", {"file_path": "tools/a.py"})], good)
    rec = rr.review_once("claude", ["fake"], "m", "p", folder, tmp_path, 5,
                         launcher=lambda *a: run)
    assert not rec["void"]


@pytest.mark.parametrize("cmd", [
    "git log --oneline -5",
    "cat C:\\somewhere\\x.py",
    "type ..\\other\\CHANGE.diff",
    "Get-Content C:/Users/someone/repo/tools/x.py",
    "ls \\\\server\\share",
    "cat /c/Users/someone/x.py",
    "ls /mnt/data",
    "cat ~/notes.txt",
    "Get-ChildItem $env:USERPROFILE",
    "dir %USERPROFILE%",
    "rg foo tools/ | git show HEAD",
    '"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git -C C:\\repo log"',
    ["bash", "-lc", "cat ../x"],
])
def test_codex_reach_flagged(tmp_path, cmd):
    folder = tmp_path / "w" / "r001"
    folder.mkdir(parents=True)
    assert rr.codex_reach(cmd, folder)


def test_codex_reach_not_flagged(tmp_path):
    folder = tmp_path / "w" / "r001"
    folder.mkdir(parents=True)
    inside = str(folder / "tools" / "markdownllm" / "watch.py")
    for cmd in ["rg foo tools/", "cat tools/markdownllm/watch.py", f"cat {inside}",
                f"Get-Content {inside.replace(chr(92), '/')}",
                f'"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n foo tools/"',
                ["bash", "-lc", "sed -n 1,40p tools/x.py"],
                "rg -n 'git' tools/"]:
        assert rr.codex_reach(cmd, folder) == [], cmd


def test_codex_outside_reach_voids_and_retries_then_stops(tmp_path):
    set_path = make_set(tmp_path)
    events = "\n".join(json.dumps(e) for e in [
        {"type": "item.completed", "item": {"id": "i1", "type": "command_execution",
                                            "command": "git log -3"}},
        {"type": "item.completed", "item": {"id": "i2", "type": "agent_message",
                                            "text": '{"findings": []}'}},
        {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}}])
    launcher = fake_launcher([(events, 0)])
    code = rr.run_arm(args_for(set_path, "codex-blind", tmp_path), launcher=launcher,
                      base_cmd=["fake-codex"], work_root=tmp_path / "w")
    assert code == 2 and len(launcher.calls) == 2
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    r = data["reviews"][0]
    assert r["void_reason"] == "reached outside the work folder" and r["outside_reach"]
    assert r["void_attempts"][0]["outside_reach"] and r["findings"] == []


def test_summary_printed(tmp_path, capsys):
    set_path = make_set(tmp_path)
    good = claude_reply(json.dumps({"findings": [F]}))
    rr.run_arm(args_for(set_path, "claude-blind", tmp_path), launcher=fake_launcher([(good, 0)]),
               base_cmd=["fake-claude"], work_root=tmp_path / "w")
    out = capsys.readouterr().out
    assert "r001:" in out and "r002:" in out and "1 findings kept, ok" in out
    assert "totals: 2 reviews, 0 void" in out and "cost $0.0200" in out


def test_order_is_seeded_by_trial(tmp_path):
    s, _ = rr.load_set(make_set(tmp_path))
    s["entries"] = [dict(s["entries"][0], id=f"r{i:03d}") for i in range(20)]
    a = [e["id"] for e in rr.ordered_entries(s, 3, None)]
    assert a == [e["id"] for e in rr.ordered_entries(s, 3, None)]
    assert a != [e["id"] for e in rr.ordered_entries(s, 4, None)]
    assert [e["id"] for e in rr.ordered_entries(s, 3, ["r005", "r001"])] == [x for x in a if x in ("r005", "r001")]
