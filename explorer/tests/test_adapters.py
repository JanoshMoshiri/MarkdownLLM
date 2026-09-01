from __future__ import annotations

import os
import sys
import subprocess
import threading
import time
import types
from pathlib import Path

import pytest

from markdownllm_explorer.composition import build_runtime
from markdownllm_explorer.adapters.cursors import CursorCodec
from markdownllm_explorer.adapters import confined_source_reader as confined_reader
from markdownllm_explorer.adapters.filesystem_catalogue import BoundaryRegistry, FilesystemSourceCatalogue, _collision_ids, _normalised_domain_id
from markdownllm_explorer.adapters.git_commit_history import (
    GitCommitHistory, _RAW_FLAGS, _added_lines_arguments, _allowed_arguments, _detail_arguments,
    _is_object_spec, _is_tree_path, _raw_arguments,
)
from markdownllm_explorer.adapters.process_runner import BoundedProcessRunner, ProcessRequest, ProcessResult
from markdownllm_explorer.adapters.thing_index import thing_identifier
from markdownllm_explorer.core.eligibility import EligibilityPolicy
from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits


@pytest.mark.contract
def test_catalogue_discovers_substrate_and_only_marked_one_level_domains(estate):
    runtime = build_runtime(estate)
    snapshot = runtime.routes.dispatch("/api/v1/estate", {})
    assert snapshot.sources[0].id.value == "substrate"
    assert snapshot.sources[0].display_name == "MarkdownLLM"
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
def test_directory_depth_is_inclusive_and_consistent_across_tree_search_counts_and_collections(tmp_path):
    root = tmp_path / "depth-estate"; root.mkdir()
    (root / "AGENTS.md").write_text("# Depth fixture\n", encoding="utf-8")
    at_one = root / "level-one"; at_one.mkdir()
    (at_one / "at-one.md").write_text("# N-1\n", encoding="utf-8")
    at_two = at_one / "level-two"; at_two.mkdir()
    (at_two / "at-two.md").write_text("# N\n", encoding="utf-8")
    at_three = at_two / "level-three"; at_three.mkdir()
    (at_three / "at-three.md").write_text("# N+1\n", encoding="utf-8")
    skill_at_two = root / "skills" / "nested"; skill_at_two.mkdir(parents=True)
    (skill_at_two / "at-two.skill.md").write_text("# Boundary skill\n", encoding="utf-8")
    skill_at_three = skill_at_two / "too-deep"; skill_at_three.mkdir()
    (skill_at_three / "at-three.skill.md").write_text("# Hidden skill\n", encoding="utf-8")
    memory_at_two = root / "things" / "insights"; memory_at_two.mkdir(parents=True)
    (memory_at_two / "at-two.md").write_text("---\nid: at-two\ntype: insight\n---\n# Boundary memory\n", encoding="utf-8")

    runtime = build_runtime(
        root,
        limits=ExplorerLimits(directory_depth=2, directory_page=50, search_page=50),
    )
    boundary_tree = runtime.routes.dispatch(
        "/api/v1/tree", {"source": ["substrate"], "path": ["level-one/level-two"]}
    )
    assert {item.path.value for item in boundary_tree.items} == {"level-one/level-two/at-two.md"}
    assert boundary_tree.partial
    with pytest.raises(ExplorerError) as caught:
        runtime.routes.dispatch(
            "/api/v1/tree", {"source": ["substrate"], "path": ["level-one/level-two/level-three"]}
        )
    assert caught.value.code == "directory_limit"

    search = runtime.routes.dispatch(
        "/api/v1/search", {"source": ["substrate"], "q": ["at-"]}
    )
    paths = {item.path.value for item in search.items}
    assert "level-one/at-one.md" in paths and "level-one/level-two/at-two.md" in paths
    assert not any("at-three" in path for path in paths)
    assert search.partial
    overview = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})
    assert overview.counts.partial
    skills = runtime.routes.dispatch(
        "/api/v1/collection", {"source": ["substrate"], "kind": ["skills"]}
    )
    memory = runtime.routes.dispatch(
        "/api/v1/collection", {"source": ["substrate"], "kind": ["memory"]}
    )
    assert [item.path.value for item in skills.items] == ["skills/nested/at-two.skill.md"]
    assert skills.partial
    assert [item.path.value for item in memory.items] == ["things/insights/at-two.md"]
    assert memory.partial


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
    assert mismatch.thing_type == "conflict"
    assert "frontmatter_type_mismatch" not in mismatch.issues


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


