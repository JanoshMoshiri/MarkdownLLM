"""Self-tests for the deterministic floor.

The framework's trust model rests on mdllm.py being correct: a regression here
silently changes what "valid" means for every domain. These tests pin the
behaviour of each mechanical check. Run: python -m pytest tools/tests -q
"""

import datetime as _dt
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
import markdownllm.doctor as doctor_module  # noqa: E402
from corpus_harness import (  # noqa: E402
    GOOD, RECENT, _consumer_with_import, _git_commit, _git_repo,
    _git_short, _git_supports_hook_run, _ns, _sync_git,
    _trust_mcp_entry, all_findings, messages, scan, thing_text,
    write,
)

# ---------------------------------------------------------------- frontmatter


def test_parse_frontmatter_valid():
    meta, body, err = mdllm.parse_frontmatter(thing_text(GOOD))
    assert err is None
    assert meta["id"] == "alpha"
    assert body.strip().startswith("# Title")


def test_parse_frontmatter_absent():
    meta, body, err = mdllm.parse_frontmatter("# Just markdown\n")
    assert (meta, err) == (None, None)
    assert body == "# Just markdown\n"


def test_parse_frontmatter_unterminated():
    _, _, err = mdllm.parse_frontmatter("---\nid: x\n# no closing fence\n")
    assert err == "unterminated frontmatter block"


def test_parse_frontmatter_non_mapping():
    _, _, err = mdllm.parse_frontmatter("---\n- a\n- b\n---\nbody\n")
    assert "not a YAML mapping" in err


# ---------------------------------------------------------------- version sync


def sentinel_files(root: Path, sentinel: str, agents: str, changelog: str):
    write(root, ".markdownllm", f"framework: MarkdownLLM\nversion: {sentinel}\n")
    write(root, "AGENTS.md", thing_text(f"name: F\nversion: {agents}"))
    write(root, "CHANGELOG.md", f"# Changelog\n\n## [{changelog}] - 2026-06-11\n\nEntry.\n")


def test_version_sync_in_sync(tmp_path):
    sentinel_files(tmp_path, "3.3.0", "3.3.0", "3.3.0")
    assert mdllm.check_version_sync(tmp_path) == []


def test_version_sync_pads_missing_patch(tmp_path):
    sentinel_files(tmp_path, "3.3", "3.3.0", "3.3.0")
    assert mdllm.check_version_sync(tmp_path) == []


def test_version_sync_detects_drift(tmp_path):
    sentinel_files(tmp_path, "3.0", "3.0", "3.3.0")
    findings = mdllm.check_version_sync(tmp_path)
    assert len(findings) == 1 and findings[0].severity == mdllm.SEV_ERROR
    assert "out of sync" in findings[0].message


def test_version_sync_skipped_outside_framework_root(tmp_path):
    write(tmp_path, "CHANGELOG.md", "## [9.9.9] - 2026-01-01\n")
    assert mdllm.check_version_sync(tmp_path) == []


# ---------------------------------------------------------------- vocabularies


def test_reserved_statuses_cannot_be_redefined():
    schema = {"types": {"insight": {"statuses": ["whatever"]}}}
    allowed, declared = mdllm.valid_statuses_for("insight", schema)
    assert allowed == ["active", "promoted", "dismissed"] and declared


def test_workflow_types_are_reserved():
    # workflow-definition / workflow-run carry fixed vocabularies a domain
    # cannot redefine (reserve-but-draft: workflow-state.md).
    allowed, declared = mdllm.valid_statuses_for("workflow-run", {"types": {"workflow-run": {"statuses": ["nope"]}}})
    assert allowed == ["active", "paused", "completed", "abandoned"] and declared
    allowed, declared = mdllm.valid_statuses_for("workflow-definition", None)
    assert allowed == ["draft", "evolving", "stable", "deprecated"] and declared


def _workflow_corpus(tmp_path, current_stage: str):
    write(tmp_path, "_schema.yaml", "schema_version: 1\ndomain: t\n")
    write(tmp_path, "things/proc.md", thing_text(
        "id: proc\ntype: workflow-definition\nstatus: stable\ncreated: 2026-06-16\n"
        "stages:\n  - id: intake\n    to: [review]\n  - id: review\n    to: []",
        "# Proc\n\nA process.\n"))
    write(tmp_path, "things/run.md", thing_text(
        f"id: run\ntype: workflow-run\nstatus: active\ncreated: 2026-06-16\n"
        f"definition: proc\ncurrent_stage: {current_stage}", "# Run\n\nA run.\n"))
    return messages(all_findings(tmp_path), mdllm.SEV_ERROR)


def test_workflow_run_current_stage_must_be_in_definition(tmp_path):
    assert _workflow_corpus(tmp_path, "intake") == []          # valid stage: clean
    errs = _workflow_corpus(tmp_path, "intkae")                # typo: caught
    assert any("current_stage" in m and "not a stage" in m for m in errs)


def test_workflow_run_requires_definition(tmp_path):
    write(tmp_path, "_schema.yaml", "schema_version: 1\ndomain: t\n")
    write(tmp_path, "things/run.md", thing_text(
        "id: run\ntype: workflow-run\nstatus: active\ncreated: 2026-06-16\n"
        "current_stage: intake", "# Run\n\nA run.\n"))
    errs = messages(all_findings(tmp_path), mdllm.SEV_ERROR)
    assert any("missing `definition`" in m for m in errs)


def _dep_corpus(tmp_path, dep_status, dependent_status="completed"):
    write(tmp_path, "_schema.yaml", "schema_version: 1\ndomain: t\n")
    write(tmp_path, "things/dep.md", thing_text(
        f"id: dep\ntype: task\nstatus: {dep_status}\ncreated: 2026-06-01"))
    write(tmp_path, "things/main.md", thing_text(
        f"id: main\ntype: task\nstatus: {dependent_status}\ncreated: 2026-06-01\n"
        "dependencies: [dep]"))
    return messages(all_findings(tmp_path), mdllm.SEV_ERROR)


def test_terminal_thing_cannot_depend_on_unfinished_work(tmp_path):
    # the gate: a completed thing with an unfinished dependency is blocked
    assert any("cannot depend on unfinished work" in e
               for e in _dep_corpus(tmp_path, "in-progress"))
    # dependency also terminal -> clean
    assert _dep_corpus(tmp_path, "completed") == []
    # a cancelled dependency counts as resolved -> clean
    assert _dep_corpus(tmp_path, "cancelled") == []
    # an unfinished dependent is fine -> the gate only guards terminal things
    assert not any("unfinished work" in e
                   for e in _dep_corpus(tmp_path, "in-progress", "in-progress"))


def test_version_lt_orders_dotted_versions():
    assert mdllm._version_lt("3.4.0", "3.8.0")
    assert mdllm._version_lt("3.7.0", "3.10.0")   # numeric, not lexical
    assert not mdllm._version_lt("3.8.0", "3.8.0")
    assert not mdllm._version_lt("3.9.0", "3.8.1")


def test_changelog_versions_since(tmp_path):
    cl = tmp_path / "CHANGELOG.md"
    cl.write_text("# Changelog\n\n## [3.8.0] - 2026-06-15\n\n## [3.7.0] - 2026-06-13\n"
                  "## [3.4.0] - 2026-06-11\n", encoding="utf-8")
    since = mdllm._changelog_versions_since(cl, "3.4.0")
    assert since == ["v3.8.0 (2026-06-15)", "v3.7.0 (2026-06-13)"]
    assert mdllm._changelog_versions_since(cl, "3.8.0") == []


def test_declared_domain_vocabulary():
    schema = {"types": {"vat-return": {"statuses": ["open", "figures-ready"]}}}
    allowed, declared = mdllm.valid_statuses_for("vat-return", schema)
    assert allowed == ["open", "figures-ready"] and declared


def test_default_vocabulary_fallback():
    allowed, declared = mdllm.valid_statuses_for("task", None)
    assert allowed == mdllm.DEFAULT_STATUSES and not declared


# ---------------------------------------------------------------- level 1


def test_missing_required_fields(tmp_path):
    write(tmp_path, "things/empty.md", thing_text("id: empty"))
    errs = messages(all_findings(tmp_path), mdllm.SEV_ERROR)
    for fld in ("type", "status", "created"):
        assert any(f"`{fld}`" in m for m in errs)


def test_status_violation_severity_declared_vs_default(tmp_path):
    write(tmp_path, "things/_schema.yaml", "")  # schema lives at root here
    write(tmp_path, "_schema.yaml",
          "types:\n  vat-return:\n    statuses: [open, figures-ready]\n")
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: vat-return\nstatus: bogus\ncreated: 2026-06-01"))
    write(tmp_path, "things/b.md", thing_text(
        "id: b\ntype: task\nstatus: bogus\ncreated: 2026-06-01"))
    findings = all_findings(tmp_path)
    by_thing = {f.thing: f.severity for f in findings if "status `bogus`" in f.message}
    assert by_thing == {"a": mdllm.SEV_ERROR, "b": mdllm.SEV_WARNING}


def test_created_not_iso_is_error(tmp_path):
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: June 1st"))
    assert any("not ISO 8601" in m for m in messages(all_findings(tmp_path), mdllm.SEV_ERROR))


def test_malformed_linked_things(tmp_path):
    write(tmp_path, "things/a.md", thing_text(
        GOOD + "linked_things:\n  - just-a-string"))
    assert any("linked_things[0]" in m for m in messages(all_findings(tmp_path), mdllm.SEV_ERROR))


def test_body_warnings(tmp_path):
    write(tmp_path, "things/alpha.md", thing_text(GOOD, body=""))
    write(tmp_path, "things/beta.md", thing_text(
        "id: beta\ntype: task\nstatus: in-progress\ncreated: 2026-06-01",
        body="no heading here\n"))
    warns = messages(all_findings(tmp_path), mdllm.SEV_WARNING)
    assert any("empty markdown body" in m for m in warns)
    assert any("title heading" in m for m in warns)


def test_id_filename_mismatch_respects_option(tmp_path):
    write(tmp_path, "things/wrong-name.md", thing_text(GOOD))
    assert any("does not match filename" in m
               for m in messages(all_findings(tmp_path), mdllm.SEV_WARNING))
    write(tmp_path, "_schema.yaml", "options:\n  id_filename_match: false\n")
    assert not any("does not match filename" in m
                   for m in messages(all_findings(tmp_path)))


# ---------------------------------------------------------------- level 2


def test_duplicate_id(tmp_path):
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    write(tmp_path, "things/other/alpha.md", thing_text(GOOD))
    assert any("duplicate id" in m for m in messages(all_findings(tmp_path), mdllm.SEV_ERROR))


def test_unknown_reference(tmp_path):
    write(tmp_path, "things/alpha.md", thing_text(
        GOOD + "dependencies: [ghost]"))
    assert any("unknown id `ghost`" in m
               for m in messages(all_findings(tmp_path), mdllm.SEV_ERROR))


