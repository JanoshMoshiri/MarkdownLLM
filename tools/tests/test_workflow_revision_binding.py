"""Git-backed workflow revision-binding and activation regression tests."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.indexes import build_index_body  # noqa: E402
from markdownllm.model import SEV_ERROR, SEV_INFO, SEV_WARNING  # noqa: E402
from markdownllm.repository_view import RepositoryView  # noqa: E402
from markdownllm.validation import validate_corpus  # noqa: E402


pytestmark = pytest.mark.gitfs


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")


def _git(root: Path, *args: str) -> str:
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "workflow-revision-tests",
        "GIT_COMMITTER_NAME": "workflow-revision-tests",
        "GIT_AUTHOR_EMAIL": "workflow-revision-tests@local",
        "GIT_COMMITTER_EMAIL": "workflow-revision-tests@local",
    })
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, env=env,
    ).stdout.strip()


def _thing(thing_id: str, thing_type: str, status: str, extra: str = "") -> str:
    return (
        "---\n"
        f"id: {thing_id}\n"
        f"type: {thing_type}\n"
        f"status: {status}\n"
        "created: 2026-08-26\n"
        f"{extra}"
        "---\n\n"
        f"# {thing_id}\n\nRevision-binding fixture.\n"
    )


def _definition(edges: str) -> str:
    return _thing(
        "process", "workflow-definition", "stable",
        f"stages:\n{edges}",
    )


def _run(*, stage: str = "intake", pin: str | None = None,
         status: str = "active", run_id: str = "run",
         informed_by: str = "") -> str:
    pin_line = f"definition_commit: {pin}\n" if pin is not None else ""
    return _thing(
        run_id, "workflow-run", status,
        "definition: process\n"
        f"{pin_line}"
        f"current_stage: {stage}\n"
        f"{informed_by}",
    )


V1 = (
    "  - id: intake\n"
    "    to: [review]\n"
    "  - id: review\n"
    "    to: []\n"
)
V2 = (
    "  - id: intake\n"
    "    to: [done]\n"
    "  - id: done\n"
    "    to: []\n"
)


def _init(root: Path) -> str:
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    _write(root, "things/process.md", _definition(V1))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "definition v1")
    return _git(root, "rev-parse", "HEAD")


def _messages(root: Path, severity: str | None = None) -> list[str]:
    _, findings = validate_corpus(root)
    return [finding.message for finding in findings
            if severity is None or finding.severity == severity]


def test_pin_resolves_and_membership_comes_from_pinned_definition(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _write(root, "things/process.md", _definition(V2))
    _write(root, "things/run.md", _run(stage="review", pin=pin))

    errors = _messages(root, SEV_ERROR)
    assert not any("definition_commit" in message for message in errors)
    assert not any("current_stage" in message for message in errors)


def test_unknown_definition_commit_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    _init(root)
    missing = "f" * 40
    _write(root, "things/run.md", _run(pin=missing))

    errors = _messages(root, SEV_ERROR)
    assert any(f"definition_commit` `{missing}` does not resolve" in message
               for message in errors)


def test_pinned_transition_uses_pinned_edges_not_later_definition(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _write(root, "things/run.md", _run(pin=pin))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "create pinned run")

    _write(root, "things/process.md", _definition(V2))
    _git(root, "add", "things/process.md")
    _git(root, "commit", "-q", "-m", "definition v2")
    _write(root, "things/run.md", _run(stage="done", pin=pin))
    _git(root, "add", "things/run.md")

    _, findings = validate_corpus(root, RepositoryView.index(root))
    assert any(
        finding.severity == SEV_ERROR
        and "transition `intake` -> `done` is not declared by pinned definition"
        in finding.message
        for finding in findings
    )


def test_definition_migration_and_cursor_move_cannot_share_a_commit(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    v1 = _init(root)
    _write(root, "things/run.md", _run(pin=v1))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "create pinned run")

    _write(root, "things/process.md", _definition(V2))
    _git(root, "add", "things/process.md")
    _git(root, "commit", "-q", "-m", "definition v2")
    v2 = _git(root, "rev-parse", "HEAD")
    _write(root, "things/run.md", _run(stage="done", pin=v2))
    _git(root, "add", "things/run.md")

    _, findings = validate_corpus(root, RepositoryView.index(root))
    assert any(
        finding.severity == SEV_ERROR
        and "changes both `definition_commit` and `current_stage`" in finding.message
        for finding in findings
    )


def test_unpinned_run_keeps_legacy_semantics_with_adoption_advisory(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    _init(root)
    _write(root, "things/run.md", _run())

    _, findings = validate_corpus(root)
    assert not [finding for finding in findings
                if finding.severity == SEV_ERROR]
    assert any(
        finding.severity == SEV_INFO
        and "has no `definition_commit`" in finding.message
        for finding in findings
    )


def test_adoption_advisory_is_silent_on_a_terminal_run(tmp_path: Path) -> None:
    """A completed run cannot adopt the pin; the remedy is unperformable.

    Retro-pinning a finished run would assert a reconstruction rather than
    record a decision, so the advisory would never be closeable and would
    train the operator to ignore Info findings.
    """
    root = tmp_path / "domain"
    _init(root)
    _write(root, "things/run.md", _run(status="completed"))

    _, findings = validate_corpus(root)
    assert not [finding for finding in findings
                if finding.severity == SEV_ERROR]
    assert not [
        finding for finding in findings
        if "has no `definition_commit`" in finding.message
    ]


def test_definition_resolution_survives_a_path_rename(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _git(root, "mv", "things/process.md", "things/renamed-process.md")
    _git(root, "commit", "-q", "-m", "move definition")
    _write(root, "things/run.md", _run(stage="review", pin=pin))

    errors = _messages(root, SEV_ERROR)
    assert not any("definition_commit" in message for message in errors)
    assert not any("current_stage" in message for message in errors)


def test_nested_corpus_resolves_pin_from_owning_repository(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    domain = repository / "examples" / "domain"
    repository.mkdir(parents=True)
    _git(repository, "init", "-q")
    _write(domain, "things/process.md", _definition(V1))
    _git(repository, "add", "-A")
    _git(repository, "commit", "-q", "-m", "nested definition v1")
    pin = _git(repository, "rev-parse", "HEAD")
    _write(domain, "things/run.md", _run(stage="review", pin=pin))

    _, findings = validate_corpus(domain)

    assert not [finding for finding in findings
                if finding.severity == SEV_ERROR]


def test_definition_commit_is_framework_vocabulary(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _write(root, "_schema.yaml", "known_fields: []\n")
    _write(root, "things/run.md", _run(pin=pin))

    warnings = _messages(root, SEV_WARNING)
    assert not any("field `definition_commit`" in message
                   for message in warnings)


def test_runs_sharing_a_revision_resolve_one_immutable_view(
    tmp_path: Path, monkeypatch,
) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _write(root, "things/run.md", _run(pin=pin))
    _write(root, "things/run-two.md", _run(pin=pin, run_id="run-two"))
    calls = 0
    real_commit = RepositoryView.commit.__func__

    def counted(cls, repository_root: Path, revision: str = "HEAD"):
        nonlocal calls
        if revision == pin:
            calls += 1
        return real_commit(cls, repository_root, revision)

    monkeypatch.setattr(RepositoryView, "commit", classmethod(counted))
    _, findings = validate_corpus(root)

    assert not [finding for finding in findings
                if finding.severity == SEV_ERROR]
    assert calls == 1


def test_completed_run_without_activation_or_output_gets_info_only(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _write(root, "things/run.md", _run(
        stage="review", pin=pin, status="completed"))

    _, findings = validate_corpus(root)
    assert any(
        finding.severity == SEV_INFO
        and "completed run has neither initiating `informed_by` evidence"
        in finding.message
        for finding in findings
    )
    assert not [finding for finding in findings
                if finding.severity == SEV_ERROR]


def test_activation_or_produced_evidence_satisfies_completed_run_advisory(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _write(root, "things/demand.md", _thing(
        "demand", "task", "completed"))
    _git(root, "add", "things/demand.md")
    _git(root, "commit", "-q", "-m", "record demand")
    demand_pin = _git(root, "rev-parse", "HEAD")
    _write(root, "things/run.md", _run(
        stage="review", pin=pin, status="completed",
        informed_by=("informed_by:\n"
                     "  - id: demand\n"
                     f"    commit: {demand_pin}\n")))

    assert not any("completed run has neither" in message
                   for message in _messages(root, SEV_INFO))

    _write(root, "things/run.md", _run(
        stage="review", pin=pin, status="completed"))
    _git(root, "add", "things/run.md")
    _git(root, "commit", "-q", "-m", "record completed run")
    run_pin = _git(root, "rev-parse", "HEAD")
    _write(root, "things/output.md", _thing(
        "output", "task", "completed",
        "informed_by:\n"
        "  - id: run\n"
        f"    commit: {run_pin}\n"))
    corpus, findings = validate_corpus(root)
    assert not any("completed run has neither" in finding.message
                   for finding in findings)
    body, _ = build_index_body(corpus, "provenance")
    assert "## run" in body and f"output (pinned @{run_pin})" in body


def test_activation_advisory_never_fires_before_completion(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    pin = _init(root)
    _write(root, "things/run.md", _run(pin=pin, status="active"))

    assert not any("completed run has neither" in message
                   for message in _messages(root, SEV_INFO))
