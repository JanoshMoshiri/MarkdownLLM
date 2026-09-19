"""`stages[].actor` — the declared half of turn-taking.

The field exists so a watcher can ask a definition *which stages wake this
role* instead of carrying that table in a shell `case` statement. These tests
pin the two properties that makes possible:

* reading the table back out of a definition (`stages_for_actor`), which is
  what `watch` consumes;
* refusing a declaration that cannot be consumed (`workflow_actor_findings`),
  which is what stops a typo becoming a watcher that silently never wakes.

The optionality is load-bearing and tested first: every definition written
before this field existed must stay valid, or the field is a migration rather
than a promotion.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.model import SEV_ERROR  # noqa: E402
from markdownllm.workflow_actors import (  # noqa: E402
    declared_actors,
    stage_actors,
    stages_for_actor,
    workflow_actor_findings,
)

from corpus_harness import scan, thing_text, write  # noqa: E402


DEFINITION = {
    "id": "spec-loop",
    "type": "workflow-definition",
    "status": "draft",
    "created": "2026-09-19",
    "stages": [
        {"id": "drafting", "to": ["reviewing"], "actor": "writer"},
        {"id": "reviewing", "to": ["drafting", "cleared"], "actor": "reviewer"},
        {"id": "cleared", "to": ["ruling"], "actor": "writer"},
        {"id": "ruling", "to": ["approved"], "actor": "cto"},
        # `approved` is terminal and nobody acts *at* it — the stage a human
        # ends the loop from declares no actor on purpose.
        {"id": "approved", "to": []},
    ],
}


def _definition(**overrides):
    merged = dict(DEFINITION)
    merged.update(overrides)
    return merged


def _corpus(tmp_path: Path, *metas: dict):
    """Write each mapping as a thing and return the scanned corpus."""
    for meta in metas:
        write(tmp_path, f"things/{meta['id']}.md",
              thing_text(yaml.safe_dump(meta, sort_keys=False)))
    corpus, _ = scan(tmp_path)
    return corpus


class TestReadingTheTable:
    def test_stages_for_actor_returns_declaration_order(self):
        assert stages_for_actor(DEFINITION, "writer") == ["drafting", "cleared"]

    def test_a_role_acting_once_gets_one_stage(self):
        assert stages_for_actor(DEFINITION, "reviewer") == ["reviewing"]

    def test_an_undeclared_role_gets_nothing_rather_than_raising(self):
        # `watch` turns this into a usable error naming the declared set; the
        # reader itself stays total.
        assert stages_for_actor(DEFINITION, "builder") == []

    def test_declared_actors_collects_across_stages(self):
        assert declared_actors(DEFINITION) == {"writer", "reviewer", "cto"}

    def test_a_stage_may_name_several_actors(self):
        several = _definition(stages=[
            {"id": "triage", "to": ["done"], "actor": ["writer", "reviewer"]},
            {"id": "done", "to": []},
        ])
        assert stages_for_actor(several, "writer") == ["triage"]
        assert stages_for_actor(several, "reviewer") == ["triage"]

    def test_a_definition_with_no_actors_reads_as_empty(self):
        bare = _definition(stages=[{"id": "drafting", "to": []}])
        assert declared_actors(bare) == set()
        assert stages_for_actor(bare, "writer") == []

    @pytest.mark.parametrize("declared", [None, 7, {"role": "writer"}, []])
    def test_stage_actors_is_total_over_junk(self, declared):
        assert stage_actors({"id": "s", "actor": declared}) == []

    def test_stage_actors_drops_blank_names(self):
        assert stage_actors({"id": "s", "actor": ["writer", "  "]}) == ["writer"]


class TestRefusingWhatCannotBeConsumed:
    def test_a_definition_without_the_field_is_silent(self, tmp_path):
        """The optionality that makes this a promotion, not a migration."""
        corpus = _corpus(tmp_path, _definition(stages=[
            {"id": "drafting", "to": ["reviewing"]},
            {"id": "reviewing", "to": []},
        ]))
        assert workflow_actor_findings(corpus) == []

    def test_a_well_formed_declaration_is_silent(self, tmp_path):
        assert workflow_actor_findings(_corpus(tmp_path, DEFINITION)) == []

    def test_an_empty_actor_is_an_error(self, tmp_path):
        corpus = _corpus(tmp_path, _definition(
            stages=[{"id": "drafting", "to": [], "actor": "  "}]))
        findings = workflow_actor_findings(corpus)
        assert [f.severity for f in findings] == [SEV_ERROR]
        assert "drafting" in findings[0].message

    def test_an_empty_actor_list_is_an_error(self, tmp_path):
        corpus = _corpus(tmp_path, _definition(
            stages=[{"id": "drafting", "to": [], "actor": []}]))
        assert [f.severity for f in workflow_actor_findings(corpus)] == [SEV_ERROR]

    def test_a_non_name_in_an_actor_list_is_an_error(self, tmp_path):
        corpus = _corpus(tmp_path, _definition(
            stages=[{"id": "drafting", "to": [], "actor": ["writer", 7]}]))
        findings = workflow_actor_findings(corpus)
        assert [f.severity for f in findings] == [SEV_ERROR]
        assert "7" in findings[0].message

    def test_a_mapping_actor_is_an_error_naming_its_type(self, tmp_path):
        corpus = _corpus(tmp_path, _definition(
            stages=[{"id": "drafting", "to": [], "actor": {"role": "writer"}}]))
        findings = workflow_actor_findings(corpus)
        assert [f.severity for f in findings] == [SEV_ERROR]
        assert "dict" in findings[0].message

    def test_an_unnamed_stage_is_still_reported_legibly(self, tmp_path):
        corpus = _corpus(tmp_path, _definition(
            stages=[{"to": [], "actor": ""}]))
        findings = workflow_actor_findings(corpus)
        assert [f.severity for f in findings] == [SEV_ERROR]
        assert "<unnamed stage>" in findings[0].message

    def test_only_workflow_definitions_are_checked(self, tmp_path):
        """A `plan` with a `stages` key is not a definition and is not ours."""
        corpus = _corpus(tmp_path, {
            "id": "some-plan", "type": "plan", "status": "in-progress",
            "created": "2026-09-19",
            "stages": [{"id": "x", "actor": 7}],
        })
        assert workflow_actor_findings(corpus) == []