def test_contradicts_requires_conflict_thing(tmp_path):
    write(tmp_path, "things/alpha.md", thing_text(
        GOOD + "linked_things:\n  - id: beta\n    relation: contradicts"))
    write(tmp_path, "things/beta.md", thing_text(
        "id: beta\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    assert any("without a `type: conflict`" in m
               for m in messages(all_findings(tmp_path), mdllm.SEV_ERROR))
    write(tmp_path, "things/clash.md", thing_text(
        "id: clash\ntype: conflict\nstatus: open\ncreated: 2026-06-01\n"
        "parties: [alpha, beta]"))
    assert not any("without a `type: conflict`" in m
                   for m in messages(all_findings(tmp_path)))


def test_supersedes_without_backlink_warns(tmp_path):
    write(tmp_path, "things/alpha.md", thing_text(
        GOOD + "linked_things:\n  - id: beta\n    relation: supersedes"))
    write(tmp_path, "things/beta.md", thing_text(
        "id: beta\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    assert any("no `superseded-by` link" in m
               for m in messages(all_findings(tmp_path), mdllm.SEV_WARNING))


def test_circular_dependency(tmp_path):
    write(tmp_path, "things/alpha.md", thing_text(GOOD + "dependencies: [beta]"))
    write(tmp_path, "things/beta.md", thing_text(
        "id: beta\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "dependencies: [alpha]"))
    assert any("circular dependency" in m
               for m in messages(all_findings(tmp_path), mdllm.SEV_ERROR))


def test_orphan_is_info(tmp_path):
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    assert any("orphaned" in m for m in messages(all_findings(tmp_path), mdllm.SEV_INFO))


def _links_to(tid, target, typ="plan", status="in-progress"):
    # a thing of `status` that declares an inbound edge to `target`
    return thing_text(f"id: {tid}\ntype: {typ}\nstatus: {status}\ncreated: 2026-06-01\n"
                      f"linked_things:\n  - id: {target}\n    relation: references")


def test_active_insight_orphaned_from_live_graph_is_info(tmp_path):
    # Liveness is graph-keyed (dissolve-continuity Phase B): an active insight is
    # "in circulation" iff a NON-TERMINAL thing has an inbound edge to it.
    # - live-ref-insight: a live (in-progress) plan points to it => clean.
    # - orphan-insight: nothing points to it => Info.
    # - terminal-ref-insight: only a completed (terminal) plan points to it => Info
    #   (a terminal source does not confer liveness).
    # - gone-insight: dismissed => not flagged (only `active` re-enters sessions).
    write(tmp_path, "things/plans/live-plan.md", _links_to("live-plan", "live-ref-insight"))
    write(tmp_path, "things/plans/done-plan.md",
          _links_to("done-plan", "terminal-ref-insight", status="completed"))
    for n in ("live-ref-insight", "orphan-insight", "terminal-ref-insight"):
        write(tmp_path, f"things/insights/{n}.md", thing_text(
            f"id: {n}\ntype: insight\nstatus: active\ncreated: 2026-06-01"))
    write(tmp_path, "things/insights/gone-insight.md", thing_text(
        "id: gone-insight\ntype: insight\nstatus: dismissed\ncreated: 2026-06-01"))
    flagged = sorted(x.thing for x in all_findings(tmp_path)
                     if x.severity == mdllm.SEV_INFO
                     and "no inbound edge from a live thing" in x.message)
    assert flagged == ["orphan-insight", "terminal-ref-insight"]


def test_open_conflict_orphaned_from_live_graph_is_info(tmp_path):
    # Same graph rule for open conflicts: live inbound edge => clean, none => Info.
    write(tmp_path, "things/plans/p.md", _links_to("p", "seen-clash"))
    write(tmp_path, "things/conflicts/seen-clash.md", thing_text(
        "id: seen-clash\ntype: conflict\nstatus: open\ncreated: 2026-06-01\nparties: [a, b]"))
    write(tmp_path, "things/conflicts/lone-clash.md", thing_text(
        "id: lone-clash\ntype: conflict\nstatus: open\ncreated: 2026-06-01\nparties: [a, b]"))
    write(tmp_path, "things/conflicts/old-clash.md", thing_text(
        "id: old-clash\ntype: conflict\nstatus: resolved\ncreated: 2026-06-01\nparties: [a, b]"))
    flagged = sorted(x.thing for x in all_findings(tmp_path)
                     if x.severity == mdllm.SEV_INFO
                     and "open conflict with no inbound edge" in x.message)
    assert flagged == ["lone-clash"]


def test_insight_circulation_is_brief_independent(tmp_path):
    # The check is now graph-keyed, NOT gated on a continuity brief existing: a
    # lone active insight with no inbound edge is flagged even with no brief.
    write(tmp_path, "things/insights/lone.md", thing_text(
        "id: lone\ntype: insight\nstatus: active\ncreated: 2026-06-01"))
    assert any("no inbound edge from a live thing" in m
               for m in messages(all_findings(tmp_path), mdllm.SEV_INFO))


def test_keep_active_disposition_exempts_orphan(tmp_path):
    # A standing/parked insight with no live inbound edge is NOT orphaned when it
    # carries `disposition: keep-active` + a reason (the deliberate reckoning).
    # Without the reason, it is nudged instead (the reason is the whole point).
    write(tmp_path, "things/insights/kept.md", thing_text(
        "id: kept\ntype: insight\nstatus: active\ncreated: 2026-06-01\n"
        'disposition: keep-active\ndisposition_reason: "a standing razor"'))
    write(tmp_path, "things/insights/kept-no-reason.md", thing_text(
        "id: kept-no-reason\ntype: insight\nstatus: active\ncreated: 2026-06-01\n"
        "disposition: keep-active"))
    orphaned = {x.thing for x in all_findings(tmp_path)
                if "no inbound edge from a live thing" in x.message}
    assert "kept" not in orphaned and "kept-no-reason" not in orphaned
    needs_reason = {x.thing for x in all_findings(tmp_path)
                    if "no `disposition_reason`" in x.message}
    assert needs_reason == {"kept-no-reason"}


# ---------------------------------------------------------------- touchpoints


def test_touchpoints_reports_declared_and_literal(tmp_path, capsys):
    write(tmp_path, "things/target.md", thing_text(
        "id: target\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    write(tmp_path, "things/dep.md", thing_text(
        "id: dep\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "linked_things:\n  - id: target\n    relation: informs"))
    write(tmp_path, "things/child.md", thing_text(
        "id: child\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "parent: target"))
    write(tmp_path, "things/d.md", thing_text(
        "id: d\ntype: decision\nstatus: made\ncreated: 2026-06-01\n"
        "informed_by:\n  - id: target\n    commit: abc1234"))
    write(tmp_path, "things/mention.md", thing_text(
        "id: mention\ntype: task\nstatus: in-progress\ncreated: 2026-06-01",
        "# Mention\n\nThis discusses target only in prose.\n"))
    rc = mdllm.cmd_touchpoints(_ns(path=str(tmp_path), id="target"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "dep -> target" in out and "relation `informs`" in out
    assert "child -> target" in out and "via `parent`" in out
    assert "d -> target" in out and "informed_by @abc1234" in out
    # mention names the target only in prose => literal tier, not declared
    assert "mention" in out.split("Literal references")[1]
    assert "Conceptual residue" in out


def test_touchpoints_unknown_id_errors(tmp_path, capsys):
    write(tmp_path, "things/a.md", thing_text(GOOD))
    rc = mdllm.cmd_touchpoints(_ns(path=str(tmp_path), id="ghost"))
    assert rc == 1 and "no thing with id `ghost`" in capsys.readouterr().out


def test_touchpoints_leaf_has_no_risk(tmp_path, capsys):
    write(tmp_path, "things/lonely.md", thing_text(
        "id: lonely\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    rc = mdllm.cmd_touchpoints(_ns(path=str(tmp_path), id="lonely"))
    out = capsys.readouterr().out
    assert rc == 0 and "carries no\nconsistency risk" not in out  # wrapped; check phrase
    assert "Nothing points at `lonely`" in out


# ---------------------------------------------------------------- cascade


def test_cascade_unblock_and_partial(tmp_path, capsys):
    write(tmp_path, "things/target.md", thing_text(
        "id: target\ntype: task\nstatus: completed\ncreated: 2026-06-01"))
    write(tmp_path, "things/other.md", thing_text(
        "id: other\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    # ready: its only prerequisite is the just-completed target
    write(tmp_path, "things/ready.md", thing_text(
        "id: ready\ntype: task\nstatus: blocked\ncreated: 2026-06-01\n"
        "priority: high\ndependencies:\n  - target"))
    # waiting: still blocked on `other`, which is not terminal
    write(tmp_path, "things/waiting.md", thing_text(
        "id: waiting\ntype: task\nstatus: blocked\ncreated: 2026-06-01\n"
        "dependencies:\n  - target\n  - other"))
    rc = mdllm.cmd_cascade(_ns(path=str(tmp_path), id="target"))
    out = capsys.readouterr().out
    assert rc == 0
    unblock_section = out.split("Unblock candidates")[1].split("Partial")[0]
    assert "ready" in unblock_section and "priority high" in unblock_section
    assert "waiting — 1/2" in out


def test_cascade_follows_blocks_reverse_edge(tmp_path, capsys):
    # The prerequisite is declared by the target's `blocks`, not the downstream's
    # `dependencies`; cascade must read both directions or go blind to it.
    write(tmp_path, "things/target.md", thing_text(
        "id: target\ntype: task\nstatus: completed\ncreated: 2026-06-01\n"
        "blocks:\n  - downstream"))
    write(tmp_path, "things/downstream.md", thing_text(
        "id: downstream\ntype: task\nstatus: blocked\ncreated: 2026-06-01"))
    rc = mdllm.cmd_cascade(_ns(path=str(tmp_path), id="target"))
    out = capsys.readouterr().out
    assert rc == 0
    assert "downstream" in out.split("Unblock candidates")[1].split("Partial")[0]


def test_cascade_parent_rollup_completion_candidate(tmp_path, capsys):
    write(tmp_path, "things/parent.md", thing_text(
        "id: parent\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    write(tmp_path, "things/target.md", thing_text(
        "id: target\ntype: task\nstatus: completed\ncreated: 2026-06-01\nparent: parent"))
    write(tmp_path, "things/sib.md", thing_text(
        "id: sib\ntype: task\nstatus: completed\ncreated: 2026-06-01\nparent: parent"))
    rc = mdllm.cmd_cascade(_ns(path=str(tmp_path), id="target"))
    out = capsys.readouterr().out
    assert rc == 0 and "completion candidate" in out and "2/2" in out


def test_cascade_parent_rollup_partial(tmp_path, capsys):
    write(tmp_path, "things/parent.md", thing_text(
        "id: parent\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    write(tmp_path, "things/target.md", thing_text(
        "id: target\ntype: task\nstatus: completed\ncreated: 2026-06-01\nparent: parent"))
    write(tmp_path, "things/sib.md", thing_text(
        "id: sib\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\nparent: parent"))
    rc = mdllm.cmd_cascade(_ns(path=str(tmp_path), id="target"))
    out = capsys.readouterr().out
    assert rc == 0 and "partial progress" in out and "1/2" in out


def test_cascade_leaf_propagates_nowhere(tmp_path, capsys):
    write(tmp_path, "things/lonely.md", thing_text(
        "id: lonely\ntype: task\nstatus: completed\ncreated: 2026-06-01"))
    rc = mdllm.cmd_cascade(_ns(path=str(tmp_path), id="lonely"))
    out = capsys.readouterr().out
    assert rc == 0 and "Nothing depends on `lonely`" in out


def test_cascade_reports_does_not_apply(tmp_path, capsys):
    # The floor reports; it never mutates domain state. `ready` stays blocked on disk.
    write(tmp_path, "things/target.md", thing_text(
        "id: target\ntype: task\nstatus: completed\ncreated: 2026-06-01"))
    p = write(tmp_path, "things/ready.md", thing_text(
        "id: ready\ntype: task\nstatus: blocked\ncreated: 2026-06-01\n"
        "dependencies:\n  - target"))
    mdllm.cmd_cascade(_ns(path=str(tmp_path), id="target"))
    assert "status: blocked" in p.read_text(encoding="utf-8")


def test_cascade_hypothetical_when_target_not_terminal(tmp_path, capsys):
    write(tmp_path, "things/target.md", thing_text(
        "id: target\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    write(tmp_path, "things/ready.md", thing_text(
        "id: ready\ntype: task\nstatus: blocked\ncreated: 2026-06-01\n"
        "dependencies:\n  - target"))
    rc = mdllm.cmd_cascade(_ns(path=str(tmp_path), id="target"))
    out = capsys.readouterr().out
    assert rc == 0 and "HYPOTHETICAL" in out


def test_cascade_unknown_id_errors(tmp_path, capsys):
    write(tmp_path, "things/a.md", thing_text(GOOD))
    rc = mdllm.cmd_cascade(_ns(path=str(tmp_path), id="ghost"))
    assert rc == 1 and "no thing with id `ghost`" in capsys.readouterr().out


# ---------------------------------------------------------------- level 3


def test_undeclared_type_and_relation_warn_required_field_errors(tmp_path):
    write(tmp_path, "_schema.yaml",
          "types:\n  vat-return:\n    statuses: [open]\n    required_fields: [period]\n"
          "relations: [has-deadline]\n")
    write(tmp_path, "things/r.md", thing_text(
        "id: r\ntype: vat-return\nstatus: open\ncreated: 2026-06-01\n"
        "linked_things:\n  - id: m\n    relation: mystery-rel"))
    write(tmp_path, "things/m.md", thing_text(
        "id: m\ntype: unheard-of\nstatus: in-progress\ncreated: 2026-06-01"))
    findings = all_findings(tmp_path)
    assert any("domain-required field `period` missing" in m
               for m in messages(findings, mdllm.SEV_ERROR))
    warns = messages(findings, mdllm.SEV_WARNING)
    assert any("type `unheard-of` not declared" in m for m in warns)
    assert any("relation `mystery-rel` not in declared vocabulary" in m for m in warns)


def test_field_registration_is_opt_in(tmp_path):
    # No `known_fields` declared => no field check, however exotic the keys.
    write(tmp_path, "_schema.yaml", "types:\n  task:\n    statuses: [in-progress]\n")
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "whatever_field: 1\nanother: 2"))
    assert not any("CORE_FIELDS" in m for m in messages(all_findings(tmp_path)))


def test_coordination_claim_fields_are_framework_vocabulary(tmp_path):
    # held_by/held_until are declared by coordination-claim.md and shipped into
    # every domain as part of the workflow-run frontmatter contract
    # (workflow-state.md), so CORE_FIELDS criterion 2 applies: a domain must
    # never be made to register the framework's own vocabulary. Unadmitted
    # until 2026-08-23, when the framework's own sprint runs took this warning
    # for using the framework's own reserved convention.
    write(tmp_path, "_schema.yaml",
          "types:\n  task:\n    statuses: [in-progress]\n"
          "known_fields:\n  - owner\n")
    write(tmp_path, "things/r.md", thing_text(
        "id: r\ntype: workflow-run\nstatus: active\ncreated: 2026-08-23\n"
        "definition: d\ncurrent_stage: build\n"
        "held_by: claude-code\nheld_until: 2026-08-24T12:00:00Z"))
    warns = messages(all_findings(tmp_path), mdllm.SEV_WARNING)
    assert not any("field `held_by`" in m for m in warns)
    assert not any("field `held_until`" in m for m in warns)


def test_field_registration_flags_unregistered_field(tmp_path):
    # Declaring `known_fields` activates the gate. CORE_FIELDS (status/created/
    # linked_things), the declared field (owner), and a per-type required_field
    # (period) all pass; the mis-keyed `relations` (the silent-loss bug) and an
    # undeclared `colour` are flagged at Warning — never Error. `tags` is NOT
    # flagged: thing.md's Recommended vocabulary (priority/tags/confidence/
    # version) joined CORE_FIELDS at the ninth review — a domain must never be
    # made to register the framework's own vocabulary (this test's previous
    # revision used `tags` as its flaggable example, encoding the defect).
    write(tmp_path, "_schema.yaml",
          "types:\n  task:\n    statuses: [in-progress]\n    required_fields: [period]\n"
          "known_fields:\n  - owner\n")
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "period: q1\nowner: jm\ntags: [x]\ncolour: red\n"
        "relations:\n  - id: b\n    relation: informs"))   # mis-keyed linked_things
    findings = all_findings(tmp_path)
    warns = messages(findings, mdllm.SEV_WARNING)
    assert any("field `relations` not in CORE_FIELDS" in m for m in warns)
    assert any("field `colour` not in CORE_FIELDS" in m for m in warns)
    # the legitimate fields are not flagged — including framework vocabulary
    assert not any("field `owner`" in m for m in warns)
    assert not any("field `period`" in m for m in warns)
    assert not any("field `status`" in m for m in warns)
    assert not any("field `tags`" in m for m in warns)
    # and it is strictly advisory — no field Error
    assert not any("CORE_FIELDS" in m for m in messages(findings, mdllm.SEV_ERROR))


# ---------------------------------------------------------------- scan


def test_scan_skips_non_things_and_excluded_dirs(tmp_path):
    write(tmp_path, "README.md", thing_text(GOOD))          # NON_THING_FILES
    write(tmp_path, "notes.md", "# free-form notes\n")       # no frontmatter
    write(tmp_path, "templates/t.md", thing_text(GOOD))      # excluded dir
    write(tmp_path, ".codex/project-note.md", thing_text(GOOD))  # adapter state
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    corpus, _ = scan(tmp_path)
    assert [t.id for t in corpus.things] == ["alpha"]


# ---------------------------------------------------------------- assertions


def seed_eval_domain(tmp_path):
    write(tmp_path, "_schema.yaml",
          "types:\n  vat-return:\n    statuses: [open, figures-ready]\n"
          "  deadline:\n    statuses: [pending, met]\n"
          "relations: [has-deadline]\n")
    write(tmp_path, "things/ret.md", thing_text(
        "id: ret\ntype: vat-return\nstatus: figures-ready\ncreated: 2026-06-01\n"
        "output_vat: 2500.00\ninput_vat: '380.00'\n"
        "linked_things:\n  - id: dl\n    relation: has-deadline"))
    write(tmp_path, "things/dl.md", thing_text(
        "id: dl\ntype: deadline\nstatus: pending\ncreated: 2026-06-01\n"
        "linked_things:\n  - id: ret\n    relation: has-deadline"))


def test_assertions_all_kinds_pass(tmp_path):
    seed_eval_domain(tmp_path)
    fixture = {"assertions": [
        {"thing_exists": "ret"},
        {"status": {"id": "ret", "equals": "figures-ready"}},
        {"field": {"id": "ret", "name": "output_vat", "equals": 2500.00}},
        {"link": {"from": "ret", "relation": "has-deadline", "to": "dl"}},
        {"validates_clean": True},
    ]}
    passed, failed, _ = mdllm.check_assertions(fixture, tmp_path)
    assert (passed, failed) == (5, 0)


def test_field_assertion_coerces_numeric_strings(tmp_path):
    seed_eval_domain(tmp_path)  # input_vat is the string '380.00'
    fixture = {"assertions": [
        {"field": {"id": "ret", "name": "input_vat", "equals": 380.00}}]}
    passed, failed, _ = mdllm.check_assertions(fixture, tmp_path)
    assert (passed, failed) == (1, 0)


def test_field_assertion_wrong_value_fails(tmp_path):
    seed_eval_domain(tmp_path)
    fixture = {"assertions": [
        {"field": {"id": "ret", "name": "output_vat", "equals": 9999.0}},
        {"thing_exists": "nonexistent"},
        {"not-an-assertion": 1}]}
    passed, failed, _ = mdllm.check_assertions(fixture, tmp_path)
    assert (passed, failed) == (0, 3)


# ---------------------------------------------------------------- kernel/index


def test_kernel_block_extraction():
    text = ("prose\n<!-- kernel -->\nrule one\n<!-- /kernel -->\n"
            "more prose\n<!--kernel-->\nrule two\n<!--/kernel-->\n")
    assert [b.strip() for b in mdllm.KERNEL_RE.findall(text)] == ["rule one", "rule two"]


def test_relationships_index_walks_structural_pointers(tmp_path):
    # The relationships index must emit the singular structural pointers
    # (`definition`, `parent`), not only `linked_things` — otherwise the
    # change-reconciliation Assimilate beat is blind to a definition's runs and a
    # parent's children. (structural-pointers-need-reverse-edge-indexing)
    write(tmp_path, "things/proc.md", thing_text(
        "id: proc\ntype: workflow-definition\nstatus: stable\ncreated: 2026-06-16\n"
        "stages:\n  - id: intake\n    to: []", "# Proc\n\nA process.\n"))
    write(tmp_path, "things/run.md", thing_text(
        "id: run\ntype: workflow-run\nstatus: active\ncreated: 2026-06-16\n"
        "definition: proc\ncurrent_stage: intake", "# Run\n\nA run.\n"))
    write(tmp_path, "things/child.md", thing_text(
        "id: child\ntype: task\nstatus: in-progress\ncreated: 2026-06-16\n"
        "parent: proc"))
    corpus, _ = scan(tmp_path)
    body, _ = mdllm.build_index_body(corpus, "relationships")
    assert "- run --definition--> proc" in body
    assert "- child --parent--> proc" in body


def test_provenance_index_reverse_map(tmp_path):
    write(tmp_path, "things/k.md", thing_text(GOOD.replace("alpha", "k")))
    write(tmp_path, "things/d.md", thing_text(
        "id: d\ntype: decision\nstatus: made\ncreated: 2026-06-01\n"
        "informed_by:\n  - id: k\n    commit: abc1234"))
    corpus, _ = scan(tmp_path)
    body, coverage = mdllm.build_index_body(corpus, "provenance")
    assert coverage == 1 and "## k" in body and "d (pinned @abc1234)" in body


def test_provenance_unreachable_commit_with_input_present_is_warning(tmp_path, capsys):
    # A pinned commit that is not reachable in this repo (e.g. history was
    # rewritten, or the pin was never valid) must NOT hard-fail CI so long as the
    # cited input is still in the corpus — the reasoning chain is intact, only the
    # anchor is stale. Non-blocking Warning, exit 0, with a re-pin nudge. The
    # message states the observable fact only — it must not assert a cause.
    _git_repo(tmp_path)
    write(tmp_path, "things/k.md", thing_text(GOOD.replace("alpha", "k")))
    write(tmp_path, "things/d.md", thing_text(
        "id: d\ntype: decision\nstatus: made\ncreated: 2026-06-01\n"
        "informed_by:\n  - id: k\n    commit: deadbee"))
    rc = mdllm.cmd_provenance(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 0
    assert "### Warnings" in out and "not reachable" in out and "re-pin" in out
    # the tool must not diagnose a cause it cannot verify
    assert "history rewritten" not in out and "history was rewritten" not in out


def test_provenance_missing_commit_and_missing_input_is_error(tmp_path, capsys):
    # But if the pinned commit is gone AND the cited input is absent from the
    # corpus, the chain is genuinely broken — that stays a blocking Error.
    _git_repo(tmp_path)
    write(tmp_path, "things/d.md", thing_text(
        "id: d\ntype: decision\nstatus: made\ncreated: 2026-06-01\n"
        "informed_by:\n  - id: ghost\n    commit: deadbee"))
    rc = mdllm.cmd_provenance(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 1 and "### Errors" in out and "chain is broken" in out
    assert "history rewritten" not in out and "history was rewritten" not in out


# ---------------------------------------------------------------- scaffold


def test_scaffold_birth_sequence(tmp_path, capsys):
    _git_repo(tmp_path)
    target = tmp_path / "client-x"
    rc = mdllm.cmd_scaffold(_ns(path=str(target)))
    out = capsys.readouterr().out
    assert rc == 0 and "first commit made" in out
    # isolation: outer repo ignores the domain, committed before domain work
    assert "client-x/" in (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert (target / ".git").exists()
    hook = target / ".git" / "hooks" / "pre-commit"
    assert hook.is_file()
    assert '.venv/Scripts/python.exe' in hook.read_text(encoding="utf-8")
    # mechanical placeholders substituted; semantic ones intact
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "framework_version_seen: " in agents and "[relative path" not in agents
    assert "[framework-root]" not in agents
    assert "Manual CLI launch — read before Session Start" in agents
    assert "tools/mdllm.ps1" in agents and "even when" in agents
    assert "estate-sync . --require-fresh" in agents
    assert "one-command" in agents and "network/filesystem approval" in agents
    assert "Git credentials are invalid" in agents
    assert agents.index("Manual CLI launch") < \
        agents.index("<!-- generated:session-start -->")
    assert "[What this domain does]" in agents  # semantic half untouched
    # the freshly scaffolded domain passes the floor with zero findings
    corpus, findings = mdllm.scan(target)
    for t in corpus.things:
        findings.extend(mdllm.validate_level1(t, corpus.schema))
    findings.extend(mdllm.validate_level2(corpus))
    findings.extend(mdllm.validate_level3(corpus))
    # 4 skills + 8 reasoning prompts (delivered since v3.24.0 — the generated
    # session-start block names them, so birth must include them)
    assert findings == [] and len(corpus.things) == 12


def test_domain_kernel_regeneration_preserves_authored_launch_contract(
        tmp_path, capsys):
    _git_repo(tmp_path)
    target = tmp_path / "manual-launch-contract"
    assert mdllm.cmd_scaffold(_ns(path=str(target))) == 0
    capsys.readouterr()
    before = (target / "AGENTS.md").read_text(encoding="utf-8")
    marker = "Manual CLI launch — read before Session Start"
    assert before.count(marker) == 1

    assert mdllm.cmd_domain_kernel(_ns(path=str(target), check=False)) == 0
    after = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert after.count(marker) == 1
    assert after[before.index(marker):before.index("## What This System Does")] == \
        before[before.index(marker):before.index("## What This System Does")]
    # Gate 7.0 is opt-in for existing domains: the authored route reinterprets
    # managed legacy commands without changing canonical generated bytes.
    _, drifted = mdllm.domain_kernel_status(
        after, mdllm.build_domain_kernel_blocks(target,
            mdllm.parse_frontmatter(after)[0] or {}))
    assert drifted == []


def test_scaffold_isolation_skips_when_blanket_rule_covers(tmp_path, capsys):
    # A blanket `domain/` rule already isolates the path: scaffold must not
    # append a named per-domain line nor make a commit naming the domain —
    # domain names are domain state and must not enter the outer repo.
    import subprocess
    _git_repo(tmp_path)
    (tmp_path / ".gitignore").write_text("domain/\n", encoding="utf-8")
    target = tmp_path / "domain" / "client-y"
    rc = mdllm.cmd_scaffold(_ns(path=str(target)))
    out = capsys.readouterr().out
    assert rc == 0 and "first commit made" in out
    assert "client-y" not in (tmp_path / ".gitignore").read_text(encoding="utf-8")
    log = subprocess.run(["git", "log", "--oneline", "--all"], cwd=tmp_path,
                         capture_output=True, text=True).stdout
    assert "client-y" not in log


def test_schema_unparseable_is_finding_not_crash(tmp_path):
    write(tmp_path, "_schema.yaml", "types:\n  [oops]:\n    statuses: [a]\n")
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    corpus, findings = mdllm.scan(tmp_path)
    assert corpus.schema is None
    assert any("unparseable" in f.message for f in findings
               if f.severity == mdllm.SEV_ERROR)


# ------------------------------------------------- scaffold-style assertions


def test_assertions_file_and_git(tmp_path):
    import subprocess
    write(tmp_path, ".gitignore", "client-tracker/\n")
    write(tmp_path, "client-tracker/AGENTS.md",
          "---\nname: x\nframework_root: ../..\n---\n# A\n")
    sub = tmp_path / "client-tracker"
    subprocess.run(["git", "init", "-q"], cwd=sub, check=True)
    subprocess.run(["git", "add", "-A"], cwd=sub, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-q", "-m", "x"], cwd=sub, check=True)
    fixture = {"assertions": [
        {"file_exists": "client-tracker/AGENTS.md"},
        {"file_exists": ["missing.md", "client-tracker/AGENTS.md"]},
        {"file_contains": {"path": "client-tracker/AGENTS.md",
                           "text": "framework_root:"}},
        {"git_repo": "client-tracker"},
        {"git_commits": {"path": "client-tracker", "min": 1}},
        {"file_contains": {"path": ".gitignore", "text": "client-tracker"}},
    ]}
    passed, failed, _ = mdllm.check_assertions(fixture, tmp_path)
    assert (passed, failed) == (6, 0)


def test_assertions_domain_dir_scoping(tmp_path):
    write(tmp_path, "client-tracker/things/alpha.md", thing_text(GOOD))
    fixture = {"domain_dir": "client-tracker", "assertions": [
        {"thing_exists": "alpha"},
        {"min_things": 1},
        {"validates_clean": True},
    ]}
    passed, failed, _ = mdllm.check_assertions(fixture, tmp_path)
    assert (passed, failed) == (3, 0)


# ---------------------------------------------------------------- doctor


def test_doctor_degraded_without_hook(tmp_path, capsys):
    _git_repo(tmp_path)
    rc = mdllm.cmd_doctor(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 1 and "DEGRADED" in out and "hook not installed" in out


def test_doctor_floor_active_with_hook(tmp_path, capsys):
    import pytest
    if not _git_supports_hook_run():
        pytest.skip("git < 2.36 — doctor reports WARN instead of execution-testing")
    _git_repo(tmp_path)
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    mdllm.cmd_install_hook(_ns(path=str(tmp_path)))
    rc = mdllm.cmd_doctor(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 0 and "FLOOR ACTIVE" in out and "EXECUTES" in out


def test_doctor_warns_on_stale_hook_body(tmp_path, capsys):
    # A hook installed at an older HOOK_BODY (here simulated by tampering) must
    # be flagged — a domain that sealed to a newer framework without re-running
    # install-hook is exactly this case. Advisory: floor stays active (rc 0).
    import pytest
    if not _git_supports_hook_run():
        pytest.skip("git < 2.36 — doctor cannot execution-test the hook")
    _git_repo(tmp_path)
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    mdllm.cmd_install_hook(_ns(path=str(tmp_path)))
    hook = tmp_path / ".git" / "hooks" / "pre-commit"
    # Differ from the current HOOK_BODY without breaking execution (a trailing
    # comment) — models an older but still-runnable hook.
    hook.write_text(hook.read_text(encoding="utf-8") + "# older-body marker\n",
                    encoding="utf-8", newline="\n")
    rc = mdllm.cmd_doctor(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 0 and "hook body is STALE" in out and "FLOOR ACTIVE" in out


def test_doctor_uses_shared_hook_execution_fallback(tmp_path, capsys, monkeypatch):
    _git_repo(tmp_path)
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    mdllm.cmd_install_hook(_ns(path=str(tmp_path), no_test=True))
    capsys.readouterr()

    observed = {}

    def compatible_result(root, hook="pre-commit", *, expected_bytes=None):
        observed["root"] = Path(root)
        observed["hook"] = hook
        observed["expected_bytes"] = expected_bytes
        return {"hook": "pre-commit", "supported": True, "executed": True,
                "passed": True, "via": "direct-compatible", "returncode": 0,
                "stdout": "", "stderr": "", "detail": ""}

    monkeypatch.setattr(doctor_module, "execution_test_hook", compatible_result)
    rc = mdllm.cmd_doctor(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out

    assert rc == 0
    assert observed["root"] == tmp_path.resolve()
    assert observed["hook"] == "pre-commit"
    assert observed["expected_bytes"]
    assert "pre-commit hook EXECUTES" in out


def test_assertions_scaffold_failures(tmp_path):
    fixture = {"domain_dir": "nope", "assertions": [
        {"file_exists": "nope/AGENTS.md"},
        {"git_repo": "nope"},
        {"git_commits": {"path": "nope", "min": 1}},
        {"min_things": 1},
        {"file_contains": {"path": ".gitignore", "text": "nope"}},
    ]}
    passed, failed, _ = mdllm.check_assertions(fixture, tmp_path)
    assert (passed, failed) == (0, 5)


# ---------------------------------------------------------------- coherence


def test_coherence_unused_vocabulary_is_info(tmp_path):
    # General check (no sentinel needed) — a domain's own _schema.yaml is its
    # spec of its types, so this is the check a domain inherits.
    write(tmp_path, "_schema.yaml",
          "types:\n  used-type:\n    statuses: [a]\n"
          "  ghost-type:\n    statuses: [b]\n")
    write(tmp_path, "things/x.md", thing_text(
        "id: x\ntype: used-type\nstatus: a\ncreated: 2026-06-01"))
    infos = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_INFO)
    assert any("declared type `ghost-type` is used by no thing" in m for m in infos)
    assert not any("`used-type`" in m for m in infos)


def test_coherence_domain_skips_framework_checks(tmp_path):
    # No .markdownllm => general checks only. A missing kernel.md must NOT error
    # here (a domain has no kernel) — the proof the hook is safe in a domain.
    write(tmp_path, "things/x.md", thing_text(GOOD))
    msgs = messages(mdllm.coherence_findings(tmp_path, 15))
    assert not any("kernel" in m.lower() for m in msgs)
    assert not any("foundational_specs" in m for m in msgs)


def test_coherence_missing_foundational_spec_errors(tmp_path):
    write(tmp_path, ".markdownllm",
          "framework: F\nversion: 1.0\n"
          "foundational_specs:\n  - present.md\n  - absent.md\n")
    write(tmp_path, "present.md", "# Present\n")
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert any("`absent.md` listed in .markdownllm but not present" in m for m in errs)
    assert not any("`present.md`" in m for m in errs)


def _framework_root_with_entry(tmp_path, catalog_block="", tier2_block=""):
    """Minimal framework root: sentinel + an AGENTS.md carrying the two
    annotated prose sections the F8a check leg reads."""
    write(tmp_path, ".markdownllm",
          "framework: F\nversion: 1.0\nfoundational_specs: []\n")
    write(tmp_path, "AGENTS.md",
          "---\nname: F\n---\n\n# F\n\n"
          "**Tier 2 — Load on demand by query type:**\n\n"
          "| Query type | Load |\n|---|---|\n" + tier2_block + "\n"
          "## Framework Specifications (Things)\n\n" + catalog_block + "\n"
          "## After\n\ntail\n")


def test_coherence_catalog_annotation_matches_frontmatter(tmp_path):
    # The catalog's (type, status) pair is derivable from the spec's own
    # frontmatter, but the one-line descriptions beside it are not — so this
    # section is CHECKED rather than generated. Truth wins; the catalog line
    # is expected to move in the same commit as the spec's status.
    write(tmp_path, "alpha.md", thing_text(
        "id: alpha\ntype: specification\nstatus: stable\ncreated: 2026-01-01"))
    _framework_root_with_entry(
        tmp_path,
        catalog_block="- **alpha.md** — Some description. "
                      "(`type: specification`, `status: draft`)\n")
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert any("`alpha.md` is annotated (`specification`, `draft`)" in m
               and "frontmatter says (`specification`, `stable`)" in m
               for m in errs)


def test_coherence_catalog_annotation_clean_when_true(tmp_path):
    write(tmp_path, "alpha.md", thing_text(
        "id: alpha\ntype: specification\nstatus: stable\ncreated: 2026-01-01"))
    _framework_root_with_entry(
        tmp_path,
        catalog_block="- **alpha.md** — Some description. "
                      "(`type: specification`, `status: stable`)\n")
    msgs = messages(mdllm.coherence_findings(tmp_path, 15))
    assert not any("alpha.md" in m and "annotated" in m for m in msgs)


def test_coherence_catalog_flags_listed_but_absent_spec(tmp_path):
    _framework_root_with_entry(
        tmp_path,
        catalog_block="- **ghost.md** — Never written. "
                      "(`type: specification`, `status: draft`)\n")
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert any("`ghost.md` is listed in the catalog but not present on disk" in m
               for m in errs)


def test_coherence_catalog_reports_when_it_cannot_look(tmp_path):
    # Null-result discipline: a section that cannot be located reports that,
    # rather than returning clean and reading like a pass.
    write(tmp_path, ".markdownllm",
          "framework: F\nversion: 1.0\nfoundational_specs: []\n")
    write(tmp_path, "AGENTS.md", "---\nname: F\n---\n\n# F\n\nNo sections.\n")
    warns = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_WARNING)
    assert any("not found" in m and "could not run" in m for m in warns)
    assert any("Tier-2 routing table marker was not found" in m for m in warns)


def test_coherence_tier2_routing_requires_a_row_per_spec(tmp_path):
    # Every Tier-2 spec in the TIERS map must be reachable from the routing
    # table: a spec nothing routes to is a spec nothing loads.
    _framework_root_with_entry(tmp_path, tier2_block="| Some query | `thing.md` |\n")
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert any("no routing row in AGENTS.md names it" in m for m in errs)


def test_coherence_tier2_routing_flags_row_naming_absent_file(tmp_path):
    _framework_root_with_entry(tmp_path, tier2_block="| Some query | `nowhere.md` |\n")
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert any("a routing row names `nowhere.md`, which is not on disk" in m
               for m in errs)


def test_coherence_tier2_routing_is_one_directional(tmp_path):
    # The table legitimately routes surfaces outside TIERS and the catalog —
    # the human-facing docs/ guides — so a mirror check would fire on correct
    # prose. Routing an uncatalogued but real file is not a finding.
    write(tmp_path, "docs/guide.md", "# Guide\n")
    _framework_root_with_entry(tmp_path, tier2_block="| Some query | `docs/guide.md` |\n")
    msgs = messages(mdllm.coherence_findings(tmp_path, 15))
    assert not any("docs/guide.md" in m for m in msgs)


def _perimeter_repo(tmp_path, born_at="1.0.0", now="3.0.0"):
    """A repo where README.md was last touched at framework `born_at` and the
    sentinel has since moved to `now` — the shape the perimeter check dates."""
    import subprocess
    _git_repo(tmp_path)
    write(tmp_path, ".markdownllm",
          f"framework: F\nversion: {born_at}\nfoundational_specs: []\n")
    write(tmp_path, "README.md", "# Readme\n\nPerimeter prose.\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "born"], cwd=tmp_path, check=True)
    write(tmp_path, ".markdownllm",
          f"framework: F\nversion: {now}\nfoundational_specs: []\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "release"], cwd=tmp_path, check=True)


def test_coherence_perimeter_flags_a_surface_releases_behind(tmp_path):
    # The interval made mechanical: a surface outside every individual blast
    # radius is dated from git rather than from a pin it would have to carry,
    # so the check creates no new surface of its own to drift.
    _perimeter_repo(tmp_path)
    infos = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_INFO)
    assert any("`README.md` was last touched when the framework was 1.0.0" in m
               and "it is now 3.0.0" in m for m in infos)


def test_coherence_perimeter_tolerates_one_minor(tmp_path):
    # Two minors, not one, and for a real artifact rather than caution: a
    # surface reconciled DURING a release cycle is touched before the version
    # bump lands, so it reads as exactly one behind while being current. A
    # one-minor threshold would fire on correct work every single cycle.
    _perimeter_repo(tmp_path, born_at="3.0.0", now="3.1.0")
    infos = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_INFO)
    assert not any("README.md" in m and "last touched" in m for m in infos)


def test_view_glob_agrees_with_path_glob(tmp_path):
    # The two branches of _view_glob must answer the same question. They did
    # not: the no-view branch delegates to Path.glob (where `*` stops at a
    # separator) while the view branch used raw fnmatch (where it does not),
    # so `*.md` meant "this directory" without a view and "the whole tree"
    # with one. The perimeter check spawned one git process per match and
    # took two minutes; the same call had been correct in the other mode.
    from markdownllm.repository_view import RepositoryView
    from markdownllm.coherence import _view_glob
    _git_repo(tmp_path)
    write(tmp_path, "top.md", "# top\n")
    write(tmp_path, "nested/deep.md", "# deep\n")
    write(tmp_path, "nested/more/deeper.md", "# deeper\n")
    plain = _view_glob(tmp_path, "*.md", None)
    viewed = _view_glob(tmp_path, "*.md", RepositoryView.worktree(tmp_path))
    assert [p.name for p in plain] == ["top.md"]
    assert [p.name for p in viewed] == ["top.md"]
    assert [p.name for p in _view_glob(tmp_path, "*/*.md",
                                       RepositoryView.worktree(tmp_path))] == ["deep.md"]


def test_coherence_tiers_warns_spec_without_tier_entry(tmp_path):
    write(tmp_path, ".markdownllm",
          "framework: F\nversion: 1.0\nfoundational_specs:\n  - not-in-tiers.md\n")
    write(tmp_path, "not-in-tiers.md", "# x\n")
    warns = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_WARNING)
    assert any("no entry in the TIERS map" in m for m in warns)


def test_coherence_tiers_warns_tier_entry_missing_from_catalog(tmp_path):
    # The mirror direction (review 6, finding 6): directional graph reads come
    # in inbound/outbound pairs, and this check ran catalog->TIERS only —
    # thing-lifecycle.md sat in the loading map uncatalogued, invisibly.
    write(tmp_path, ".markdownllm",
          "framework: F\nversion: 1.0\nfoundational_specs:\n  - thing.md\n")
    write(tmp_path, "thing.md", "# x\n")
    warns = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_WARNING)
    assert any("in the TIERS map (tools/markdownllm/repo.py) but not in" in m for m in warns)
    assert not any("`thing.md` is in the TIERS map" in m for m in warns)


def test_coherence_example_staleness(tmp_path):
    # An example pinned behind the sentinel teaches an old shape; only the
    # walk + re-pin quiets the warning (review 6: both shipped examples sat
    # at 3.4.0 for thirteen minor versions with nothing watching).
    write(tmp_path, ".markdownllm",
          "framework: F\nversion: 3.17.3\nfoundational_specs: []\n")
    write(tmp_path, "examples/demo/AGENTS.md",
          "---\nname: D\nframework_root: ../..\nframework_version_seen: 3.4.0\n"
          "---\n\n# D\n")
    warns = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_WARNING)
    assert any("framework_version_seen 3.4.0" in m for m in warns)
    write(tmp_path, "examples/demo/AGENTS.md",
          "---\nname: D\nframework_root: ../..\nframework_version_seen: 3.17.3\n"
          "---\n\n# D\n")
    warns = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_WARNING)
    assert not any("framework_version_seen" in m for m in warns)


def test_coherence_stable_staleness_is_info(tmp_path):
    import subprocess
    _git_repo(tmp_path)
    spec = ("id: spec\ntype: specification\nstatus: stable\ncreated: 2026-06-01")
    write(tmp_path, "things/spec.md", thing_text(spec))
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add spec"], cwd=tmp_path, check=True)
    write(tmp_path, "things/spec.md", thing_text(spec, "# Spec\n\nEdited.\n"))
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "edit spec"], cwd=tmp_path, check=True)
    infos = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_INFO)
    assert any("marked `stable` but changed" in m for m in infos)


def test_coherence_index_drift_errors(tmp_path):
    write(tmp_path, "things/a.md", thing_text(
        GOOD + "linked_things:\n  - id: b\n    relation: relates-to"))
    write(tmp_path, "things/b.md", thing_text(
        "id: b\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    mdllm.cmd_index(_ns(path=str(tmp_path), action="rebuild", signal="relationships"))
    # mutate the relationship so the stored index is now stale
    write(tmp_path, "things/a.md", thing_text(
        GOOD + "linked_things:\n  - id: b\n    relation: supersedes"))
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert any("DRIFT" in m for m in errs)


def test_empty_trigger_index_is_in_sync_immediately_after_rebuild(
        tmp_path, capsys):
    write(tmp_path, "things/a.md", thing_text(GOOD))
    args = _ns(path=str(tmp_path), signal="triggers")

    assert mdllm.cmd_index(_ns(**vars(args), action="rebuild")) == 0
    capsys.readouterr()
    assert mdllm.cmd_index(_ns(**vars(args), action="check")) == 0
    assert "triggers: in sync (coverage 0)" in capsys.readouterr().out


# ---------------------------------------------------------------- triggers


def test_triggers_reports_every_declared_type(tmp_path, capsys):
    # Fired conditions print as hits; conditions the floor cannot evaluate
    # print in the skipped section — never silence. `relationship` (and any
    # unrecognised type) got exactly that silence until review 6, finding 3:
    # the no-silent-default law violated in miniature by its own enforcer.
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "due_date: 2026-06-10\n"
        "triggers:\n"
        "  - type: time\n    condition: due_date_passed\n    action: escalate\n"
        "  - type: relationship\n    watch: b\n    on: status_changed_to\n"
        "    action: re_evaluate\n"
        "  - type: cosmic\n    condition: alignment\n    action: none\n"))
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "escalate" in out                                   # evaluated hit
    assert "Not mechanically evaluable" in out                 # skipped section
    assert "`relationship` trigger" in out and "left to the agent" in out
    assert "unrecognised trigger type `cosmic`" in out


def test_stale_trigger_reads_git_history_not_mtime(tmp_path, capsys):
    import subprocess
    p = write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        "triggers:\n  - type: time\n    condition: stale\n"
        "    threshold: 30d\n    action: revisit\n"))
    # No git repo: mtime fallback — a freshly written file is not stale.
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    assert "revisit" not in capsys.readouterr().out
    # Last commit for the file is months old but the working-copy mtime is
    # fresh (a checkout or a stray touch does exactly this): activity is the
    # commit stream, so the trigger fires anyway (review 5 drift item).
    old = {**os.environ, "GIT_AUTHOR_DATE": "2026-05-01T12:00:00",
           "GIT_COMMITTER_DATE": "2026-05-01T12:00:00"}
    git = ["git", "-c", "user.email=t@t", "-c", "user.name=t"]
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(git + ["add", "."], cwd=tmp_path, check=True)
    subprocess.run(git + ["commit", "-q", "-m", "x"], cwd=tmp_path,
                   check=True, env=old)
    os.utime(p)  # mtime says "just now"; git says May
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    assert "revisit" in capsys.readouterr().out


def test_free_text_time_condition_with_date_is_evaluated(tmp_path, capsys):
    # A `type: time` trigger whose condition is free text naming an ISO date
    # fell through every inner branch — and the unknown-type else is on TYPE,
    # so it was never reported at all (estate audit FW-1: 8 of 28 triggers
    # silently dropped, one 10 days past its date in a report reading "No
    # trigger conditions currently true.").
    import datetime as dt
    soon = (dt.date.today() + dt.timedelta(days=10)).isoformat()
    far = (dt.date.today() + dt.timedelta(days=90)).isoformat()
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        "triggers:\n  - type: time\n    condition: review after 2026-01-15\n"
        "    action: escalate\n"))
    write(tmp_path, "things/b.md", thing_text(
        f"id: b\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        f"triggers:\n  - type: time\n    condition: renew by {soon}\n"
        f"    action: renew\n"))
    write(tmp_path, "things/c.md", thing_text(
        f"id: c\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        f"triggers:\n  - type: time\n    condition: archive on {far}\n"
        f"    action: archive\n"))
    write(tmp_path, "things/d.md", thing_text(
        "id: d\ntype: task\nstatus: completed\ncreated: 2026-01-01\n"
        "triggers:\n  - type: time\n    condition: review after 2026-01-15\n"
        "    action: escalate\n"))
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "date 2026-01-15 reached" in out and "escalate" in out  # past, live
    # Within-30d look-aheads land in their own Upcoming section, never among
    # the fired lines — the fired/upcoming split (substrate reconciliation,
    # 2026-08-09; the v3.29.0 conflation read a quiet domain as pressured).
    assert "Upcoming (within 30 days — not yet fired)" in out
    assert "fires in" in out and "renew" in out                    # within 30d
    assert out.index("renew by") > out.index("Upcoming")           # in that section
    assert "archive" in out and "Horizon" in out                   # beyond 30d
    assert out.count("escalate") == 1                              # d is settled


def test_free_text_time_condition_without_date_is_skipped_loudly(tmp_path, capsys):
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        "triggers:\n  - type: time\n    condition: when the audit closes\n"
        "    action: surface\n"))
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "Not mechanically evaluable" in out
    assert "names no parseable date" in out


def test_date_type_is_alias_of_time(tmp_path, capsys):
    # One character of drift from `time` must not kill the control.
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        "due_date: 2026-02-01\n"
        "triggers:\n  - type: date\n    condition: due_date_passed\n"
        "    action: escalate\n"))
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "due_date 2026-02-01 passed" in out and "escalate" in out
    assert "unrecognised trigger type" not in out


def test_overdue_is_not_suppressed_by_a_declared_trigger(tmp_path, capsys):
    # The deadline scan read `if days < 0 and not meta.get("triggers")` — so
    # the more carefully authored thing (past due AND declaring a trigger the
    # evaluator could not read) printed nothing at all (estate audit FW-1).
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        "due_date: 2026-02-01\n"
        "triggers:\n  - type: time\n    condition: when the audit closes\n"
        "    action: surface\n"))
    write(tmp_path, "things/b.md", thing_text(
        "id: b\ntype: task\nstatus: in-progress\ncreated: 2026-01-01\n"
        "due_date: 2026-02-01\n"))
    mdllm.cmd_triggers(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "a: OVERDUE" in out                       # trigger no longer hides it
    assert "b: OVERDUE" in out and "no trigger declared" in out


# ---------------------------------------------------------------- domain kernel


def _agents_with_blocks(authored_tail: str = "KEEP VERBATIM") -> str:
    blocks = "".join(
        f"<!-- generated:{n} -->\n_(placeholder)_\n<!-- /generated:{n} -->\n\n"
        for n in mdllm.DOMAIN_KERNEL_BLOCKS)
    return ("---\nname: T\ndescription: d\nframework_root: ../..\n"
            "framework_version_seen: 3.14.0\n---\n\n"
            "# T Agent\n\n## What This System Does\n\nAuthored identity line.\n\n"
            + blocks + f"## Authored Tail\n\n{authored_tail}.\n")


def test_domain_kernel_fills_all_blocks(tmp_path):
    text = _agents_with_blocks()
    meta, _, _ = mdllm.parse_frontmatter(text)
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    new_text, written, missing = mdllm.apply_domain_kernel(text, blocks)
    assert set(written) == set(mdllm.DOMAIN_KERNEL_BLOCKS)
    assert missing == []
    assert "_(placeholder)_" not in new_text  # every block was replaced


def test_domain_kernel_preserves_authored_content(tmp_path):
    text = _agents_with_blocks(authored_tail="UNIQUE-SENTINEL-9417")
    meta, _, _ = mdllm.parse_frontmatter(text)
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    new_text, _, _ = mdllm.apply_domain_kernel(text, blocks)
    assert "UNIQUE-SENTINEL-9417" in new_text          # authored tail kept
    assert "Authored identity line." in new_text        # authored head kept
    assert new_text.startswith("---\nname: T\n")         # frontmatter verbatim


def test_domain_kernel_is_idempotent(tmp_path):
    text = _agents_with_blocks()
    meta, _, _ = mdllm.parse_frontmatter(text)
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    once, _, _ = mdllm.apply_domain_kernel(text, blocks)
    twice, _, _ = mdllm.apply_domain_kernel(once, blocks)
    assert once == twice
    _, drifted = mdllm.domain_kernel_status(once, blocks)
    assert drifted == []


def test_domain_kernel_check_detects_drift(tmp_path):
    meta, _, _ = mdllm.parse_frontmatter(_agents_with_blocks())
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    filled, _, _ = mdllm.apply_domain_kernel(_agents_with_blocks(), blocks)
    tampered = filled.replace("Then await intent.", "Then do whatever.")
    present, drifted = mdllm.domain_kernel_status(tampered, blocks)
    assert "session-start" in present
    assert "session-start" in drifted


def test_domain_kernel_types_render_optional_descriptions(tmp_path):
    # `description:` is the schema documenting its own vocabulary, beside
    # `statuses:` and `required_fields:`. Rendered where declared.
    write(tmp_path, "things/_schema.yaml",
          "types:\n  case:\n    description: One regulated matter, start to close\n"
          "    statuses: [open, closed]\n")
    block = mdllm.build_domain_kernel_blocks(tmp_path, {})["types"]
    assert "- `case` — One regulated matter, start to close (statuses: open / closed)" in block


def test_domain_kernel_types_are_byte_stable_without_descriptions(tmp_path):
    # The estate guarantee behind F8a: no existing domain declares
    # `description:`, so this rendering must be exactly what it was before the
    # field existed. If this string changes, every domain's managed block
    # drifts at once and their commits block on a coherence Error until each
    # is regenerated — the reason reserved-type descriptions were rejected.
    write(tmp_path, "things/_schema.yaml",
          "types:\n  case:\n    statuses: [open, closed]\n    required_fields: [ref]\n")
    block = mdllm.build_domain_kernel_blocks(tmp_path, {})["types"]
    assert "- `case` — statuses: open / closed · required: ref" in block
    assert block.startswith(
        "**Declared domain types** (from `things/_schema.yaml` — the authority; "
        "regenerate on schema change):")


def test_domain_kernel_types_cite_the_schema_they_actually_read(tmp_path):
    # A framework root keeps its schema at the root; a domain keeps it under
    # things/. The block used to hardcode the domain path, so at the root it
    # named an authority it had not read — the defect class F8a exists to end.
    write(tmp_path, "_schema.yaml", "types:\n  plan:\n    statuses: [open]\n")
    block = mdllm.build_domain_kernel_blocks(tmp_path, {})["types"]
    assert "from `_schema.yaml`" in block
    assert "things/_schema.yaml" not in block


def test_domain_kernel_types_omit_reserved_descriptions(tmp_path):
    # Reserved types are the tool's vocabulary; kernel.md names the set and
    # routes each to its owning spec. The block lists them and says nothing
    # more, deliberately.
    write(tmp_path, "things/_schema.yaml",
          "types:\n  case:\n    statuses: [open]\n")
    block = mdllm.build_domain_kernel_blocks(tmp_path, {})["types"]
    tail = block.split("Framework-reserved types")[1]
    assert "`insight`" in tail and "`workflow-run`" in tail
    assert "—" not in tail   # names only, no glosses


def test_domain_kernel_tier_lists_skills(tmp_path):
    (tmp_path / "skills").mkdir()
    (tmp_path / "skills" / "t-workflow.skill.md").write_text("x", encoding="utf-8")
    meta, _, _ = mdllm.parse_frontmatter(_agents_with_blocks())
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    assert "skills/t-workflow.skill.md" in blocks["tier-routing"]


def test_domain_kernel_hooks_include_domain_hard_hooks(tmp_path):
    meta = {"hard_hooks": [{"hook": "post-write", "action": "rebuild the index",
                            "anchor": "git-fs"}]}
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    h = blocks["hooks"]
    assert "post-write" in h and "rebuild the index" in h and "`git-fs`" in h


def test_domain_kernel_unmarked_agents_yields_no_blocks(tmp_path):
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, {})
    plain = "---\nname: T\n---\n\n# T\n\nNo managed blocks here.\n"
    _, written, missing = mdllm.apply_domain_kernel(plain, blocks)
    assert written == []
    assert set(missing) == set(mdllm.DOMAIN_KERNEL_BLOCKS)


