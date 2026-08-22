"""The session gate — per-domain attestation freshness at the commit
boundary. Lifted from test_mdllm.py along its banner (sprint 2, F6;
floor-structure-residue item 4)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from corpus_harness import (  # noqa: E402
    RECENT, _git_commit, _git_repo, _ns, _sync_git, thing_text,
    write,
)


# ------------------------------------------------------------- session gate
# (cowork-integrity-estate-sweep Phase 10: the contract-load fail-safe. The
# gate holds the commit boundary — the one anchor every breached harness
# session still had to pass — and its claim is deliberately narrow: the
# attestation proves session-start ran in this clone, i.e. the Tier-0
# contract was emitted, not that it was heeded.)

GATE_SCHEMA_WARN = "schema_version: 1\ndomain: t\noptions:\n  session_gate: warn\n"
GATE_SCHEMA_STRICT = "schema_version: 1\ndomain: t\noptions:\n  session_gate: strict\n"


def _gate(root):
    corpus, _ = mdllm.scan(root)
    return mdllm.session_gate_findings(root, corpus)


def _write_attest(root, age_hours=0):
    import datetime as _dt
    import subprocess as _sp
    gd = _sp.run(["git", "rev-parse", "--git-dir"], cwd=root,
                 capture_output=True, text=True).stdout.strip()
    stamp = (_dt.datetime.now(_dt.timezone.utc)
             - _dt.timedelta(hours=age_hours)).isoformat()
    from markdownllm.session_contract import contract_fingerprint
    ((root / gd).resolve() / "mdllm-attest").write_text(
        f"{stamp} deadbeef contract={contract_fingerprint(root)} "
        "evidence=emitted delivery=digest-only\n", encoding="utf-8")


def test_session_gate_silent_when_undeclared(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    assert _gate(tmp_path) == []


def test_session_gate_warn_fires_without_attestation(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "birth")
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_WARN)
    findings = _gate(tmp_path)
    assert len(findings) == 1
    assert findings[0].severity == mdllm.SEV_WARNING
    # The no-attestation message names BOTH readings — fresh-clone ordering
    # and a contract-less working clone — because the floor cannot tell them
    # apart (substrate reconciliation C2, 2026-08-09; the old wording accused
    # every fresh clone of a skip and taught operators to discount the gate).
    assert "no session-start attestation" in findings[0].message
    assert "mid-flight" in findings[0].message
    assert "session-start" in findings[0].message  # the remedy names the command


def test_session_gate_strict_escalates_to_error(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "birth")
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    findings = _gate(tmp_path)
    assert {f.severity for f in findings} == {mdllm.SEV_ERROR}


def test_session_gate_fresh_attestation_is_clean(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "birth")
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    _write_attest(tmp_path)
    assert _gate(tmp_path) == []


def test_session_gate_stale_attestation_fires(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "birth")
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    _write_attest(tmp_path, age_hours=mdllm.SESSION_GATE_WINDOW_HOURS + 1)
    findings = _gate(tmp_path)
    assert len(findings) == 1 and "old" in findings[0].message


def test_session_gate_no_git_repo_is_silent(tmp_path):
    # No git dir => nothing will ever commit here; the gate has no boundary
    # to hold and must not manufacture findings for ad-hoc corpus reads.
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    assert _gate(tmp_path) == []


def test_session_start_writes_attestation(tmp_path, capsys):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "base")
    mdllm.cmd_session_start(_ns(path=str(tmp_path)))
    capsys.readouterr()
    assert _gate(tmp_path) == []
    import subprocess as _sp
    gd = _sp.run(["git", "rev-parse", "--git-dir"], cwd=tmp_path,
                 capture_output=True, text=True).stdout.strip()
    attest = (tmp_path / gd).resolve() / "mdllm-attest"
    assert attest.is_file()
    tokens = attest.read_text(encoding="utf-8").split()
    stamp, sha = tokens[0], tokens[1]
    assert len(sha) >= 7  # HEAD sha recorded beside the timestamp
    # The kernel token records what the emission did (Phase 2).
    assert any(t.startswith("kernel=") for t in tokens[2:])
    assert any(t.startswith("contract=") for t in tokens[2:])
    assert "evidence=emitted" in tokens[2:]
    assert not any(t.startswith(("read=", "applied=", "compliant="))
                   for t in tokens[2:])


def test_session_gate_expires_on_contract_change_not_unrelated_head_movement(
        tmp_path, capsys):
    _git_repo(tmp_path)
    write(tmp_path, "AGENTS.md", "---\nname: T\n---\n\n# T\n")
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "base")
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    mdllm.cmd_session_start(_ns(path=str(tmp_path)))
    capsys.readouterr()
    assert _gate(tmp_path) == []

    # Domain work and HEAD movement do not change the operative contract.
    write(tmp_path, "things/work.md", thing_text(
        "id: work\ntype: note\nstatus: in-progress\ncreated: 2026-08-20\n"))
    _git_commit(tmp_path, "ordinary work")
    assert _gate(tmp_path) == []

    write(tmp_path, "AGENTS.md", "---\nname: T\n---\n\n# T\n\nChanged contract.\n")
    findings = _gate(tmp_path)
    assert len(findings) == 1
    assert findings[0].severity == mdllm.SEV_ERROR
    assert "contract changed" in findings[0].message


def test_legacy_attestation_is_fresh_but_contract_currency_is_unknown(tmp_path):
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "base")
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    import datetime as _dt
    import subprocess as _sp
    gd = _sp.run(["git", "rev-parse", "--git-dir"], cwd=tmp_path,
                 capture_output=True, text=True).stdout.strip()
    stamp = _dt.datetime.now(_dt.timezone.utc).isoformat()
    ((tmp_path / gd).resolve() / "mdllm-attest").write_text(
        f"{stamp} deadbeef\n", encoding="utf-8")
    findings = _gate(tmp_path)
    assert len(findings) == 1
    assert findings[0].severity == mdllm.SEV_WARNING
    assert "legacy attestation" in findings[0].message


def test_session_start_attests_and_the_clone_then_clears_the_gate(tmp_path,
                                                                  capsys):
    """Emitting the contract must satisfy the gate that demands it.

    Under `session_gate: strict` a hook-opened session once began with a
    commit-blocking Error, because the rendering the scaffolded hook used
    returned before the attestation write — the gate firing against the one
    integration that emits its contract mechanically (field report
    2026-08-13). The attestation attests to EMISSION, so every emitting path
    must record it. Only one rendering survives today; the rule does not
    depend on that.
    """
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "base")
    import subprocess as _sp
    gd = _sp.run(["git", "rev-parse", "--git-dir"], cwd=tmp_path,
                 capture_output=True, text=True).stdout.strip()
    attest = (tmp_path / gd).resolve() / "mdllm-attest"
    assert not attest.exists()

    mdllm.cmd_session_start(_ns(path=str(tmp_path)))
    capsys.readouterr()

    assert attest.is_file(), "session-start emitted the contract but did not attest"
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    assert _gate(tmp_path) == [], "a freshly attested clone must clear the gate"


def test_retrospective_debt_is_surfaced_at_session_start(tmp_path, capsys,
                                                         monkeypatch):
    """A domain owing a retrospective must be told so at t=0.

    The cadence check reached only one of two renderings while both existed
    (field report 2026-08-13); it was invisible in the field only because
    that domain happened to be current.
    """
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "base")

    from markdownllm import validation as _validation

    class _Finding:
        message = "last retrospective was 40 days ago (cadence 30d)"

    monkeypatch.setattr(_validation, "retrospective_findings",
                        lambda domain, corpus, **kw: [_Finding()])

    mdllm.cmd_session_start(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out

    assert "Retrospective cadence:" in out
    assert "40 days ago" in out


def test_install_hook_no_test_skips_the_full_validate(tmp_path, capsys):
    """`--no-test` must skip the execution test and downgrade the claim.

    The execution test fires a real pre-commit — a full validate, minutes on a
    large domain, long enough to trip a harness tool timeout and read as a
    hang. Skipping is opt-in and must never report the hook as proven.
    """
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))

    rc = mdllm.cmd_install_hook(_ns(path=str(tmp_path), no_test=True))
    out = capsys.readouterr().out

    assert rc == 0
    assert "SKIPPED" in out and "unproven" in out
    assert "ran and passed" not in out, "skipping must not claim execution"
    assert (tmp_path / ".git" / "hooks" / "pre-commit").is_file()


def test_session_start_names_an_openable_kernel(tmp_path, capsys):
    """The kernel lives in the framework root, so a bare name is unopenable.

    From inside a domain, `kernel.md` resolves to a file that does not exist
    and the first read fails (field report 2026-08-13). Regression guard:
    this defect was originally fixed only in a second rendering, so removing
    that rendering would have silently restored it here.
    """
    _git_repo(tmp_path)
    write(tmp_path, "things/base.md", thing_text(
        "id: base\ntype: note\nstatus: not-started\ncreated: 2026-07-16\n"))
    _git_commit(tmp_path, "base")

    mdllm.cmd_session_start(_ns(path=str(tmp_path)))
    out = capsys.readouterr().out

    # The direct channel emits the kernel under a header naming the openable
    # reference (Phase 2); the regression intent is unchanged — the name a
    # reader is given must resolve from inside the domain.
    line = next(l for l in out.splitlines()
                if l.startswith("## The operative kernel"))
    reference = line.split("`")[1]
    assert reference != "kernel.md", "a bare name resolves inside the domain"
    assert (tmp_path / reference).resolve().is_file()


def test_session_gate_silent_on_unborn_head(tmp_path):
    # The birth commit: repo exists, HEAD does not. The contract files are
    # being created in this very commit, so there was nothing to have read —
    # the gate holds from the second commit onward. Regression for the CI
    # failure where scaffold's first commit was blocked by the strict gate
    # its own template had just declared.
    _git_repo(tmp_path)
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    assert _gate(tmp_path) == []


def test_session_gate_holds_from_second_commit(tmp_path):
    # ...and the exemption dies with the first commit: same repo, one commit
    # in history, still no attestation -> strict Error.
    _git_repo(tmp_path)
    write(tmp_path, "_schema.yaml", GATE_SCHEMA_STRICT)
    _git_commit(tmp_path, "birth")
    findings = _gate(tmp_path)
    assert {f.severity for f in findings} == {mdllm.SEV_ERROR}


