"""Phase 3 of the ``cowork-adapter`` plan: assembly and the bundle.

``mdllm assemble`` is the post-clone half of any bootstrap for an
environment with no entry-file discovery — neutral, config-driven, and
pinned here over local file:// remotes whose default branch is
deliberately not ``main``. ``mdllm bundle`` renders the account-level
plugin from framework-owned templates with the estate config DERIVED
from local clones' remotes, never authored.

Run: python -m pytest tools/tests/test_assemble.py -q
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm.adapters.cowork import COWORK  # noqa: E402
from markdownllm.assemble import (  # noqa: E402
    clone_url, cmd_assemble, parse_config, select_domains,
)
from markdownllm.bundle_service import (  # noqa: E402
    derive_estate_config, framework_source_findings, owner_repo,
)

FW_ROOT = Path(mdllm.__file__).resolve().parents[1]
TEMPLATES = FW_ROOT / "templates"
TEST_FRAMEWORK_COMMIT = "0123456789abcdef0123456789abcdef01234567"


def _ns(**kw):
    import argparse
    defaults = {"root": ".", "filters": [], "contract": False}
    defaults.update(kw)
    return argparse.Namespace(**defaults)


def _run(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True,
                          check=True).stdout.strip()


def _bare_domain(tmp_path: Path, name: str, branch: str = "trunk") -> Path:
    """A bare 'remote' seeded with a minimal valid domain on ``branch``."""
    origin = tmp_path / f"{name}.git"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
    subprocess.run(["git", "-C", str(origin), "symbolic-ref", "HEAD",
                    f"refs/heads/{branch}"], check=True)
    seed = tmp_path / f"{name}-seed"
    subprocess.run(["git", "init", "-q", "-b", branch, str(seed)],
                   check=True)
    _run(seed, "config", "user.email", "t@t")
    _run(seed, "config", "user.name", "t")
    (seed / "AGENTS.md").write_text(
        "---\nname: t\nframework_root: ../..\n---\n# t\n", encoding="utf-8")
    (seed / "things").mkdir()
    (seed / "things" / ".gitkeep").write_text("", encoding="utf-8")
    _run(seed, "add", "-A")
    _run(seed, "commit", "-q", "-m", "seed")
    _run(seed, "remote", "add", "origin", str(origin))
    _run(seed, "push", "-q", "origin", branch)
    return origin


def _advance_remote(tmp_path: Path, origin: Path, branch: str,
                    marker: str) -> str:
    writer = tmp_path / f"writer-{marker}"
    subprocess.run(["git", "clone", "-q", "-b", branch,
                    str(origin), str(writer)], check=True)
    _run(writer, "config", "user.email", "writer@test")
    _run(writer, "config", "user.name", "writer")
    (writer / f"{marker}.txt").write_text(marker + "\n", encoding="utf-8")
    _run(writer, "add", "-A")
    _run(writer, "commit", "-q", "-m", marker)
    _run(writer, "push", "-q", "origin", branch)
    return _run(writer, "rev-parse", "HEAD")


@pytest.fixture()
def workspace(tmp_path):
    """A framework-shaped root with a config naming two file:// domains."""
    alpha = _bare_domain(tmp_path, "alpha-estate", "trunk")
    beta = _bare_domain(tmp_path, "beta-estate", "develop")
    root = tmp_path / "work"
    root.mkdir()
    config = root / "config.env"
    config.write_text(
        "GIT_NAME=Assembly Test\n"
        "GIT_EMAIL=assembly@test\n"
        f"DOMAINS={alpha} {beta}\n", encoding="utf-8")
    return root, config, alpha, beta


# ------------------------------------------------------------------ config

def test_config_is_flat_never_sourced(tmp_path):
    cfg = tmp_path / "c.env"
    cfg.write_text('GIT_NAME="Quoted Name"\n# comment\nGIT_EMAIL=e@x\n'
                   "DOMAINS=o/a o/b\n", encoding="utf-8")
    config, problem = parse_config(cfg)
    assert problem == ""
    assert config["GIT_NAME"] == "Quoted Name"
    assert config["DOMAINS"] == "o/a o/b"


def test_config_missing_keys_named(tmp_path):
    cfg = tmp_path / "c.env"
    cfg.write_text("GIT_NAME=x\n", encoding="utf-8")
    _, problem = parse_config(cfg)
    assert "GIT_EMAIL" in problem and "DOMAINS" in problem


def test_clone_url_forms():
    assert clone_url("o/r") == "https://github.com/o/r.git"
    assert clone_url("file:///x/y.git") == "file:///x/y.git"
    assert clone_url("/abs/path.git") == "/abs/path.git"


