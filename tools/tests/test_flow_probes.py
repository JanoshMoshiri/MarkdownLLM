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
    RECENT, _git_repo, _git_supports_hook_run, _ns, mdllm, write,
)


def _clone(src: Path, dst: Path) -> None:
    subprocess.run(["git", "clone", "-q", str(src), str(dst)], check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=dst, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=dst, check=True)


def _scaffold(tmp_path: Path, name: str = "born") -> Path:
    """A real domain, born the way `mdllm scaffold` births one."""
    _git_repo(tmp_path)                      # the outer repo the isolation commit needs
    target = tmp_path / name
    rc = mdllm.cmd_scaffold(_ns(path=str(target), harness="claude", autopush="false"))
    assert rc == 0, "scaffold must succeed before any probe can mean anything"
    return target


def _attest(target: Path, capsys) -> None:
    """The clone-local Tier-0 attestation a strict-gated domain needs before
    its second commit. Every probe below commits, so every probe needs it."""
    mdllm.cmd_session_start(_ns(path=str(target)))
    capsys.readouterr()


def _commit(target: Path, msg: str) -> subprocess.CompletedProcess:
    subprocess.run(["git", "add", "-A"], cwd=target, check=True)
    return subprocess.run(["git", "commit", "-m", msg], cwd=target,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def _commit_or_fail(target: Path, msg: str) -> None:
    done = _commit(target, msg)
    assert done.returncode == 0, (
        f"probe setup commit failed ({msg}):\n" + done.stdout + done.stderr)


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


# --------------------------------------------------------------- probe 3


def test_probe_invariant_breach_is_observable_as_tree_state(tmp_path, capsys):
    """A trigger can fire on bytes HEAD does not contain — and you can tell.

    Round 8 of the review loop reclassified "triggers read committed state
    only" from tool mechanics to **discipline guarantee**: the evaluator reads
    the working tree, and it is the `post-write:commit` invariant that makes
    tree and HEAD coincide. That correction lives in prose, in one CHANGELOG
    entry and one kernel sentence, and prose is the tier the loop measured as
    never holding clean. This probe makes it observable instead.

    What it pins, precisely: an uncommitted edit to a watched thing IS enough
    to fire a dependency trigger, and the discrepancy IS detectable (the tree
    is dirty; HEAD still holds the old status). Both halves matter. If the
    first stopped being true, the evaluator would have quietly become
    commit-reading and the doctrine would be wrong in the other direction; if
    the second stopped being true, a discipline breach would be invisible,
    which is the condition under which a guarantee resting on discipline
    silently becomes no guarantee at all.

    This probe deliberately does NOT assert that the floor prevents the
    breach. It must not: the evaluator reading the tree is what makes
    `mdllm triggers` useful while you work. Prevention is the commit hook's
    job, and the invariant's.
    """
    if not _git_supports_hook_run():
        pytest.skip("git too old to execute hooks reliably")
    target = _scaffold(tmp_path)
    capsys.readouterr()
    _attest(target, capsys)

    write(target, "things/prerequisite.md",
          f"---\nid: prerequisite\ntype: note\nstatus: in-progress\n"
          f"created: {RECENT}\n---\n\n# Prerequisite\n\nNot done yet.\n")
    write(target, "things/dependent.md",
          f"---\nid: dependent\ntype: note\nstatus: not-started\n"
          f"created: {RECENT}\ntriggers:\n  - type: dependency\n"
          f"    watch: [prerequisite]\n    on: status_changed_to\n"
          f"    value: completed\n    action: unblock\n---\n\n"
          f"# Dependent\n\nWaits on the prerequisite.\n")
    _commit_or_fail(target, "create: the watched pair")

    # Committed state: the prerequisite is not done, so nothing fires.
    mdllm.cmd_triggers(_ns(path=str(target), estate=False))
    committed = capsys.readouterr().out
    assert "dependent" not in committed, (
        "nothing should fire while the prerequisite is in-progress:\n"
        + committed)

    # The breach: complete the prerequisite in the WORKING TREE only.
    prereq = target / "things" / "prerequisite.md"
    prereq.write_text(
        prereq.read_text(encoding="utf-8").replace(
            "status: in-progress", "status: completed"),
        encoding="utf-8")

    mdllm.cmd_triggers(_ns(path=str(target), estate=False))
    dirty = capsys.readouterr().out
    assert "dependent" in dirty, (
        "the evaluator reads the tree — an uncommitted completion must fire "
        "the watcher, or the discipline-vs-mechanics correction is wrong:\n"
        + dirty)

    # ...and the discrepancy is detectable, which is what makes a guarantee
    # resting on discipline auditable rather than merely hoped for.
    porcelain = subprocess.run(["git", "status", "--porcelain"], cwd=target,
                               capture_output=True, text=True,
                               encoding="utf-8").stdout
    assert "things/prerequisite.md" in porcelain, (
        "the breach must be visible in tree state:\n" + porcelain)
    at_head = subprocess.run(
        ["git", "show", "HEAD:things/prerequisite.md"], cwd=target,
        capture_output=True, text=True, encoding="utf-8").stdout
    assert "status: in-progress" in at_head, (
        "committed state must still hold the old status — otherwise there "
        "was no breach to observe")


# --------------------------------------------------------------- probe 4


def test_probe_refresh_end_to_end_surfaces_seals_and_clears_drift(tmp_path,
                                                                  capsys):
    """Version drift surfaces at session start, seals on adoption, and the
    managed blocks regenerate on the way through.

    Three mechanisms that only mean anything in sequence, and which no unit
    test composes: the session-start version check (the operator's first
    sight of drift), `refresh` reporting the unabsorbed CHANGELOG delta (what
    adoption actually requires), and `--seal` closing it afterwards. The
    ordering is the contract — sealing before adoption would make the flag a
    lie, and the floor's half is to refuse to seal silently.

    **Departure from the plan's text, deliberate.** The plan says
    "version-bump a scratch sentinel". The sentinel is the *framework's*
    `.markdownllm`, shared by every test in this suite and by the running
    tool — and this file already carries a probe
    (`..._leaves_an_out_of_estate_framework_untouched`) that exists because a
    test mutating a shared framework-root file caused three regressions. So
    the drift is created from the domain's side instead, by lowering
    `framework_version_seen`. It is the same delta observed from the other
    end, and it touches nothing shared.

    The assertions are relational, never literal: no version string is
    written here, because a probe that names one becomes a release chore.
    """
    target = _scaffold(tmp_path)
    capsys.readouterr()

    agents = target / "AGENTS.md"
    born = agents.read_text(encoding="utf-8")
    meta, _, err = mdllm.parse_frontmatter(born)
    assert not err
    current = str((meta or {}).get("framework_version_seen") or "")
    assert current, "a scaffolded domain must record the version it was born at"

    # Born current: refresh has nothing to say.
    mdllm.cmd_refresh(_ns(path=str(target), seal=False))
    at_birth = capsys.readouterr().out
    assert "Up to date" in at_birth, at_birth

    # Drift, from the domain's side.
    agents.write_text(
        born.replace(f"framework_version_seen: {current}",
                     "framework_version_seen: 3.0.0"),
        encoding="utf-8")

    # 1. Session start surfaces it — the operator's first sight.
    mdllm.cmd_session_start(_ns(path=str(target)))
    started = capsys.readouterr().out
    assert "3.0.0" in started and current in started, (
        "session start must name both the seen and the live version:\n"
        + started)

    # 2. Refresh reports what adoption requires, and does NOT seal on its own.
    mdllm.cmd_refresh(_ns(path=str(target), seal=False))
    reported = capsys.readouterr().out
    assert "Up to date" not in reported, reported
    assert "Versions not yet absorbed" in reported, reported
    assert "framework_version_seen: 3.0.0" in agents.read_text(
        encoding="utf-8"), "a report must not seal — adoption is semantic"

    # 3. --seal closes it, once the agent has adopted.
    mdllm.cmd_refresh(_ns(path=str(target), seal=True))
    capsys.readouterr()
    sealed = agents.read_text(encoding="utf-8")
    assert f"framework_version_seen: {current}" in sealed, (
        "--seal must bump the domain to the live framework version")

    # 4. And the domain is clean afterwards: blocks regenerated, drift gone.
    smeta, _, serr = mdllm.parse_frontmatter(sealed)
    assert not serr
    blocks = mdllm.build_domain_kernel_blocks(target, smeta or {})
    present, drifted = mdllm.domain_kernel_status(sealed, blocks)
    assert present and drifted == [], f"refresh left managed drift: {drifted}"

    mdllm.cmd_refresh(_ns(path=str(target), seal=False))
    after = capsys.readouterr().out
    assert "Up to date" in after, after


# --------------------------------------------------------------- probe 5


def test_probe_session_close_delimits_worklog_and_advances_the_flip_window(
        tmp_path, capsys):
    """One `session-end:` commit closes two windows, and they must agree.

    `session-end:` carries a double definition that took ten releases to
    settle (review-loop rounds 7-8): it is the ritual's routine closer, and
    it is the mechanical delimiter for two *separate* readers —
    `worklog`'s session grouping and session-start's verified-flip window.
    Two consumers reading one convention through two independent
    implementations is exactly the seam a cold read cannot check and a unit
    test would stub away: each could be individually correct while silently
    disagreeing about where a session ends.

    The flip window is the half with teeth. It is the visibility leg of the
    quarantine discipline — every `verified: true` flip surfaced where the
    operator already looks, so a wrong or rogue one cannot pass unseen. A
    window that failed to advance would re-announce old flips until the
    operator learned to skim them, and a window that advanced too eagerly
    would hide a live one. Both failures are silent; both are pinned here.

    **The edge is off-by-one on purpose, and this probe was written against
    the wrong one first.** The window skips HEAD when hunting for its base,
    so standing *on* the closer the flips are still shown — you are meant to
    see what you are closing, which is precisely when the session-end ritual
    reports them. It advances at the next session's first commit. That
    nuance has carried an explanatory comment since the feature was born
    (bf66b12), it is one line, and it is the kind of subtlety a refactor
    drops silently in either direction. So both edges are asserted below.
    """
    if not _git_supports_hook_run():
        pytest.skip("git too old to execute hooks reliably")
    target = _scaffold(tmp_path)
    capsys.readouterr()
    _attest(target, capsys)

    # Quarantine, then the attributable flip — two commits, as the floor
    # requires: a born-verified external thing is refused outright.
    write(target, "things/ingested.md",
          f"---\nid: ingested\ntype: note\nstatus: not-started\n"
          f"created: {RECENT}\norigin: external\nverified: false\n"
          f"---\n\n# Ingested\n\nFrom outside.\n")
    _commit_or_fail(target, "create: ingested under quarantine")

    ingested = target / "things" / "ingested.md"
    ingested.write_text(
        ingested.read_text(encoding="utf-8").replace(
            "verified: false", "verified: true\nverified_by: A Human"),
        encoding="utf-8")
    _commit_or_fail(target, "verify: ingested")

    # Open window: the flip is surfaced.
    # Assert the FLIP line, not the id: the digest also names this thing on
    # its Watched line (external things it does not own), and a bare id match
    # would pass on the wrong reader entirely — it did, first time round.
    mdllm.cmd_session_start(_ns(path=str(target)))
    open_window = capsys.readouterr().out
    assert "Verified flips" in open_window, (
        "a flip inside the open window must be surfaced:\n" + open_window)
    assert "`ingested` @" in open_window and "A Human" in open_window, (
        "and surfaced attributably — an unattributed flip is the thing the "
        "visibility leg exists to expose:\n" + open_window)

    # Close the session.
    write(target, "things/after.md",
          f"---\nid: after\ntype: note\nstatus: not-started\n"
          f"created: {RECENT}\n---\n\n# After\n\nBody.\n")
    _commit_or_fail(target, "session-end: the probe's session")

    # Edge 1 — standing ON the closer, the flip is still surfaced. This is
    # the session-end ritual's own view: it reports the flips it is closing
    # over, so the window must not have advanced out from under it yet.
    mdllm.cmd_session_start(_ns(path=str(target)))
    on_the_closer = capsys.readouterr().out
    assert "Verified flips" in on_the_closer and "A Human" in on_the_closer, (
        "a session-end at HEAD must still show the session's own flips — "
        "the ritual reports what it is closing:\n" + on_the_closer)

    # Edge 2 — one commit into the next session, the window has advanced.
    write(target, "things/next-session.md",
          f"---\nid: next-session\ntype: note\nstatus: not-started\n"
          f"created: {RECENT}\n---\n\n# Next\n\nBody.\n")
    _commit_or_fail(target, "create: the next session's first work")

    mdllm.cmd_session_start(_ns(path=str(target)))
    closed_window = capsys.readouterr().out
    assert "Verified flips" not in closed_window, (
        "the flip window must advance past a session-end commit, or old "
        "flips are re-announced until the operator skims them:\n"
        + closed_window)
    assert "A Human" not in closed_window, closed_window
    # The thing itself is still watched — advancing the FLIP window must not
    # drop it from the digest's other readers. Two windows, one delimiter,
    # separate meanings.
    assert "`ingested`" in closed_window, (
        "advancing the flip window must not un-watch the thing:\n"
        + closed_window)

    # Reader 2 — worklog delimits on the same commit, from its own code path.
    # Membership is the contract, not text order: the view prints sessions
    # newest-first and heads each block with its CLOSER's subject, so "appears
    # earlier in the output" means nothing. Read the block and check who is
    # in it.
    mdllm.cmd_worklog(_ns(path=str(target), write=False))
    log = capsys.readouterr().out
    header = "session-end: the probe's session"
    assert header in log, log
    block = log[log.index(header):]
    end = block.find("\n## ", 1)
    if end != -1:
        block = block[:end]

    assert "verify: ingested" in block, (
        "the flip commit belongs to the session its closer ends:\n" + block)
    assert "create: ingested under quarantine" in block, (
        "so does the quarantine commit that preceded it:\n" + block)
    assert "create: the next session's first work" not in block, (
        "a commit made after the closer belongs to the NEXT session — if it "
        "lands in this block, worklog and the flip window disagree about "
        "where a session ends:\n" + block)