def test_generated_blocks_reference_only_live_subcommands(tmp_path):
    # The domain-kernel drift check compares generated blocks against the same
    # builder that writes them, so a builder naming a phantom subcommand is
    # invisible to it. The parser registry is a DIFFERENT artifact: cross-check
    # every emitted `mdllm <sub>` against it. (Regression: the generated
    # session-start block shipped a nonexistent `mdllm orient` for weeks.)
    import re
    sub = next(a for a in mdllm.build_cli()._subparsers._group_actions)
    live = set(sub.choices)
    text = _agents_with_blocks()
    meta, _, _ = mdllm.parse_frontmatter(text)
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    referenced = set()
    for body in blocks.values():
        referenced |= set(re.findall(r"`(?:python [^`]*mdllm\.py|mdllm) ([a-z][a-z-]*)", body))
    assert referenced, "expected the generated blocks to reference subcommands"
    assert referenced <= live, f"generated blocks name phantom subcommands: {referenced - live}"


def test_coherence_flags_domain_kernel_drift(tmp_path):
    meta, _, _ = mdllm.parse_frontmatter(_agents_with_blocks())
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, meta)
    filled, _, _ = mdllm.apply_domain_kernel(_agents_with_blocks(), blocks)
    tampered = filled.replace("Then await intent.", "Then improvise.")
    write(tmp_path, "AGENTS.md", tampered)
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert any("domain-kernel block" in m for m in errs)