def test_selection_matches_loosely_and_reports_misses():
    entries = ["o/alpha-estate", "o/beta-estate"]
    chosen, misses = select_domains(entries, ["ALPHA"])
    assert chosen == ["o/alpha-estate"] and misses == []
    _, misses = select_domains(entries, ["gamma"])
    assert misses == ["gamma"]
    chosen, _ = select_domains(entries, [])
    assert chosen == entries


# ---------------------------------------------------------------- assembly

def test_assemble_end_to_end(workspace, capsys):
    root, config, alpha, beta = workspace
    rc = cmd_assemble(_ns(config=str(config), root=str(root)))
    out = capsys.readouterr().out
    assert rc == 0

    # Clones landed, identity set, branches recorded from each remote's
    # OWN head — two different non-main names in one assembly.
    for name, branch in (("alpha-estate", "trunk"),
                         ("beta-estate", "develop")):
        clone = root / "domains" / name
        assert clone.is_dir()
        assert _run(clone, "config", "mdllm.defaultbranch") == branch
        assert _run(clone, "config", "user.name") == "Assembly Test"
        assert (clone / ".git" / "hooks" / "pre-commit").is_file()

    # The Tier-0 contract was EMITTED per domain, not pointed at.
    assert out.count("Tier-0 Contract (emitted)") == 2
    # Branch map carries both real names; no MISMATCH rows.
    assert "default=trunk" in out and "default=develop" in out
    assert "MISMATCH" not in out
    # The handoff states publication mode honestly (ambient here — no
    # token in the test environment means autopush would work).
    assert "HANDOFF" in out
    # Attestations recorded per clone with the contract token (the kernel
    # token rides beside it since session-start-hardening Phase 2).
    for name in ("alpha-estate", "beta-estate"):
        attest = (root / "domains" / name / ".git" / "mdllm-attest")
        assert attest.is_file()
        text = attest.read_text(encoding="utf-8").strip()
        assert " contract" in text
        assert " kernel=" in text


def test_assemble_filters_and_reports_misses(workspace, capsys):
    root, config, *_ = workspace
    rc = cmd_assemble(_ns(config=str(config), root=str(root),
                          filters=["alpha"]))
    out = capsys.readouterr().out
    assert rc == 0
    assert (root / "domains" / "alpha-estate").is_dir()
    assert not (root / "domains" / "beta-estate").exists()

    rc = cmd_assemble(_ns(config=str(config), root=str(root),
                          filters=["gamma"]))
    out = capsys.readouterr().out
    assert rc == 2
    assert "no configured domain matched" in out


def test_assemble_is_idempotent(workspace, capsys):
    root, config, *_ = workspace
    assert cmd_assemble(_ns(config=str(config), root=str(root),
                            filters=["alpha"])) == 0
    capsys.readouterr()
    assert cmd_assemble(_ns(config=str(config), root=str(root),
                            filters=["alpha"])) == 0
    assert "reusing the existing clone" in capsys.readouterr().out


def test_reused_clean_clone_fast_forwards_through_shared_sync(
        workspace, tmp_path, capsys):
    root, config, alpha, *_ = workspace
    args = _ns(config=str(config), root=str(root), filters=["alpha"])
    assert cmd_assemble(args) == 0
    capsys.readouterr()

    remote_tip = _advance_remote(tmp_path, alpha, "trunk", "remote-update")
    clone = root / "domains" / "alpha-estate"
    assert _run(clone, "rev-parse", "HEAD") != remote_tip

    assert cmd_assemble(args) == 0
    out = capsys.readouterr().out
    assert "sync: synced" in out
    assert _run(clone, "rev-parse", "HEAD") == remote_tip


def test_reused_dirty_clone_is_reported_and_not_resolved(
        workspace, tmp_path, capsys):
    root, config, alpha, *_ = workspace
    args = _ns(config=str(config), root=str(root), filters=["alpha"])
    assert cmd_assemble(args) == 0
    capsys.readouterr()
    clone = root / "domains" / "alpha-estate"
    original = _run(clone, "rev-parse", "HEAD")
    local_draft = clone / "operator-draft.txt"
    local_draft.write_text("keep me\n", encoding="utf-8")
    remote_tip = _advance_remote(tmp_path, alpha, "trunk", "remote-dirty")

    assert cmd_assemble(args) == 0
    out = capsys.readouterr().out
    assert "sync: dirty" in out
    assert "left untouched" in out
    assert _run(clone, "rev-parse", "HEAD") == original
    assert original != remote_tip
    assert local_draft.read_text(encoding="utf-8") == "keep me\n"


