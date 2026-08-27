from __future__ import annotations

import os
import sys
import subprocess
import threading
from pathlib import Path

import pytest

from markdownllm_explorer.composition import build_runtime
from markdownllm_explorer.adapters.cursors import CursorCodec
from markdownllm_explorer.adapters.filesystem_catalogue import BoundaryRegistry, FilesystemSourceCatalogue, _collision_ids, _normalised_domain_id
from markdownllm_explorer.adapters.git_commit_history import GitCommitHistory
from markdownllm_explorer.adapters.process_runner import BoundedProcessRunner, ProcessRequest, ProcessResult
from markdownllm_explorer.core.eligibility import EligibilityPolicy
from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits


@pytest.mark.contract
def test_catalogue_discovers_substrate_and_only_marked_one_level_domains(estate):
    runtime = build_runtime(estate)
    snapshot = runtime.routes.dispatch("/api/v1/estate", {})
    assert snapshot.sources[0].id.value == "substrate"
    assert [source.id.value for source in snapshot.sources[1:]] == ["domain/demo", "domain/marked-non-git"]
    assert all("unmarked" not in source.id.value for source in snapshot.sources)
    assert "domain_marker_missing" in {issue.code for issue in snapshot.issues}


@pytest.mark.contract
def test_catalogue_reports_invalid_marker_shape_without_hiding_valid_sources(estate):
    invalid = estate / "domain" / "invalid-marker" / "AGENTS.md"; invalid.mkdir(parents=True)
    snapshot = build_runtime(estate).routes.dispatch("/api/v1/estate", {})
    assert [source.id.value for source in snapshot.sources[1:]] == ["domain/demo", "domain/marked-non-git"]
    assert "domain_marker_invalid" in {issue.code for issue in snapshot.issues}


@pytest.mark.unit
def test_domain_identity_normalisation_detects_case_and_unicode_collisions():
    composed = _normalised_domain_id("Café")
    decomposed = _normalised_domain_id("Cafe\u0301")
    assert composed == decomposed == _normalised_domain_id("CAFÉ")
    assert _collision_ids([composed, decomposed]) == {composed}


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
@pytest.mark.parametrize(("eligible_files", "expected"), [(1, "ok"), (2, "ok"), (3, "directory_limit")])
def test_directory_scan_limit_n_minus_one_n_n_plus_one(tmp_path, eligible_files, expected):
    root = tmp_path / f"estate-{eligible_files}"; root.mkdir()
    (root / "AGENTS.md").write_text("# root", encoding="utf-8")
    for index in range(eligible_files):
        (root / f"file-{index}.md").write_text("# file", encoding="utf-8")
    runtime = build_runtime(root, limits=ExplorerLimits(candidate_scan=3, directory_page=10))
    if expected == "ok":
        assert len(runtime.routes.dispatch("/api/v1/tree", {"source": ["substrate"]}).items) == eligible_files + 1
    else:
        with pytest.raises(ExplorerError) as caught:
            runtime.routes.dispatch("/api/v1/tree", {"source": ["substrate"]})
        assert caught.value.code == expected


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
    assert "rendered_mode_unsupported" in plain.issues


@pytest.mark.contract
def test_document_links_are_same_source_markdown_or_labelled_https_only(estate):
    (estate / "links.md").write_text(
        "[inside](skills/demo.md) [plain](script.py) [mail](mailto:test@example.invalid) "
        "[web](https://example.invalid/path) [scheme](javascript:alert(1))",
        encoding="utf-8",
    )
    runtime = build_runtime(estate)
    rendered = runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["links.md"], "mode": ["rendered"]}).content
    assert '#source=substrate&amp;path=skills/demo.md' in rendered
    assert 'href="https://example.invalid/path" target="_blank" rel="noopener noreferrer external"' in rendered
    assert "mailto:" not in rendered and "javascript:" not in rendered
    assert "plain" in rendered and "inert-link" not in rendered


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
    for number in range(2, 5):
        (estate / f"commit-{number}.md").write_text(f"# {number}", encoding="utf-8")
        git(estate, "add", f"commit-{number}.md"); git(estate, "commit", "-m", f"fixture: {number}")
    runtime = build_runtime(estate, limits=ExplorerLimits(commit_page=1))
    first = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})
    assert first.commits.next_cursor and first.commits.items[0].subject == "fixture: 4"
    (estate / "next.md").write_text("# next", encoding="utf-8")
    git(estate, "add", "next.md"); git(estate, "commit", "-m", "fixture: next")
    second = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"], "cursor": [first.commits.next_cursor]})
    assert second.commits.items[0].subject == "fixture: 3"
    fresh = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})
    assert fresh.commits.items[0].subject == "fixture: next"