@pytest.mark.unit
def test_macos_open_handle_final_path_is_validated(tmp_path, monkeypatch):
    target = tmp_path / "opened.md"
    target.write_text("opened", encoding="utf-8")

    def fcntl_success(file_descriptor, operation, buffer):
        assert file_descriptor >= 0 and operation == 50
        encoded = os.fsencode(target)
        buffer[:len(encoded)] = encoded
        return 0

    monkeypatch.setattr(confined_reader, "sys", types.SimpleNamespace(platform="darwin"))
    monkeypatch.setitem(sys.modules, "fcntl", types.SimpleNamespace(fcntl=fcntl_success, F_GETPATH=50))
    with target.open("rb") as handle:
        assert confined_reader._opened_final_path(handle) == target.resolve()

    monkeypatch.setitem(sys.modules, "fcntl", types.SimpleNamespace(fcntl=lambda *_: (_ for _ in ()).throw(OSError())))
    with target.open("rb") as handle, pytest.raises(ExplorerError) as caught:
        confined_reader._opened_final_path(handle)
    assert caught.value.code == "source_unreadable"

def _head_sha(runtime) -> str:
    return runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]}).commits.items[0].sha


@pytest.mark.contract
def test_commit_detail_lists_changed_paths_and_marks_unopenable_ones(estate):
    runtime = build_runtime(estate)
    detail = runtime.routes.dispatch("/api/v1/commit", {"source": ["substrate"], "sha": [_head_sha(runtime)]})
    openable = {file.path.value: file.openable for file in detail.files}
    assert detail.subject == "fixture: initial"
    assert all(file.change == "added" for file in detail.files)
    assert openable["AGENTS.md"] is True
    # Git reports every path the commit touched. Source admission, not git,
    # decides which of them this source may show.
    assert openable[".env"] is False
    assert openable["secret-token.md"] is False
    assert openable["domain/demo/AGENTS.md"] is False


@pytest.mark.contract
def test_historical_read_returns_commit_content_with_added_ranges(estate):
    runtime = build_runtime(estate)
    sha = _head_sha(runtime)
    record = runtime.routes.dispatch(
        "/api/v1/commit-file", {"source": ["substrate"], "sha": [sha], "path": ["AGENTS.md"]}
    )
    assert "Fixture substrate" in record.content
    assert record.sha == sha
    # A root commit adds every line of every file it introduces.
    assert record.added_ranges == ((1, len(record.content.splitlines())),)


@pytest.mark.contract
@pytest.mark.parametrize(
    ("path", "code"),
    [
        (".env", "path_excluded"),
        ("secret-token.md", "path_excluded"),
        ("domain/demo/AGENTS.md", "path_excluded"),
        ("binary.md", "binary_unsupported"),
        ("latin.md", "encoding_unsupported"),
    ],
)
def test_historical_read_applies_the_same_refusals_as_a_live_read(estate, path, code):
    runtime = build_runtime(estate)
    with pytest.raises(ExplorerError) as caught:
        runtime.routes.dispatch(
            "/api/v1/commit-file",
            {"source": ["substrate"], "sha": [_head_sha(runtime)], "path": [path]},
        )
    assert caught.value.code == code


@pytest.mark.unit
@pytest.mark.parametrize(
    "path",
    [
        "../outside.md", "a/../../b.md", "/absolute.md", "", ".", "a//b.md",
        "--upload-pack=touch", "-x", "a:b.md", "a" * 1025,
    ],
)
def test_tree_path_gate_rejects_traversal_option_and_spec_injection(path):
    assert _is_tree_path(path) is False
    assert _is_object_spec("0" * 40 + ":" + path) is False
    assert _allowed_arguments(["cat-file", "blob", "0" * 40 + ":" + path]) is False
    assert _allowed_arguments(_added_lines_arguments("1" * 40, "0" * 40, path)) is False
    assert _allowed_arguments(_added_lines_arguments(None, "0" * 40, path)) is False


