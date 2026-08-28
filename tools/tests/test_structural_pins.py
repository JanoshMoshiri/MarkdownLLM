"""Structural-pin resolution at the commit boundary.

A transcribed SHA is unverifiable by reading, so the floor resolves it
against git instead. These pin the four properties the check is for: a real
pin passes, an invented one blocks, every pin in a corpus costs one git
process, and an environment where git cannot be consulted is reported as
"could not look" rather than as clean.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import structural_pins  # noqa: E402
from markdownllm.model import SEV_ERROR, SEV_WARNING, scan  # noqa: E402
from markdownllm.structural_pins import (  # noqa: E402
    PIN_SUBJECT, structural_pin_findings,
)
from markdownllm.validation import validate_corpus  # noqa: E402


pytestmark = pytest.mark.gitfs

NONEXISTENT = "bdb95714c3a7e2f08d61b95a2f4ee90c1d2a4f6b"


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")


def _git(root: Path, *args: str) -> str:
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "structural-pin-tests",
        "GIT_COMMITTER_NAME": "structural-pin-tests",
        "GIT_AUTHOR_EMAIL": "structural-pin-tests@local",
        "GIT_COMMITTER_EMAIL": "structural-pin-tests@local",
    })
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, env=env,
    ).stdout.strip()


def _thing(thing_id: str, thing_type: str = "task",
           status: str = "in-progress", extra: str = "") -> str:
    return (
        "---\n"
        f"id: {thing_id}\n"
        f"type: {thing_type}\n"
        f"status: {status}\n"
        "created: 2026-08-28\n"
        f"{extra}"
        "---\n\n"
        f"# {thing_id}\n\nStructural-pin fixture.\n"
    )


def _seeded_repo(root: Path) -> str:
    """A repository with one committed input, returning its full commit id."""
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    _write(root, "things/input.md", _thing("input"))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "record the input")
    return _git(root, "rev-parse", "HEAD")


def _decision(pin: str, decision_id: str = "d", input_id: str = "input") -> str:
    return _thing(
        decision_id, "decision", "made",
        f"informed_by:\n  - id: {input_id}\n    commit: {pin}\n")


def _findings(root: Path):
    corpus, _ = scan(root)
    return structural_pin_findings(root, corpus)


def _errors(findings):
    return [f for f in findings if f.severity == SEV_ERROR]


# ---------------------------------------------------------------- resolution


def test_pin_naming_a_real_commit_passes(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    pin = _seeded_repo(root)
    _write(root, "things/d.md", _decision(pin))

    assert _findings(root) == []


def test_short_pin_that_resolves_passes(tmp_path: Path) -> None:
    # Abbreviation is a style question the floor does not own; resolvability is
    # the only property this check asserts.
    root = tmp_path / "domain"
    pin = _seeded_repo(root)
    _write(root, "things/d.md", _decision(pin[:8]))

    assert _findings(root) == []


def test_pin_naming_no_commit_is_an_error(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    _seeded_repo(root)
    _write(root, "things/d.md", _decision(NONEXISTENT))

    errors = _errors(_findings(root))
    assert len(errors) == 1
    assert errors[0].thing == "d"
    assert "`informed_by[0].commit`" in errors[0].message
    assert NONEXISTENT in errors[0].message
    assert "resolves to no commit" in errors[0].message
    # The tool reports the observable fact; it must not diagnose a cause it
    # cannot verify (the discipline `mdllm provenance` already holds).
    assert "history" not in errors[0].message


def test_pin_that_resolves_to_a_tree_is_not_a_commit(tmp_path: Path) -> None:
    # `^{commit}` peeling is what makes this a *commit* check: an object id
    # that exists but is not a commit resolves to nothing.
    root = tmp_path / "domain"
    _seeded_repo(root)
    tree = _git(root, "rev-parse", "HEAD^{tree}")
    _write(root, "things/d.md", _decision(tree))

    assert len(_errors(_findings(root))) == 1


def test_error_reaches_the_validation_pass_the_pre_commit_leg_runs(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    _seeded_repo(root)
    _write(root, "things/d.md", _decision(NONEXISTENT))

    _, findings = validate_corpus(root)
    assert any(f.severity == SEV_ERROR and "resolves to no commit" in f.message
               for f in findings)


# ------------------------------------------------------------------ batching


def test_every_pin_in_a_corpus_costs_one_git_consultation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "domain"
    pin = _seeded_repo(root)
    for i in range(6):
        _write(root, f"things/d{i}.md",
               _decision(pin if i % 2 == 0 else NONEXISTENT, f"d{i}"))

    calls: list[list[str]] = []
    real = structural_pins._git

    def counted(cwd, args, stdin=None):
        calls.append(list(args))
        return real(cwd, args, stdin)

    monkeypatch.setattr(structural_pins, "_git", counted)
    findings = _findings(root)

    # Three bad pins, one Error each — and a batch that stops at the first
    # failure would have reported only one of them.
    assert len(_errors(findings)) == 3
    assert sum(1 for args in calls if args[0] == "cat-file") == 1


def test_a_repeated_pin_is_asked_about_once(tmp_path: Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "domain"
    pin = _seeded_repo(root)
    for i in range(4):
        _write(root, f"things/d{i}.md", _decision(pin, f"d{i}"))

    sent: list[str] = []
    real = structural_pins._git

    def capture(cwd, args, stdin=None):
        if args and args[0] == "cat-file" and stdin is not None:
            sent.append(stdin)
        return real(cwd, args, stdin)

    monkeypatch.setattr(structural_pins, "_git", capture)
    assert _findings(root) == []
    assert len(sent) == 1 and sent[0].count("\n") == 1


# ------------------------------------------------------ honest degradation


def test_git_unavailable_reports_that_it_could_not_look(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "domain"
    _seeded_repo(root)
    _write(root, "things/d.md", _decision(NONEXISTENT))

    def no_git(*args, **kwargs):
        raise OSError("git: command not found")

    monkeypatch.setattr(structural_pins.subprocess, "run", no_git)
    findings = _findings(root)

    # Not clean, and not an Error either: the pin's validity is unknown from
    # here, and a check that cannot see must not mint a finding about content.
    assert _errors(findings) == []
    assert len(findings) == 1
    warning = findings[0]
    assert warning.severity == SEV_WARNING and warning.thing == PIN_SUBJECT
    assert "could not look" in warning.message
    assert "1 structural commit pin(s) could not be resolved" in warning.message


def test_corpus_outside_any_repository_reports_that_it_could_not_look(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "loose"
    _write(root, "things/d.md", _decision(NONEXISTENT))
    monkeypatch.setattr(structural_pins, "repository_root", lambda _root: None)

    findings = _findings(root)
    assert _errors(findings) == []
    assert len(findings) == 1 and findings[0].thing == PIN_SUBJECT
    assert "no Git repository owns this corpus" in findings[0].message


def test_a_partial_answer_leaves_the_unanswered_pins_unclaimed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Git answered about one pin and said nothing about the other. The silence
    # is not evidence, so the second pin gets the could-not-look Warning rather
    # than a pass or an Error.
    root = tmp_path / "domain"
    pin = _seeded_repo(root)
    _write(root, "things/d0.md", _decision(pin, "d0"))
    _write(root, "things/d1.md", _decision(NONEXISTENT, "d1"))

    real = structural_pins._git

    def truncated(cwd, args, stdin=None):
        out = real(cwd, args, stdin)
        if args and args[0] == "cat-file":
            out.stdout = out.stdout.splitlines(keepends=True)[0]
        return out

    monkeypatch.setattr(structural_pins, "_git", truncated)
    findings = _findings(root)
    assert _errors(findings) == []
    assert len(findings) == 1 and findings[0].thing == PIN_SUBJECT


def test_a_corpus_with_no_local_pin_is_silent_without_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Quiet when there is nothing to check. A check that fired on every
    # pin-free corpus in every git-less environment would teach the operator
    # to ignore it.
    root = tmp_path / "loose"
    _write(root, "things/plain.md", _thing("plain"))

    def no_git(*args, **kwargs):
        raise OSError("git: command not found")

    monkeypatch.setattr(structural_pins.subprocess, "run", no_git)
    assert _findings(root) == []


# ------------------------------------------------------------------ scoping


def test_foreign_source_commit_is_not_resolved_against_this_repository(
    tmp_path: Path,
) -> None:
    # The cross-domain triple pins a commit in the SOURCE domain's repository.
    # Resolving it here would report "missing" for a correct pin, and its
    # remedy — "re-pin to a local commit" — is one no honest author could
    # perform. `mdllm imports-check` owns that resolution.
    root = tmp_path / "domain"
    _seeded_repo(root)
    _write(root, "things/imported.md", _thing(
        "imported", "insight", "active",
        "origin: external\nverified: true\n"
        "source_domain: elsewhere\nsource_id: imported\n"
        f"source_commit: {NONEXISTENT}\n"))

    assert _findings(root) == []


def test_definition_commit_is_reported_once_by_its_own_resolver(
    tmp_path: Path,
) -> None:
    # It is a local pin, so the registry records it; the boundary check skips
    # it so a single wrong pin cannot yield two Errors saying the same thing.
    root = tmp_path / "domain"
    _seeded_repo(root)
    _write(root, "things/process.md", _thing(
        "process", "workflow-definition", "stable",
        "stages:\n  - id: intake\n    next: [review]\n  - id: review\n"))
    _write(root, "things/run.md", _thing(
        "run", "workflow-run", "active",
        f"definition: process\ndefinition_commit: {NONEXISTENT}\n"
        "current_stage: intake\n"))

    assert _findings(root) == []
    _, findings = validate_corpus(root)
    unresolved = [f for f in findings
                  if f.severity == SEV_ERROR and NONEXISTENT in f.message]
    assert len(unresolved) == 1
    assert "definition_commit" in unresolved[0].message


def test_a_pin_carrying_whitespace_cannot_inject_batch_request_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    # `--batch-check` is line-oriented; a value with a newline in it could
    # otherwise add a request line and desynchronise the positional answers.
    root = tmp_path / "domain"
    pin = _seeded_repo(root)
    _write(root, "things/d.md", _thing(
        "d", "decision", "made",
        "informed_by:\n  - id: input\n"
        f"    commit: \"{pin} {pin}\"\n"))

    sent: list[str] = []
    real = structural_pins._git

    def capture(cwd, args, stdin=None):
        if args and args[0] == "cat-file":
            sent.append(stdin or "")
        return real(cwd, args, stdin)

    monkeypatch.setattr(structural_pins, "_git", capture)
    errors = _errors(_findings(root))

    assert len(errors) == 1 and "resolves to no commit" in errors[0].message
    assert sent == []  # nothing sendable, so git was never asked
