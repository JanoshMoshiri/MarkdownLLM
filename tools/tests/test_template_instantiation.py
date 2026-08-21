"""Instantiate every distributable thing template into a valid corpus.

Source lint catches malformed YAML and undeclared relation choices cheaply.
This test is the complementary birth exercise: replace the choices/placeholders
an operator is expected to fill, parse the resulting files as real things, and
run the CLI validator's corpus boundary over the assembled set.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.model import SEV_ERROR, parse_frontmatter  # noqa: E402
from markdownllm.repo import framework_version  # noqa: E402
from markdownllm.validation import validate_corpus  # noqa: E402


FRAMEWORK_ROOT = Path(__file__).resolve().parents[2]
FRAMEWORK_VERSION = framework_version(FRAMEWORK_ROOT)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _render(source: Path, replacements: dict[str, str]) -> str:
    text = source.read_text(encoding="utf-8")
    for old, new in replacements.items():
        assert old in text, f"stale birth-test token {old!r} for {source}"
        text = text.replace(old, new)
    meta, _, error = parse_frontmatter(text, source=source)
    assert error is None, f"rendered {source.name}: {error}"
    assert meta is not None, f"rendered {source.name} has no frontmatter"
    return text


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True,
    )
    return result.stdout.strip()


def test_every_distributable_thing_template_builds_a_valid_corpus(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "template-birth@local")
    _git(tmp_path, "config", "user.name", "template-birth")
    _write(
        tmp_path / "things" / "_schema.yaml",
        """schema_version: 1
domain: template-birth
options:
  id_filename_match: false
types:
  artifact:
    statuses: [evolving, stable, deprecated]
relations: [informs, supports, challenges, contradicts]
""",
    )

    # Real graph targets make the test exercise reference resolution rather
    # than merely YAML parsing. The commit is the pinned decision input.
    for item in ("support-one", "support-two"):
        _write(
            tmp_path / "things" / f"{item}.md",
            "---\n"
            f"id: {item}\n"
            "type: insight\nstatus: active\nversion: 1.0\n"
            "created: 2026-08-20\nsource: human\nconfidence: high\n"
            "origin: stated\n---\n\n# Support\n\nFixture support.\n",
        )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "test: seed template targets")
    pinned_commit = _git(tmp_path, "rev-parse", "HEAD")

    common = {"[ISO-date]": "2026-08-20"}
    renderings = {
        "things/template-insight.md": (
            FRAMEWORK_ROOT / "templates" / "insight.md.template",
            common | {
                "[descriptive-insight-id]": "template-insight",
                "[YYYY-MM-DD]": "2026-08-20",
                "human|agent|both": "agent",
                "high|medium|low": "medium",
                "stated|inferred|synthesised": "synthesised",
                "[related-thing-id]": "support-one",
                "informs|challenges|supports": "supports",
            },
        ),
        "things/template-conflict.md": (
            FRAMEWORK_ROOT / "templates" / "conflict.md.template",
            common | {
                "[descriptive-conflict-id]": "template-conflict",
                "[YYYY-MM-DD]": "2026-08-20",
                "[thing-id-a]": "support-one",
                "[thing-id-b]": "support-two",
                "low|medium": "medium",
                "stated|inferred": "inferred",
            },
        ),
        "things/template-decision.md": (
            FRAMEWORK_ROOT / "templates" / "decision.md.template",
            common | {
                "[descriptive-kebab-case-id]": "template-decision",
                "[YYYY-MM-DD]": "2026-08-20",
                "human|agent|both": "both",
                "high|medium|low": "high",
                "[knowledge-thing-id]": "support-one",
                "[full 40-hex sha of the commit whose version was actually "
                "used — never abbreviated; an all-digit short sha parses as "
                "YAML int and a suffix-matched abbreviation can pin the "
                "wrong object]": pinned_commit,
                "[produced-output-or-affected-thing]": "support-two",
            },
        ),
        "things/template-birth-retrospective.md": (
            FRAMEWORK_ROOT / "templates" / "retrospective.md.template",
            common | {
                "[domain]": "template-birth",
                "[YYYY-MM]": "2026-08",
                "[domain-id]": "template-birth",
                "[open-loop-or-insight-id]": "support-one",
            },
        ),
        "things/sample-process-definition.md": (
            FRAMEWORK_ROOT / "templates" / "workflow-definition.md.template",
            common | {
                "[process-name]": "sample-process",
                "[first-stage]": "intake",
                "[second-stage]": "review",
                "[third-stage]": "complete",
            },
        ),
        "things/run-template-instance.md": (
            FRAMEWORK_ROOT / "templates" / "workflow-run.md.template",
            common | {
                "[instance-name]": "template-instance",
                "[process-name]": "sample-process",
                "[stage-id]": "intake",
                "[operator-or-agent-id]": "agent-one",
            },
        ),
        "things/_index/template-birth-schema-index.md": (
            FRAMEWORK_ROOT / "templates" / "indexes" / "schema.md.template",
            common | {
                "[domain]": "template-birth",
                "[ISO-datetime]": "2026-08-20T12:00:00+00:00",
                "[short-sha]": pinned_commit[:12],
                "[count of things scanned]": "8",
                "[version]": FRAMEWORK_VERSION,
            },
        ),
        "things/_index/template-birth-triggers-index.md": (
            FRAMEWORK_ROOT / "templates" / "indexes" / "triggers.md.template",
            common | {
                "[domain]": "template-birth",
                "[ISO-datetime]": "2026-08-20T12:00:00+00:00",
                "[short-sha]": pinned_commit[:12],
                "[count of things scanned]": "8",
                "[version]": FRAMEWORK_VERSION,
            },
        ),
        "evidence/validation-record-template-birth.md": (
            FRAMEWORK_ROOT / "evidence" / "sanitised-validation-record.md.template",
            common | {"[short-abstract-label]": "template-birth"},
        ),
    }

    expected_sources = {
        *(FRAMEWORK_ROOT / "templates").glob("*.md.template"),
        *(FRAMEWORK_ROOT / "templates" / "indexes").glob("*.md.template"),
        FRAMEWORK_ROOT / "evidence" / "sanitised-validation-record.md.template",
    }
    # Domain/skill templates are tested by scaffold birth; this set owns the
    # standalone thing/index/evidence templates and fails when a new one lands
    # without an executable birth rendering.
    expected_sources = {
        p for p in expected_sources
        if p.name not in {
            "AGENTS.md.template",
            "domain-read.thing.skill.md.template",
            "domain-specification.skill.md.template",
            "domain-workflow.skill.md.template",
            "domain-write.thing.skill.md.template",
        }
    }
    assert {source for source, _ in renderings.values()} == expected_sources

    for relative, (source, replacements) in renderings.items():
        _write(tmp_path / relative, _render(source, replacements))

    _, findings = validate_corpus(tmp_path)
    errors = [finding for finding in findings if finding.severity == SEV_ERROR]
    assert errors == []
