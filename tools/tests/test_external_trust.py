"""The repository/external-I/O boundary is deny-by-default and clone-local."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm import imports_check as imports_mod  # noqa: E402


def _repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    return path


def _book(root: Path, name: str, entry: dict) -> None:
    (root / ".mcp.json").write_text(
        json.dumps({"mcpServers": {name: entry}}), encoding="utf-8")


def _grant(root: Path, name: str, entry: dict,
           permissions: tuple[str, ...] | None = None):
    policy = mdllm.LocalExternalTrustPolicy()
    digest = policy.evaluate(root, name, entry).entry_hash
    permissions = permissions or tuple(
        p.value for p in mdllm.required_capabilities(entry))
    return mdllm.grant_external_trust(
        root, name, entry, permissions, digest)


def _stdio_server(tmp_path: Path, *, body: str = "manifest",
                  sleep: float = 0.0) -> tuple[dict, Path]:
    marker = tmp_path / "protocol.json"
    script = tmp_path / "server.py"
    script.write_text(
        "import json, pathlib, sys, time\n"
        f"marker = pathlib.Path({str(marker)!r})\n"
        "methods = []\n"
        "for line in sys.stdin:\n"
        "    msg = json.loads(line); methods.append(msg.get('method'))\n"
        f"    time.sleep({sleep!r})\n"
        "    if msg.get('method') == 'initialize':\n"
        "        print(json.dumps({'jsonrpc':'2.0','id':msg['id'],"
        "'result':{'protocolVersion':'test','capabilities':{},'serverInfo':{}}}),"
        " flush=True)\n"
        "    elif msg.get('method') == 'resources/read':\n"
        f"        text = {body!r}\n"
        "        print(json.dumps({'jsonrpc':'2.0','id':msg['id'],"
        "'result':{'contents':[{'text':text}]}}), flush=True)\n"
        "marker.write_text(json.dumps(methods), encoding='utf-8')\n",
        encoding="utf-8",
    )
    return {"command": sys.executable, "args": [str(script)]}, marker


def test_untrusted_repository_command_is_never_spawned(tmp_path):
    root = _repo(tmp_path / "consumer")
    marker = tmp_path / "spawned"
    entry = {
        "command": sys.executable,
        "args": ["-c", f"from pathlib import Path; Path({str(marker)!r}).touch()"],
    }
    _book(root, "malicious", entry)

    coverage = mdllm.face_coverage(root)

    assert coverage[0]["state"] == "unevaluable-untrusted"
    assert not marker.exists()


def test_trigger_and_session_paths_leave_untrusted_route_unevaluable(
        tmp_path, capsys):
    root = _repo(tmp_path / "consumer")
    marker = tmp_path / "spawned"
    entry = {
        "command": sys.executable,
        "args": ["-c", f"from pathlib import Path; Path({str(marker)!r}).touch()"],
    }
    _book(root, "source", entry)
    things = root / "things"
    things.mkdir()
    (things / "watcher.md").write_text(
        "---\nid: watcher\ntype: note\nstatus: in-progress\ncreated: 2026-08-20\n"
        "triggers:\n  - type: import\n    condition: porch_offers_unimported\n"
        "    source: source\n    action: surface\n---\n\n# Watcher\n",
        encoding="utf-8",
    )

    assert mdllm.cmd_triggers(SimpleNamespace(path=str(root), estate=False)) == 0
    trigger_output = capsys.readouterr().out
    assert "untrusted and was not executed" in trigger_output
    assert not marker.exists()

    assert mdllm.cmd_session_start(
        SimpleNamespace(path=str(root), contract=False)) == 0
    session_output = capsys.readouterr().out
    assert "not mechanically evaluable" in session_output
    assert not marker.exists()


def test_grant_is_git_local_hash_bound_and_config_drift_revokes_it(tmp_path):
    root = _repo(tmp_path / "consumer")
    entry = {"command": "safe-command", "args": ["one"]}
    _book(root, "source", entry)
    granted = _grant(root, "source", entry)

    assert granted.authorized
    assert granted.store_path is not None
    assert granted.store_path.is_relative_to(root / ".git")
    status = subprocess.run(
        ["git", "status", "--short"], cwd=root, capture_output=True,
        text=True, check=True).stdout
    assert ".mcp.json" in status
    assert "external-trust" not in status and "markdownllm" not in status

    changed = {"command": "safe-command", "args": ["two"]}
    decision = mdllm.LocalExternalTrustPolicy().evaluate(root, "source", changed)
    assert decision.state == "unevaluable-untrusted"
    assert decision.entry_hash != granted.entry_hash
    assert not decision.granted


def test_capabilities_are_independent_and_partial_trust_does_not_execute(tmp_path):
    root = _repo(tmp_path / "consumer")
    marker = tmp_path / "spawned"
    entry = {
        "command": sys.executable,
        "args": ["-c", f"from pathlib import Path; Path({str(marker)!r}).touch()"],
    }
    _book(root, "source", entry)
    decision = _grant(root, "source", entry, ("command",))

    assert decision.command_authorized
    assert not decision.body_read_authorized
    assert decision.state == "unevaluable-untrusted"
    state, got = imports_mod._mcp_face_read(entry, root, [], "source")
    assert (state, got) == ("unevaluable-untrusted", None)
    assert not marker.exists()


def test_review_redacts_header_values_query_values_and_secret_args(tmp_path, capsys):
    root = _repo(tmp_path / "consumer")
    entry = {
        "url": "https://example.invalid/mcp?token=top-secret&mode=read",
        "headers": {"Authorization": "Bearer top-secret", "X-Mode": "read"},
    }
    _book(root, "remote", entry)

    rc = mdllm.cmd_external_trust(SimpleNamespace(
        action="review", server="remote", path=str(root),
        expected_hash=None, allow=None))
    output = capsys.readouterr().out

    assert rc == 0
    assert "top-secret" not in output
    assert "Authorization" in output and "X-Mode" in output
    assert "Entry hash: sha256:" in output
    assert "token=" in output and "mode=" in output


def test_command_review_states_that_trust_is_not_a_sandbox(tmp_path, capsys):
    root = _repo(tmp_path / "consumer")
    entry = {"command": "reviewed-server", "args": ["--serve"]}
    _book(root, "source", entry)

    rc = mdllm.cmd_external_trust(SimpleNamespace(
        action="review", server="source", path=str(root),
        expected_hash=None, allow=None))
    output = capsys.readouterr().out

    assert rc == 0
    assert "current OS user's authority" in output
    assert "does not sandbox it" in output


def test_trust_requires_the_reviewed_hash_and_is_revocable(tmp_path):
    root = _repo(tmp_path / "consumer")
    entry = {"command": "source-server", "args": []}
    _book(root, "source", entry)
    policy = mdllm.LocalExternalTrustPolicy()
    digest = policy.evaluate(root, "source", entry).entry_hash

    bad = mdllm.cmd_external_trust(SimpleNamespace(
        action="trust", server="source", path=str(root),
        expected_hash="sha256:" + "0" * 64,
        allow=["command", "body-read"]))
    assert bad == 2
    assert policy.evaluate(root, "source", entry).state == "unevaluable-untrusted"

    good = mdllm.cmd_external_trust(SimpleNamespace(
        action="trust", server="source", path=str(root),
        expected_hash=digest, allow=["command", "body-read"]))
    assert good == 0
    assert policy.evaluate(root, "source", entry).authorized

    revoked = mdllm.cmd_external_trust(SimpleNamespace(
        action="revoke", server="source", path=str(root),
        expected_hash=None, allow=None))
    assert revoked == 0
    assert policy.evaluate(root, "source", entry).state == "unevaluable-untrusted"


def test_duplicate_config_keys_cannot_be_reviewed_or_trusted(tmp_path, capsys):
    root = _repo(tmp_path / "consumer")
    (root / ".mcp.json").write_text(
        '{"mcpServers":{"source":{"command":"safe","command":"evil"}}}',
        encoding="utf-8")

    rc = mdllm.cmd_external_trust(SimpleNamespace(
        action="review", server="source", path=str(root),
        expected_hash=None, allow=None))
    output = capsys.readouterr().out

    assert rc == 2
    assert "duplicate JSON key 'command'" in output
    assert not (root / ".git" / "markdownllm" / "external-trust.json").exists()


@pytest.mark.parametrize("url", [
    "file:///etc/passwd",
    "ftp://127.0.0.1/content",
    "http://example.invalid/mcp",
    "https://user:password@example.invalid/mcp",
])
def test_unsafe_network_declarations_are_invalid(url, tmp_path):
    root = _repo(tmp_path / "consumer")
    decision = mdllm.LocalExternalTrustPolicy().evaluate(
        root, "remote", {"url": url})
    assert decision.state == "unevaluable-invalid-config"


def test_arbitrary_untrusted_https_url_never_reaches_network_adapter(
        tmp_path, monkeypatch):
    root = _repo(tmp_path / "consumer")
    entry = {"url": "https://exfiltration.invalid/mcp",
             "headers": {"Authorization": "Bearer secret"}}

    def forbidden(*args, **kwargs):
        raise AssertionError("network adapter called for untrusted repository data")

    monkeypatch.setattr(imports_mod, "_mcp_http_read", forbidden)
    state, got = imports_mod._mcp_face_read(entry, root, ["manifest://x"], "x")
    assert (state, got) == ("unevaluable-untrusted", None)


def test_http_redirect_is_not_followed(tmp_path):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    calls = {"target": 0}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            self.rfile.read(length)
            if self.path == "/redirect":
                self.send_response(307)
                self.send_header("Location", "/target")
                self.send_header("Content-Length", "0")
                self.end_headers()
            else:
                calls["target"] += 1
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", "2")
                self.end_headers(); self.wfile.write(b"{}")

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        root = _repo(tmp_path / "consumer")
        entry = {"url": f"http://127.0.0.1:{server.server_address[1]}/redirect"}
        _grant(root, "remote", entry)
        state, got = imports_mod._mcp_face_read(
            entry, root, ["manifest://remote"], "remote")
        assert (state, got) == ("unreachable", None)
        assert calls["target"] == 0
    finally:
        server.shutdown(); server.server_close()


def test_stdio_response_is_bounded_and_timeout_is_bounded(tmp_path):
    huge_entry, _ = _stdio_server(
        tmp_path, body="x" * (imports_mod.MAX_EXTERNAL_RESPONSE_BYTES + 1))
    assert imports_mod._mcp_client_read(
        huge_entry["command"], huge_entry["args"], tmp_path,
        ["manifest://x"]) is None

    slow_entry, _ = _stdio_server(tmp_path, sleep=1.0)
    assert imports_mod._mcp_client_read(
        slow_entry["command"], slow_entry["args"], tmp_path,
        ["manifest://x"], timeout=0.05) is None


def test_trusted_stdio_completes_initialize_initialized_then_reads(tmp_path):
    root = _repo(tmp_path / "consumer")
    entry, marker = _stdio_server(tmp_path, body="quoted external data")
    _grant(root, "source", entry)

    state, got = imports_mod._mcp_face_read(
        entry, root, ["manifest://source"], "source")

    assert state == "ok"
    assert got == {"manifest://source": "quoted external data"}
    assert json.loads(marker.read_text(encoding="utf-8")) == [
        "initialize", "notifications/initialized", "resources/read"]


def test_legacy_short_commit_pin_matches_only_its_full_hex_commit():
    full = "abcdef1234567890abcdef1234567890abcdef12"
    assert imports_mod._pins_match("abcdef1", full)
    assert imports_mod._pins_match(full, "abcdef123456")
    assert not imports_mod._pins_match("abcdef0", full)
    assert not imports_mod._pins_match("abc", full)
    assert not imports_mod._pins_match("not-hex-prefix", full)