def test_coherence_ignores_unmarked_agents(tmp_path):
    write(tmp_path, "AGENTS.md", "---\nname: T\n---\n\n# T\n\nPlain entry file.\n")
    errs = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_ERROR)
    assert not any("domain-kernel" in m for m in errs)


# ---------------------------------------------------------------- session start


def _wired_domain(tmp_path, fw_version: str, seen: str | None):
    (tmp_path / "fw").mkdir()
    (tmp_path / "fw" / ".markdownllm").write_text(
        f"framework: X\nversion: {fw_version}\n", encoding="utf-8")
    fm = "name: D\nframework_root: ../fw\n"
    if seen is not None:
        fm += f"framework_version_seen: {seen}\n"
    write(tmp_path / "dom", "AGENTS.md", f"---\n{fm}---\n\n# D\n")
    return tmp_path / "dom"


def test_session_start_in_sync(tmp_path, capsys):
    dom = _wired_domain(tmp_path, "3.14.0", "3.14.0")
    mdllm.cmd_session_start(_ns(path=str(dom)))
    assert "Version: in sync" in capsys.readouterr().out


def test_session_start_detects_mismatch(tmp_path, capsys):
    dom = _wired_domain(tmp_path, "3.14.0", "3.0.0")
    mdllm.cmd_session_start(_ns(path=str(dom)))
    assert "Version: MISMATCH" in capsys.readouterr().out


