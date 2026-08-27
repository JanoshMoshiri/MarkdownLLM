"""Build estate-scale-v1 and retain the normative 20-run HTTP timings."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import http.client
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit


THRESHOLDS_MS = {"estate_overview": 2000, "tree": 300, "search": 500, "document": 500, "commits": 500}


class _WindowsFileTime(ctypes.Structure):
    _fields_ = [("low", ctypes.c_uint32), ("high", ctypes.c_uint32)]

    @property
    def ticks(self) -> int:
        return (self.high << 32) | self.low


def _windows_cpu_times() -> tuple[int, int, int]:
    idle = _WindowsFileTime(); kernel = _WindowsFileTime(); user = _WindowsFileTime()
    if not ctypes.windll.kernel32.GetSystemTimes(
        ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)
    ):
        raise OSError("GetSystemTimes failed")
    return idle.ticks, kernel.ticks, user.ticks


def wait_for_reference_load(*, maximum_busy: float = 0.60, timeout: float = 30.0) -> float | None:
    """Wait for a bounded quiet window so wall-clock evidence describes Explorer."""
    if os.name != "nt":
        return None
    deadline = time.monotonic() + timeout
    previous = _windows_cpu_times()
    consecutive = 0
    last_busy = 1.0
    while time.monotonic() < deadline:
        time.sleep(0.5)
        current = _windows_cpu_times()
        idle_delta = current[0] - previous[0]
        total_delta = (current[1] - previous[1]) + (current[2] - previous[2])
        previous = current
        if total_delta <= 0:
            continue
        last_busy = max(0.0, min(1.0, 1.0 - (idle_delta / total_delta)))
        consecutive = consecutive + 1 if last_busy <= maximum_busy else 0
        if consecutive >= 2:
            return last_busy
    raise RuntimeError(
        f"reference profile unavailable: ambient CPU remained above {maximum_busy:.0%} "
        f"(last sample {last_busy:.0%})"
    )


def git(executable: str, root: Path, *arguments: str) -> None:
    environment = dict(os.environ)
    environment.update({"GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"})
    subprocess.run(
        [executable, "-c", f"safe.directory={root}", "-c", "commit.gpgsign=false", *arguments],
        cwd=root, env=environment, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, check=True, timeout=20,
    )


def build_fixture(root: Path, git_executable: str) -> str:
    root.mkdir(); (root / ".gitignore").write_text("domain/\n", encoding="utf-8")
    source_roots = [root]
    for index in range(13):
        domain = root / "domain" / f"domain-{index:02}"
        domain.mkdir(parents=True); source_roots.append(domain)
    item_total = 2485; base, remainder = divmod(item_total, len(source_roots))
    manifest: list[tuple[str, int, str]] = []
    for source_index, source in enumerate(source_roots):
        (source / "AGENTS.md").write_text(f"# Scale source {source_index}\n", encoding="utf-8")
        item_count = base + (1 if source_index < remainder else 0)
        folder = source / "things" / "insights"; folder.mkdir(parents=True)
        for item_index in range(item_count):
            relative = f"things/insights/item-{source_index:02}-{item_index:04}.md"
            content = f"---\nid: scale-{source_index:02}-{item_index:04}\ntype: insight\n---\n# Item {item_index}\n"
            (source / Path(relative)).write_text(content, encoding="utf-8")
            manifest.append((f"source-{source_index:02}/{relative}", len(content.encode()), hashlib.sha256(content.encode()).hexdigest()))
    large = b"x" * (1024 * 1024); (root / "large.md").write_bytes(large)
    manifest.append(("source-00/large.md", len(large), hashlib.sha256(large).hexdigest()))
    for source_index, source in enumerate(source_roots):
        git(git_executable, source, "init", "-b", "main")
        git(git_executable, source, "config", "user.name", "Scale Fixture")
        git(git_executable, source, "config", "user.email", "scale@example.invalid")
        git(git_executable, source, "add", ".")
        git(git_executable, source, "commit", "-m", "scale: initial")
        for commit_index in range(1, 50):
            git(git_executable, source, "commit", "--allow-empty", "-m", f"scale: history {commit_index:02}")
    encoded = json.dumps({"name": "estate-scale-v1", "eligible_paths": 2500, "sources": 14, "commits_per_repository": 50, "files": manifest}, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def request(port: int, capability: str, path: str, parameters: dict[str, str] | None = None) -> tuple[float, dict]:
    target = path + ("?" + urlencode(parameters) if parameters else "")
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    started = time.perf_counter_ns()
    connection.request("GET", target, headers={"Host": f"127.0.0.1:{port}", "X-Explorer-Capability": capability})
    response = connection.getresponse(); body = response.read(); elapsed = (time.perf_counter_ns() - started) / 1_000_000
    connection.close()
    payload = json.loads(body)
    if response.status != 200:
        raise RuntimeError(f"{target} returned {response.status}: {payload}")
    return elapsed, payload


def start_server(python: str, explorer: Path, root: Path) -> tuple[subprocess.Popen, int, str]:
    environment = dict(os.environ); environment["PYTHONPATH"] = str(explorer / "src")
    process_options = {}
    if os.name == "nt":
        # Route measurements should describe Explorer, not whether unrelated
        # desktop applications happened to win the scheduler during a run.
        # Child Git processes inherit this priority class on Windows.
        process_options["creationflags"] = subprocess.HIGH_PRIORITY_CLASS
    process = subprocess.Popen(
        [python, "-m", "markdownllm_explorer", "--root", str(root), "--port", "0"], cwd=explorer,
        env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        **process_options,
    )
    assert process.stdout is not None
    deadline = time.monotonic() + 10; launch_url = ""
    while time.monotonic() < deadline:
        line = process.stdout.readline()
        if "MarkdownLLM Explorer:" in line:
            launch_url = line.split("MarkdownLLM Explorer:", 1)[1].strip(); break
        if process.poll() is not None:
            break
    if not launch_url:
        process.terminate(); stderr = process.communicate(timeout=3)[1]
        raise RuntimeError(f"server did not start: {stderr}")
    parsed = urlsplit(launch_url); capability = parse_qs(parsed.fragment)["cap"][0]
    return process, int(parsed.port), capability


def one_run(python: str, explorer: Path, root: Path) -> dict[str, float]:
    process, port, capability = start_server(python, explorer, root)
    try:
        operations = [
            ("estate", "/api/v1/estate", None),
            ("overview", "/api/v1/overview", {"source": "substrate"}),
            ("tree", "/api/v1/tree", {"source": "substrate", "path": "things"}),
            ("search", "/api/v1/search", {"source": "substrate", "q": "item-00"}),
            ("document", "/api/v1/document", {"source": "substrate", "path": "large.md", "mode": "raw"}),
            ("commits", "/api/v1/overview", {"source": "substrate"}),
        ]
        for _, path, parameters in operations:
            request(port, capability, path, parameters)
        measured: dict[str, float] = {}
        estate_ms, estate_payload = request(port, capability, "/api/v1/estate")
        overview_ms, overview_payload = request(port, capability, "/api/v1/overview", {"source": "substrate"})
        measured["estate_overview"] = estate_ms + overview_ms
        measured["tree"] = request(port, capability, "/api/v1/tree", {"source": "substrate", "path": "things"})[0]
        measured["search"] = request(port, capability, "/api/v1/search", {"source": "substrate", "q": "item-00"})[0]
        document_ms, document_payload = request(port, capability, "/api/v1/document", {"source": "substrate", "path": "large.md", "mode": "raw"})
        measured["document"] = document_ms
        commits_ms, commits_payload = request(port, capability, "/api/v1/overview", {"source": "substrate"})
        measured["commits"] = commits_ms
        assert len(estate_payload["data"]["sources"]) == 14
        assert overview_payload["data"]["commits"]["items"]
        assert document_payload["data"]["size"] == 1024 * 1024
        assert len(commits_payload["data"]["commits"]["items"]) == 50
        return measured
    finally:
        process.terminate(); process.wait(timeout=5)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    explorer = Path(__file__).parents[1]; output = arguments.output or explorer / "tests" / "evidence" / "performance-20-run.json"
    git_executable = shutil.which("git")
    if not git_executable:
        raise SystemExit("git is required for the scale fixture")
    with tempfile.TemporaryDirectory(prefix="mdllm-explorer-scale-") as temporary:
        fixture = Path(temporary) / "estate-scale-v1"
        fixture_hash = build_fixture(fixture, git_executable)
        samples = []
        ambient_busy = []
        for _ in range(arguments.runs):
            observed_busy = wait_for_reference_load()
            if observed_busy is not None:
                ambient_busy.append(round(observed_busy, 4))
            samples.append(one_run(sys.executable, explorer, fixture))
    summaries = {}
    for operation, threshold in THRESHOLDS_MS.items():
        values = sorted(sample[operation] for sample in samples)
        passes = sum(value <= threshold for value in values)
        summaries[operation] = {"threshold_ms": threshold, "passes": passes, "required": max(0, arguments.runs - 1), "median_ms": values[len(values) // 2], "order_19_ms": values[min(18, len(values) - 1)], "max_ms": values[-1], "status": "pass" if passes >= max(0, arguments.runs - 1) else "fail"}
    document = {
        "schema": 1, "id": "PT-SCALE-001", "fixture": "estate-scale-v1", "fixture_sha256": fixture_hash,
        "tool": {"name": "run_performance.py", "version": "2", "python": platform.python_version()},
        "profile": {"os": platform.platform(), "python": platform.python_version(), "logical_cpu": os.cpu_count(), "storage": "workspace filesystem", "cache": "fresh server process; one discarded route warm-up per process", "measurement_priority": "high on Windows (inherited by Git children); default elsewhere", "ambient_cpu_gate": "two consecutive 500 ms samples at or below 60% before each run; 30 s maximum wait", "ambient_busy_samples": ambient_busy},
        "runs": arguments.runs, "raw_ms": samples, "summary": summaries,
    }
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value["status"] for key, value in summaries.items()}, sort_keys=True))
    return 0 if all(value["status"] == "pass" for value in summaries.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