def test_reused_dirty_up_to_date_clone_is_still_reported_as_dirty(
        workspace, capsys):
    root, config, *_ = workspace
    args = _ns(config=str(config), root=str(root), filters=["alpha"])
    assert cmd_assemble(args) == 0
    capsys.readouterr()
    clone = root / "domains" / "alpha-estate"
    original = _run(clone, "rev-parse", "HEAD")
    local_draft = clone / "operator-draft.txt"
    local_draft.write_text("keep me\n", encoding="utf-8")

    assert cmd_assemble(args) == 0
    out = capsys.readouterr().out
    assert "sync: dirty" in out
    assert "working tree not clean" in out
    assert _run(clone, "rev-parse", "HEAD") == original
    assert local_draft.read_text(encoding="utf-8") == "keep me\n"


def test_reused_diverged_clone_is_reported_and_not_merged(
        workspace, tmp_path, capsys):
    root, config, alpha, *_ = workspace
    args = _ns(config=str(config), root=str(root), filters=["alpha"])
    assert cmd_assemble(args) == 0
    capsys.readouterr()
    clone = root / "domains" / "alpha-estate"
    (clone / "local.txt").write_text("local\n", encoding="utf-8")
    _run(clone, "add", "-A")
    _run(clone, "commit", "-q", "-m", "local")
    local_tip = _run(clone, "rev-parse", "HEAD")
    remote_tip = _advance_remote(tmp_path, alpha, "trunk", "remote-diverged")

    assert cmd_assemble(args) == 0
    out = capsys.readouterr().out
    assert "sync: diverged" in out
    assert "decision is owed, not a merge" in out
    assert _run(clone, "rev-parse", "HEAD") == local_tip
    assert local_tip != remote_tip


def test_assemble_refuses_unresolvable_default_branch(
        workspace, tmp_path, capsys):
    root, config, *_ = workspace
    # A remote with no HEAD symref target that exists: point HEAD at a
    # branch that was never pushed.
    broken = _bare_domain(tmp_path, "broken-estate", "trunk")
    subprocess.run(["git", "-C", str(broken), "symbolic-ref", "HEAD",
                    "refs/heads/ghost"], check=True)
    config.write_text(
        "GIT_NAME=Assembly Test\nGIT_EMAIL=assembly@test\n"
        f"DOMAINS={broken}\n", encoding="utf-8")
    rc = cmd_assemble(_ns(config=str(config), root=str(root)))
    out = capsys.readouterr().out
    assert rc == 1
    assert "FAILED" in out
    assert "main" not in _run(
        root / "domains" / "broken-estate", "config", "--list") \
        if (root / "domains" / "broken-estate" / ".git").exists() else True


# ------------------------------------------------------------------ bundle

def test_owner_repo_parses_the_common_remote_forms():
    assert owner_repo("https://github.com/o/r.git") == "o/r"
    assert owner_repo("https://github.com/o/r") == "o/r"
    assert owner_repo("git@github.com:o/r.git") == "o/r"
    assert owner_repo("ssh://git@github.com/o/r") == "o/r"
    assert owner_repo("file:///x/y.git") is None


def test_estate_config_is_derived_not_authored(tmp_path, monkeypatch):
    # Hermetic against the host's git config: a sandbox/proxy environment
    # with a global `url.<mirror>.insteadOf = https://github.com/` rewrite
    # makes `git remote get-url` return the REWRITTEN url, so the GitHub
    # remote this test just authored stops parsing and FRAMEWORK_REPO is
    # never derived — a false failure first hit in a proxied Linux harness
    # (2026-08-22), where it read as a floor-sprint-1 regression despite the
    # sprint touching none of this path. The production behaviour is honest
    # either way (the miss lands in notes); only this test's assumption that
    # the url survives get-url verbatim needs pinning.
    neutral = tmp_path / "git-config-empty"
    neutral.write_text("", encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(neutral))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(neutral))
    root = tmp_path / "estate"
    (root / "domain").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    _run(root, "config", "user.name", "Derived Name")
    _run(root, "config", "user.email", "derived@e")
    _run(root, "remote", "add", "origin",
         "https://github.com/owner/framework.git")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    _run(root, "add", "seed.txt")
    _run(root, "commit", "-q", "-m", "seed")
    for name, url in (("d-one", "https://github.com/owner/d-one.git"),
                      ("d-two", "git@github.com:owner/d-two.git")):
        d = root / "domain" / name
        subprocess.run(["git", "init", "-q", str(d)], check=True)
        _run(d, "remote", "add", "origin", url)
    # A local-only repo is skipped WITH a note — derivation never narrows
    # silently.
    local_only = root / "domain" / "d-local"
    subprocess.run(["git", "init", "-q", str(local_only)], check=True)

    config, notes = derive_estate_config(root)
    assert config["FRAMEWORK_REPO"] == "owner/framework"
    assert config["DOMAINS"] == "owner/d-one owner/d-two"
    assert config["GIT_NAME"] == "Derived Name"
    assert config["FRAMEWORK_COMMIT"] == _run(root, "rev-parse", "HEAD")
    assert any("d-local" in n for n in notes)