def test_session_start_flags_unsealed_domain(tmp_path, capsys):
    dom = _wired_domain(tmp_path, "3.14.0", None)
    mdllm.cmd_session_start(_ns(path=str(dom)))
    assert "Version: STALE" in capsys.readouterr().out


def test_session_start_always_emits_imperative(tmp_path, capsys):
    write(tmp_path / "dom", "AGENTS.md", "---\nname: D\n---\n\n# D\n")
    mdllm.cmd_session_start(_ns(path=str(tmp_path / "dom")))
    out = capsys.readouterr().out
    assert "Session Start" in out and "before the user's first request" in out


def test_session_start_framework_root_is_not_a_stale_domain(tmp_path, capsys):
    # A framework root carries .markdownllm and points framework_root at itself;
    # it must not report itself as a stale downstream domain.
    (tmp_path / ".markdownllm").write_text("framework: X\nversion: 3.15.0\n", encoding="utf-8")
    write(tmp_path, "AGENTS.md", "---\nname: F\nframework_root: .\n---\n\n# F\n")
    mdllm.cmd_session_start(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "framework root (v3.15.0)" in out
    assert "STALE" not in out


# ---------------------------------------------------------------- phase 5 rollout


def _agents_drifted(meta_fm: str) -> str:
    body = "# D\n\n" + "".join(
        f"<!-- generated:{n} -->\n_(old placeholder)_\n<!-- /generated:{n} -->\n\n"
        for n in mdllm.DOMAIN_KERNEL_BLOCKS)
    return f"---\n{meta_fm}---\n\n{body}"


def test_scaffold_deploys_slash_commands(tmp_path):
    _git_repo(tmp_path)
    target = tmp_path / "client-y"
    mdllm.cmd_scaffold(_ns(path=str(target)))
    assert (target / ".claude" / "commands" / "end-session.md").is_file()
    assert (target / ".claude" / "commands" / "retrospective.md").is_file()
    assert (target / ".github" / "prompts" / "end-session.prompt.md").is_file()


def test_scaffold_writes_hardened_adapter(tmp_path):
    import json
    _git_repo(tmp_path)
    target = tmp_path / "client-z"
    mdllm.cmd_scaffold(_ns(path=str(target)))
    settings = json.loads((target / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert "SessionStart" in settings["hooks"] and "PostToolUse" in settings["hooks"]
    # estate-sync still runs FIRST (hard hook 4 — orientation reads the log,
    # and the log is only whole after the fetch), but the ordering now lives
    # in the neutral runner: Claude launches matching handlers in parallel,
    # so a two-handler list never guaranteed it. One handler delegates the
    # whole ordered binding.
    handlers = settings["hooks"]["SessionStart"][0]["hooks"]
    assert len(handlers) == 1
    assert "harness-event claude-code session-start " in handlers[0]["command"]
    assert "tools/mdllm.py" in handlers[0]["command"]
    from markdownllm.harness_ports import LIFECYCLE_INTENTS
    assert list(LIFECYCLE_INTENTS["session-start"]) == [
        "estate-sync", "session-start"]


def test_refresh_regenerates_domain_kernel(tmp_path):
    (tmp_path / "fw").mkdir()
    (tmp_path / "fw" / ".markdownllm").write_text(
        "framework: X\nversion: 3.15.0\n", encoding="utf-8")
    (tmp_path / "fw" / "CHANGELOG.md").write_text(
        "## [3.15.0] - 2026-06-23\n- new\n", encoding="utf-8")
    dom = tmp_path / "dom"
    write(dom, "AGENTS.md", _agents_drifted(
        "name: D\nframework_root: ../fw\nframework_version_seen: 3.0.0\n"))
    mdllm.cmd_refresh(_ns(path=str(dom), seal=False))
    text = (dom / "AGENTS.md").read_text(encoding="utf-8")
    _, drifted = mdllm.domain_kernel_status(
        text, mdllm.build_domain_kernel_blocks(dom, {"name": "D"}))
    assert drifted == []   # the stale placeholders were regenerated


def test_doctor_reports_domain_kernel_status(tmp_path, capsys):
    _git_repo(tmp_path)
    blocks = mdllm.build_domain_kernel_blocks(tmp_path, {})
    filled, _, _ = mdllm.apply_domain_kernel(_agents_drifted("name: D\n"), blocks)
    write(tmp_path, "AGENTS.md", filled)
    mdllm.cmd_doctor(_ns(path=str(tmp_path)))
    assert "domain-kernel in sync" in capsys.readouterr().out


# ------------------------------------------------------ mcp-serve (Phase 1)

def _mcp_domain(tmp_path):
    write(tmp_path, "things/income/rent.md", thing_text(
        "id: rent-statement-2026\ntype: deliverable\nstatus: completed\n"
        "created: 2026-06-01\nexposed: true\ntags: [income]\n"
        "linked_things:\n  - id: internal-note\n    relation: informs\n"
        "informed_by:\n  - id: internal-note\n    commit: deadbee\n"
        "parties: [internal-note]",
        "# Rent Statement 2026\n\nTotal income: 12000.\n"))
    write(tmp_path, "things/internal/secret.md", thing_text(
        "id: internal-note\ntype: note\nstatus: in-progress\ncreated: 2026-06-01",
        "# Internal Note\n\nNot for export.\n"))
    corpus, _ = mdllm.scan(tmp_path)
    return corpus


def test_mcp_exposed_only(tmp_path):
    corpus = _mcp_domain(tmp_path)
    # internal-note carries no `exposed: true` — it stays behind the membrane.
    assert {t.id for t in mdllm.mcp_exposed_things(corpus)} == {"rent-statement-2026"}


def test_mcp_query_things_filters(tmp_path):
    corpus = _mcp_domain(tmp_path)
    assert [r["id"] for r in mdllm.mcp_query_things(corpus)] == ["rent-statement-2026"]
    assert mdllm.mcp_query_things(corpus, typ="note") == []   # not exposed at all
    assert mdllm.mcp_query_things(corpus, text="income")      # body text hit
    assert mdllm.mcp_query_things(corpus, text="nope") == []


def test_mcp_get_deliverable_stamps_triple(tmp_path):
    corpus = _mcp_domain(tmp_path)
    d = mdllm.mcp_get_deliverable(tmp_path, corpus, "dom", "rent-statement-2026")
    assert d["reference_triple"]["source_domain"] == "dom"
    assert d["reference_triple"]["source_id"] == "rent-statement-2026"
    assert d["reference_triple"]["source_commit"] == "unknown"  # tmp_path isn't a git repo
    assert "Total income" in d["content"]
    # the producer's internal graph never crosses; descriptive fields do.
    assert "linked_things" not in d["frontmatter"]
    assert "informed_by" not in d["frontmatter"]
    assert "parties" not in d["frontmatter"]
    assert d["frontmatter"]["type"] == "deliverable" and d["frontmatter"]["exposed"] is True


def test_mcp_egress_strips_producer_graph(tmp_path):
    corpus = _mcp_domain(tmp_path)
    # both crossing paths source-scope: the resource read carries no foreign ids.
    th = mdllm.mcp_read_resource(tmp_path, corpus, "dom", "thing://dom/rent-statement-2026")
    assert "Rent Statement" in th["text"]            # body crosses
    assert "linked_things" not in th["text"]         # graph does not
    # provenance pins and conflict parties are relational too — the rule is
    # "every field carrying producer-local ids", not the road test's symptom
    # list (review 6, finding 2: these two leaked for two versions).
    assert "informed_by" not in th["text"]
    assert "parties" not in th["text"]
    assert "internal-note" not in th["text"]         # the foreign id is gone


def test_mcp_get_deliverable_refuses_unexposed_and_traversal(tmp_path):
    corpus = _mcp_domain(tmp_path)
    # only exposed ids resolve; unexposed and path-traversal strings both miss.
    assert mdllm.mcp_get_deliverable(tmp_path, corpus, "dom", "internal-note") is None
    assert mdllm.mcp_get_deliverable(tmp_path, corpus, "dom", "../../etc/passwd") is None


def test_mcp_manifest_is_server_card_shaped(tmp_path):
    corpus = _mcp_domain(tmp_path)
    m = mdllm.mcp_build_manifest(tmp_path, corpus, "dom")
    assert m["domain_id"] == "dom"
    assert [k["id"] for k in m["knows"]] == ["rent-statement-2026"]
    assert "source_commit" in m["knows"][0]   # per-thing pin on the face
    assert set(m["can_do"]) == {"query_things", "get_deliverable"}


def test_mcp_read_resource(tmp_path):
    corpus = _mcp_domain(tmp_path)
    man = mdllm.mcp_read_resource(tmp_path, corpus, "dom", "manifest://dom")
    assert man and man["mimeType"] == "application/json"
    th = mdllm.mcp_read_resource(tmp_path, corpus, "dom", "thing://dom/rent-statement-2026")
    assert th and "Rent Statement" in th["text"]
    assert mdllm.mcp_read_resource(tmp_path, corpus, "dom", "thing://dom/internal-note") is None
    assert mdllm.mcp_read_resource(tmp_path, corpus, "dom", "bogus://x") is None


# ----------------------------------------------- imports-check (Phase 2 freshness)

def test_imports_freshness_fresh_then_stale(tmp_path):
    import subprocess as sp
    src = tmp_path / "srcdom"
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
        "# The Spec\n\nv1.\n"))
    sp.run(["git", "init", "-q"], cwd=src, check=True)
    _git_commit(src, "create spec")
    pin = _git_short(src)  # single commit: the spec's last-change == HEAD

    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", pin,
        {"command": sys.executable, "args": [str(Path(mdllm.__file__)), "mcp-serve", str(src)]},
        body="# The Spec\n\nv1.\n")  # a faithful mirror — content matches the face

    # 1. FRESH — pin matches the source's current per-thing commit (read via the face)
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "fresh"

    # 2. STALE — change the source thing and re-commit; the pin now lags
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
        "# The Spec\n\nv2 CHANGED.\n"))
    _git_commit(src, "revise spec")
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "stale"
    assert rows["imported-spec"]["current"] != pin
    # body actually moved -> the species that owes the re-quarantine ritual
    assert rows["imported-spec"]["species"] == "content changed"


def test_imports_freshness_stale_species_content_identical(tmp_path):
    # v3.27.0 (vantage-brief-cluster Ask 4): a source-side commit touching only
    # what egress strips (a triggers: block) moves the pin with NO crossable
    # change. The mirror is honest; only the pin lags. Re-quarantine — a
    # human's attributed flip — is not owed; re-pinning is.
    import subprocess as sp
    src = tmp_path / "srcdom"
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
        "# The Spec\n\nv1.\n"))
    sp.run(["git", "init", "-q"], cwd=src, check=True)
    _git_commit(src, "create spec")
    pin = _git_short(src)

    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", pin,
        {"command": sys.executable, "args": [str(Path(mdllm.__file__)), "mcp-serve", str(src)]},
        body="# The Spec\n\nv1.\n")

    # source gains a triggers: block — pin moves, face body does not
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true\n"
        "triggers:\n  - type: time\n    condition: \"2026-12-01 reached\"\n    action: \"review\"",
        "# The Spec\n\nv1.\n"))
    _git_commit(src, "add trigger only")
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "stale"
    assert rows["imported-spec"]["species"] == "content identical"


def test_imports_freshness_unreachable_is_unknown(tmp_path):
    # the offline case must report UNKNOWN, never a silent "fresh".
    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", "deadbee",
        {"command": "this-binary-does-not-exist-xyz", "args": ["mcp-serve", "/nope"]})
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "unreachable"


def test_imports_freshness_no_address_book_entry(tmp_path):
    con = tmp_path / "condom"
    con.mkdir()  # no .mcp.json at all
    write(con, "things/imported.md", thing_text(
        "id: imported-spec\ntype: external-spec\nstatus: ingested\ncreated: 2026-06-02\n"
        "origin: external\nverified: false\nsource_domain: srcdom\n"
        "source_id: the-spec\nsource_commit: deadbee",
        "# Imported Spec\n\nQuarantined.\n"))
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "no-address-book-entry"


def test_imports_freshness_diverged_when_mirror_edited(tmp_path):
    # The second sync direction — source behind mirror. The pins agree, but
    # the mirror's content no longer matches the face: the loop was bypassed
    # (the felt estate failure: someone updated the copy in the consumer
    # instead of the source). Detected consumer-side through the porch — no
    # multi-root read, no source-git access, the membrane holds.
    import subprocess as sp
    src = tmp_path / "srcdom"
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
        "# The Spec\n\nv1.\n"))
    sp.run(["git", "init", "-q"], cwd=src, check=True)
    _git_commit(src, "create spec")
    pin = _git_short(src)

    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", pin,
        {"command": sys.executable, "args": [str(Path(mdllm.__file__)), "mcp-serve", str(src)]})
    # Faithful mirror first: body matches the face -> fresh.
    write(con, "things/imported.md", thing_text(
        f"id: imported-spec\ntype: external-spec\nstatus: ingested\ncreated: 2026-06-02\n"
        f"origin: external\nverified: false\nsource_domain: srcdom\n"
        f"source_id: the-spec\nsource_commit: {pin}",
        "# The Spec\n\nv1.\n"))
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "fresh"
    # Edit the MIRROR, not the source: pin still current, content differs.
    write(con, "things/imported.md", thing_text(
        f"id: imported-spec\ntype: external-spec\nstatus: ingested\ncreated: 2026-06-02\n"
        f"origin: external\nverified: false\nsource_domain: srcdom\n"
        f"source_id: the-spec\nsource_commit: {pin}",
        "# The Spec\n\nv1 EDITED IN THE CONSUMER.\n"))
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "diverged"


