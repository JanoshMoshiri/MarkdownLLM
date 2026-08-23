"""Flow probes — the execution layer a cold read structurally cannot verify.

`coherence-mechanism-build` Phase 3. The eight-round review loop measured
where coherence actually comes from: derived surfaces held clean in all eight
rounds, hand prose never did, and the single execution-layer probe
outperformed every cold read. These are that finding turned into a suite.

A probe pins one END-TO-END FLOW by its observable output. It is integration-
shaped on purpose — a probe that mocked the flow would be verifying the mock,
and the defects this layer exists to catch live exactly in the seams a mock
replaces. Each fails in CI if the behaviour it pins regresses, with no human
reading anything.

Deliberately not unit tests, and deliberately not duplicating them: the gate,
the hook bodies and the generator all have unit coverage. What had none was
the ORDER these compose in when a real operator meets them for the first time.
"""

import subprocess
from pathlib import Path

import pytest

from corpus_harness import (  # noqa: F401
    _git_repo, _git_supports_hook_run, _ns, mdllm, write,
)


def _clone(src: Path, dst: Path) -> None:
    subprocess.run(["git", "clone", "-q", str(src), str(dst)], check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=dst, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=dst, check=True)


def _scaffold(tmp_path: Path, name: str = "born") -> Path:
    """A real domain, born the way `mdllm scaffold` births one."""
    _git_repo(tmp_path)                      # the outer repo the isolation commit needs
    target = tmp_path / name
    rc = mdllm.cmd_scaffold(_ns(path=str(target), autopush="false"))
    assert rc == 0, "scaffold must succeed before any probe can mean anything"
    return target


# --------------------------------------------------------------- probe 1


def test_probe_fresh_clone_boot(tmp_path, capsys):
    """A cold clone reports SETUP ORDERING, not a validation failure, and is
    clean the moment the attestation exists.

    This is the flow the plan records as having already outperformed every
    cold read; the work here is making it repeatable. The failure it guards
    is specific and has happened: a fresh gated clone cannot have a
    session-start attestation yet, so a doctor run before session-start
    always finds the gate blocking. Reporting that as "validation failing"
    is the cry-wolf shape — the one line an operator must never discount,
    firing spuriously at every single clone.
    """
    if not _git_supports_hook_run():
        pytest.skip("git too old to execute hooks reliably")
    target = _scaffold(tmp_path)
    capsys.readouterr()

    clone = tmp_path / "cold-clone"
    _clone(target, clone)
    # Hooks are .git-local: a clone has none until the operator installs them.
    # That IS the fresh-clone boot sequence, not a fixture convenience.
    mdllm.cmd_install_hook(_ns(path=str(clone)))
    capsys.readouterr()

    mdllm.cmd_doctor(_ns(path=str(clone)))
    before = capsys.readouterr().out
    assert "setup ordering, not a validation failure" in before, before
    assert "failed to execute" not in before

    mdllm.cmd_session_start(_ns(path=str(clone)))
    capsys.readouterr()

    mdllm.cmd_doctor(_ns(path=str(clone)))
    after = capsys.readouterr().out
    assert "validation currently clean" in after, after
    assert "setup ordering" not in after


# --------------------------------------------------------------- probe 2


def test_probe_scaffold_birth_lands_whole(tmp_path, capsys):
    """Birth delivers a committed, generated, prompt-carrying domain.

    Four facts in one flow, each of which has been wrong at least once:
    the birth commit lands; the managed blocks match a fresh generation
    (a domain born drifted is born lying); the reasoning prompts are
    delivered at all (the 2026-08-01 sweep found every domain instructed to
    run prompts it did not have) and graph-stripped (their `linked_things`
    point into the FRAMEWORK's id space, which does not resolve in a domain).
    """
    target = _scaffold(tmp_path)
    capsys.readouterr()

    log = subprocess.run(["git", "log", "--oneline"], cwd=target,
                         capture_output=True, text=True, encoding="utf-8")
    assert log.returncode == 0 and log.stdout.strip(), \
        "the birth commit must exist in the domain's own repo"

    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    meta, _, err = mdllm.parse_frontmatter(agents)
    assert not err
    blocks = mdllm.build_domain_kernel_blocks(target, meta or {})
    present, drifted = mdllm.domain_kernel_status(agents, blocks)
    assert present, "a newborn domain must carry the managed blocks"
    assert drifted == [], f"born drifted: {drifted}"

    prompts = sorted((target / "prompts").glob("*.md"))
    assert prompts, "the session-start block instructs prompts that must exist"
    for p in prompts:
        pmeta, _, perr = mdllm.parse_frontmatter(p.read_text(encoding="utf-8"))
        assert not perr, f"{p.name}: {perr}"
        assert "linked_things" not in (pmeta or {}), (
            f"{p.name} carries framework-space links into a domain")


def test_probe_birth_leaves_an_out_of_estate_framework_untouched(tmp_path,
                                                                 capsys):
    """Scaffolding OUTSIDE the framework root must not touch its terms file.

    Birth registers a newborn's name in the framework root's local
    `.boundary-terms`, so framework commits cannot mention it until the
    operator deletes the line. `fw_root` is the RUNNING TOOL's checkout, not
    the target's context — so before this guard, every scaffold anywhere on
    the machine appended a name to that operator-owned file, the test suite
    included. Those synthetic names then appear in the suite's own tracked
    source, and the boundary check began falsely refusing commits touching
    `tools/tests/`: three regressions, the third blocking four commits in one
    session, with the adder recorded as unattributed because the search had
    been scoped to `boundary.py`.

    This probe is the reason the class cannot come back, and it exists
    because the sprint that added the terms audit had its own commit blocked
    by its own probes.
    """
    from markdownllm.boundary import TERMS_FILE
    fw_terms = Path(mdllm.__file__).resolve().parents[1] / TERMS_FILE
    before = fw_terms.read_text(encoding="utf-8") if fw_terms.is_file() else None
    _scaffold(tmp_path, name="out-of-estate-probe")
    capsys.readouterr()
    after = fw_terms.read_text(encoding="utf-8") if fw_terms.is_file() else None
    assert after == before, (
        "a scaffold outside the framework root mutated its local boundary "
        "terms file")


def test_probe_birth_gate_holds_from_the_second_commit(tmp_path, capsys):
    """The gate blocks the SECOND commit, not the birth commit.

    The asymmetry is the whole design and it is easy to regress in either
    direction: blocking the birth commit deadlocks scaffold against its own
    output, and never blocking makes the gate decorative. Only an executed
    commit can tell the two apart, which is why this is a probe.
    """
    if not _git_supports_hook_run():
        pytest.skip("git too old to execute hooks reliably")
    target = _scaffold(tmp_path)
    capsys.readouterr()

    write(target, "things/second.md",
          "---\nid: second\ntype: note\nstatus: not-started\n"
          "created: 2026-08-23\n---\n\n# Second\n\nBody.\n")
    subprocess.run(["git", "add", "-A"], cwd=target, check=True)
    second = subprocess.run(["git", "commit", "-m", "create: second"],
                            cwd=target, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    combined = second.stdout + second.stderr
    assert second.returncode != 0, (
        "a strict-gated domain must refuse the second commit without an "
        "attestation:\n" + combined)
    assert "session-start" in combined, combined

    mdllm.cmd_session_start(_ns(path=str(target)))
    capsys.readouterr()
    third = subprocess.run(["git", "commit", "-m", "create: second"],
                           cwd=target, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
    assert third.returncode == 0, (
        "an attested clone must commit:\n" + third.stdout + third.stderr)