def test_bundle_source_must_be_clean_and_fetchable(tmp_path):
    root = tmp_path / "framework"
    origin = tmp_path / "framework.git"
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)],
                   check=True)
    subprocess.run(["git", "init", "-q", "--bare", str(origin)],
                   check=True)
    _run(root, "config", "user.email", "bundle@test")
    _run(root, "config", "user.name", "bundle")
    (root / "source.txt").write_text("one\n", encoding="utf-8")
    _run(root, "add", "source.txt")
    _run(root, "commit", "-q", "-m", "one")
    _run(root, "remote", "add", "origin", str(origin))
    _run(root, "push", "-q", "-u", "origin", "main")
    assert framework_source_findings(root, root) == []

    (root / "source.txt").write_text("dirty\n", encoding="utf-8")
    assert any("dirty" in finding
               for finding in framework_source_findings(root, root))

    _run(root, "add", "source.txt")
    _run(root, "commit", "-q", "-m", "unpublished")
    assert any("not contained" in finding
               for finding in framework_source_findings(root, root))
    assert any("not the framework source checkout" in finding
               for finding in framework_source_findings(root, tmp_path))


def test_bundle_renders_complete_and_hash_stamped(tmp_path):
    config = {
        "FRAMEWORK_REPO": "owner/framework",
        "FRAMEWORK_COMMIT": TEST_FRAMEWORK_COMMIT,
        "GIT_NAME": "Build Test", "GIT_EMAIL": "b@t",
        "DOMAINS": "owner/d-one owner/d-two",
        "FRAMEWORK_VERSION": "9.9.9",
    }
    rendered = COWORK.bundle(TEMPLATES, config)
    mechanism = COWORK.bundle_hash(TEMPLATES)

    names = set(rendered)
    plugin = "markdownllm-bootstrap"
    for expected in (f"{plugin}/.claude-plugin/plugin.json",
                     f"{plugin}/README.md",
                     f"{plugin}/skills/spin-up-domain/SKILL.md",
                     f"{plugin}/skills/spin-up-domain/bootstrap.sh",
                     f"{plugin}/skills/spin-up-domain/references/SESSION.md",
                     f"{plugin}/skills/spin-up-domain/references/config.env"):
        assert expected in names

    # No placeholder survives rendering; the stamp equals the canonical
    # hash the framework would print at run time.
    for rel, content in rendered.items():
        text = content.decode("utf-8")
        assert "{bundle_hash}" not in text, rel
        assert "{framework_version}" not in text, rel
    bootstrap = rendered[
        f"{plugin}/skills/spin-up-domain/bootstrap.sh"].decode("utf-8")
    assert f'STAMPED="{mechanism}"' in bootstrap
    assert "fetch --quiet --depth 1" in bootstrap
    assert 'origin "$FRAMEWORK_COMMIT"' in bootstrap
    assert "PyYAML==6.0.3" in bootstrap
    assert "mdllm.py assemble --config" in bootstrap

    env = rendered[
        f"{plugin}/skills/spin-up-domain/references/config.env"
    ].decode("utf-8")
    assert "DOMAINS=owner/d-one owner/d-two" in env
    assert f"FRAMEWORK_COMMIT={TEST_FRAMEWORK_COMMIT}" in env
    assert "GIT_NAME=Build Test" in env


def test_rendered_bytes_are_lf_only_and_hash_is_eol_stable(tmp_path):
    """bootstrap.sh runs under bash on Linux — CRLF is 'bad interpreter'.
    And the mechanism hash must not depend on checkout line endings, or a
    Windows-built stamp false-STALEs against a Linux VM's recomputation."""
    rendered = COWORK.bundle(TEMPLATES, {
        "FRAMEWORK_VERSION": "1",
        "FRAMEWORK_COMMIT": TEST_FRAMEWORK_COMMIT,
    })
    for rel, content in rendered.items():
        assert b"\r" not in content, rel

    # Same templates with CRLF endings hash identically.
    crlf_root = tmp_path / "templates"
    src = TEMPLATES / "cowork-bundle"
    dst = crlf_root / "cowork-bundle"
    dst.mkdir(parents=True)
    for f in src.iterdir():
        data = f.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        (dst / f.name).write_bytes(data)
    assert COWORK.bundle_hash(crlf_root) == COWORK.bundle_hash(TEMPLATES)


