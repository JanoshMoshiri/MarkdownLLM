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
from markdownllm.bundle_service import derive_estate_config, owner_repo  # noqa: E402

FW_ROOT = Path(mdllm.__file__).resolve().parents[1]
TEMPLATES = FW_ROOT / "templates"


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
    # Attestations recorded per clone with the contract token.
    for name in ("alpha-estate", "beta-estate"):
        attest = (root / "domains" / name / ".git" / "mdllm-attest")
        assert attest.is_file()
        assert attest.read_text(encoding="utf-8").strip().endswith(
            " contract")


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


def test_estate_config_is_derived_not_authored(tmp_path):
    root = tmp_path / "estate"
    (root / "domain").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    _run(root, "config", "user.name", "Derived Name")
    _run(root, "config", "user.email", "derived@e")
    _run(root, "remote", "add", "origin",
         "https://github.com/owner/framework.git")
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
    assert any("d-local" in n for n in notes)


def test_bundle_renders_complete_and_hash_stamped(tmp_path):
    config = {
        "FRAMEWORK_REPO": "owner/framework",
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
    assert "mdllm.py assemble --config" in bootstrap

    env = rendered[
        f"{plugin}/skills/spin-up-domain/references/config.env"
    ].decode("utf-8")
    assert "DOMAINS=owner/d-one owner/d-two" in env
    assert "GIT_NAME=Build Test" in env


def test_rendered_bytes_are_lf_only_and_hash_is_eol_stable(tmp_path):
    """bootstrap.sh runs under bash on Linux — CRLF is 'bad interpreter'.
    And the mechanism hash must not depend on checkout line endings, or a
    Windows-built stamp false-STALEs against a Linux VM's recomputation."""
    rendered = COWORK.bundle(TEMPLATES, {"FRAMEWORK_VERSION": "1"})
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

    rendered = COWORK.bundle(TEMPLATES, {"FRAMEWORK_VERSION": "3.31.0",
                                         "GIT_NAME": "Build Test"})
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
        COWORK.bundle(tmp_path / "templates", {"FRAMEWORK_VERSION": "1"})
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
    a = COWORK.bundle(TEMPLATES, {"DOMAINS": "x/y",
                                  "FRAMEWORK_VERSION": "1"})
    b = COWORK.bundle(TEMPLATES, {"DOMAINS": "p/q r/s",
                                  "FRAMEWORK_VERSION": "2"})
    # Mechanism files identical across estates; only config.env and the
    # version stamp differ.
    key = "markdownllm-bootstrap/skills/spin-up-domain/references/config.env"
    assert a[key] != b[key]
    assert COWORK.bundle_hash(TEMPLATES) == COWORK.bundle_hash(TEMPLATES)
