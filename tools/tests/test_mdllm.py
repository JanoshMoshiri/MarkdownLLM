"""Self-tests for the deterministic floor.

The framework's trust model rests on mdllm.py being correct: a regression here
silently changes what "valid" means for every domain. These tests pin the
behaviour of each mechanical check. Run: python -m pytest tools/tests -q
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402

# Tests that commit (scaffold's nested repo, hook execution) must not depend
# on the machine's global git identity — CI runners and sandboxes have none.
# (portability-claims-need-execution-tests, applied to the test suite itself.)
for _k in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_k, "floor-tests")
for _k in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_k, "floor-tests@local")


def _git_supports_hook_run() -> bool:
    import re as _re
    import subprocess as _sp
    out = _sp.run(["git", "--version"], capture_output=True, text=True)
    m = _re.search(r"(\d+)\.(\d+)", out.stdout or "")
    return bool(m) and (int(m.group(1)), int(m.group(2))) >= (2, 36)


# ---------------------------------------------------------------- helpers


def thing_text(fm: str, body: str = "# Title\n\nBody text.\n") -> str:
    return f"---\n{fm.strip()}\n---\n\n{body}"


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def scan(root: Path):
    corpus, findings = mdllm.scan(root)
    return corpus, findings


def all_findings(root: Path):
    corpus, findings = scan(root)
    for t in corpus.things:
        findings.extend(mdllm.validate_level1(t, corpus.schema))
    findings.extend(mdllm.validate_level2(corpus))
    findings.extend(mdllm.validate_level3(corpus))
    return findings


def messages(findings, severity=None):
    return [f.message for f in findings if severity in (None, f.severity)]


GOOD = """\
id: alpha
type: task
status: in-progress
created: 2026-06-01
"""


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


def _brief(names):
    body = "# Brief\n\n## Live Insights\n" + "".join(f"- `{n}`\n" for n in names)
    return thing_text("id: dom-brief\ntype: continuity-brief\nstatus: live\n"
                      "created: 2026-06-01", body)


def test_active_insight_not_in_brief_is_info(tmp_path):
    # session-memory.md promises the floor surfaces this. Active insight named
    # in the brief: clean. Active insight absent: Info. Dismissed insight absent:
    # not flagged (only `active` re-enters sessions).
    write(tmp_path, "continuity.md", _brief(["listed-insight"]))
    write(tmp_path, "things/insights/listed-insight.md", thing_text(
        "id: listed-insight\ntype: insight\nstatus: active\ncreated: 2026-06-01"))
    write(tmp_path, "things/insights/orphan-insight.md", thing_text(
        "id: orphan-insight\ntype: insight\nstatus: active\ncreated: 2026-06-01"))
    write(tmp_path, "things/insights/gone-insight.md", thing_text(
        "id: gone-insight\ntype: insight\nstatus: dismissed\ncreated: 2026-06-01"))
    brief = [(x.thing, x.message) for x in all_findings(tmp_path)
             if x.severity == mdllm.SEV_INFO and "continuity brief" in x.message]
    assert ("orphan-insight", ) == tuple(t for t, _ in brief)  # only the orphan
    assert all("active insight not in continuity brief" in m for _, m in brief)


def test_open_conflict_not_in_brief_is_info(tmp_path):
    write(tmp_path, "continuity.md", _brief([]))
    write(tmp_path, "things/conflicts/live-clash.md", thing_text(
        "id: live-clash\ntype: conflict\nstatus: open\ncreated: 2026-06-01\n"
        "parties: [a, b]"))
    write(tmp_path, "things/conflicts/old-clash.md", thing_text(
        "id: old-clash\ntype: conflict\nstatus: resolved\ncreated: 2026-06-01\n"
        "parties: [a, b]"))
    brief = [(x.thing, x.message) for x in all_findings(tmp_path)
             if x.severity == mdllm.SEV_INFO and "continuity brief" in x.message]
    assert ("live-clash", ) == tuple(t for t, _ in brief)
    assert all("open conflict not in continuity brief" in m for _, m in brief)


def test_brief_completeness_skipped_without_brief(tmp_path):
    # No continuity brief (e.g. fresh scaffold) => the check is silent.
    write(tmp_path, "things/insights/lone.md", thing_text(
        "id: lone\ntype: insight\nstatus: active\ncreated: 2026-06-01"))
    assert not any("continuity brief" in m for m in messages(all_findings(tmp_path)))


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


def test_field_registration_flags_unregistered_field(tmp_path):
    # Declaring `known_fields` activates the gate. CORE_FIELDS (status/created/
    # linked_things), the declared field (owner), and a per-type required_field
    # (period) all pass; the mis-keyed `relations` (the silent-loss bug) and an
    # undeclared `tags` are flagged at Warning — never Error.
    write(tmp_path, "_schema.yaml",
          "types:\n  task:\n    statuses: [in-progress]\n    required_fields: [period]\n"
          "known_fields:\n  - owner\n")
    write(tmp_path, "things/a.md", thing_text(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-06-01\n"
        "period: q1\nowner: jm\ntags: [x]\n"
        "relations:\n  - id: b\n    relation: informs"))   # mis-keyed linked_things
    findings = all_findings(tmp_path)
    warns = messages(findings, mdllm.SEV_WARNING)
    assert any("field `relations` not in CORE_FIELDS" in m for m in warns)
    assert any("field `tags` not in CORE_FIELDS" in m for m in warns)
    # the legitimate fields are not flagged
    assert not any("field `owner`" in m for m in warns)
    assert not any("field `period`" in m for m in warns)
    assert not any("field `status`" in m for m in warns)
    # and it is strictly advisory — no field Error
    assert not any("CORE_FIELDS" in m for m in messages(findings, mdllm.SEV_ERROR))


# ---------------------------------------------------------------- scan


def test_scan_skips_non_things_and_excluded_dirs(tmp_path):
    write(tmp_path, "README.md", thing_text(GOOD))          # NON_THING_FILES
    write(tmp_path, "notes.md", "# free-form notes\n")       # no frontmatter
    write(tmp_path, "templates/t.md", thing_text(GOOD))      # excluded dir
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
    assert (target / ".git" / "hooks" / "pre-commit").is_file()
    # mechanical placeholders substituted; semantic ones intact
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "framework_version_seen: " in agents and "[relative path" not in agents
    assert "[What this domain does]" in agents  # semantic half untouched
    # the freshly scaffolded domain passes the floor with zero findings
    corpus, findings = mdllm.scan(target)
    for t in corpus.things:
        findings.extend(mdllm.validate_level1(t, corpus.schema))
    findings.extend(mdllm.validate_level2(corpus))
    findings.extend(mdllm.validate_level3(corpus))
    assert findings == [] and len(corpus.things) == 4


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


def _ns(**kw):
    from types import SimpleNamespace
    return SimpleNamespace(**kw)


def _git_repo(tmp_path):
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)


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


def test_coherence_tiers_warns_spec_without_tier_entry(tmp_path):
    write(tmp_path, ".markdownllm",
          "framework: F\nversion: 1.0\nfoundational_specs:\n  - not-in-tiers.md\n")
    write(tmp_path, "not-in-tiers.md", "# x\n")
    warns = messages(mdllm.coherence_findings(tmp_path, 15), mdllm.SEV_WARNING)
    assert any("no entry in the TIERS map" in m for m in warns)


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
