"""Self-tests for the deterministic floor.

The framework's trust model rests on mdllm.py being correct: a regression here
silently changes what "valid" means for every domain. These tests pin the
behaviour of each mechanical check. Run: python -m pytest tools/tests -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402


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
    _git_repo(tmp_path)
    write(tmp_path, "things/alpha.md", thing_text(GOOD))
    mdllm.cmd_install_hook(_ns(path=str(tmp_path)))
    rc = mdllm.cmd_doctor(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out
    assert rc == 0 and "FLOOR ACTIVE" in out and "EXECUTES" in out


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