@pytest.mark.contract
def test_bounded_process_runner_enforces_output_and_deadline(tmp_path):
    runner = BoundedProcessRunner()
    base = dict(executable=sys.executable, cwd=tmp_path, environment=dict(os.environ), output_limit=8)
    with pytest.raises(ExplorerError) as output_error:
        runner.run(ProcessRequest(arguments=("-c", "print('x' * 20)"), timeout_seconds=2, **base))
    assert output_error.value.code == "git_unavailable"
    with pytest.raises(ExplorerError) as timeout_error:
        runner.run(ProcessRequest(arguments=("-c", "import time; time.sleep(1)"), timeout_seconds=0.05, **base))
    assert timeout_error.value.code == "git_timeout"
    assert not [thread for thread in threading.enumerate() if thread.name == "explorer-process-capture"]


@pytest.mark.contract
def test_bounded_process_runner_repeated_floods_leave_no_threads_or_children(tmp_path):
    runner = BoundedProcessRunner()
    base = dict(executable=sys.executable, cwd=tmp_path, environment=dict(os.environ), output_limit=8)
    for _ in range(5):
        with pytest.raises(ExplorerError):
            runner.run(ProcessRequest(arguments=("-c", "import sys; sys.stdout.buffer.write(b'x' * 4000000)"), timeout_seconds=2, **base))
        assert not [thread for thread in threading.enumerate() if thread.name == "explorer-process-capture"]
    for _ in range(3):
        with pytest.raises(ExplorerError) as caught:
            runner.run(ProcessRequest(arguments=("-c", "import time; time.sleep(2)"), timeout_seconds=0.03, **base))
        assert caught.value.code == "git_timeout"
        assert not [thread for thread in threading.enumerate() if thread.name == "explorer-process-capture"]


@pytest.mark.contract
def test_git_adapter_supplies_fixed_argv_environment_and_limits(estate):
    class CapturingRunner:
        def __init__(self): self.requests = []
        def run(self, request):
            self.requests.append(request); arguments = request.arguments
            if "--show-toplevel" in arguments:
                return ProcessResult(0, f"{estate}\n{estate / '.git'}\n{estate / '.git'}\n".encode())
            if "--verify" in arguments: return ProcessResult(0, ("a" * 40 + "\n").encode())
            if "symbolic-ref" in arguments: return ProcessResult(0, b"main\n")
            if "status" in arguments: return ProcessResult(0, ("# branch.oid " + "a" * 40 + "\n# branch.head main\n").encode())
            if "log" in arguments: return ProcessResult(0, ("a" * 40 + "\x00subject\x00author\x002026-01-01T00:00:00Z\x00\x1e").encode())
            if "cat-file" in arguments: return ProcessResult(0, b"")
            raise AssertionError(arguments)

    registry = BoundaryRegistry(); catalogue = FilesystemSourceCatalogue(estate, "domain", registry, EligibilityPolicy()); snapshot = catalogue.discover()
    runner = CapturingRunner(); history = GitCommitHistory(registry, CursorCodec(b"x" * 32), ExplorerLimits(), sys.executable, runner)
    token = snapshot.sources[0].boundary_token
    assert history.repository_state(token).kind == "repository"
    history.commits(token, None)
    assert runner.requests
    for request in runner.requests:
        assert request.executable == sys.executable and request.cwd == estate
        assert request.output_limit == 1024 * 1024 and request.timeout_seconds == 3.0
        assert "PATH" not in request.environment and "HOME" not in request.environment
        assert request.environment["GIT_OPTIONAL_LOCKS"] == "0" and request.environment["GIT_CONFIG_GLOBAL"] == os.devnull
        assert "core.hooksPath=" + os.devnull in request.arguments
        assert "core.fsmonitor=false" in request.arguments and "protocol.file.allow=never" in request.arguments
        assert "core.alternateRefsCommand=" in request.arguments