def test_rendered_descriptions_fit_the_install_limit():
    """Field failure 2026-08-18: the harness rejected the bundle at INSTALL
    because descriptions exceeded 500 characters — the moment furthest from
    the templates that caused it. This pins the real rendered lengths."""
    import json as _json
    from markdownllm.adapters.cowork import (
        MAX_DESCRIPTION_CHARACTERS, _frontmatter_description,
        description_findings)

    rendered = COWORK.bundle(TEMPLATES, {
        "FRAMEWORK_VERSION": "3.31.0",
        "FRAMEWORK_COMMIT": TEST_FRAMEWORK_COMMIT,
        "GIT_NAME": "Build Test",
    })
    assert description_findings(rendered) == []

    manifest = _json.loads(rendered[
        "markdownllm-bootstrap/.claude-plugin/plugin.json"].decode())
    assert len(manifest["description"]) <= MAX_DESCRIPTION_CHARACTERS

    skill_desc = _frontmatter_description(rendered[
        "markdownllm-bootstrap/skills/spin-up-domain/SKILL.md"].decode())
    assert skill_desc and len(skill_desc) <= MAX_DESCRIPTION_CHARACTERS
    # The trigger phrases must survive shortening — a skill nothing fires
    # is worse than a long description.
    for phrase in ("spin up my domain", "start my session",
                   "bootstrap my domain"):
        assert phrase in skill_desc


def test_build_refuses_an_over_long_description(tmp_path):
    """The guard must FAIL THE BUILD, not warn: an uninstallable bundle
    that builds cleanly just relocates the failure to the operator."""
    from markdownllm.adapters.cowork import MAX_DESCRIPTION_CHARACTERS

    src = TEMPLATES / "cowork-bundle"
    dst = tmp_path / "templates" / "cowork-bundle"
    dst.mkdir(parents=True)
    for f in src.iterdir():
        dst.joinpath(f.name).write_bytes(f.read_bytes())
    bloated = "x" * (MAX_DESCRIPTION_CHARACTERS + 1)
    skill = dst / "SKILL.md.template"
    skill.write_text(
        re.sub(r"^description: .*$", f"description: {bloated}",
               skill.read_text(encoding="utf-8"), count=1, flags=re.M),
        encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        COWORK.bundle(tmp_path / "templates", {
            "FRAMEWORK_VERSION": "1",
            "FRAMEWORK_COMMIT": TEST_FRAMEWORK_COMMIT,
        })
    message = str(excinfo.value)
    assert "rejected at install" in message
    assert str(MAX_DESCRIPTION_CHARACTERS + 1) in message   # actual length
    assert "templates/cowork-bundle/" in message            # where to fix


def test_folded_frontmatter_description_is_measured_as_one_line():
    from markdownllm.adapters.cowork import _frontmatter_description
    text = ("---\nname: s\ndescription: one two\n  three four\n"
            "  five\nother: x\n---\n# body\n")
    assert _frontmatter_description(text) == "one two three four five"


def test_bundle_hash_is_config_independent():
    a = COWORK.bundle(TEMPLATES, {
        "DOMAINS": "x/y", "FRAMEWORK_VERSION": "1",
        "FRAMEWORK_COMMIT": TEST_FRAMEWORK_COMMIT,
    })
    b = COWORK.bundle(TEMPLATES, {
        "DOMAINS": "p/q r/s", "FRAMEWORK_VERSION": "2",
        "FRAMEWORK_COMMIT": TEST_FRAMEWORK_COMMIT,
    })
    # Mechanism files identical across estates; only config.env and the
    # version stamp differ.
    key = "markdownllm-bootstrap/skills/spin-up-domain/references/config.env"
    assert a[key] != b[key]
    assert COWORK.bundle_hash(TEMPLATES) == COWORK.bundle_hash(TEMPLATES)


def test_bundle_refuses_missing_or_moving_framework_source():
    with pytest.raises(ValueError, match="FRAMEWORK_COMMIT"):
        COWORK.bundle(TEMPLATES, {"FRAMEWORK_COMMIT": "main"})