@pytest.mark.unit
def test_git_argument_allowlist_admits_only_the_declared_history_templates():
    sha, parent = "0" * 40, "1" * 40
    assert _allowed_arguments(_added_lines_arguments(parent, sha, "things/insights/one.md")) is True
    assert _allowed_arguments(_added_lines_arguments(None, sha, "things/insights/one.md")) is True
    assert _allowed_arguments(_raw_arguments(parent, sha)) is True
    assert _allowed_arguments(_raw_arguments(None, sha)) is True
    assert _allowed_arguments(_detail_arguments(sha)) is True
    assert _allowed_arguments(["cat-file", "blob", f"{sha}:things/insights/one.md"]) is True
    assert _allowed_arguments(["cat-file", "-s", f"{sha}:things/insights/one.md"]) is True
    # A short or non-hex revision is not a commit this adapter will name.
    assert _allowed_arguments(["cat-file", "blob", "abc:one.md"]) is False
    assert _allowed_arguments(["cat-file", "blob", f"{sha}:"]) is False
    assert _allowed_arguments(["cat-file", "blob", "HEAD:one.md"]) is False
    # The empty-tree marker is admitted only where a first parent belongs.
    assert _allowed_arguments(["diff-tree", *_RAW_FLAGS, sha, "--root"]) is False
    assert _allowed_arguments(["diff-tree", *_RAW_FLAGS, "--root", "--root"]) is False
    assert _allowed_arguments(["diff-tree", *_RAW_FLAGS, "HEAD", sha]) is False
    # Nothing outside the templates, however harmless it looks.
    assert _allowed_arguments(["cat-file", "-p", f"{sha}:one.md"]) is False
    assert _allowed_arguments(["show", sha]) is False
    assert _allowed_arguments(["fetch", "origin"]) is False
    assert _allowed_arguments(["diff-tree", "-p", sha]) is False


@pytest.mark.contract
def test_commit_routes_reject_a_revision_that_is_not_a_full_sha(estate):
    runtime = build_runtime(estate)
    for sha in ["HEAD", "abc1234", "0" * 39, "z" * 40]:
        with pytest.raises(ExplorerError) as caught:
            runtime.routes.dispatch("/api/v1/commit", {"source": ["substrate"], "sha": [sha]})
        assert caught.value.code in {"invalid_request", "source_changed"}

_THING = """---
id: {identifier}
type: {kind}
---
# {title}
"""


@pytest.mark.contract
def test_memory_groups_run_z_to_a_with_titles_ascending_inside(tmp_path):
    root = tmp_path / "ordered"
    root.mkdir()
    (root / "AGENTS.md").write_text("# Ordered fixture", encoding="utf-8")
    layout = {
        "conflicts": ("conflict", ["Beta clash", "Alpha clash"]),
        "decisions": ("decision", ["Delta call"]),
        "insights": ("insight", ["Gamma note"]),
        "retrospectives": ("retrospective", ["Epsilon review"]),
    }
    for folder, (kind, titles) in layout.items():
        directory = root / "things" / folder
        directory.mkdir(parents=True)
        for index, title in enumerate(titles):
            body = _THING.format(identifier=f"{folder}-{index}", kind=kind, title=title)
            (directory / f"{folder}-{index}.md").write_text(body, encoding="utf-8")

    page = build_runtime(root).routes.dispatch(
        "/api/v1/collection", {"source": ["substrate"], "kind": ["memory"]}
    )
    groups = [item.group for item in page.items]
    ordered = [group for index, group in enumerate(groups) if index == 0 or groups[index - 1] != group]
    assert ordered == ["Retrospectives", "Insights", "Decisions", "Conflicts"]
    conflicts = [item.title for item in page.items if item.group == "Conflicts"]
    assert conflicts == ["Alpha clash", "Beta clash"]


@pytest.mark.contract
def test_memory_groups_are_dynamic_and_overview_count_matches(tmp_path):
    root = tmp_path / "dynamic-groups"
    root.mkdir()
    (root / "AGENTS.md").write_text("# Dynamic groups", encoding="utf-8")
    documents = {
        "things/working-documents/nested/draft.md": _THING.format(identifier="draft", kind="artifact", title="Draft"),
        "things/requirement_specs/current.md": _THING.format(identifier="requirement", kind="specification", title="Requirement"),
        "things/plans/roadmap.markdown": _THING.format(identifier="roadmap", kind="plan", title="Roadmap"),
    }
    for relative, body in documents.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    (root / "things" / "empty").mkdir(parents=True)
    (root / "things" / "not-markdown" / "note.txt").parent.mkdir(parents=True)
    (root / "things" / "not-markdown" / "note.txt").write_text("not curated", encoding="utf-8")

    runtime = build_runtime(root)
    page = runtime.routes.dispatch("/api/v1/collection", {"source": ["substrate"], "kind": ["memory"]})
    overview = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]})

    assert [(item.group, item.path.value) for item in page.items] == [
        ("Working Documents", "things/working-documents/nested/draft.md"),
        ("Requirement Specs", "things/requirement_specs/current.md"),
        ("Plans", "things/plans/roadmap.markdown"),
    ]
    assert overview.counts.memory == len(page.items) == 3
    assert not any("frontmatter_type_mismatch" in item.issues for item in page.items)

