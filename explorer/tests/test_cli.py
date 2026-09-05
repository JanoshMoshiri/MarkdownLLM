from __future__ import annotations

import http.client
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

import pytest

from markdownllm_explorer import __main__ as cli


EXPLORER = Path(__file__).parents[1]


def process_group_options() -> dict:
    return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}


def interrupt(process: subprocess.Popen) -> None:
    if os.name == "nt": process.send_signal(signal.CTRL_BREAK_EVENT)
    else: os.killpg(process.pid, signal.SIGINT)


def cli_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(EXPLORER / "src")
    return environment


@pytest.mark.system
def test_cli_requires_root_and_reports_invalid_configuration(tmp_path):
    missing = subprocess.run([sys.executable, "-m", "markdownllm_explorer"], cwd=tmp_path, env=cli_environment(), capture_output=True, text=True, timeout=5)
    assert missing.returncode == 2 and "--root" in missing.stderr
    invalid = subprocess.run([sys.executable, "-m", "markdownllm_explorer", "--root", str(tmp_path / "absent")], cwd=tmp_path, env=cli_environment(), capture_output=True, text=True, timeout=5)
    assert invalid.returncode == 2 and "startup failed" in invalid.stderr.casefold() and str(tmp_path) not in invalid.stderr
    invalid_port = subprocess.run([sys.executable, "-m", "markdownllm_explorer", "--root", str(tmp_path), "--port", "70000"], cwd=tmp_path, env=cli_environment(), capture_output=True, text=True, timeout=5)
    assert invalid_port.returncode == 2 and "between 0 and 65535" in invalid_port.stderr


@pytest.mark.system
def test_cli_launches_from_arbitrary_cwd_with_packaged_assets(estate, tmp_path):
    process = subprocess.Popen(
        [sys.executable, "-m", "markdownllm_explorer", "--root", str(estate), "--port", "0"],
        cwd=tmp_path, env=cli_environment(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        **process_group_options(),
    )
    try:
        assert process.stdout is not None
        deadline = time.monotonic() + 8; url = ""
        while time.monotonic() < deadline:
            line = process.stdout.readline()
            if "MarkdownLLM Explorer:" in line:
                url = line.split("MarkdownLLM Explorer:", 1)[1].strip(); break
        assert url
        parsed = urlsplit(url); connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=3)
        connection.request("GET", "/health", headers={"Host": f"127.0.0.1:{parsed.port}"})
        response = connection.getresponse(); payload = json.loads(response.read()); connection.close()
        assert response.status == 200 and payload["status"] == "ok"
        connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=3)
        connection.request("GET", "/", headers={"Host": f"127.0.0.1:{parsed.port}"})
        response = connection.getresponse(); body = response.read(); connection.close()
        assert response.status == 200 and b"/js/app.js" in body
        active = socket.create_connection(("127.0.0.1", parsed.port), timeout=3)
        active.sendall(f"GET /health HTTP/1.1\r\nHost: 127.0.0.1:{parsed.port}\r\n".encode())
        started = time.monotonic(); interrupt(process); assert process.wait(timeout=6) == 0
        assert time.monotonic() - started <= 5.5
        active.close()
    finally:
        if process.poll() is None:
            process.kill(); process.wait(timeout=5)


@pytest.mark.system
def test_cli_requested_port_collision_is_controlled(estate, tmp_path):
    listener = socket.socket(); listener.bind(("127.0.0.1", 0)); listener.listen(1)
    try:
        port = listener.getsockname()[1]
        result = subprocess.run(
            [sys.executable, "-m", "markdownllm_explorer", "--root", str(estate), "--port", str(port)],
            cwd=tmp_path, env=cli_environment(), capture_output=True, text=True, timeout=8,
        )
        assert result.returncode == 2 and "startup failed" in result.stderr.casefold()
    finally:
        listener.close()


@pytest.mark.unit
def test_cli_open_browser_hands_off_capability_url(estate, monkeypatch):
    class FinishedServer:
        def __init__(self):
            self.closed = False
            self.joined = None

        def serve_forever(self, poll_interval=0.2):
            return

        def server_close(self):
            self.closed = True

        def join_active(self, timeout):
            self.joined = timeout

    runtime = object(); server = FinishedServer(); opened = []
    monkeypatch.setattr(cli, "build_runtime", lambda root, domain: runtime)
    monkeypatch.setattr(cli, "build_server", lambda value, port: (server, "http://127.0.0.1:43121/#cap=opaque"))

    result = cli.main(["--root", str(estate), "--open-browser"], browser_opener=lambda url: opened.append(url) or True)

    assert result == 0 and opened == ["http://127.0.0.1:43121/#cap=opaque"]
    assert server.closed and server.joined == 4.5


@pytest.mark.unit
@pytest.mark.parametrize("stop_signal", [signal.SIGINT, signal.SIGTERM])
def test_cli_restores_background_stop_signals_and_closes_server(estate, monkeypatch, stop_signal):
    handlers = {signal.SIGINT: signal.SIG_IGN, signal.SIGTERM: signal.SIG_DFL}
    if hasattr(signal, "SIGBREAK"):
        handlers[signal.SIGBREAK] = signal.SIG_DFL
    original = handlers.copy()

    def register(item, handler):
        previous = handlers[item]
        handlers[item] = handler
        return previous

    class InterruptedServer:
        closed = False
        joined = None

        def serve_forever(self, poll_interval):
            handlers[stop_signal](stop_signal, None)

        def server_close(self):
            self.closed = True

        def join_active(self, timeout):
            self.joined = timeout

    server = InterruptedServer()
    monkeypatch.setattr(cli.signal, "signal", register)
    monkeypatch.setattr(cli, "build_runtime", lambda *_: object())
    monkeypatch.setattr(cli, "build_server", lambda *_: (server, "http://127.0.0.1:43121/#cap=opaque"))
    assert cli.main(["--root", str(estate)]) == 0
    assert server.closed and server.joined == 4.5
    assert handlers == original


@pytest.mark.system
@pytest.mark.skipif(os.name != "posix", reason="requires POSIX inherited signal dispositions")
def test_background_cli_accepts_stop_after_inheriting_ignored_sigint(estate, tmp_path):
    program = (
        "import signal; signal.signal(signal.SIGINT, signal.SIG_IGN); "
        "from markdownllm_explorer.__main__ import main; raise SystemExit(main())"
    )
    process = subprocess.Popen(
        [sys.executable, "-c", program, "--root", str(estate)],
        cwd=tmp_path, env=cli_environment(), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, start_new_session=True,
    )
    try:
        assert process.stdout is not None
        # Wait for readiness over HTTP before interrupting.
        process.stdout.readline()
        url = process.stdout.readline().split("MarkdownLLM Explorer:", 1)[1].strip()
        parsed = urlsplit(url)
        connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=5)
        connection.request("GET", "/health")
        response = connection.getresponse()
        assert response.status == 200
        response.read()
        connection.close()
        process.send_signal(signal.SIGINT)
        assert process.wait(timeout=6) == 0
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