def test_estate_check_batches_named_roots_only(tmp_path, capsys):
    # The estate view is batching over per-consumer reads: named roots in,
    # per-consumer sections + a roll-up out. Nothing discovered, nothing
    # persisted, no per-source reverse map.
    import subprocess as sp
    src = tmp_path / "srcdom"
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
        "# The Spec\n\nv1.\n"))
    sp.run(["git", "init", "-q"], cwd=src, check=True)
    _git_commit(src, "create spec")
    pin = _git_short(src)

    con_a = tmp_path / "con-a"
    con_a.mkdir()
    _consumer_with_import(con_a, "srcdom", "the-spec", pin,
        {"command": sys.executable, "args": [str(Path(mdllm.__file__)), "mcp-serve", str(src)]})
    write(con_a, "things/imported.md", thing_text(
        f"id: imported-spec\ntype: external-spec\nstatus: ingested\ncreated: 2026-06-02\n"
        f"origin: external\nverified: false\nsource_domain: srcdom\n"
        f"source_id: the-spec\nsource_commit: {pin}",
        "# The Spec\n\nv1.\n"))
    con_b = tmp_path / "con-b"
    con_b.mkdir()  # no .mcp.json: its import has no route
    write(con_b, "things/other.md", thing_text(
        "id: other-import\ntype: external-spec\nstatus: ingested\ncreated: 2026-06-02\n"
        "origin: external\nverified: false\nsource_domain: srcdom\n"
        "source_id: the-spec\nsource_commit: deadbee",
        "# Other\n\nX.\n"))
    rc = mdllm.cmd_estate_check(_ns(paths=[str(con_a), str(con_b)]))
    out = capsys.readouterr().out
    assert rc == 0
    assert "### con-a" in out and "### con-b" in out       # per-consumer, not per-source
    assert "fresh      imported-spec" in out
    assert "NO-ROUTE   other-import" in out
    assert "Estate roll-up" in out
    assert "never an index" in out


def test_estate_check_rejects_non_directory(tmp_path, capsys):
    rc = mdllm.cmd_estate_check(_ns(paths=[str(tmp_path / "nope")]))
    assert rc == 1
    assert "not a directory" in capsys.readouterr().out


def test_pins_match_survives_yaml_int_coercion():
    # v3.27.0 (vantage-brief-cluster Ask 2): an unquoted all-digit short hash
    # (`source_commit: 2399917`, ~1/16 of hashes) parses as int and false-flagged
    # a healthy import STALE against its own pin. Two consumer domains hit it
    # independently; CI flaked on it when three tests minted one all-digit hash.
    from markdownllm.imports_check import _pins_match
    assert _pins_match(2399917, "2399917")          # the felt case: int vs str
    assert _pins_match("2399917", 2399917)          # either side may coerce
    assert _pins_match("abc1234", "abc1234")
    assert _pins_match(" abc1234 ", "abc1234")      # whitespace never a difference
    assert not _pins_match("abc1234", "abc1235")
    assert not _pins_match(None, "abc1234")         # absence is never a match
    assert not _pins_match(2399917, None)


def test_imports_check_summary_states_coverage(tmp_path, capsys):
    # "26 import(s); 0 stale." over zero possible comparisons is the count of
    # comparisons never made rendered as assurance (estate audit FW-2). The
    # summary must state coverage, and zero coverage must say so in words.
    con = tmp_path / "condom"
    con.mkdir()
    for i in (1, 2):
        write(con, f"things/imp{i}.md", thing_text(
            f"id: imp-{i}\ntype: external-spec\nstatus: ingested\n"
            f"created: 2026-06-02\norigin: external\nverified: false",
            "# Import\n\nNo triple.\n"))
    mdllm.cmd_imports_check(_ns(path=str(con)))
    out = capsys.readouterr().out
    assert "0 stale, 0 diverged, 0 fresh" in out
    assert "2 could not be checked" in out
    assert "COVERAGE: 0/2" in out
    assert "asserts nothing about freshness" in out


def test_mcp_serve_stdio_roundtrip(tmp_path):
    # End-to-end transport: drive the real stdio JSON-RPC loop as a subprocess.
    import json as _json, subprocess as _sp
    _mcp_domain(tmp_path)
    msgs = "\n".join(_json.dumps(m) for m in [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "get_deliverable", "arguments": {"id": "rent-statement-2026"}}},
    ]) + "\n"
    out = _sp.run([sys.executable, str(Path(mdllm.__file__)), "mcp-serve", str(tmp_path)],
                  input=msgs, capture_output=True, text=True, timeout=30).stdout
    by_id = {r.get("id"): r for r in (_json.loads(l) for l in out.splitlines() if l.strip())}
    assert by_id[1]["result"]["serverInfo"]["name"] == "mdllm-domain:" + tmp_path.name
    assert {t["name"] for t in by_id[2]["result"]["tools"]} == {"query_things", "get_deliverable"}
    payload = _json.loads(by_id[3]["result"]["content"][0]["text"])
    assert payload["reference_triple"]["source_id"] == "rent-statement-2026"


# ------------------------------------- mcp-serve --http (Phase 5 transport leg)


def _http_face(root, domain_id=None):
    # Run the Streamable HTTP porch on an ephemeral loopback port; the caller
    # gets (server, endpoint) and owns shutdown.
    import threading
    server = mdllm.mcp_http_server(root, domain_id or root.name, "127.0.0.1", 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/mcp"


def _http_post(endpoint, msg, headers=None):
    import json as _json, urllib.request
    req = urllib.request.Request(
        endpoint, data=_json.dumps(msg).encode(), method="POST",
        headers={"Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode()
            return r.status, (_json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        return e.code, None


def test_mcp_serve_http_roundtrip(tmp_path):
    # The transport swap the stdio loop promised: same dispatcher, same face,
    # different pipe. JSON-RPC over POST /mcp, responses as application/json.
    import json as _json
    _mcp_domain(tmp_path)
    server, endpoint = _http_face(tmp_path)
    try:
        code, init = _http_post(endpoint, {"jsonrpc": "2.0", "id": 1,
                                           "method": "initialize", "params": {}})
        assert code == 200
        assert init["result"]["serverInfo"]["name"] == "mdllm-domain:" + tmp_path.name
        # a notification is accepted with 202 and no body
        code, body = _http_post(endpoint, {"jsonrpc": "2.0",
                                           "method": "notifications/initialized"})
        assert code == 202 and body is None
        # the face is identical to stdio's: manifest + provenance-stamped fetch
        code, man = _http_post(endpoint, {"jsonrpc": "2.0", "id": 2,
                                          "method": "resources/read",
                                          "params": {"uri": f"manifest://{tmp_path.name}"}})
        assert code == 200
        man_doc = _json.loads(man["result"]["contents"][0]["text"])
        assert [k["id"] for k in man_doc["knows"]] == ["rent-statement-2026"]
        code, d = _http_post(endpoint, {"jsonrpc": "2.0", "id": 3,
                                        "method": "tools/call",
                                        "params": {"name": "get_deliverable",
                                                   "arguments": {"id": "rent-statement-2026"}}})
        payload = _json.loads(d["result"]["content"][0]["text"])
        assert payload["reference_triple"]["source_id"] == "rent-statement-2026"
        # the membrane holds across this pipe too
        code, miss = _http_post(endpoint, {"jsonrpc": "2.0", "id": 4,
                                           "method": "resources/read",
                                           "params": {"uri": f"thing://{tmp_path.name}/internal-note"}})
        assert code == 200 and "error" in miss
    finally:
        server.shutdown(); server.server_close()


def test_mcp_serve_http_guards(tmp_path):
    # DNS-rebinding defence: browser-borne (Origin-carrying) requests must be
    # loopback-origin; GET has no stream to offer; the endpoint is /mcp.
    import urllib.request
    _mcp_domain(tmp_path)
    server, endpoint = _http_face(tmp_path)
    try:
        code, _ = _http_post(endpoint, {"jsonrpc": "2.0", "id": 1,
                                        "method": "initialize", "params": {}},
                             headers={"Origin": "http://evil.example"})
        assert code == 403
        code, _ = _http_post(endpoint, {"jsonrpc": "2.0", "id": 1,
                                        "method": "initialize", "params": {}},
                             headers={"Origin": "http://localhost:3000"})
        assert code == 200
        try:
            with urllib.request.urlopen(endpoint, timeout=10) as r:
                code = r.status
        except urllib.error.HTTPError as e:
            code = e.code
        assert code == 405
        code, _ = _http_post(endpoint.replace("/mcp", "/nope"),
                             {"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        assert code == 404
    finally:
        server.shutdown(); server.server_close()


def test_mcp_serve_http_rescans_per_request(tmp_path):
    # Stateless server, git is the state: a long-lived HTTP porch must serve
    # the repo as it stands, not as it stood at bind time.
    _mcp_domain(tmp_path)
    server, endpoint = _http_face(tmp_path)
    try:
        uri = f"thing://{tmp_path.name}/rent-statement-2026"
        _, r1 = _http_post(endpoint, {"jsonrpc": "2.0", "id": 1,
                                      "method": "resources/read", "params": {"uri": uri}})
        assert "12000" in r1["result"]["contents"][0]["text"]
        write(tmp_path, "things/income/rent.md", thing_text(
            "id: rent-statement-2026\ntype: deliverable\nstatus: completed\n"
            "created: 2026-06-01\nexposed: true",
            "# Rent Statement 2026\n\nTotal income: 99999 REVISED.\n"))
        _, r2 = _http_post(endpoint, {"jsonrpc": "2.0", "id": 2,
                                      "method": "resources/read", "params": {"uri": uri}})
        assert "99999 REVISED" in r2["result"]["contents"][0]["text"]
    finally:
        server.shutdown(); server.server_close()


def test_mcp_http_loopback_only():
    # The refusal is the control: no routable bind until the OAuth 2.1 leg.
    assert mdllm.mcp_host_is_loopback("127.0.0.1")
    assert mdllm.mcp_host_is_loopback("localhost")
    assert mdllm.mcp_host_is_loopback("::1")
    assert mdllm.mcp_host_is_loopback("127.0.0.53")
    assert not mdllm.mcp_host_is_loopback("0.0.0.0")
    assert not mdllm.mcp_host_is_loopback("192.168.1.10")
    assert not mdllm.mcp_host_is_loopback("example.com")
    assert not mdllm.mcp_host_is_loopback("")


def test_imports_freshness_over_http(tmp_path):
    # Domain-to-domain over the wire: the consumer's address book carries a
    # `url` entry; the whole fresh -> stale membrane read works unchanged.
    import subprocess as sp
    src = tmp_path / "srcdom"
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
        "# The Spec\n\nv1.\n"))
    sp.run(["git", "init", "-q"], cwd=src, check=True)
    _git_commit(src, "create spec")
    pin = _git_short(src)

    server, endpoint = _http_face(src, "srcdom")
    try:
        con = tmp_path / "condom"
        con.mkdir()
        _consumer_with_import(con, "srcdom", "the-spec", pin,
                              {"url": endpoint}, body="# The Spec\n\nv1.\n")
        rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
        assert rows["imported-spec"]["state"] == "fresh"

        write(src, "things/spec.md", thing_text(
            "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
            "# The Spec\n\nv2 CHANGED.\n"))
        _git_commit(src, "revise spec")
        rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
        assert rows["imported-spec"]["state"] == "stale"
        assert rows["imported-spec"]["species"] == "content changed"

        # face coverage reads the manifest through the same url entry
        cov = {c["source"]: c for c in mdllm.face_coverage(con)}
        assert cov["srcdom"]["state"] == "ok" and cov["srcdom"]["offered"] == 1
    finally:
        server.shutdown(); server.server_close()


def test_mcp_serve_http_token_gate(tmp_path):
    # The probe control: with a token set, possession is the authorization —
    # no header 401, wrong token 401, right token 200. Per-run by design.
    import threading
    _mcp_domain(tmp_path)
    server = mdllm.mcp_http_server(tmp_path, tmp_path.name, "127.0.0.1", 0,
                                   token="probe-secret")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    endpoint = f"http://127.0.0.1:{server.server_address[1]}/mcp"
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    try:
        code, _ = _http_post(endpoint, init)
        assert code == 401
        code, _ = _http_post(endpoint, init,
                             headers={"Authorization": "Bearer wrong"})
        assert code == 401
        code, body = _http_post(endpoint, init,
                                headers={"Authorization": "Bearer probe-secret"})
        assert code == 200 and "result" in body
    finally:
        server.shutdown(); server.server_close()


def test_imports_freshness_over_http_with_token(tmp_path):
    # The full probe shape: a token-gated porch read through a url entry whose
    # `headers` carry the bearer token (the .mcp.json convention).
    import subprocess as sp, threading
    src = tmp_path / "srcdom"
    write(src, "things/spec.md", thing_text(
        "id: the-spec\ntype: deliverable\nstatus: approved\ncreated: 2026-06-01\nexposed: true",
        "# The Spec\n\nv1.\n"))
    sp.run(["git", "init", "-q"], cwd=src, check=True)
    _git_commit(src, "create spec")
    pin = _git_short(src)

    server = mdllm.mcp_http_server(src, "srcdom", "127.0.0.1", 0, token="probe-secret")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    endpoint = f"http://127.0.0.1:{server.server_address[1]}/mcp"
    try:
        con = tmp_path / "condom"
        con.mkdir()
        _consumer_with_import(con, "srcdom", "the-spec", pin,
                              {"url": endpoint,
                               "headers": {"Authorization": "Bearer probe-secret"}},
                              body="# The Spec\n\nv1.\n")
        rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
        assert rows["imported-spec"]["state"] == "fresh"
        # without the token the read is refused -> honest "unreachable"
        _consumer_with_import(con, "srcdom", "the-spec", pin,
                              {"url": endpoint}, body="# The Spec\n\nv1.\n")
        rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
        assert rows["imported-spec"]["state"] == "unreachable"
    finally:
        server.shutdown(); server.server_close()


def test_imports_freshness_http_unreachable_is_unknown(tmp_path):
    # A dead endpoint is "sync state unknown" — never a silent fresh.
    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", "abc1234",
                          {"url": "http://127.0.0.1:9/mcp"})  # port 9: discard
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "unreachable"


# ------------------------------------------------- quarantine flip discipline
# (verified-flip-enforcement plan: the verified flip is an auditable event —
# born-verified and attribution are procedure checks keyed to git, never a
# truth claim about whether the human review was real.)


EXT_UNVERIFIED = f"""id: ext-doc
type: reference
status: not-started
created: {RECENT}
origin: external
verified: false
"""

EXT_VERIFIED_ATTRIBUTED = f"""id: ext-doc
type: reference
status: not-started
created: {RECENT}
origin: external
verified: true
verified_by: A Human
"""

EXT_VERIFIED_ANON = f"""id: ext-doc
type: reference
status: not-started
created: {RECENT}
origin: external
verified: true
"""


def _quarantine(root):
    corpus, _ = mdllm.scan(root)
    return mdllm.quarantine_findings(root, corpus)


def test_quarantine_born_verified_fires(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ATTRIBUTED))
    _git_commit(tmp_path, "import: ext-doc, already flipped")
    msgs = [f.message for f in _quarantine(tmp_path)]
    assert any("born `verified: true`" in m for m in msgs)
    assert all(f.severity == mdllm.SEV_WARNING for f in _quarantine(tmp_path))


def test_quarantine_two_commit_flip_is_clean(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_UNVERIFIED))
    _git_commit(tmp_path, "import: ext-doc (quarantined)")
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ATTRIBUTED))
    _git_commit(tmp_path, "verify: ext-doc (A Human)")
    assert _quarantine(tmp_path) == []


