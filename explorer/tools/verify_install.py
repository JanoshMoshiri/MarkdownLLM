"""Build, install offline into a clean venv, and launch from an arbitrary cwd."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import platform
import signal
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


def run(command: list[str], *, cwd: Path, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True, check=True, timeout=timeout)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode(); digest.update(relative)
        if path.is_file(): digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def group_options() -> dict:
    return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}


def interrupt(process: subprocess.Popen) -> None:
    if os.name == "nt": process.send_signal(signal.CTRL_BREAK_EVENT)
    else: os.killpg(process.pid, signal.SIGINT)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    explorer = Path(__file__).parents[1].resolve()
    arguments.wheelhouse = arguments.wheelhouse.resolve()
    output = arguments.output or explorer / "tests" / "evidence" / "clean-install.json"
    arguments.wheelhouse.mkdir(parents=True, exist_ok=True)
    run([
        arguments.python, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation",
        "--wheel-dir", str(arguments.wheelhouse), str(explorer),
    ], cwd=explorer)
    wheels = sorted(arguments.wheelhouse.glob("markdownllm_explorer-*.whl"))
    dependency_wheels = sorted(arguments.wheelhouse.glob("pyyaml-6.0.3-*.whl"))
    if len(wheels) != 1 or not dependency_wheels:
        raise SystemExit("wheelhouse must contain one Explorer wheel and the exact PyYAML 6.0.3 platform wheel")
    with tempfile.TemporaryDirectory(prefix="mdllm-explorer-install-") as temporary:
        root = Path(temporary); environment = root / "clean-env"; arbitrary = root / "arbitrary-cwd"; fixture = root / "fixture"
        arbitrary.mkdir(); fixture.mkdir(); (fixture / "AGENTS.md").write_text("# Installed fixture\n", encoding="utf-8")
        run([arguments.python, "-m", "venv", str(environment)], cwd=root)
        installed_python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        executable = environment / ("Scripts/mdllm-explorer.exe" if os.name == "nt" else "bin/mdllm-explorer")
        install = run([
            str(installed_python), "-m", "pip", "install", "--no-index", "--find-links", str(arguments.wheelhouse),
            str(wheels[0]), "PyYAML==6.0.3",
        ], cwd=arbitrary)
        probe = run([
            str(installed_python), "-c",
            "import importlib.resources,json,markdownllm_explorer,yaml; p=importlib.resources.files('markdownllm_explorer.delivery.static'); print(json.dumps({'version':markdownllm_explorer.__version__,'yaml':yaml.__version__,'index':p.joinpath('index.html').is_file(),'app':p.joinpath('js/app.js').is_file(),'css':p.joinpath('app.css').is_file()}))",
        ], cwd=arbitrary)
        package_probe = json.loads(probe.stdout)
        fixture_before = tree_digest(fixture); cwd_before = tree_digest(arbitrary)
        process = subprocess.Popen(
            [str(executable), "--root", str(fixture), "--port", "0"], cwd=arbitrary,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            **group_options(),
        )
        lifecycle = {"status": "fail"}
        try:
            assert process.stdout is not None
            deadline = time.monotonic() + 10; launch_url = ""
            while time.monotonic() < deadline:
                line = process.stdout.readline()
                if "MarkdownLLM Explorer:" in line:
                    launch_url = line.split("MarkdownLLM Explorer:", 1)[1].strip(); break
                if process.poll() is not None: break
            if not launch_url:
                raise RuntimeError(process.stderr.read() if process.stderr else "installed CLI did not start")
            parsed = urlsplit(launch_url); capability = parse_qs(parsed.fragment)["cap"][0]; port = int(parsed.port)
            def request(path: str, authenticated: bool = False):
                connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
                headers = {"Host": f"127.0.0.1:{port}"}
                if authenticated: headers["X-Explorer-Capability"] = capability
                connection.request("GET", path, headers=headers); response = connection.getresponse(); body = response.read(); connection.close()
                return response.status, body
            health = request("/health"); shell = request("/"); asset = request("/js/app.js"); estate = request("/api/v1/estate", True)
            assert health[0] == shell[0] == asset[0] == estate[0] == 200
            assert json.loads(health[1])["version"] == package_probe["version"]
            assert json.loads(estate[1])["data"]["sources"][0]["id"] == "substrate"
            active = socket.create_connection(("127.0.0.1", port), timeout=3)
            active.sendall(f"GET /health HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n".encode())
            started = time.monotonic(); interrupt(process); exit_code = process.wait(timeout=6); elapsed = time.monotonic() - started
            active.close()
            assert exit_code == 0 and elapsed <= 5.5
            missing = subprocess.run([str(executable), "--root", str(root / "missing")], cwd=arbitrary, capture_output=True, text=True, timeout=8)
            listener = socket.socket(); listener.bind(("127.0.0.1", 0)); listener.listen(1)
            try:
                collision = subprocess.run([str(executable), "--root", str(fixture), "--port", str(listener.getsockname()[1])], cwd=arbitrary, capture_output=True, text=True, timeout=8)
            finally: listener.close()
            assert missing.returncode == collision.returncode == 2
            assert tree_digest(fixture) == fixture_before and tree_digest(arbitrary) == cwd_before
            lifecycle = {
                "status": "pass", "real_interrupt": True, "active_request_at_interrupt": True,
                "shutdown_seconds": round(elapsed, 3), "invalid_root_exit": missing.returncode,
                "port_collision_exit": collision.returncode, "fixture_immutable": True, "launch_cwd_immutable": True,
            }
        finally:
            if process.poll() is None:
                process.kill(); process.wait(timeout=5)
        document = {
            "schema": 1, "id": "ST-INSTALL-001", "status": "pass", "offline_install": True,
            "tool": {"name": "verify_install.py", "version": "1"},
            "install_flags": ["--no-index", "--find-links"], "arbitrary_cwd": True, "console_script": executable.name,
            "python_executed": platform.python_version(), "python_3_10": "unexecuted-no-runtime-available",
            "lifecycle": lifecycle,
            "package_probe": package_probe, "runtime_routes": ["/health", "/", "/js/app.js", "/api/v1/estate"],
            "explorer_wheel": {"name": wheels[0].name, "sha256": hashlib.sha256(wheels[0].read_bytes()).hexdigest()},
            "dependency_wheel": {"name": dependency_wheels[0].name, "sha256": hashlib.sha256(dependency_wheels[0].read_bytes()).hexdigest()},
            "installer_output_tail": install.stdout[-1000:],
        }
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"id": document["id"], "status": document["status"], "wheel": document["explorer_wheel"]["name"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
