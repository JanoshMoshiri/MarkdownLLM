from __future__ import annotations

import time

import pytest

from markdownllm_explorer.composition import build_runtime
from tools import run_performance


@pytest.mark.performance
def test_generated_estate_tree_and_search_are_bounded(tmp_path):
    root = tmp_path / "scale"; root.mkdir(); (root / "AGENTS.md").write_text("# Scale", encoding="utf-8")
    files = root / "things" / "insights"; files.mkdir(parents=True)
    for index in range(1200):
        (files / f"item-{index:04}.md").write_text(f"---\nid: item-{index}\ntype: insight\n---\n# Item {index}", encoding="utf-8")
    started = time.perf_counter(); runtime = build_runtime(root); startup = time.perf_counter() - started
    started = time.perf_counter(); page = runtime.routes.dispatch("/api/v1/search", {"source": ["substrate"], "q": ["item-11"]}); search = time.perf_counter() - started
    assert startup < 2.0 and search < 3.0
    assert 1 <= len(page.items) <= 200


@pytest.mark.performance
def test_reference_load_gate_requires_two_consecutive_quiet_samples(monkeypatch):
    if run_performance.os.name != "nt":
        pytest.skip("Windows CPU gate")
    samples = iter(
        [
            (0, 0, 0),
            (30, 50, 50),   # 70% busy: resets the consecutive count.
            (110, 100, 100),  # 20% busy: first quiet sample.
            (180, 150, 150),  # 30% busy: second quiet sample.
        ]
    )
    monkeypatch.setattr(run_performance, "_windows_cpu_times", lambda: next(samples))
    monkeypatch.setattr(run_performance.time, "sleep", lambda seconds: None)

    assert run_performance.wait_for_reference_load() == pytest.approx(0.3)


@pytest.mark.performance
def test_reference_load_gate_fails_when_profile_window_is_unavailable():
    if run_performance.os.name != "nt":
        pytest.skip("Windows CPU gate")
    with pytest.raises(RuntimeError, match="reference profile unavailable"):
        run_performance.wait_for_reference_load(timeout=0)
