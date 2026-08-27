from __future__ import annotations

import os
from pathlib import Path

import pytest

from markdownllm_explorer.composition import build_runtime
from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits


@pytest.mark.contract
def test_catalogue_discovers_substrate_and_only_marked_one_level_domains(estate):
    runtime = build_runtime(estate)
    snapshot = runtime.routes.dispatch("/api/v1/estate", {})
    assert snapshot.sources[0].id.value == "substrate"
    assert [source.id.value for source in snapshot.sources[1:]] == ["domain/demo", "domain/marked-non-git"]
    assert all("unmarked" not in source.id.value for source in snapshot.sources)


@pytest.mark.contract
def test_substrate_tree_excludes_owned_domain_tree_and_secrets(estate):
    runtime = build_runtime(estate)
    page = runtime.routes.dispatch("/api/v1/tree", {"source": ["substrate"]})
    names = {item.name for item in page.items}
    assert "domain" not in names
    assert ".env" not in names
    assert "secret-token.md" not in names
    with pytest.raises(ExplorerError) as caught:
        runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["domain/demo/AGENTS.md"]})
    assert caught.value.code == "path_excluded"


@pytest.mark.contract
def test_domain_and_substrate_return_distinct_documents(estate):
    runtime = build_runtime(estate)
    substrate = runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["AGENTS.md"], "mode": ["raw"]})
    domain = runtime.routes.dispatch("/api/v1/document", {"source": ["domain/demo"], "path": ["AGENTS.md"], "mode": ["raw"]})
    assert "Fixture substrate" in substrate.content
    assert "Demo domain" in domain.content


@pytest.mark.contract
def test_tree_is_lazy_sorted_and_page_cursor_is_stable(estate):
    runtime = build_runtime(estate, limits=ExplorerLimits(directory_page=2))
    first = runtime.routes.dispatch("/api/v1/tree", {"source": ["substrate"]})
    assert len(first.items) == 2 and first.next_cursor
    second = runtime.routes.dispatch("/api/v1/tree", {"source": ["substrate"], "cursor": [first.next_cursor]})
    assert not ({item.path.value for item in first.items} & {item.path.value for item in second.items})
    (estate / "README.md").write_text("# Changed\n", encoding="utf-8")
    with pytest.raises(ExplorerError) as caught:
        runtime.routes.dispatch("/api/v1/tree", {"source": ["substrate"], "cursor": [first.next_cursor]})
    assert caught.value.code == "source_changed"


@pytest.mark.contract
def test_search_returns_only_eligible_owned_paths(estate):
    runtime = build_runtime(estate)
    page = runtime.routes.dispatch("/api/v1/search", {"source": ["substrate"], "q": ["demo"]})
    paths = {item.path.value for item in page.items}
    assert "skills/demo.md" in paths
    assert not any(path.startswith("domain/") or "token" in path for path in paths)


@pytest.mark.contract
def test_skills_and_memory_share_document_paths_and_report_metadata_issues(estate):
    runtime = build_runtime(estate)
    skills = runtime.routes.dispatch("/api/v1/collection", {"source": ["substrate"], "kind": ["skills"]})
    assert [item.path.value for item in skills.items] == ["skills/demo.md"]
    memory = runtime.routes.dispatch("/api/v1/collection", {"source": ["substrate"], "kind": ["memory"]})
    assert len(memory.items) == 2
    assert all("duplicate_id" in item.issues for item in memory.items)
    mismatch = next(item for item in memory.items if item.path.value.endswith("two.md"))
    assert "frontmatter_type_mismatch" in mismatch.issues


@pytest.mark.contract
def test_document_raw_and_rendered_modes_have_one_representation(estate):
    runtime = build_runtime(estate)
    raw = runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["skills/demo.md"], "mode": ["raw"]})
    styled = runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["skills/demo.md"], "mode": ["rendered"]})
    assert raw.mode.value == "raw" and "---" in raw.content and "<h1>" not in raw.content
    assert styled.mode.value == "rendered" and "<h1>Demo Skill</h1>" in styled.content and "---" not in styled.content
    plain = runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["script.py"], "mode": ["rendered"]})
    assert plain.mode.value == "raw" and plain.content.splitlines() == ["print('plain text only')"] and "<" not in plain.content


@pytest.mark.contract
@pytest.mark.parametrize(("path", "code"), [("binary.md", "binary_unsupported"), ("latin.md", "encoding_unsupported"), ("secret-token.md", "path_excluded")])
def test_unsupported_and_excluded_documents_have_stable_codes(estate, path, code):
    runtime = build_runtime(estate)
    with pytest.raises(ExplorerError) as caught:
        runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": [path]})
    assert caught.value.code == code


@pytest.mark.contract
def test_file_size_limit_enforces_n_minus_one_n_and_n_plus_one(estate):
    for size, expected in [(7, "ok"), (8, "ok"), (9, "file_too_large")]:
        (estate / "edge.txt").write_bytes(b"x" * size)
        runtime = build_runtime(estate, limits=ExplorerLimits(file_bytes=8))
        if expected == "ok":
            assert runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["edge.txt"]}).size == size
        else:
            with pytest.raises(ExplorerError) as caught:
                runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["edge.txt"]})
            assert caught.value.code == expected


@pytest.mark.gitfs
def test_git_history_is_exact_source_owned_and_newest_first(estate):
    runtime = build_runtime(estate)
    root = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})
    domain = runtime.routes.dispatch("/api/v1/overview", {"source": ["domain/demo"]})
    nongit = runtime.routes.dispatch("/api/v1/overview", {"source": ["domain/marked-non-git"]})
    assert root.repository.kind == "repository" and root.commits.items[0].author_name == "Fixture User"
    assert domain.repository.kind == "repository" and domain.commits.items[0].author_name == "Domain User"
    assert nongit.repository.kind == "unavailable" and not nongit.commits.items


@pytest.mark.gitfs
def test_git_cursor_is_pinned_to_head(estate):
    from conftest import git
    runtime = build_runtime(estate, limits=ExplorerLimits(commit_page=1))
    first = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})
    assert first.commits.next_cursor is None  # fixture begins with one commit
    (estate / "next.md").write_text("# next", encoding="utf-8")
    git(estate, "add", "next.md"); git(estate, "commit", "-m", "fixture: next")
    second = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})
    assert second.commits.items[0].subject == "fixture: next"


@pytest.mark.gitfs
def test_symlink_escape_is_not_discoverable(estate, tmp_path):
    outside = tmp_path / "outside.md"; outside.write_text("outside", encoding="utf-8")
    link = estate / "escape.md"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlink creation is unavailable")
    runtime = build_runtime(estate)
    paths = {item.path.value for item in runtime.routes.dispatch("/api/v1/search", {"source": ["substrate"], "q": ["escape"]}).items}
    assert "escape.md" not in paths
