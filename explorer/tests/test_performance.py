from __future__ import annotations

import time

import pytest

from markdownllm_explorer.composition import build_runtime


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

