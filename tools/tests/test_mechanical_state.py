"""Total trigger outcomes and Git-backed workflow transition regression tests."""

from __future__ import annotations

import os
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.repository_view import RepositoryView  # noqa: E402
from markdownllm.triggers import (  # noqa: E402
    TriggerOutcome,
    evaluate,
    evaluate_results,
)
from markdownllm.validation import (  # noqa: E402
    cmd_validate,
    validate_corpus,
)


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")


def _thing(thing_id: str, extra: str = "", *, status: str = "in-progress",
           thing_type: str = "task") -> str:
    return (
        "---\n"
        f"id: {thing_id}\n"
        f"type: {thing_type}\n"
        f"status: {status}\n"
        "created: 2026-08-20\n"
        f"{extra}"
        "---\n\n"
        f"# {thing_id}\n\nState fixture.\n"
    )


def test_every_trigger_declaration_has_one_typed_total_result(tmp_path: Path) -> None:
    _write(tmp_path, "things/done.md", _thing("done", status="completed"))
    _write(tmp_path, "things/target.md", _thing(
        "target",
        "due_date: 2026-01-01\n"
        "triggers:\n"
        "  - type: time\n"
        "    condition: due_date_passed\n"
        "    action: escalate\n"
        "  - type: dependency\n"
        "    on: status_changed_to\n"
        "    watch: [done]\n"
        "    value: cancelled\n"
        "    action: unblock\n"
        "  - type: relationship\n"
        "    condition: the sponsor decides\n"
        "    action: re_evaluate\n"
        "  - type: time\n"
        "    condition: stale\n"
        "    threshold: whenever\n"
        "    action: surface\n"
        "  - type: dependency\n"
        "    on: status_changed_to\n"
        "    watch: [done, absent]\n"
        "    value: completed\n"
        "    action: unblock\n"
        "  - type: threshold\n"
        "    condition: subtasks_complete\n"
        "    action: suggest_completion\n"
        "  - type: threshold\n"
        "    condition: made_up\n"
        "    action: surface\n"
        "  - type: cosmic\n"
        "    condition: alignment\n"
        "    action: surface\n"
        "  - not-a-mapping\n",
    ))

    results = evaluate_results(tmp_path)
    target = [result for result in results if result.thing_id == "target"]

    assert len(target) == 9
    assert [result.outcome for result in target[:4]] == [
        TriggerOutcome.FIRED,
        TriggerOutcome.NOT_FIRED,
        TriggerOutcome.UNEVALUABLE,
        TriggerOutcome.INVALID,
    ]
    assert target[4].outcome is TriggerOutcome.INVALID
    assert "absent" in target[4].reason
    assert target[5].outcome is TriggerOutcome.INVALID
    assert "empty set is not completion" in target[5].reason
    assert target[6].outcome is TriggerOutcome.INVALID
    assert "unknown threshold condition" in target[6].reason
    assert target[7].outcome is TriggerOutcome.INVALID
    assert "unrecognised trigger type" in target[7].reason
    assert target[8].outcome is TriggerOutcome.INVALID

    # The established CLI/programmatic projection stays a five-item tuple.
    fired, upcoming, horizon, skipped, advisories = evaluate(tmp_path)
    assert any("due_date 2026-01-01 passed" in line for line in fired)
    assert not upcoming and not horizon and not advisories
    assert any("invalid stale trigger" in line for line in skipped)
    assert not any("all watched (done, absent)" in line for line in fired)


def test_absent_or_partial_subtask_set_never_becomes_success(tmp_path: Path) -> None:
    _write(tmp_path, "things/done.md", _thing("done", status="completed"))
    _write(tmp_path, "things/parent.md", _thing(
        "parent",
        "linked_things:\n"
        "  - id: done\n"
        "    relation: subtask\n"
        "  - id: missing\n"
        "    relation: subtask\n"
        "triggers:\n"
        "  - type: threshold\n"
        "    condition: subtasks_complete\n"
        "    action: suggest_completion\n",
    ))

    result = next(r for r in evaluate_results(tmp_path)
                  if r.thing_id == "parent")
    assert result.outcome is TriggerOutcome.INVALID
    assert "`missing`" in result.reason
    assert not any("all subtasks complete" in line for line in evaluate(tmp_path)[0])


def _git(root: Path, *args: str) -> str:
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "mechanical-state-tests",
        "GIT_COMMITTER_NAME": "mechanical-state-tests",
        "GIT_AUTHOR_EMAIL": "mechanical-state-tests@local",
        "GIT_COMMITTER_EMAIL": "mechanical-state-tests@local",
    })
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, env=env,
    ).stdout.strip()


def _workflow_repo(root: Path) -> None:
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    _write(root, "things/process.md", _thing(
        "process", "stages:\n"
        "  - id: intake\n"
        "    to: [review]\n"
        "  - id: review\n"
        "    to: [done]\n"
        "  - id: done\n"
        "    to: []\n",
        status="stable", thing_type="workflow-definition",
    ))
    _write(root, "things/run.md", _thing(
        "run", "definition: process\ncurrent_stage: intake\n",
        status="active", thing_type="workflow-run",
    ))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed workflow")


def _set_run_stage(root: Path, stage: str) -> None:
    _write(root, "things/run.md", _thing(
        "run", f"definition: process\ncurrent_stage: {stage}\n",
        status="active", thing_type="workflow-run",
    ))


def test_index_validation_blocks_undeclared_transition_despite_worktree_repair(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    _workflow_repo(root)

    _set_run_stage(root, "done")
    _git(root, "add", "things/run.md")
    _set_run_stage(root, "review")  # valid draft, but not the staged candidate

    candidate = RepositoryView.index(root)
    _, findings = validate_corpus(root, candidate)
    assert any(
        finding.severity == "Error"
        and "transition `intake` -> `done` is not declared" in finding.message
        for finding in findings
    )
    assert cmd_validate(Namespace(path=str(root), quiet=True, view="index")) == 1


def test_index_validation_accepts_declared_transition(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    _workflow_repo(root)
    _set_run_stage(root, "review")
    _git(root, "add", "things/run.md")

    assert cmd_validate(Namespace(path=str(root), quiet=True, view="index")) == 0


def test_same_candidate_cannot_rewrite_definition_to_authorize_its_transition(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    _workflow_repo(root)

    _write(root, "things/process.md", _thing(
        "process", "stages:\n"
        "  - id: intake\n"
        "    to: [review, done]\n"
        "  - id: review\n"
        "    to: [done]\n"
        "  - id: done\n"
        "    to: []\n",
        status="stable", thing_type="workflow-definition",
    ))
    _set_run_stage(root, "done")
    _git(root, "add", "things/process.md", "things/run.md")

    _, findings = validate_corpus(root, RepositoryView.index(root))
    assert any(
        "transition `intake` -> `done` is not declared by prior definition"
        in finding.message for finding in findings
    )