def test_quarantine_heal_by_reverification(tmp_path):
    # A historical born-verified finding disappears once the thing is
    # re-quarantined and re-flipped in a separate attributed commit.
    _git_repo(tmp_path)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ANON))
    _git_commit(tmp_path, "import: born verified (the sin)")
    assert any("born" in f.message for f in _quarantine(tmp_path))
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_UNVERIFIED))
    _git_commit(tmp_path, "re-quarantine: ext-doc")
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ATTRIBUTED))
    _git_commit(tmp_path, "verify: ext-doc (A Human)")
    assert _quarantine(tmp_path) == []


def test_quarantine_attribution_missing(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_UNVERIFIED))
    _git_commit(tmp_path, "import")
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ANON))
    _git_commit(tmp_path, "verify without attribution")
    msgs = [f.message for f in _quarantine(tmp_path)]
    assert len(msgs) == 1 and "verified_by" in msgs[0]


def test_quarantine_strict_escalates_to_error(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "_schema.yaml",
          "schema_version: 1\ndomain: t\noptions:\n  quarantine: strict\n")
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ANON))
    _git_commit(tmp_path, "import: born verified, anonymous")
    sevs = {f.severity for f in _quarantine(tmp_path)}
    assert sevs == {mdllm.SEV_ERROR}


def test_quarantine_uncommitted_new_file_is_boundary_case(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "base")
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ATTRIBUTED))
    msgs = [f.message for f in _quarantine(tmp_path)]
    assert any("about to be born" in m for m in msgs)


def test_quarantine_pending_flip_of_committed_thing_is_clean(tmp_path):
    # HEAD holds verified: false; the working tree flips it — a distinct
    # commit from creation by construction, so born-verified must not fire.
    _git_repo(tmp_path)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_UNVERIFIED))
    _git_commit(tmp_path, "import")
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ATTRIBUTED))
    assert _quarantine(tmp_path) == []


def test_quarantine_ignores_non_external_and_unverified(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/own.md", thing_text(
        "id: own\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"
        "verified: true\n"))  # not origin: external — out of scope
    # RECENT, not a literal: an external thing older than 30 days legitimately
    # earns the quarantine-age Info, which is a different check from the ones
    # under test here.
    write(tmp_path, "things/ext.md", thing_text(
        f"id: ext\ntype: note\nstatus: not-started\ncreated: {RECENT}\n"
        "origin: external\nverified: false\n"))  # still quarantined — fine
    _git_commit(tmp_path, "seed")
    assert _quarantine(tmp_path) == []


def test_session_start_surfaces_verified_flips(tmp_path, capsys):
    _git_repo(tmp_path)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_UNVERIFIED))
    _git_commit(tmp_path, "import: ext-doc (quarantined)")
    import subprocess as sp
    sp.run(["git", "commit", "-q", "--allow-empty", "-m",
            "session-end: previous session closes"], cwd=tmp_path, check=True)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_VERIFIED_ATTRIBUTED))
    _git_commit(tmp_path, "verify: ext-doc (A Human)")
    import argparse
    mdllm.cmd_session_start(argparse.Namespace(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert "Verified flips since last session (1)" in out
    assert "`ext-doc`" in out and "verified_by: A Human" in out


def test_session_start_quiet_without_flips(tmp_path, capsys):
    _git_repo(tmp_path)
    write(tmp_path, "things/ext-doc.md", thing_text(EXT_UNVERIFIED))
    _git_commit(tmp_path, "import: ext-doc (still quarantined)")
    import argparse
    mdllm.cmd_session_start(argparse.Namespace(path=str(tmp_path)))
    assert "Verified flips" not in capsys.readouterr().out


# ------------------------------------------- schema-declared terminal statuses


def _terminal_corpus(tmp_path, type_block: str, status: str):
    """One thing of type `doc`, with the domain's type declaration supplied."""
    write(tmp_path, "_schema.yaml",
          "schema_version: 1\ndomain: t\ntypes:\n" + type_block)
    write(tmp_path, "things/d.md", thing_text(
        f"id: d\ntype: doc\nstatus: {status}\ncreated: 2026-06-01"))
    corpus, _ = scan(tmp_path)
    return corpus


def test_terminal_defaults_to_universal_set_when_undeclared():
    # A domain that declares nothing behaves exactly as it did before the
    # per-type field existed — this is the no-regression pin.
    assert mdllm.terminal_statuses_for(None, "anything") == mdllm.TERMINAL_STATUSES
    assert mdllm.terminal_statuses_for({"types": {"doc": {}}}, "doc") == mdllm.TERMINAL_STATUSES
    assert mdllm.is_terminal(None, {"type": "doc", "status": "completed"}) is True
    assert mdllm.is_terminal(None, {"type": "doc", "status": "approved-current"}) is False


def test_terminal_declaration_replaces_rather_than_extends(tmp_path):
    # `completed` is universally terminal, but this type never declared it —
    # the declaration is authoritative, so it must NOT leak back in.
    schema = {"types": {"doc": {"statuses": ["draft", "approved-current", "retired"],
                                "terminal_statuses": ["approved-current", "retired"]}}}
    assert mdllm.terminal_statuses_for(schema, "doc") == {"approved-current", "retired"}
    assert mdllm.is_terminal(schema, {"type": "doc", "status": "approved-current"}) is True
    assert mdllm.is_terminal(schema, {"type": "doc", "status": "draft"}) is False
    assert mdllm.is_terminal(schema, {"type": "doc", "status": "completed"}) is False


def test_terminal_declaration_ignores_values_outside_the_vocabulary(tmp_path):
    schema = {"types": {"doc": {"statuses": ["draft", "retired"],
                                "terminal_statuses": ["retired", "typo-status"]}}}
    assert mdllm.terminal_statuses_for(schema, "doc") == {"retired"}


def test_terminal_declaration_outside_vocabulary_is_reported(tmp_path):
    corpus = _terminal_corpus(
        tmp_path,
        "  doc:\n    statuses: [draft, retired]\n    terminal_statuses: [retired, nope]\n",
        "draft")
    msgs = messages(mdllm.validate_level3(corpus), mdllm.SEV_WARNING)
    assert any("terminal_statuses" in m and "nope" in m for m in msgs)


def test_reserved_types_carry_tool_owned_terminal_statuses():
    # A domain cannot redeclare a reserved type, so the tool owns which of its
    # statuses mean settled — otherwise a `stable` skill counts as open work.
    assert mdllm.terminal_statuses_for(None, "skill") == {"stable", "deprecated"}
    assert mdllm.is_terminal(None, {"type": "skill", "status": "stable"}) is True
    assert mdllm.is_terminal(None, {"type": "skill", "status": "draft"}) is False
    assert mdllm.is_terminal(None, {"type": "conflict", "status": "resolved"}) is True
    assert mdllm.is_terminal(None, {"type": "conflict", "status": "open"}) is False


def test_reserved_type_terminal_declaration_is_ignored_and_reported(tmp_path):
    write(tmp_path, "_schema.yaml",
          "schema_version: 1\ndomain: t\ntypes:\n"
          "  skill:\n    terminal_statuses: [draft]\n")
    write(tmp_path, "things/s.md", thing_text(
        "id: s\ntype: skill\nstatus: draft\ncreated: 2026-06-01"))
    corpus, _ = scan(tmp_path)
    # ignored: the tool's own set still governs
    assert mdllm.is_terminal(corpus.schema, {"type": "skill", "status": "draft"}) is False
    msgs = messages(mdllm.validate_level3(corpus), mdllm.SEV_WARNING)
    assert any("framework-reserved" in m for m in msgs)


def test_orientation_open_loops_respect_declared_terminal_statuses(tmp_path):
    # The end-to-end reason this exists: a signed, in-force document is not a
    # loop the next session has to close.
    write(tmp_path, "_schema.yaml",
          "schema_version: 1\ndomain: t\ntypes:\n"
          "  doc:\n    statuses: [draft, approved-current, retired]\n"
          "    terminal_statuses: [approved-current, retired]\n")
    write(tmp_path, "things/live.md", thing_text(
        "id: live\ntype: doc\nstatus: approved-current\ncreated: 2026-06-01"))
    write(tmp_path, "things/wip.md", thing_text(
        "id: wip\ntype: doc\nstatus: draft\ncreated: 2026-06-01"))
    from markdownllm.session import _orient_forward
    lines = "\n".join(_orient_forward(tmp_path))
    assert "Open loops (1)" in lines
    assert "`wip`" in lines and "`live`" not in lines


def test_orientation_watched_is_not_owned(tmp_path):
    # v3.27.0 (vantage-brief-cluster Ask 1): a mirror's status is the source's
    # state restated — not a loop here. The estate measurement: landing 27
    # imports doubled the reported open-loop count with zero new owned work.
    # Exclusion, not hiding: watched things get their own line.
    write(tmp_path, "things/mine.md", thing_text(
        "id: mine\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    write(tmp_path, "things/mirror.md", thing_text(
        "id: mirror\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "origin: external\nverified: false\nsource_domain: srcdom\n"
        "source_id: the-task\nsource_commit: 'abc1234'"))
    from markdownllm.session import _orient_forward
    lines = "\n".join(_orient_forward(tmp_path))
    assert "Open loops (1)" in lines and "`mine`" in lines
    assert "Watched (1)" in lines and "`mirror`" in lines
    # the mirror appears only under Watched, never in the owned listing
    owned_block = lines.split("Watched")[0]
    assert "`mirror`" not in owned_block


def _commit_all(tmp_path, msg):
    import subprocess
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "--no-verify", "-m", msg],
                   cwd=tmp_path, check=True)












# ---------------------------------------------------------------------------
# Disclosure boundary (boundary-disclosure-check plan). The invariant under
# test everywhere: capability without vocabulary — no terms file means silent
# no-op (that IS the CI behaviour), and the terms file itself must never be
# tracked. All fixture terms below are synthetic.


def _boundary_repo(tmp_path, terms="secretco ==> the client\ncodename-x\n"):
    _git_repo(tmp_path)
    (tmp_path / ".gitignore").write_text(".boundary-terms\n", encoding="utf-8")
    (tmp_path / ".boundary-terms").write_text(
        "# synthetic fixture vocabulary\n" + terms, encoding="utf-8")


def test_boundary_noop_without_terms_file(tmp_path, capsys):
    _git_repo(tmp_path)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, quiet=False))
    assert rc == 0 and "skipped" in capsys.readouterr().out


def test_boundary_staged_addition_blocks_and_suggests(tmp_path, capsys):
    import subprocess
    _boundary_repo(tmp_path)
    (tmp_path / "doc.md").write_text("work for SecretCo this week\n",
                                     encoding="utf-8")
    subprocess.run(["git", "add", "doc.md"], cwd=tmp_path, check=True)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, quiet=True))
    out = capsys.readouterr().out
    assert rc == 1 and "BLOCKED" in out and "the client" in out


def test_boundary_staged_clean_passes(tmp_path, capsys):
    import subprocess
    _boundary_repo(tmp_path)
    (tmp_path / "doc.md").write_text("work for the client this week\n",
                                     encoding="utf-8")
    subprocess.run(["git", "add", "doc.md"], cwd=tmp_path, check=True)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, quiet=True))
    assert rc == 0


def test_boundary_filename_match_blocks(tmp_path, capsys):
    import subprocess
    _boundary_repo(tmp_path)
    (tmp_path / "codename-x-notes.md").write_text("clean body\n",
                                                  encoding="utf-8")
    subprocess.run(["git", "add", "codename-x-notes.md"], cwd=tmp_path,
                   check=True)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, quiet=True))
    assert rc == 1 and "filename" in capsys.readouterr().out


def test_boundary_message_mode(tmp_path, capsys):
    _boundary_repo(tmp_path)
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text("fix: adjust CODENAME-X rollout\n", encoding="utf-8")
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=str(msg),
                                history=False, quiet=True))
    assert rc == 1 and "commit message" in capsys.readouterr().out
    msg.write_text("fix: adjust rollout\n", encoding="utf-8")
    assert mdllm.cmd_boundary(_ns(path=str(tmp_path), message=str(msg),
                                  history=False, quiet=True)) == 0


def test_boundary_self_guard_blocks_tracked_terms_file(tmp_path, capsys):
    import subprocess
    _boundary_repo(tmp_path)
    subprocess.run(["git", "add", "-f", ".boundary-terms"], cwd=tmp_path,
                   check=True)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, quiet=True))
    assert rc == 1 and "TRACKED" in capsys.readouterr().out


def test_boundary_history_audit(tmp_path, capsys):
    import subprocess
    _boundary_repo(tmp_path)
    (tmp_path / "old.md").write_text("SecretCo deliverable\n", encoding="utf-8")
    subprocess.run(["git", "add", "old.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "notes on codename-x"],
                   cwd=tmp_path, check=True)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=True, quiet=True))
    out = capsys.readouterr().out
    assert rc == 1
    assert "commit " in out          # the message hit
    assert "rev:path" in out          # the blob hit


def test_boundary_parse_comments_and_blanks(tmp_path):
    _boundary_repo(tmp_path, terms="\n# comment only\nplain-term\n"
                                   "spaced ==> replacement here\n")
    terms = mdllm.load_terms(tmp_path)
    assert ("plain-term", None) in terms
    assert ("spaced", "replacement here") in terms
    assert len(terms) == 2


def test_boundary_audit_terms_flags_entry_in_tracked_content(tmp_path, capsys):
    # A term present in the repo's OWN tracked content is not a private
    # identifier: either noise (which keeps the other legs permanently red) or
    # a leak already committed. Both actionable — hence a check, not a warning.
    import subprocess
    _boundary_repo(tmp_path)
    (tmp_path / "fixture.md").write_text("mentions codename-x inline\n",
                                         encoding="utf-8")
    subprocess.run(["git", "add", "fixture.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add fixture"],
                   cwd=tmp_path, check=True)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, audit_terms=True, quiet=True))
    out = capsys.readouterr().out
    assert rc == 1
    assert ".boundary-terms:3" in out       # comment line 1, secretco 2, codename-x 3
    assert "fixture.md" in out


def test_boundary_audit_terms_never_prints_the_term(tmp_path, capsys):
    # The invariant that shapes this leg. The staged and message legs print a
    # term because they are refusing a specific edit; this leg reports a word
    # that is ALREADY in tracked content, so naming it adds exposure without
    # adding information the operator cannot get from the line number.
    import subprocess
    _boundary_repo(tmp_path)
    (tmp_path / "fixture.md").write_text("mentions codename-x inline\n",
                                         encoding="utf-8")
    subprocess.run(["git", "add", "fixture.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add fixture"],
                   cwd=tmp_path, check=True)
    mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None, history=False,
                           audit_terms=True, quiet=True))
    out = capsys.readouterr().out
    assert "codename-x" not in out.lower()
    assert "secretco" not in out.lower()


def test_boundary_audit_terms_clean_when_nothing_tracked(tmp_path, capsys):
    import subprocess
    _boundary_repo(tmp_path)
    (tmp_path / "fixture.md").write_text("nothing sensitive here\n",
                                         encoding="utf-8")
    subprocess.run(["git", "add", "fixture.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add fixture"],
                   cwd=tmp_path, check=True)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, audit_terms=True, quiet=False))
    out = capsys.readouterr().out
    assert rc == 0 and "terms file clean" in out


def test_boundary_audit_terms_noops_without_terms_file(tmp_path, capsys):
    _git_repo(tmp_path)
    rc = mdllm.cmd_boundary(_ns(path=str(tmp_path), message=None,
                                history=False, audit_terms=True, quiet=False))
    assert rc == 0 and "skipped" in capsys.readouterr().out


def test_located_terms_carry_their_line_numbers(tmp_path):
    _boundary_repo(tmp_path, terms="\n# comment only\nplain-term\n"
                                   "spaced ==> replacement here\n")
    located = mdllm.load_located_terms(tmp_path)
    assert (4, "plain-term", None) in located
    assert (5, "spaced", "replacement here") in located
    # and the flat loader still returns exactly what every other leg expects
    assert mdllm.load_terms(tmp_path) == [("plain-term", None),
                                          ("spaced", "replacement here")]


def test_install_hook_writes_commit_msg_hook(tmp_path):
    _git_repo(tmp_path)
    mdllm.cmd_install_hook(_ns(path=str(tmp_path)))
    msg_hook = tmp_path / ".git" / "hooks" / "commit-msg"
    assert msg_hook.is_file()
    body = msg_hook.read_text(encoding="utf-8")
    assert "boundary" in body and '--message "$1"' in body


# ---------------------------------------------------------------------------
# Floor presence at orientation. The real case: git hooks live in .git/hooks,
# which is never cloned — a re-cloned domain silently loses its git-fs anchor
# and orients clean. session-start surfaces it; doctor keeps the deep probe.