def _lines(*rows: str) -> str:
    """Build file text from its lines, so the cases below read as files."""
    return "".join(f"{row}\n" for row in rows)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (_lines("---", "id: plain", "type: insight", "---", "# Body"), "plain"),
        (_lines("---", 'id: "quoted"', "---"), "quoted"),
        (_lines("---", "id: 'single'", "---"), "single"),
        (_lines("---", "type: insight", "id: later", "---"), "later"),
        (_lines("# No frontmatter", "id: body-line"), None),
        (_lines("---", "type: insight", "---", "id: after-the-fence"), None),
        (_lines("---", "nested:", "  id: not-top-level", "---"), None),
        (_lines("---", "id:", "---"), None),
        ("", None),
    ],
)
def test_thing_identifier_reads_only_a_top_level_frontmatter_id(text, expected):
    assert thing_identifier(text) == expected


def _reference_estate(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("# Reference fixture", encoding="utf-8")
    # An identifier that does not match its filename is exactly the case a
    # filename-matching shortcut would miss.
    (root / "orchestration.md").write_text(
        _THING.format(identifier="orchestration-specification", kind="specification", title="Orchestration"),
        encoding="utf-8",
    )
    things = root / "things" / "decisions"
    things.mkdir(parents=True)
    (things / "settled.md").write_text(
        _THING.format(identifier="settled", kind="decision", title="Settled"), encoding="utf-8"
    )


@pytest.mark.contract
def test_references_resolve_identifiers_to_paths_and_report_the_rest(tmp_path):
    root = tmp_path / "references"
    _reference_estate(root)
    resolution = build_runtime(root).routes.dispatch(
        "/api/v1/references",
        {"source": ["substrate"], "ids": ["orchestration-specification,settled,absent-thing"]},
    )
    assert resolution.resolved["orchestration-specification"].value == "orchestration.md"
    assert resolution.resolved["settled"].value == "things/decisions/settled.md"
    assert resolution.unresolved == ("absent-thing",)


@pytest.mark.contract
def test_a_contested_identifier_resolves_to_nothing_rather_than_to_one_of_them(tmp_path):
    root = tmp_path / "contested"
    _reference_estate(root)
    duplicate = root / "things" / "decisions" / "duplicate.md"
    duplicate.write_text(_THING.format(identifier="settled", kind="decision", title="Also settled"), encoding="utf-8")
    resolution = build_runtime(root).routes.dispatch(
        "/api/v1/references", {"source": ["substrate"], "ids": ["settled"]}
    )
    assert resolution.resolved == {}
    assert resolution.unresolved == ("settled",)


@pytest.mark.contract
def test_reference_lookups_are_bounded_in_count_and_identifier_length(tmp_path):
    root = tmp_path / "bounded"
    _reference_estate(root)
    runtime = build_runtime(root)
    for ids in [",".join(f"id-{index}" for index in range(201)), "x" * 201, "", " , "]:
        with pytest.raises(ExplorerError) as caught:
            runtime.routes.dispatch("/api/v1/references", {"source": ["substrate"], "ids": [ids]})
        assert caught.value.code == "invalid_request"


@pytest.mark.contract
def test_reference_index_rebuilds_when_the_source_changes(tmp_path):
    root = tmp_path / "changing"
    _reference_estate(root)
    runtime = build_runtime(root)
    index = runtime.routes._use_cases.resolve_references._index
    source = runtime.routes._use_cases.resolve_references._catalogue.source("substrate")
    assert index.resolve(source.boundary_token, ("added-later",))[1] == ("added-later",)
    (root / "things" / "decisions" / "added.md").write_text(
        _THING.format(identifier="added-later", kind="decision", title="Added later"), encoding="utf-8"
    )
    # The cached mapping is only reused while the walk still agrees with it.
    index._cached.clear()
    resolved, missing, _ = index.resolve(source.boundary_token, ("added-later",))
    assert missing == ()
    assert resolved["added-later"].value == "things/decisions/added.md"


def _repo(tmp_path: Path, name: str):
    root = tmp_path / name
    root.mkdir(parents=True)

    def run(*arguments: str) -> str:
        result = subprocess.run(
            ["git", "-c", f"safe.directory={root}", *arguments],
            cwd=root, capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()

    (root / "AGENTS.md").write_text("# fixture", encoding="utf-8")
    run("init", "-b", "main")
    run("config", "user.name", "Fixture")
    run("config", "user.email", "fixture@example.invalid")
    return root, run


@pytest.mark.gitfs
def test_commit_detail_reports_merges_roots_and_deletions_against_the_first_parent(tmp_path):
    """A merge reported zero changed files until the comparison became a pair.

    `diff-tree --first-parent` prints nothing at all for a merge commit, so the
    whole view was blank on exactly the commits that join work together.
    """
    root, run = _repo(tmp_path, "merges")
    (root / "base.md").write_text("base\n", encoding="utf-8")
    run("add", "."); run("commit", "-m", "base")
    run("checkout", "-b", "side")
    (root / "from-side.md").write_text("side\nlines\n", encoding="utf-8")
    run("add", "."); run("commit", "-m", "side")
    run("checkout", "main")
    (root / "from-main.md").write_text("main\n", encoding="utf-8")
    run("add", "."); run("commit", "-m", "main")
    run("merge", "--no-ff", "side", "-m", "merge")
    (root / "base.md").unlink()
    run("add", "--all"); run("commit", "-m", "remove base")

    runtime = build_runtime(root)
    by_subject = {
        item.subject: runtime.routes.dispatch("/api/v1/commit", {"source": ["substrate"], "sha": [item.sha]})
        for item in runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]}).commits.items
    }
    assert [(f.change, f.path.value) for f in by_subject["merge"].files] == [("added", "from-side.md")]
    assert [(f.change, f.path.value) for f in by_subject["base"].files] == [
        ("added", "AGENTS.md"), ("added", "base.md"),
    ]
    assert [(f.change, f.path.value, f.openable) for f in by_subject["remove base"].files] == [
        ("deleted", "base.md", False),
    ]


