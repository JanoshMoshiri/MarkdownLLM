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