@pytest.mark.gitfs
@pytest.mark.parametrize("store_shape", ["alternates", "http-alternates", "promisor"])
def test_git_history_rejects_external_or_lazy_object_stores(estate, tmp_path, store_shape):
    outside = tmp_path / "outside-objects"; outside.mkdir()
    info = estate / ".git" / "objects" / "info"; info.mkdir(exist_ok=True)
    pack = estate / ".git" / "objects" / "pack"; pack.mkdir(exist_ok=True)
    if store_shape == "alternates":
        (info / "alternates").write_text(str(outside), encoding="utf-8")
    elif store_shape == "http-alternates":
        (info / "http-alternates").write_text("https://example.invalid/objects", encoding="utf-8")
    else:
        (pack / "pack-probe.promisor").write_bytes(b"")
    overview = build_runtime(estate).routes.dispatch("/api/v1/overview", {"source": ["substrate"]})
    assert overview.repository.kind == "external-store"
    assert overview.repository.issue == "git_store_external"
    assert not overview.commits.items


@pytest.mark.gitfs
def test_git_history_rejects_worktree_pointer_before_invoking_git(tmp_path):
    root = tmp_path / "pointer-source"; root.mkdir()
    (root / "AGENTS.md").write_text("# Pointer source\n", encoding="utf-8")
    outside = tmp_path / "outside-git"; outside.mkdir()
    (root / ".git").write_text(f"gitdir: {outside}\n", encoding="utf-8")

    runtime = build_runtime(root)
    overview = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})

    assert overview.repository.kind == "external-store"
    assert overview.repository.issue == "git_store_external"
    assert not overview.commits.items


@pytest.mark.gitfs
def test_symlink_escape_is_not_discoverable(estate, tmp_path):
    outside = tmp_path / "outside.md"; outside.write_text("outside", encoding="utf-8")
    link = estate / "escape.md"
    try:
        try:
            link.symlink_to(outside)
        except OSError:
            outside_directory = tmp_path / "outside-directory"; outside_directory.mkdir(); (outside_directory / "outside.md").write_text("outside", encoding="utf-8")
            link = estate / "escape-directory"
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside_directory)], capture_output=True, text=True, timeout=5)
            assert result.returncode == 0, "neither file symlinks nor directory junctions are available"
        runtime = build_runtime(estate)
        paths = {item.path.value for item in runtime.routes.dispatch("/api/v1/search", {"source": ["substrate"], "q": ["escape"]}).items}
        assert not any(path.startswith("escape") for path in paths)
    finally:
        if link.is_symlink() or getattr(link, "is_junction", lambda: False)():
            link.unlink()


@pytest.mark.gitfs
def test_reparse_or_symlink_parent_is_rejected_even_when_target_stays_inside_source(estate):
    target = estate / "inside-target"; target.mkdir(); (target / "linked.md").write_text("inside", encoding="utf-8")
    link = estate / "inside-alias"
    try:
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, text=True, timeout=5)
            if result.returncode: pytest.skip("junction creation is unavailable")
        else:
            link.symlink_to(target, target_is_directory=True)
        runtime = build_runtime(estate)
        with pytest.raises(ExplorerError) as caught:
            runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["inside-alias/linked.md"]})
        assert caught.value.code in {"path_outside_source", "path_type_changed"}
    finally:
        if link.is_symlink() or getattr(link, "is_junction", lambda: False)():
            link.unlink()