def test_session_start_flags_missing_floor(tmp_path):
    from markdownllm.session import _floor_status
    _git_repo(tmp_path)
    line = _floor_status(tmp_path)
    assert line and "NOT INSTALLED" in line and "install-hook" in line


def test_session_start_quiet_when_floor_installed(tmp_path):
    from markdownllm.session import _floor_status
    _git_repo(tmp_path)
    mdllm.cmd_install_hook(_ns(path=str(tmp_path)))
    assert _floor_status(tmp_path) is None


def test_session_start_flags_stale_hook_body(tmp_path):
    from markdownllm.session import _floor_status
    _git_repo(tmp_path)
    mdllm.cmd_install_hook(_ns(path=str(tmp_path)))
    hook = tmp_path / ".git" / "hooks" / "pre-commit"
    hook.write_text(hook.read_text(encoding="utf-8") + "# older body\n",
                    encoding="utf-8", newline="\n")
    line = _floor_status(tmp_path)
    assert line and "STALE" in line and "pre-commit" in line


def test_session_start_floor_check_skips_non_repo(tmp_path):
    from markdownllm.session import _floor_status
    assert _floor_status(tmp_path) is None


# ---------------------------------------------------------------------------
# candidates (touchpoints.py) — the cue question made mechanical:
# additions/modifications/deletions/renames get truthful cues; exposed publishes
# (estate-cadence-cluster Phase 4; inflection-candidates-are-computable)
# ---------------------------------------------------------------------------

def _seed_candidates_repo(tmp_path):
    root = tmp_path / "dom"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    (root / "things" / "spine.md").write_text(
        "---\nid: spine\ntype: note\nstatus: active\ncreated: 2026-08-01\n---\n# S\n",
        encoding="utf-8")
    for i in range(3):
        (root / "things" / f"leaf{i}.md").write_text(
            "---\nid: leaf%d\ntype: note\nstatus: active\ncreated: 2026-08-01\n"
            "linked_things:\n  - id: spine\n    relation: references\n---\n# L\n" % i,
            encoding="utf-8")
    (root / "things" / "porch.md").write_text(
        "---\nid: porch-thing\ntype: note\nstatus: active\ncreated: 2026-08-01\n"
        "exposed: true\n---\n# P\n", encoding="utf-8")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "seed")
    return root


def _run_candidates(root, capsys):
    from markdownllm.touchpoints import cmd_candidates
    import argparse
    rc = cmd_candidates(argparse.Namespace(path=str(root)))
    return rc, capsys.readouterr().out


def test_candidates_modified_reasoned_from_thing_advises(tmp_path, capsys):
    root = _seed_candidates_repo(tmp_path)
    p = root / "things" / "spine.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nrevised\n", encoding="utf-8")
    _sync_git(root, "add", "-A")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0
    assert "cue: `spine`" in out and "3 inbound" in out and "touchpoints spine" in out


def test_candidates_added_thing_asks_duplicate_and_contradiction_question(tmp_path, capsys):
    root = _seed_candidates_repo(tmp_path)
    (root / "things" / "fresh.md").write_text(
        "---\nid: fresh\ntype: specification\nstatus: draft\ncreated: 2026-08-04\n---\n# F\n",
        encoding="utf-8")
    _sync_git(root, "add", "-A")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0
    assert "cue: `fresh` is new" in out
    assert "duplicate ownership" in out and "latent contradiction" in out


def test_candidates_deleted_thing_routes_removal_and_withdrawal(tmp_path, capsys):
    root = _seed_candidates_repo(tmp_path)
    (root / "things" / "porch.md").unlink()
    _sync_git(root, "add", "-A")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0
    assert "`porch-thing` is deleted" in out
    assert "withdraws it from consumers" in out


def test_candidates_rename_names_path_consumers(tmp_path, capsys):
    root = _seed_candidates_repo(tmp_path)
    _sync_git(root, "mv", "things/spine.md", "things/backbone.md")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0
    assert "moved `things/spine.md` -> `things/backbone.md`" in out
    assert "literal/path consumers" in out


def test_candidates_modified_leaf_is_silent(tmp_path, capsys):
    root = _seed_candidates_repo(tmp_path)
    p = root / "things" / "leaf0.md"
    p.write_text(p.read_text(encoding="utf-8") + "\ntweak\n", encoding="utf-8")
    _sync_git(root, "add", "-A")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0 and out == ""  # leaf has no inbound edges; below threshold


def test_candidates_modified_exposed_thing_says_it_publishes(tmp_path, capsys):
    root = _seed_candidates_repo(tmp_path)
    p = root / "things" / "porch.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nedit\n", encoding="utf-8")
    _sync_git(root, "add", "-A")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0
    assert "porch: `porch-thing` is exposed" in out and "publishes" in out


def test_candidates_definition_surface_advises_regardless_of_fanin(tmp_path, capsys):
    root = _seed_candidates_repo(tmp_path)
    skill = root / "things" / "askill.md"
    skill.write_text(
        "---\nid: a-skill\ntype: skill\nstatus: draft\ncreated: 2026-08-01\n---\n# K\n",
        encoding="utf-8")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "add skill")
    skill.write_text(skill.read_text(encoding="utf-8") + "\nrevised\n", encoding="utf-8")
    _sync_git(root, "add", "-A")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0
    assert "cue: `a-skill`" in out and "definition surface" in out


def test_candidates_modified_insight_advises_with_zero_fanin(tmp_path, capsys):
    # v3.26.1 membership fix: an insight exists only to be reasoned from, so a
    # modified insight cues with NO fan-in requirement (the felt gap: porch-bound
    # insights edited with no cue). Same contract for `decision`.
    root = _seed_candidates_repo(tmp_path)
    for tid, typ in (("a-lesson", "insight"), ("a-ruling", "decision")):
        f = root / "things" / f"{tid}.md"
        f.write_text(
            "---\nid: %s\ntype: %s\nstatus: active\ncreated: 2026-08-01\n---\n# T\n"
            % (tid, typ), encoding="utf-8")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "add insight + decision")
    for tid in ("a-lesson", "a-ruling"):
        f = root / "things" / f"{tid}.md"
        f.write_text(f.read_text(encoding="utf-8") + "\nrevised\n", encoding="utf-8")
    _sync_git(root, "add", "-A")
    rc, out = _run_candidates(root, capsys)
    assert rc == 0
    assert "cue: `a-lesson`" in out and "definition surface" in out
    assert "cue: `a-ruling`" in out


def test_install_hook_writes_post_commit_leg(tmp_path):
    from markdownllm.scaffold import install_hook
    root = tmp_path / "r"
    root.mkdir()
    _sync_git(root, "init", "-q")
    install_hook(root)
    post = root / ".git" / "hooks" / "post-commit"
    assert post.is_file()
    body = post.read_text(encoding="utf-8")
    assert "autopush" in body and "exit 0" in body
    assert "--force" not in body  # structurally outside the vocabulary


# ---------------------------------------------------------------------------
# retrospective-cadence surfacing (session.py / triggers.py) — the v3.24.0
# sensor gains the moment (session start) and the altitude (estate roll-up)
# where it can be acted on (estate-cadence-cluster Phase 2)
# ---------------------------------------------------------------------------

def _dated_git(cwd, date, *args):
    import os
    import subprocess
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = date
    env["GIT_AUTHOR_DATE"] = date
    return subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                           *args], cwd=cwd, env=env, capture_output=True, text=True)


def _seed_overdue_domain(root):
    """A domain born 100 days ago, active this week, no retrospective ever."""
    import datetime as dt
    (root / "things").mkdir(parents=True, exist_ok=True)
    _sync_git(root, "init", "-q")
    old = (dt.date.today() - dt.timedelta(days=100)).isoformat() + "T12:00:00"
    (root / "things" / "seed.md").write_text(
        "---\nid: seed\ntype: note\nstatus: active\ncreated: 2026-04-01\n---\n# S\n",
        encoding="utf-8")
    _dated_git(root, old, "add", "-A")
    _dated_git(root, old, "commit", "-q", "-m", "born")
    (root / "things" / "recent.md").write_text(
        "---\nid: recent\ntype: note\nstatus: active\ncreated: 2026-08-01\n---\n# R\n",
        encoding="utf-8")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "recent work")
    return root


def test_session_start_surfaces_retrospective_debt(tmp_path, capsys):
    from markdownllm.session import cmd_session_start
    import argparse
    root = _seed_overdue_domain(tmp_path / "dom")
    cmd_session_start(argparse.Namespace(path=str(root)))
    out = capsys.readouterr().out
    assert "Retrospective cadence" in out
    assert "no retrospective has ever been written" in out


def test_session_start_cadence_quiet_for_young_domain(tmp_path, capsys):
    from markdownllm.session import cmd_session_start
    import argparse
    root = tmp_path / "young"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    (root / "things" / "seed.md").write_text(
        "---\nid: seed\ntype: note\nstatus: active\ncreated: 2026-08-01\n---\n# S\n",
        encoding="utf-8")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "born recently")
    cmd_session_start(argparse.Namespace(path=str(root)))
    out = capsys.readouterr().out
    # Quiet when healthy — the formatted finding line specifically: the
    # emitted kernel's own text mentions the phrase, so the assert targets
    # the digest line, not the whole output.
    assert "- **Retrospective cadence:**" not in out


def test_estate_sweep_rolls_up_retrospective_debt(tmp_path, capsys):
    from markdownllm.triggers import cmd_triggers
    import argparse
    estate = tmp_path / "estate"
    estate.mkdir()
    _sync_git(estate, "init", "-q")
    (estate / "x.txt").write_text("root\n", encoding="utf-8")
    _sync_git(estate, "add", "-A")
    _sync_git(estate, "commit", "-q", "-m", "root")
    (estate / "domain").mkdir()
    _seed_overdue_domain(estate / "domain" / "overdue")
    cmd_triggers(argparse.Namespace(path=str(estate), estate=True))
    out = capsys.readouterr().out
    assert "RETROSPECTIVE DEBT" in out
    assert "1 domain(s) owe a retrospective" in out


# ------------------------------------------ substrate-totality-residue regressions
# Each of these pins a branch where the floor rendered a state it could not
# look at as a definite answer. If a fix reverts, the confident-wrong answer
# returns and the matching test fails (things/plans/substrate-totality-residue.md).


def test_import_trigger_unreachable_route_is_unevaluable_not_notfired(
        tmp_path, capsys):
    # #1, proved on contact: a genuinely unspawnable route must land in "not
    # mechanically evaluable", never in a confident not-fired ("no watched
    # import state matches") — the sibling porch branch already said so.
    from markdownllm.triggers import TriggerOutcome, evaluate_typed
    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", "deadbee",
        {"command": "this-binary-does-not-exist-xyz",
         "args": ["mcp-serve", "/nope"]})
    write(con, "things/watcher.md", thing_text(
        "id: watcher\ntype: note\nstatus: in-progress\ncreated: 2026-06-01\n"
        "triggers:\n  - type: import\n    condition: state_is\n"
        "    watch: [imported-spec]\n    action: re_evaluate"))
    # Same fixture, imports report: the row is non-`fresh` (done-when bullet 3).
    rows = {r["id"]: r for r in mdllm.imports_freshness(con)}
    assert rows["imported-spec"]["state"] == "unreachable"
    res = [r for r in evaluate_typed(con).results if r.thing_id == "watcher"]
    assert res and res[0].outcome is TriggerOutcome.UNEVALUABLE
    rc = mdllm.cmd_triggers(_ns(path=str(con)))
    out = capsys.readouterr().out
    assert rc == 0
    assert "No trigger conditions currently true." in out
    assert "left unevaluable" in out and "unreachable" in out


def test_import_trigger_watching_for_unreachable_still_fires(tmp_path, capsys):
    # The care in the fix: unavailability the trigger explicitly watches FOR
    # stays a match candidate — only the unasked-for case degrades.
    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", "deadbee",
        {"command": "this-binary-does-not-exist-xyz",
         "args": ["mcp-serve", "/nope"]})
    write(con, "things/watcher.md", thing_text(
        "id: watcher\ntype: note\nstatus: in-progress\ncreated: 2026-06-01\n"
        "triggers:\n  - type: import\n    condition: state_is\n"
        "    watch: [imported-spec]\n    value: [unreachable]\n"
        "    action: escalate"))
    rc = mdllm.cmd_triggers(_ns(path=str(con)))
    out = capsys.readouterr().out
    assert rc == 0
    assert "watcher: import `imported-spec` is unreachable" in out


def test_imports_freshness_pin_current_unread_content_is_not_fresh(
        tmp_path, monkeypatch):
    # #2: pin current but the face returned no content for the thing — the
    # divergence direction was unverifiable, so `fresh` would assert a
    # comparison that never happened.
    import json
    import markdownllm.imports_check as ic
    con = tmp_path / "condom"
    con.mkdir()
    _consumer_with_import(con, "srcdom", "the-spec", "deadbee",
        {"command": sys.executable, "args": ["-c", "pass"]})
    man = json.dumps({"knows": [{"id": "the-spec", "source_commit": "deadbee"}]})
    monkeypatch.setattr(
        ic, "_mcp_face_read",
        lambda cfg, cwd, uris, server, **kw: ("ok", {"manifest://srcdom": man}))
    rows = {r["id"]: r for r in ic.imports_freshness(con)}
    assert rows["imported-spec"]["state"] != "fresh"
    assert rows["imported-spec"]["state"] == "unreachable"
    assert "unverifiable" in rows["imported-spec"]["detail"]


def test_provenance_pin_not_satisfied_by_suffix_named_neighbour(
        tmp_path, capsys):
    # #3: `my-spec.md` must not satisfy a pin for `spec` — the suffix match
    # suppressed the broken-chain Error the check exists to raise.
    import subprocess as sp
    _git_repo(tmp_path)
    write(tmp_path, "things/my-spec.md", thing_text(GOOD.replace("alpha", "my-spec")))
    sp.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    sp.run(["git", "commit", "-q", "-m", "seed"], cwd=tmp_path, check=True)
    sha = sp.run(["git", "rev-parse", "HEAD"], cwd=tmp_path,
                 capture_output=True, text=True).stdout.strip()
    write(tmp_path, "things/d.md", thing_text(
        "id: d\ntype: decision\nstatus: made\ncreated: 2026-06-01\n"
        f"informed_by:\n  - id: spec\n    commit: {sha}"))
    rc = mdllm.cmd_provenance(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 1 and "### Errors" in out
    assert "`spec` not found" in out


def test_estate_sweep_failed_retrospective_is_unknown_not_quiet(
        tmp_path, capsys, monkeypatch):
    # Sibling: a failed retrospective computation must not render identically
    # to "no debt owed".
    import subprocess as sp
    import markdownllm.validation as validation_mod
    monkeypatch.chdir(tmp_path)
    sp.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "domain").mkdir()
    dom = tmp_path / "domain" / "alpha"
    write(dom, "things/t.md", thing_text(
        "id: t\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    sp.run(["git", "init", "-q"], cwd=dom, check=True)

    def boom(*a, **k):
        raise RuntimeError("boom")
    monkeypatch.setattr(validation_mod, "retrospective_findings", boom)
    rc = mdllm.cmd_triggers(_ns(path=".", estate=True))
    out = capsys.readouterr().out
    assert rc == 0
    assert "retrospective state UNKNOWN" in out
    assert "unknown retrospective state" in out


def test_sync_failed_git_remote_is_not_local_only(tmp_path, monkeypatch):
    # Sibling: `git remote` failing to run is an unknown publication surface,
    # not a deliberately unpublished repo.
    import markdownllm.sync as sync_mod
    repo = tmp_path / "r"
    repo.mkdir()
    monkeypatch.setattr(sync_mod, "_git", lambda *a, **k: None)
    res = sync_mod.sync_repo(repo)
    assert res.state is sync_mod.SyncState.FETCH_FAILED
    assert "unknown" in res.detail


def test_origin_external_predicate_is_whitespace_normalising():
    # Sibling: one spelling for the quarantine-class predicate. A quoted
    # YAML scalar can carry surrounding whitespace; arithmetic, provenance
    # and membrane checks must agree on membership.
    from markdownllm.model import origin_is_external
    assert origin_is_external({"origin": "external"})
    assert origin_is_external({"origin": " external "})
    assert not origin_is_external({"origin": "internal"})
    assert not origin_is_external({"origin": None})
    assert not origin_is_external({})
    assert not origin_is_external(None)