@pytest.mark.gitfs
def test_commit_file_list_is_bounded_and_labelled_partial(tmp_path):
    root, run = _repo(tmp_path, "many")
    for index in range(6):
        (root / f"file-{index}.md").write_text(f"# {index}\n", encoding="utf-8")
    run("add", "."); run("commit", "-m", "many files")
    runtime = build_runtime(root, limits=ExplorerLimits(commit_files=3))
    sha = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]}).commits.items[0].sha
    detail = runtime.routes.dispatch("/api/v1/commit", {"source": ["substrate"], "sha": [sha]})
    assert len(detail.files) == 3 and detail.partial is True


@pytest.mark.gitfs
def test_historical_read_survives_a_rewrite_larger_than_the_patch_budget(tmp_path):
    """A 565 KB file failed with `git_unavailable` before the patch had a budget.

    The blob is inside the 1 MiB read limit; the patch describing its rewrite is
    not, because a patch carries both sides of every change.
    """
    root, run = _repo(tmp_path, "rewrite")
    big = root / "big.md"
    big.write_text("".join(f"original line {index}\n" for index in range(24000)), encoding="utf-8")
    run("add", "."); run("commit", "-m", "first")
    big.write_text("".join(f"replacement line {index}\n" for index in range(24000)), encoding="utf-8")
    run("add", "."); run("commit", "-m", "rewrite")
    assert big.stat().st_size < 1024 * 1024

    runtime = build_runtime(root)
    sha = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]}).commits.items[0].sha
    record = runtime.routes.dispatch(
        "/api/v1/commit-file", {"source": ["substrate"], "sha": [sha], "path": ["big.md"]}
    )
    assert record.ranges_known is True and record.added_ranges == ((1, 24000),)

    # With a budget too small for the patch, the file is still served and the
    # marking is reported unavailable rather than as "nothing changed".
    starved = build_runtime(root, limits=ExplorerLimits(diff_output_bytes=2048))
    degraded = starved.routes.dispatch(
        "/api/v1/commit-file", {"source": ["substrate"], "sha": [sha], "path": ["big.md"]}
    )
    assert degraded.ranges_known is False and degraded.added_ranges == ()
    assert degraded.content.startswith("replacement line 0")


