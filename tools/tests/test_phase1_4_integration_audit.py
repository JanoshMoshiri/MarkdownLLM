"""Cross-phase regressions found by the Phase 1-4 integration audit."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from argparse import Namespace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import imports_check as imports_mod  # noqa: E402
from markdownllm import scaffold as scaffold_mod  # noqa: E402
from markdownllm import sync as sync_mod  # noqa: E402
from markdownllm.coherence import coherence_findings  # noqa: E402
from markdownllm.repository_transaction import RepositoryTransaction  # noqa: E402
from markdownllm.touchpoints import cmd_candidates  # noqa: E402
from markdownllm.validation import check_version_sync  # noqa: E402


for _key in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_key, "phase-audit-tests")
for _key in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_key, "phase-audit-tests@local")


def _git(root: Path, *args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=check,
        capture_output=True, text=True,
    ).stdout.strip()


def _repo(root: Path, *, seed: bool = False) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    if seed:
        (root / "seed.txt").write_text("seed\n", encoding="utf-8")
        _git(root, "add", "seed.txt")
        _git(root, "commit", "-q", "-m", "seed")
    return root


def _thing(identifier: str, *, exposed: bool = False,
           frontmatter: bool = True) -> str:
    if not frontmatter:
        return "# No longer a thing\n"
    exposure = "exposed: true\n" if exposed else ""
    return (
        "---\n"
        f"id: {identifier}\n"
        "type: note\n"
        "status: in-progress\n"
        "created: 2026-08-20\n"
        f"{exposure}"
        "---\n\n"
        f"# {identifier}\n"
    )


def test_malformed_address_book_is_invalid_not_a_missing_route(tmp_path):
    root = _repo(tmp_path / "consumer")
    things = root / "things"
    things.mkdir()
    (things / "import.md").write_text(
        "---\nid: imported\ntype: note\nstatus: in-progress\n"
        "created: 2026-08-20\norigin: external\nsource_domain: source\n"
        "source_id: offered\nsource_commit: abcdef1\n---\n\n# Import\n",
        encoding="utf-8",
    )
    (root / ".mcp.json").write_text(
        '{"mcpServers":{"source":{"command":"safe"},"source":{"command":"evil"}}}',
        encoding="utf-8",
    )

    rows = imports_mod.imports_freshness(root)

    assert rows[0]["state"] == "unevaluable-invalid-config"


def test_http_response_budget_applies_to_the_whole_mcp_operation(tmp_path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            message = json.loads(self.rfile.read(length))
            method = message.get("method")
            if method == "notifications/initialized":
                self.send_response(202)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            if method == "initialize":
                result = {
                    "jsonrpc": "2.0", "id": message["id"],
                    "result": {"protocolVersion": "test", "capabilities": {},
                               "serverInfo": {}},
                }
            else:
                result = {
                    "jsonrpc": "2.0", "id": message["id"],
                    "result": {"contents": [{"text": "x" * 220}]},
                }
            body = json.dumps(result).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/mcp"
        result = imports_mod._mcp_http_read(
            url, ["thing://source/one", "thing://source/two"],
            max_response_bytes=600,
        )
        assert result is None
    finally:
        server.shutdown()
        server.server_close()


def test_candidate_modification_reports_identity_and_exposure_removal(
        tmp_path, capsys):
    root = _repo(tmp_path / "domain")
    target = root / "things" / "target.md"
    target.parent.mkdir()
    target.write_text(_thing("old-id", exposed=True), encoding="utf-8")
    _git(root, "add", "things/target.md")
    _git(root, "commit", "-q", "-m", "base")

    target.write_text(_thing("new-id", exposed=False), encoding="utf-8")
    _git(root, "add", "things/target.md")

    assert cmd_candidates(Namespace(path=str(root), view="index")) == 0
    output = capsys.readouterr().out
    assert "identity `old-id` -> `new-id`" in output
    assert "withdraws" in output and "old-id" in output


def test_candidate_modification_that_removes_frontmatter_is_a_deletion(
        tmp_path, capsys):
    root = _repo(tmp_path / "domain")
    target = root / "things" / "target.md"
    target.parent.mkdir()
    target.write_text(_thing("old-id", exposed=True), encoding="utf-8")
    _git(root, "add", "things/target.md")
    _git(root, "commit", "-q", "-m", "base")

    target.write_text(_thing("unused", frontmatter=False), encoding="utf-8")
    _git(root, "add", "things/target.md")

    assert cmd_candidates(Namespace(path=str(root), view="index")) == 0
    output = capsys.readouterr().out
    assert "old-id" in output and "deleted" in output
    assert "withdraws" in output


def test_duplicate_framework_sentinel_is_a_finding_not_an_exception(tmp_path):
    root = tmp_path / "framework"
    root.mkdir()
    (root / ".markdownllm").write_text(
        "version: 1.0.0\nversion: 2.0.0\n", encoding="utf-8")

    validation = check_version_sync(root)
    coherence = coherence_findings(root, window=10)

    assert any(f.severity == "Error" and "duplicate key 'version'" in f.message
               for f in validation)
    assert any(f.severity == "Error" and "duplicate key 'version'" in f.message
               for f in coherence)


def test_autopush_publishes_only_the_current_branch_upstream(tmp_path):
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "--bare", "-q", str(remote))
    repo = _repo(tmp_path / "repo")
    (repo / "AGENTS.md").write_text(
        "---\ngit:\n  autopush: true\n---\n", encoding="utf-8")
    (repo / "main.txt").write_text("main 1\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "main 1")
    _git(repo, "branch", "-M", "main")
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-q", "-u", "origin", "main")

    _git(repo, "checkout", "-q", "-b", "other")
    (repo / "other.txt").write_text("other 1\n", encoding="utf-8")
    _git(repo, "add", "other.txt")
    _git(repo, "commit", "-q", "-m", "other 1")
    _git(repo, "push", "-q", "-u", "origin", "other")
    remote_other = _git(remote, "rev-parse", "refs/heads/other")
    (repo / "other.txt").write_text("other 2\n", encoding="utf-8")
    _git(repo, "add", "other.txt")
    _git(repo, "commit", "-q", "-m", "other 2")

    _git(repo, "checkout", "-q", "main")
    (repo / "main.txt").write_text("main 2\n", encoding="utf-8")
    _git(repo, "add", "main.txt")
    _git(repo, "commit", "-q", "-m", "main 2")
    _git(repo, "config", "push.default", "matching")

    result = sync_mod.autopush_repo(repo)

    assert result["state"] == "published"
    assert _git(remote, "rev-parse", "refs/heads/main") == _git(repo, "rev-parse", "main")
    assert _git(remote, "rev-parse", "refs/heads/other") == remote_other


def test_scaffold_escapes_gitignore_pattern_characters(tmp_path):
    outer = _repo(tmp_path / "outer", seed=True)
    target = outer / "domains[private]" / "new-domain"

    assert scaffold_mod.cmd_scaffold(
        SimpleNamespace(path=str(target), harness="none")) == 0

    check = subprocess.run(
        ["git", "-C", str(outer), "check-ignore", "-q", "--",
         "domains[private]/new-domain/"], capture_output=True, text=True)
    assert check.returncode == 0


def test_scaffold_refuses_moved_outer_head_before_birth_writes(tmp_path):
    outer = _repo(tmp_path / "outer", seed=True)
    target = outer / "new-domain"
    isolation = scaffold_mod._preflight_outer_isolation(target)
    assert isinstance(isolation.transaction, RepositoryTransaction)

    _git(outer, "commit", "-q", "--allow-empty", "-m", "concurrent move")

    try:
        scaffold_mod._initialise_and_isolate(target, isolation)
    except SystemExit as exc:
        assert "HEAD moved" in str(exc)
    else:
        raise AssertionError("a moved optimistic base was accepted")
    assert not target.exists()
    assert not (outer / ".gitignore").exists()
    assert _git(outer, "log", "-1", "--format=%s") == "concurrent move"


def test_scaffold_compare_and_swap_rejects_head_move_during_apply(
        tmp_path, monkeypatch):
    outer = _repo(tmp_path / "outer", seed=True)
    target = outer / "new-domain"
    isolation = scaffold_mod._preflight_outer_isolation(target)
    original = RepositoryTransaction._run_hook
    moved = {"done": False}

    def concurrent_commit(self, name, args, env):
        if name == "pre-commit" and not moved["done"]:
            clean_env = os.environ.copy()
            clean_env.pop("GIT_INDEX_FILE", None)
            subprocess.run(
                ["git", "-C", str(outer), "commit", "-q", "--allow-empty",
                 "--no-verify", "-m", "concurrent during apply"],
                check=True, env=clean_env)
            moved["done"] = True
        return original(self, name, args, env)

    monkeypatch.setattr(RepositoryTransaction, "_run_hook", concurrent_commit)
    try:
        scaffold_mod._initialise_and_isolate(target, isolation)
    except SystemExit as exc:
        assert "HEAD moved" in str(exc)
    else:
        raise AssertionError("compare-and-swap accepted a moved HEAD")

    assert not target.exists()
    assert not (outer / ".gitignore").exists()
    assert _git(outer, "log", "-1", "--format=%s") == "concurrent during apply"


def test_scaffold_transaction_supports_an_unborn_outer_repo(tmp_path):
    outer = _repo(tmp_path / "outer")
    target = outer / "new-domain"

    assert scaffold_mod.cmd_scaffold(SimpleNamespace(
        path=str(target), harness="none")) == 0

    assert _git(outer, "show", "--pretty=format:", "--name-only", "HEAD") == ".gitignore"
    assert _git(outer, "diff", "--cached", "--name-only") == ""


def test_scaffold_autopush_is_default_off_and_explicitly_enableable(tmp_path):
    default_domain = tmp_path / "default-domain"
    enabled_domain = tmp_path / "enabled-domain"

    assert scaffold_mod.cmd_scaffold(SimpleNamespace(
        path=str(default_domain), harness="none")) == 0
    assert scaffold_mod.cmd_scaffold(SimpleNamespace(
        path=str(enabled_domain), harness="none", autopush="true")) == 0

    assert sync_mod._autopush_enabled(default_domain) is False
    assert sync_mod._autopush_enabled(enabled_domain) is True
    assert "autopush: false" in (default_domain / "AGENTS.md").read_text(
        encoding="utf-8")
    assert "autopush: true" in (enabled_domain / "AGENTS.md").read_text(
        encoding="utf-8")
