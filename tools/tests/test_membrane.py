"""The membrane attention cluster — face coverage, the ingested
species, estate-check clone-walk discovery, and type: import triggers.
Lifted from test_mdllm.py along its banner (sprint 2, F6;
floor-structure-residue item 4)."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from corpus_harness import (  # noqa: E402
    _consumer_with_import, _git_commit, _ns, _sync_git,
    _trust_mcp_entry, thing_text, write,
)


# ---------------------------------------------------------------------------
# membrane attention cluster: face coverage, the ingested species,
# estate-check clone-walk discovery, and type: import triggers
# ---------------------------------------------------------------------------

def _producer(tmp_path, name="srcdom", n_things=2):
    import subprocess as sp
    src = tmp_path / name
    for i in range(n_things):
        write(src, f"things/spec{i}.md", thing_text(
            f"id: spec-{i}\ntype: deliverable\nstatus: approved\n"
            f"created: 2026-06-01\nexposed: true",
            f"# Spec {i}\n\nv1.\n"))
    sp.run(["git", "init", "-q"], cwd=src, check=True)
    _git_commit(src, "create specs")
    return src


def _server_cfg(src):
    return {"command": sys.executable,
            "args": [str(Path(mdllm.__file__)), "mcp-serve", str(src)]}


def test_face_coverage_sees_the_unimported_face(tmp_path):
    # The hole: an address-book entry with ZERO imports never got read at all,
    # so the consumer scored a clean report over an unread face.
    import json
    src = _producer(tmp_path, n_things=3)
    con = tmp_path / "condom"
    write(con, ".mcp.json", json.dumps({"mcpServers": {"srcdom": _server_cfg(src)}}))
    write(con, "things/own.md", thing_text(
        "id: own-thing\ntype: note\nstatus: in-progress\ncreated: 2026-06-01"))
    _trust_mcp_entry(con, "srcdom", _server_cfg(src))
    cov = mdllm.face_coverage(con)
    assert len(cov) == 1
    assert cov[0]["source"] == "srcdom" and cov[0]["state"] == "ok"
    assert cov[0]["offered"] == 3 and cov[0]["imported"] == 0


def test_face_coverage_counts_imports_and_unreachable(tmp_path):
    import json
    src = _producer(tmp_path, n_things=2)
    con = tmp_path / "condom"
    _consumer_with_import(con, "srcdom", "spec-0", "abc1234", _server_cfg(src))
    # second book entry that cannot be spawned
    book = json.loads((con / ".mcp.json").read_text(encoding="utf-8"))
    book["mcpServers"]["ghost"] = {"command": "no-such-binary-xyz", "args": []}
    (con / ".mcp.json").write_text(json.dumps(book), encoding="utf-8")
    _trust_mcp_entry(con, "ghost", book["mcpServers"]["ghost"])
    cov = {c["source"]: c for c in mdllm.face_coverage(con)}
    assert cov["srcdom"]["offered"] == 2 and cov["srcdom"]["imported"] == 1
    assert cov["ghost"]["state"] == "unreachable"


def test_ingested_species_reports_clock_not_coverage_failure(tmp_path, capsys):
    write(tmp_path, "things/register-mirror.md", thing_text(
        "id: register-mirror\ntype: record\nstatus: ingested\ncreated: 2026-06-01\n"
        "origin: external\nverified: false\nsource_system: google-drive\n"
        "source_ref: /exports/register.xlsx\nsource_checked: 2026-07-21"))
    write(tmp_path, "things/undated-mirror.md", thing_text(
        "id: undated-mirror\ntype: record\nstatus: ingested\ncreated: 2026-06-01\n"
        "origin: external\nverified: false\nsource_system: email"))
    rows = {r["id"]: r for r in mdllm.imports_freshness(tmp_path)}
    assert rows["register-mirror"]["state"] == "ingested"
    assert rows["register-mirror"]["checked"] == "2026-07-21"
    assert rows["undated-mirror"]["state"] == "ingested"
    assert rows["undated-mirror"]["checked"] is None
    rc = mdllm.cmd_imports_check(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 0
    assert "2 ingested" in out and "oldest check 2026-07-21" in out
    assert "COVERAGE: 0/0" in out  # ingested never counts as unchecked membrane coverage
    assert "1 undated" in out


def test_ingestion_without_source_system_stays_incomplete(tmp_path):
    write(tmp_path, "things/orphan.md", thing_text(
        "id: orphan\ntype: record\nstatus: ingested\ncreated: 2026-06-01\n"
        "origin: external\nverified: false"))
    rows = mdllm.imports_freshness(tmp_path)
    assert rows[0]["state"] == "incomplete"


def test_import_trigger_state_is_fires_on_stale(tmp_path, capsys):
    # The fired-unseen class: the source moves under the pin, and the trigger
    # vocabulary can finally name what imports-check computes.
    src = _producer(tmp_path, n_things=1)
    con = tmp_path / "condom"
    _consumer_with_import(con, "srcdom", "spec-0", "aaa0000", _server_cfg(src),
                          body="# Spec 0\n\nv1.\n")  # pin != real commit -> stale
    write(con, "things/watcher.md", thing_text(
        "id: watcher\ntype: note\nstatus: in-progress\ncreated: 2026-06-01\n"
        "triggers:\n  - type: import\n    condition: state_is\n"
        "    watch: [imported-spec]\n    action: re_evaluate"))
    rc = mdllm.cmd_triggers(_ns(path=str(con)))
    out = capsys.readouterr().out
    assert rc == 0
    assert "watcher: import `imported-spec` is stale" in out


def test_import_trigger_porch_offers_unimported(tmp_path, capsys):
    import json
    src = _producer(tmp_path, n_things=3)
    con = tmp_path / "condom"
    write(con, ".mcp.json", json.dumps({"mcpServers": {"srcdom": _server_cfg(src)}}))
    write(con, "things/watcher.md", thing_text(
        "id: watcher\ntype: note\nstatus: in-progress\ncreated: 2026-06-01\n"
        "triggers:\n  - type: import\n    condition: porch_offers_unimported\n"
        "    source: srcdom\n    action: surface"))
    _trust_mcp_entry(con, "srcdom", _server_cfg(src))
    rc = mdllm.cmd_triggers(_ns(path=str(con)))
    out = capsys.readouterr().out
    assert rc == 0
    assert "watcher: face `srcdom` offers 3, imported 0" in out


def test_import_trigger_unknown_watch_is_honest(tmp_path, capsys):
    write(tmp_path, "things/watcher.md", thing_text(
        "id: watcher\ntype: note\nstatus: in-progress\ncreated: 2026-06-01\n"
        "triggers:\n  - type: import\n    condition: state_is\n"
        "    watch: [ghost-import]\n    action: surface"))
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "watches `ghost-import` but no such import exists" in out


def test_import_trigger_fresh_import_stays_quiet(tmp_path, capsys):
    src = _producer(tmp_path, n_things=1)
    pin_src = src  # single-commit repo: per-thing pin == HEAD
    import subprocess as sp
    pin = sp.run(["git", "rev-parse", "--short", "HEAD"], cwd=pin_src,
                 capture_output=True, text=True).stdout.strip()
    con = tmp_path / "condom"
    _consumer_with_import(con, "srcdom", "spec-0", pin, _server_cfg(src),
                          body="# Spec 0\n\nv1.\n")
    write(con, "things/watcher.md", thing_text(
        "id: watcher\ntype: note\nstatus: in-progress\ncreated: 2026-06-01\n"
        "triggers:\n  - type: import\n    condition: state_is\n"
        "    watch: [imported-spec]\n    action: re_evaluate"))
    mdllm.cmd_triggers(_ns(path=str(con)))
    out = capsys.readouterr().out
    assert "import `imported-spec`" not in out
    assert "No trigger conditions currently true." in out


def test_triggers_estate_sweep_rolls_up(tmp_path, capsys, monkeypatch):
    import subprocess as sp
    monkeypatch.chdir(tmp_path)
    sp.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "domain").mkdir()
    dom = tmp_path / "domain" / "alpha"
    write(dom, "things/overdue.md", thing_text(
        "id: overdue-item\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "due_date: 2026-06-15"))
    sp.run(["git", "init", "-q"], cwd=dom, check=True)
    rc = mdllm.cmd_triggers(_ns(path=".", estate=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "Estate Trigger Sweep" in out and "not an estate manifest" in out
    assert "### alpha" in out and "OVERDUE" in out
    assert "### Roll-up" in out and "alpha: 1 fired" in out


def test_estate_check_no_args_walks_local_clones(tmp_path, capsys, monkeypatch):
    # Discovery is repos-not-membranes: no args -> walk the same clone set
    # estate-sync walks, and say so in the header.
    import subprocess as sp
    monkeypatch.chdir(tmp_path)
    sp.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "domain").mkdir()
    dom = tmp_path / "domain" / "alpha"
    write(dom, "things/own.md", thing_text(
        "id: own-thing\ntype: note\nstatus: in-progress\ncreated: 2026-06-01"))
    sp.run(["git", "init", "-q"], cwd=dom, check=True)
    rc = mdllm.cmd_estate_check(_ns(paths=[]))
    out = capsys.readouterr().out
    assert rc == 0
    assert "local clones walked" in out and "not an estate manifest" in out
    assert "alpha" in out




def test_fast_path_substitutes_only_this_installations_launcher(tmp_path):
    # The books carry the portable launch route; the floor's own reads
    # substitute sys.executable + our own mdllm.py — but ONLY when the entry
    # resolves to this installation's entry script. Anything else runs
    # verbatim (2026-08-30: the launcher's per-spawn probe exceeded the 10s
    # membrane deadline, so every granted route still read unreachable).
    import sys as _sys
    from markdownllm.imports_check import _fast_path_launcher
    own_tools = Path(__file__).resolve().parents[1]

    cfg = {"command": "pwsh",
           "args": ["-NoProfile", "-File", str(own_tools / "mdllm.ps1"),
                    "mcp-serve", "../src"]}
    fast = _fast_path_launcher(cfg, tmp_path)
    assert fast is not None
    exe, args = fast
    assert exe == _sys.executable
    assert args == [str(own_tools / "mdllm.py"), "mcp-serve", "../src"]

    # python-shaped entry, relative to the consumer root
    consumer = tmp_path / "domain" / "consumer"
    consumer.mkdir(parents=True)
    rel = Path(os.path.relpath(own_tools / "mdllm.py", consumer)).as_posix()
    fast = _fast_path_launcher(
        {"command": "python", "args": [rel, "mcp-serve", "../src"]}, consumer)
    assert fast is not None and fast[0] == _sys.executable

    # a foreign mdllm.ps1 is NOT ours to substitute
    foreign = tmp_path / "elsewhere" / "tools"
    foreign.mkdir(parents=True)
    (foreign / "mdllm.ps1").write_text("# not ours\n")
    assert _fast_path_launcher(
        {"command": "pwsh",
         "args": ["-File", str(foreign / "mdllm.ps1"),
                  "mcp-serve", "../src"]}, tmp_path) is None

    # a different subcommand runs verbatim
    assert _fast_path_launcher(
        {"command": "pwsh",
         "args": ["-File", str(own_tools / "mdllm.ps1"),
                  "validate", "."]}, tmp_path) is None

    # an unrecognised command shape runs verbatim
    assert _fast_path_launcher(
        {"command": "node",
         "args": [str(own_tools / "mdllm.py"), "mcp-serve", "../s"]},
        tmp_path) is None
