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
    ns = argparse.Namespace(set=str(set_path), arm=arm, model="test-model-id", effort="xhigh", trial=1,
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
                complete=True, prompt_sha="p" * 64, model="m", effort=None):
    r = {"schema": 1, "arm": arm, "vendor": arm.split("-")[0], "model_requested": model,
         "prompt_sha256": prompt_sha, "set_sha256": set_sha, "trial": trial, "complete": complete,
         "reviews": [{"entry": "r001", "findings": findings or [], "void": False},
                     {"entry": "r002", "findings": [], "void": False}]}
    if effort is not None:
        r["effort_requested"] = effort
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


def test_model_and_effort_never_pooled(tmp_path, capsys):
    set_path = make_set(tmp_path)
    _, sha = rr.load_set(set_path)
    res = tmp_path / "res"
    res.mkdir()
    result_file(res, "a.json", sha, trial=1, effort="xhigh")
    result_file(res, "b.json", sha, trial=2, effort="high")
    result_file(res, "c.json", sha, trial=3)  # no effort_requested: counts as default
    result_file(res, "d.json", sha, trial=4, effort="default")
    result_file(res, "e.json", sha, trial=5, effort="xhigh", model="other")
    groups, skipped = sr.load_results([str(res)], sha)
    assert not skipped
    assert {(k[1], k[2]): sorted(v) for k, v in groups.items()} == {
        ("m", "xhigh"): [1], ("m", "high"): [2], ("m", "default"): [3, 4], ("other", "xhigh"): [5]}
    assert sr.main(["--set", str(set_path), "--results", str(res)]) == 0
    out = capsys.readouterr().out
    assert "3 values of effort" in out and "2 values of model" in out
    assert "effort xhigh" in out and "effort default" in out


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
    good = claude_stream([("Read", {"file_path": "CHANGE.diff"})], "Done.\n" + json.dumps({"findings": [F]}))
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
    rec = rr.review_once("claude", ["fake"], "m", "default", "p", folder, tmp_path, 5,
                         launcher=lambda *a: run)
    assert rec["void"] and rec["void_reason"] == "reached outside the work folder"
    assert rec["outside_reach"]
    run["stdout"] = claude_stream([("Read", {"file_path": "tools/a.py"})], good)
    rec = rr.review_once("claude", ["fake"], "m", "default", "p", folder, tmp_path, 5,
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
    good = claude_stream([("Read", {"file_path": "CHANGE.diff"})], json.dumps({"findings": [F]}))
    rr.run_arm(args_for(set_path, "claude-blind", tmp_path), launcher=fake_launcher([(good, 0)]),
               base_cmd=["fake-claude"], work_root=tmp_path / "w")
    out = capsys.readouterr().out
    assert "r001:" in out and "r002:" in out and "1 findings kept, ok" in out
    assert "totals: 2 reviews, 0 void" in out and "cost $0.0200" in out


def test_claude_effort_flag():
    cmd = rr.claude_command(["claude"], "m", "xhigh", "p")
    i = cmd.index("--effort")
    assert cmd[i + 1] == "xhigh"
    assert "--effort" not in rr.claude_command(["claude"], "m", "default", "p")


def test_codex_effort_flag(tmp_path):
    cmd = rr.codex_command(["codex"], "m", "xhigh", tmp_path, tmp_path / "l.txt")
    i = cmd.index('model_reasoning_effort="xhigh"')
    assert cmd[i - 1] == "-c"
    assert cmd[-1] == "-"
    plain = rr.codex_command(["codex"], "m", "default", tmp_path, tmp_path / "l.txt")
    assert not any("model_reasoning_effort" in a for a in plain)


def test_codex_windows_sandbox_named(tmp_path):
    cmd = rr.codex_command(["codex"], "m", "xhigh", tmp_path, tmp_path / "l.txt")
    named = 'windows.sandbox="elevated"' in cmd
    assert named == (rr.os.name == "nt")
    assert cmd[cmd.index("--sandbox") + 1] == "read-only"


def test_review_that_read_nothing_is_void(tmp_path):
    set_path = make_set(tmp_path)
    empty = claude_reply(json.dumps({"findings": []}))
    launcher = fake_launcher([(empty, 0)])
    code = rr.run_arm(args_for(set_path, "claude-blind", tmp_path), launcher=launcher,
                      base_cmd=["fake-claude"], work_root=tmp_path / "w")
    assert code != 0
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    assert data["reviews"][0]["void"] and "read nothing" in data["reviews"][0]["void_reason"]
    assert rr.reads_made("codex", {"commands": ["Get-Content CHANGE.diff"]})
    assert not rr.reads_made("codex", {"commands": []})


def test_effort_is_required_and_checked():
    with pytest.raises(SystemExit):
        rr.main(["--set", "x", "--arm", "claude-blind", "--model", "m", "--trial", "1"])
    with pytest.raises(SystemExit):
        rr.main(["--set", "x", "--arm", "claude-blind", "--model", "m", "--effort", "huge",
                 "--trial", "1"])


def test_payload_records_effort_and_launch_carries_it(tmp_path, capsys):
    set_path = make_set(tmp_path)
    good = claude_stream([("Read", {"file_path": "CHANGE.diff"})], json.dumps({"findings": []}))
    launcher = fake_launcher([(good, 0)])
    assert rr.run_arm(args_for(set_path, "claude-blind", tmp_path), launcher=launcher,
                      base_cmd=["fake-claude"], work_root=tmp_path / "w") == 0
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    assert data["effort_requested"] == "xhigh" and data["model_requested"] == "test-model-id"
    assert all(c[c.index("--effort") + 1] == "xhigh" for c in launcher.calls)
    out = capsys.readouterr().out
    assert "[test-model-id, effort xhigh]" in out
    assert "summary claude-blind t1 [test-model-id, effort xhigh]" in out


def test_order_is_seeded_by_trial(tmp_path):
    s, _ = rr.load_set(make_set(tmp_path))
    s["entries"] = [dict(s["entries"][0], id=f"r{i:03d}") for i in range(20)]
    a = [e["id"] for e in rr.ordered_entries(s, 3, None)]
    assert a == [e["id"] for e in rr.ordered_entries(s, 3, None)]
    assert a != [e["id"] for e in rr.ordered_entries(s, 4, None)]
    assert [e["id"] for e in rr.ordered_entries(s, 3, ["r005", "r001"])] == [x for x in a if x in ("r005", "r001")]


# ---------------------------------------------------------------- on the road

def make_manifest(tmp_path, set_path, fail=()):
    s, sha = rr.load_set(set_path)
    doc = {"set_sha256": sha, "bundles": [
        {"id": e["id"], "commit": e["commit"], "bundle_sha256": "b" * 64, "commits_in_bundle": 9,
         "leak_check": "fail" if e["id"] in fail else "pass", "failures": []}
        for e in s["entries"]]}
    p = tmp_path / "bundles.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def road_args(set_path, arm, tmp_path, **kw):
    ns = args_for(set_path, arm, tmp_path, bundles=str(make_manifest(tmp_path, set_path)),
                  prepare_only=False)
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


def road_meta(commit, **kw):
    m = {"exit_code": 0, "timed_out": False, "seconds": 12.5,
         "harness_version": "2.1.318 (Claude Code)", "vendor": "claude",
         "head_reviewed": "d" * 40, "entry_commit": commit, "message_shown": False,
         "harness_run": True, "bundle_sha256": "b" * 64, "preflight_failures": [],
         "config_before": "f" * 64, "config_after": "f" * 64, "config_changed": []}
    m.update(kw)
    return m


def road_stdout(stream, meta=None, last=None):
    out = stream
    if last is not None:
        out += "\n" + rr.LAST_DELIM + "\n" + last
    if meta is not None:
        out += "\n" + rr.META_DELIM + "\n" + json.dumps(meta) + "\n"
    return out


def fake_distro(prompt_sha=None, script_sha=None, run_sha=None, store_sha="b" * 64, stdout=""):
    calls = []
    sha = lambda src: hashlib.sha256(rr.lf_bytes(src)).hexdigest()
    known = {rr.DISTRO_PROMPT: prompt_sha or sha(rr.ROAD_PROMPT),
             rr.REVIEW_ONE: script_sha or sha(rr.ROAD_SCRIPT),
             rr.REVIEW_RUN: run_sha or sha(rr.ROAD_RUN_SCRIPT)}

    def distro(argv, stdin=None, timeout=300):
        calls.append((argv, stdin))
        if "sha256sum" in argv:
            lines = [f"{known.get(a) or store_sha}  {a}" for a in argv[7:]
                     if a in known or a.startswith(rr.BUNDLE_STORE + "/")]
            return {"exit_code": 0, "stderr": "", "stdout": "\n".join(lines) + "\n"}
        return {"exit_code": 0, "stdout": stdout, "stderr": ""}
    distro.calls = calls
    return distro


def road_launcher(outputs, timed_out=False, stderr=""):
    calls = []

    def launcher(cmd, cwd, stdin, timeout):
        calls.append((cmd, stdin, timeout))
        out = outputs[min(len(calls) - 1, len(outputs) - 1)]
        return {"stdout": out, "stderr": stderr, "exit_code": 0, "timed_out": timed_out,
                "started": "s", "ended": "e", "seconds": 1.0}
    launcher.calls = calls
    return launcher


@pytest.mark.parametrize("arm", rr.ROAD_ARMS)
def test_road_argv_is_simple_tokens(arm):
    vendor, show = rr.road_parts(arm)
    cmd = rr.road_command(vendor, arm, 3, "r001", "gpt-6.1-sol", "xhigh", 1800, show)
    assert cmd[:6] == ["wsl.exe", "-d", "review-road", "-u", "root", "--"]
    assert cmd[6] == rr.REVIEW_RUN == "/usr/local/sbin/review-run"
    assert cmd[7:] == [vendor, arm, "3", "r001", "gpt-6.1-sol", "xhigh", "1800", "1" if show else "0"]
    assert all(rr.ARGV_TOKEN.match(a) for a in cmd[1:])
    assert show == arm.endswith("-message")
    prep = rr.road_command(vendor, arm, 3, "r001", "m", "xhigh", 60, show, prepare_only=True)
    assert prep[7] == "--prepare-only" and len(prep) == len(cmd) + 1


@pytest.mark.parametrize("bad", ["m x", "m;rm", "'m'", 'a"b', "$HOME", "a|b", "", "a\nb", "a&b"])
def test_road_argv_refuses_unsafe_tokens(bad):
    with pytest.raises(ValueError):
        rr.road_command("claude", "claude-road", 1, "r001", bad, "xhigh", 60, False)


def test_split_road_output():
    stream = '{"type": "x"}\n{"type": "y"}'
    meta = road_meta("c" * 40)
    p = rr.split_road_output(road_stdout(stream, meta))
    assert p["stream"].strip() == stream and p["last_message"] is None and p["meta"] == meta
    last = 'Line one.\n{"findings": []}'
    p = rr.split_road_output(road_stdout(stream, meta, last=last).replace("\n", "\r\n"))
    assert p["last_message"] == last and p["meta"] == meta and p["stream"].strip() == stream
    p = rr.split_road_output(road_stdout(stream, meta, last=""))
    assert p["last_message"] == "" and p["meta"] == meta
    p = rr.split_road_output(stream)
    assert p["meta"] is None and p["last_message"] is None
    p = rr.split_road_output(stream + "\n" + rr.META_DELIM + "\nnot json\n")
    assert p["meta"] is None and p["stream"].strip() == stream


def _entry():
    return {"id": "r001", "commit": C_ITEM}


def _road(vendor, out, **kw):
    launcher = road_launcher([out], **{k: v for k, v in kw.items() if k in ("timed_out", "stderr")})
    distro = fake_distro()
    rec = rr.review_road_once(vendor, f"{vendor}-road", 1, _entry(), "m", "xhigh", 60, False,
                              launcher=launcher, distro=distro)
    return rec, launcher, distro


def codex_events(*cmds, text='{"findings": []}'):
    evs = [{"type": "item.completed", "item": {"id": f"i{n}", "type": "command_execution",
                                               "command": c}} for n, c in enumerate(cmds)]
    evs.append({"type": "item.completed", "item": {"id": "m", "type": "agent_message", "text": text}})
    evs.append({"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}})
    return "\n".join(json.dumps(e) for e in evs)


def test_road_claude_read_nothing_is_void():
    rec, _, _ = _road("claude", road_stdout(claude_reply('{"findings": []}'), road_meta(C_ITEM)))
    assert rec["void"] and rec["void_reason"] == "read nothing: the reviewer used no tool"


def test_road_claude_records_commands_tests_and_build():
    stream = claude_stream([("Bash", {"command": "python -m pytest -q tools/tests"}),
                            ("Read", {"file_path": "/etc/passwd"}),
                            ("Bash", {"command": "git log -3"})], json.dumps({"findings": [F]}))
    rec, launcher, _ = _road("claude", road_stdout(stream, road_meta(C_ITEM)))
    assert not rec["void"] and rec["findings"] == [dict(F)]
    assert rec["tool_counts"] == {"Bash": 2, "Read": 1}
    assert rec["commands"] == ["python -m pytest -q tools/tests", "git log -3"]
    assert rec["ran_tests"] and rec["test_commands"] == ["python -m pytest -q tools/tests"]
    assert rec["harness_build"] == "2.1.318 (Claude Code)" and rec["head_reviewed"] == "d" * 40
    assert "outside_reach" not in rec  # no reach rule on the road
    cmd, stdin, timeout = launcher.calls[0]
    assert stdin is None and timeout == 60 + rr.ROAD_MARGIN


def test_road_codex_needs_a_command_and_uses_last_message():
    rec, _, _ = _road("codex", road_stdout(codex_events(), road_meta(C_ITEM, vendor="codex"),
                                           last='{"findings": []}'))
    assert rec["void"] and rec["void_reason"] == "read nothing: the reviewer executed no command"
    out = road_stdout(codex_events("bash -lc 'cat ~/.bashrc; ls /home/reviewer/road/bundles'",
                                   "python3 -m unittest discover", text="ignored"),
                      road_meta(C_ITEM, vendor="codex", harness_version="codex-cli 0.169.0"),
                      last="Checked.\n" + json.dumps({"findings": [F]}))
    rec, _, _ = _road("codex", out)
    assert not rec["void"] and len(rec["findings"]) == 1 and rec["trailing_text"] is False
    assert rec["ran_tests"] and rec["harness_build"] == "codex-cli 0.169.0"
    assert rec["road_reach"] and "road/bundles" in rec["road_reach"][0]
    assert rec["tokens"] == {"input_tokens": 10, "output_tokens": 2}


def test_road_void_rules():
    ok_stream = claude_stream([("Read", {"file_path": "x"})], '{"findings": []}')
    rec, _, _ = _road("claude", ok_stream, stderr="boom")  # no meta: review-one died
    assert rec["void"] and "did not finish" in rec["void_reason"]
    rec, _, _ = _road("claude", road_stdout(ok_stream, road_meta(C_ITEM, exit_code=124, timed_out=True)))
    assert rec["void"] and rec["void_reason"].startswith("timeout")
    rec, _, _ = _road("claude", road_stdout(ok_stream, road_meta(C_CONTROL)))
    assert rec["void"] and "not the entry commit" in rec["void_reason"]
    bad = claude_stream([("Read", {"file_path": "x"})], "no json at all")
    rec, _, _ = _road("claude", road_stdout(bad, road_meta(C_ITEM, exit_code=1)))
    assert rec["void"] and rec["void_reason"].startswith("exit 1, no parsable reply")
    rec, _, _ = _road("claude", road_stdout(bad, road_meta(C_ITEM)))
    assert rec["void"] and rec["void_reason"].startswith("unparsable reply")
    rec, _, _ = _road("claude", "nothing", stderr="boom")
    assert rec["void"] and "boom" in rec["raw_final_message"] and rec["stderr_tail"] == "boom"


def test_road_windows_side_timeout_cleans_the_distro():
    rec, _, distro = _road("claude", "", timed_out=True)
    assert rec["void"] and rec["void_reason"] == "timeout after 60s"
    argvs = [a for a, _ in distro.calls]
    assert any(a[6:] == ["pkill", "-KILL", "-u", "reviewer"] for a in argvs)
    assert any(a[6:] == ["rm", "-rf", rr.DISTRO_WORK, rr.DISTRO_STAGE] for a in argvs)


def test_road_dry_run_launches_nothing(tmp_path, capsys):
    set_path = make_set(tmp_path)
    for arm, model in (("claude-road", "claude-opus-5-5"), ("codex-road", "gpt-6.1-sol")):
        args = road_args(set_path, arm, tmp_path, dry_run=True, model=model, timeout=None)
        assert rr.run_arm(args, launcher=lambda *a: pytest.fail("launched"),
                          distro=lambda *a, **k: pytest.fail("distro touched")) == 0
    out = capsys.readouterr().out
    assert ("wsl.exe -d review-road -u root -- /usr/local/sbin/review-run "
            "claude claude-road 1 r001 claude-opus-5-5 xhigh 1800 0") in out
    assert "review-run codex codex-road 1 r002 gpt-6.1-sol xhigh 1800 0" in out
    assert not (tmp_path / "out").exists()


def test_road_refuses_failed_bundle_and_foreign_manifest(tmp_path):
    set_path = make_set(tmp_path)
    args = road_args(set_path, "claude-road", tmp_path, dry_run=True)
    args.bundles = str(make_manifest(tmp_path, set_path, fail=("r002",)))
    with pytest.raises(ValueError, match="r002"):
        rr.run_arm(args)
    args.entries = "r001"
    assert rr.run_arm(args) == 0  # the passed entry alone may run
    doc = json.loads(Path(args.bundles).read_text(encoding="utf-8"))
    doc["set_sha256"] = "0" * 64
    Path(args.bundles).write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(ValueError, match="for set"):
        rr.run_arm(args)


def test_road_refuses_stale_install(tmp_path):
    set_path = make_set(tmp_path)
    code = rr.run_arm(road_args(set_path, "claude-road", tmp_path),
                      launcher=lambda *a: pytest.fail("launched"),
                      distro=fake_distro(prompt_sha="0" * 64))
    assert code == 3 and not (tmp_path / "out").exists()


def test_road_run_records_and_completes(tmp_path, capsys):
    set_path = make_set(tmp_path)
    s, _ = rr.load_set(set_path)
    good = {e["id"]: road_stdout(claude_stream([("Bash", {"command": "pytest -q"})],
                                               json.dumps({"findings": [F]})), road_meta(e["commit"]))
            for e in s["entries"]}
    order = [e["id"] for e in rr.ordered_entries(s, 1, None)]
    launcher = road_launcher(["garbage"] + [good[i] for i in order])
    distro = fake_distro()
    assert rr.run_arm(road_args(set_path, "claude-road", tmp_path), launcher=launcher,
                      distro=distro) == 0
    assert len(launcher.calls) == 3  # one void retried, then two clean reviews
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    assert data["complete"] and data["road"] and data["distro"] == "review-road"
    assert data["prompt_file"] == "prompt-road.md"
    assert data["prompt_sha256"] == hashlib.sha256(rr.lf_bytes(rr.ROAD_PROMPT)).hexdigest() \
        == data["prompt_sha256_in_distro"]
    assert data["review_one_sha256"] == data["review_one_sha256_in_distro"]
    assert data["review_run_sha256"] == data["review_run_sha256_in_distro"]
    assert data["bundle_store"] == "/srv/review-road/bundles" and data["bundle_store_verified"]
    assert all(r["config_changed"] == [] and r["config_before"] == "f" * 64 for r in data["reviews"])
    assert data["harness_build"] == "2.1.318 (Claude Code)" and data["message_shown"] is False
    assert data["timeout_s"] == 5 and 'web_search="disabled"' in data["web_search"]
    first = data["reviews"][0]
    assert first["retries"] == 1 and first["void_attempts"][0]["void_reason"]
    assert all(r["ran_tests"] and r["commands"] == ["pytest -q"] for r in data["reviews"])
    assert all(r["bundle_sha256"] == "b" * 64 for r in data["reviews"])
    text = res.read_text(encoding="utf-8")
    assert '"kind"' not in text and FAKE_FIX not in text and '"defects"' not in text
    hash_checks = [a for a, _ in distro.calls if "sha256sum" in a]
    # installed files and root store at start, then installed files before the
    # retry and before the second entry
    assert len(hash_checks) == 4
    store = [a for a in hash_checks if any(x.startswith(rr.BUNDLE_STORE) for x in a)]
    assert len(store) == 1 and f"{rr.BUNDLE_STORE}/r001.bundle" in store[0]
    assert "ran tests" in capsys.readouterr().out


def test_road_two_voids_stop(tmp_path):
    set_path = make_set(tmp_path)
    launcher = road_launcher(["garbage"])
    assert rr.run_arm(road_args(set_path, "codex-road-message", tmp_path), launcher=launcher,
                      distro=fake_distro()) == 2
    assert len(launcher.calls) == 2
    assert all(c[0][-1] == "1" for c in launcher.calls)  # message shown on -message arms
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    assert data["complete"] is False and "two consecutive" in data["stopped"]
    assert data["message_shown"] is True


def test_road_default_out_dir(tmp_path):
    set_path = make_set(tmp_path)
    s, _ = rr.load_set(set_path)
    outs = [road_stdout(claude_stream([("Read", {"file_path": "x"})], '{"findings": []}'),
                        road_meta(e["commit"])) for e in rr.ordered_entries(s, 1, None)]
    args = road_args(set_path, "claude-road", tmp_path, out=None)
    assert rr.run_arm(args, launcher=road_launcher(outs), distro=fake_distro(), repo=tmp_path) == 0
    assert list((tmp_path / "evals" / "results" / "review-catch-road").glob("*-claude-road-t1.json"))


def test_install_sends_lf_bytes_and_checks_hashes():
    distro = fake_distro()
    assert rr.install(distro) == 0
    sent = {a[7]: data for a, data in distro.calls if a[6] == "tee"}
    assert sent[rr.REVIEW_ONE] == rr.lf_bytes(rr.ROAD_SCRIPT) and b"\r" not in sent[rr.REVIEW_ONE]
    assert sent[rr.REVIEW_RUN] == rr.lf_bytes(rr.ROAD_RUN_SCRIPT) and b"\r" not in sent[rr.REVIEW_RUN]
    assert sent[rr.DISTRO_PROMPT] == rr.lf_bytes(rr.ROAD_PROMPT)
    argvs = [a[6:] for a, _ in distro.calls]
    assert ["chmod", "755", rr.REVIEW_RUN] in argvs and ["chmod", "-R", "600", "/srv/review-road"] in argvs
    assert ["chmod", "700", "/srv/review-road", rr.BUNDLE_STORE] in argvs
    assert all(rr.ARGV_TOKEN.match(x) for a, _ in distro.calls for x in a[1:])
    assert rr.install(fake_distro(script_sha="0" * 64)) == 1
    assert rr.install(fake_distro(run_sha="0" * 64)) == 1


def test_main_install_and_prepare_only_flags(monkeypatch):
    monkeypatch.setattr(rr, "install", lambda: 7)
    assert rr.main(["--install"]) == 7
    with pytest.raises(SystemExit):
        rr.main(["--install", "--dry-run"])
    with pytest.raises(SystemExit):
        rr.main(["--set", "x", "--arm", "claude-blind", "--model", "m", "--effort", "xhigh",
                 "--trial", "1", "--prepare-only"])


def test_review_one_script_is_lf_and_names_the_flags():
    raw = rr.ROAD_SCRIPT.read_bytes()
    text = raw.decode("utf-8")
    assert raw.startswith(b"#!/bin/bash\n")
    for flag in ("--dangerously-skip-permissions", "--disallowedTools WebSearch,WebFetch",
                 "--no-session-persistence", "--output-format stream-json --verbose",
                 "--ephemeral --sandbox danger-full-access", "web_search=\"disabled\"",
                 "--output-last-message", rr.LAST_DELIM, rr.META_DELIM, "Change under review.",
                 "--prepare-only", "trap cleanup EXIT", 'mktemp -d "$WORKROOT/review.XXXXXXXX"',
                 'rm -f "$BUNDLE"', ".codex/config.toml", ".claude/settings.json", "config_changed",
                 "preflight_failures", "/srv/review-road"):
        assert flag in text, flag
    run = rr.ROAD_RUN_SCRIPT.read_bytes()
    assert run.startswith(b"#!/bin/bash\n") and b"\r" not in run
    for needle in (b"/srv/review-road/bundles", b"install -o reviewer -g reviewer -m 600",
                   b"/usr/local/sbin/review-shell.sh /usr/local/bin/review-one", b"trap 'rm -f"):
        assert needle in run, needle


def test_scorer_reads_road_clone_paths():
    d = {"file": "tools/markdownllm/x.py", "ranges": [[100, 110]]}
    assert sr.classify(f(105, 105, "/home/reviewer/work/review.aB3xY9zQ/tools/markdownllm/x.py"), d) == "hit"
    assert sr.classify(f(105, 105, "/home/reviewer/work/review.aB3xY9zQ/markdownllm/x.py"), d) == "miss"
    assert sr.classify(f(105, 105, "tools/markdownllm/x.py"), d) == "hit"
    assert sr.classify(f(105, 105, "/home/reviewer/other/tools/markdownllm/x.py"), d) == "miss"


def test_scorer_keeps_road_arms_apart(tmp_path):
    set_path = make_set(tmp_path)
    _, sha = rr.load_set(set_path)
    res = tmp_path / "res"
    res.mkdir()
    result_file(res, "a.json", sha, arm="claude-road", trial=1, effort="xhigh")
    result_file(res, "b.json", sha, arm="claude-road-message", trial=1, effort="xhigh")
    result_file(res, "c.json", sha, arm="claude-blind", trial=1, effort="xhigh")
    groups, skipped = sr.load_results([str(res)], sha)
    assert not skipped and len(groups) == 3


def test_road_config_change_voids_and_stops_the_arm(tmp_path, capsys):
    set_path = make_set(tmp_path)
    s, _ = rr.load_set(set_path)
    first = rr.ordered_entries(s, 1, None)[0]
    stream = claude_stream([("Read", {"file_path": "x"})], json.dumps({"findings": [F]}))
    out = road_stdout(stream, road_meta(first["commit"], config_after="e" * 64,
                                        config_changed=["~/.claude/settings.json (modified)"]))
    launcher = road_launcher([out])
    assert rr.run_arm(road_args(set_path, "claude-road", tmp_path), launcher=launcher,
                      distro=fake_distro()) == 2
    assert len(launcher.calls) == 1  # no retry, no second entry
    (res,) = list((tmp_path / "out").glob("*.json"))
    data = json.loads(res.read_text(encoding="utf-8"))
    r = data["reviews"][0]
    assert r["void"] and r["void_reason"] == "changed the harness configuration" and r["findings"] == []
    assert r["config_changed"] == ["~/.claude/settings.json (modified)"] and r["config_after"] == "e" * 64
    assert data["complete"] is False and "changed the harness configuration" in data["stopped"]
    assert "settings.json" in data["stopped"]


def test_road_config_change_wins_over_timeout():
    stream = claude_stream([("Read", {"file_path": "x"})], '{"findings": []}')
    rec, _, _ = _road("claude", road_stdout(stream, road_meta(
        C_ITEM, exit_code=124, timed_out=True, config_changed=["~/.codex/config.toml (added)"])))
    assert rec["void_reason"] == "changed the harness configuration" and rec["stop_arm"]


def test_road_preflight_failure_and_staged_bundle_mismatch_void():
    stream = claude_stream([("Read", {"file_path": "x"})], '{"findings": []}')
    rec, _, _ = _road("claude", road_stdout(stream, road_meta(
        C_ITEM, harness_run=False, exit_code=None,
        preflight_failures=["bundle within reach: /home/reviewer/road/x.bundle"])))
    assert rec["void"] and rec["void_reason"].startswith("preflight failed, harness not started")
    assert "x.bundle" in rec["void_reason"] and not rec["stop_arm"]
    rec = rr.review_road_once("claude", "claude-road", 1, _entry(), "m", "xhigh", 60, False,
                              launcher=road_launcher([road_stdout(stream, road_meta(C_ITEM))]),
                              distro=fake_distro(), bundle_sha256="a" * 64)
    assert rec["void"] and rec["void_reason"] == "the staged bundle differs from the manifest"


def test_road_refuses_store_mismatch(tmp_path):
    set_path = make_set(tmp_path)
    for kw in ({"prepare_only": True}, {}):
        code = rr.run_arm(road_args(set_path, "claude-road", tmp_path, **kw),
                          launcher=lambda *a: pytest.fail("launched"),
                          distro=fake_distro(store_sha="0" * 64))
        assert code == 3
    assert not (tmp_path / "out").exists()


def test_road_prepare_only_runs_review_run_with_the_flag(tmp_path, capsys):
    set_path = make_set(tmp_path)
    distro = fake_distro(stdout="HEAD reviewed: abc")
    assert rr.run_arm(road_args(set_path, "codex-road-message", tmp_path, prepare_only=True,
                                entries="r001"),
                      launcher=lambda *a: pytest.fail("launched"), distro=distro) == 0
    runs = [a for a, _ in distro.calls if a[6] == rr.REVIEW_RUN]
    assert runs == [rr.road_command("codex", "codex-road-message", 1, "r001", "test-model-id",
                                    "xhigh", 5, True, prepare_only=True)]
    assert "HEAD reviewed: abc" in capsys.readouterr().out