@pytest.mark.gitfs
def test_a_filename_holding_glob_characters_is_a_path_not_a_pattern(tmp_path):
    root, run = _repo(tmp_path, "globs")
    (root / "notes[draft].md").write_text("a\nb\n", encoding="utf-8")
    (root / "notesd.md").write_text("x\n", encoding="utf-8")
    run("add", "."); run("commit", "-m", "one")
    (root / "notesd.md").write_text("x\ny\nz\n", encoding="utf-8")
    run("add", "."); run("commit", "-m", "two")

    runtime = build_runtime(root)
    sha = runtime.routes.dispatch("/api/v1/overview", {"source": ["substrate"]}).commits.items[0].sha
    untouched = runtime.routes.dispatch(
        "/api/v1/commit-file", {"source": ["substrate"], "sha": [sha], "path": ["notes[draft].md"]}
    )
    # Read as a pattern, this matched notesd.md and reported its added lines.
    assert untouched.added_ranges == ()


@pytest.mark.contract
@pytest.mark.parametrize("path", ["node_modules./pkg.js", "node_modules../pkg.js"])
def test_an_ignored_directory_resists_a_spelling_the_filesystem_settles(tmp_path, path):
    """Windows discards trailing dots when resolving a component, so the
    spelling a caller supplies and the path that is opened are not the same."""
    root = tmp_path / "settled"
    root.mkdir()
    (root / "AGENTS.md").write_text("# fixture", encoding="utf-8")
    modules = root / "node_modules"
    modules.mkdir()
    (modules / "pkg.js").write_text("ignored\n", encoding="utf-8")
    runtime = build_runtime(root)
    with pytest.raises(ExplorerError) as caught:
        runtime.routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": [path], "mode": ["raw"]})
    assert caught.value.code in {"path_excluded", "file_not_found"}


@pytest.mark.contract
def test_reference_index_survives_a_source_written_while_it_is_read(tmp_path):
    """An agent session edits the estate while an operator browses it.

    A walk interrupted by that must yield an incomplete index, never an error
    the browser would render as every reference being absent.
    """
    root = tmp_path / "churn"
    root.mkdir()
    (root / "AGENTS.md").write_text("# fixture", encoding="utf-8")
    decisions = root / "things" / "decisions"
    decisions.mkdir(parents=True)
    for index in range(120):
        (decisions / f"thing-{index}.md").write_text(
            _THING.format(identifier=f"thing-{index}", kind="decision", title=f"Thing {index}"), encoding="utf-8"
        )
    runtime = build_runtime(root)
    stop = threading.Event()

    def churn() -> None:
        index = 0
        while not stop.is_set():
            (decisions / f"new-{index}.md").write_text(
                _THING.format(identifier=f"new-{index}", kind="decision", title=f"New {index}"), encoding="utf-8"
            )
            index += 1
            time.sleep(0.002)

    writer = threading.Thread(target=churn, daemon=True)
    writer.start()
    try:
        outcomes = [
            runtime.routes.dispatch("/api/v1/references", {"source": ["substrate"], "ids": ["thing-1"]})
            for _ in range(8)
        ]
    finally:
        stop.set(); writer.join(timeout=2)
    # Never an error, and never a bare "not found": a walk the writer cut short
    # yields an incomplete index, and an incomplete index reports an unfound
    # reference as unchecked rather than as absent.
    assert all(item.resolved or item.partial for item in outcomes)


@pytest.mark.contract
def test_reference_index_is_keyed_on_source_identity_not_the_boundary_token(tmp_path):
    """Estate discovery mints fresh tokens, and a browser reload triggers it."""
    root = tmp_path / "keyed"
    _reference_estate(root)
    runtime = build_runtime(root)
    index = runtime.routes._use_cases.resolve_references._index
    runtime.routes.dispatch("/api/v1/references", {"source": ["substrate"], "ids": ["settled"]})
    for _ in range(3):
        runtime.routes.dispatch("/api/v1/estate", {})
        runtime.routes.dispatch("/api/v1/references", {"source": ["substrate"], "ids": ["settled"]})
    assert len(index._cached) == 1


@pytest.mark.contract
def test_concurrent_cold_reference_lookups_share_one_build(tmp_path):
    root = tmp_path / "single-flight"
    _reference_estate(root)
    runtime = build_runtime(root)
    index = runtime.routes._use_cases.resolve_references._index
    builds: list[int] = []
    original = index._build

    def counted(token, listing):
        builds.append(1)
        time.sleep(0.05)
        return original(token, listing)

    index._build = counted
    threads = [
        threading.Thread(
            target=lambda: runtime.routes.dispatch(
                "/api/v1/references", {"source": ["substrate"], "ids": ["settled"]}
            )
        )
        for _ in range(6)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len(builds) == 1
