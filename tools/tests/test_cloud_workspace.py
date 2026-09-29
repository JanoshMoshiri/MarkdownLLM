"""Existing-checkout bootstrap: real Git and floor execution on Linux."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from markdownllm import cloud_bootstrap as boot
from markdownllm.adapters.codex import CODEX
from markdownllm.cloud_service import write_artifacts
from markdownllm.bundle_service import framework_source_findings
from markdownllm.sync import publication_policy, autopush_repo

SOURCE = Path(__file__).resolve().parents[2]


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], text=True,
                          capture_output=True, check=True).stdout.strip()


def init(root):
    root.mkdir(parents=True)
    git(root, "init", "-q", "-b", "trunk")
    git(root, "config", "user.name", "Fixture")
    git(root, "config", "user.email", "fixture@example.invalid")


def config(workspace="/workspace/MarkdownLLM/domain"):
    return dict(schema_version=1,
                framework_repo="https://github.com/fixture/framework.git",
                framework_commit="a" * 40,
                domain_repo="https://github.com/fixture/engineering.git",
                workspace_directory=workspace, publication="pr")


@pytest.fixture
def estate(tmp_path, monkeypatch):
    if os.name == "nt":
        pytest.skip("Linux VM contract; run this module under WSL as well")
    monkeypatch.delenv("GH_PAT", raising=False)
    monkeypatch.delenv("MDLLM_GIT_TOKEN", raising=False)
    neutral = tmp_path / "gitconfig"
    neutral.write_text("")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(neutral))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    framework = tmp_path / "published-framework"
    init(framework)
    shutil.copytree(SOURCE / "tools/markdownllm", framework / "tools/markdownllm",
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy2(SOURCE / "tools/mdllm.py", framework / "tools/mdllm.py")
    (framework / ".gitignore").write_text("domain/\ndomains/\nrepositories/\n.venv/\n__pycache__/\n")
    (framework / "_schema.yaml").write_text("exclude: [repositories]\n")
    (framework / ".markdownllm").write_text("framework: MarkdownLLM\nversion: 3.42.0\n")
    (framework / "kernel.md").write_text("# Fixture kernel\nRead the entry contract.\n")
    git(framework, "add", ".")
    git(framework, "commit", "-qm", "fixture framework")
    # The manifest stays a real HTTPS URL; Git's test-only rewrite supplies a
    # hermetic local remote without production exceptions for file URLs.
    subprocess.run(["git", "config", "--global",
                    f"url.{framework.as_uri()}.insteadOf",
                    "https://github.com/fixture/framework.git"], check=True)
    root = tmp_path / "workspace" / "MarkdownLLM"
    domain = root / "domain" / "engineering"
    init(domain)
    git(domain, "remote", "add", "origin", "https://github.com/fixture/engineering.git")
    (domain / "AGENTS.md").write_text(
        "---\nname: Engineering\nframework_root: ../..\n"
        "framework_version_seen: 3.42.0\ngit:\n  autopush: true\n---\n# Engineering\n")
    (domain / "_schema.yaml").write_text("options:\n  session_gate: strict\n")
    git(domain, "add", ".")
    git(domain, "commit", "-qm", "domain baseline")
    cfg = config(domain.parent.as_posix())
    cfg["framework_commit"] = git(framework, "rev-parse", "HEAD")
    return root, domain, cfg


def test_strict_manifest(tmp_path):
    path = tmp_path / "environment.json"
    path.write_text(json.dumps(config()))
    assert boot.load_config(path)["publication"] == "pr"
    path.write_text('{"schema_version":1,"schema_version":1}')
    with pytest.raises(ValueError, match="duplicate"):
        boot.load_config(path)
    for field, value in [("framework_commit", "main"), ("publication", True),
                         ("publication", "autopush"), ("schema_version", True),
                         ("workspace_directory", "/workspace/../domain"),
                         ("framework_repo", "https://token@github.com/a/b.git")]:
        cfg = config()
        cfg[field] = value
        with pytest.raises(ValueError):
            boot.validate_config(cfg)


def test_artifacts_are_lf_only_and_never_overwrite(tmp_path):
    rendered = CODEX.cloud_artifacts(SOURCE, config())
    assert all(b"\r" not in data for data in rendered.values())
    write_artifacts(tmp_path, rendered)
    write_artifacts(tmp_path, rendered, check=True)
    target = tmp_path / ".codex/cloud/bootstrap.sh"
    target.write_text("operator contents\n")
    with pytest.raises(ValueError, match="differs"):
        write_artifacts(tmp_path, rendered)
    assert target.read_text() == "operator contents\n"
    for escape in ("../escape", "/escape", "C:/escape", "..\\escape", "."):
        with pytest.raises(ValueError, match="escaping"):
            write_artifacts(tmp_path, {escape: b"bad"})


def test_preview_relaxes_only_publication(tmp_path):
    source = tmp_path / "framework"
    init(source)
    (source / "source.txt").write_text("committed")
    git(source, "add", ".")
    git(source, "commit", "-qm", "source")
    assert framework_source_findings(source, source)
    assert framework_source_findings(source, source, require_published=False) == []
    (source / "source.txt").write_text("uncommitted")
    assert any("dirty" in finding for finding in framework_source_findings(
        source, source, require_published=False))


def test_fresh_and_cached_assembly_preserve_selected_checkout(estate):
    root, domain, cfg = estate
    git(domain, "checkout", "--detach")
    (domain / "draft.txt").write_text("keep this draft")
    git(domain, "add", "draft.txt")
    state = (git(domain, "rev-parse", "HEAD"), git(domain, "write-tree"),
             git(domain, "status", "--porcelain"))
    assert boot.materialise(cfg, domain) == root
    assert boot.materialise(cfg, domain) == root
    assert state == (git(domain, "rev-parse", "HEAD"), git(domain, "write-tree"),
                     git(domain, "status", "--porcelain"))
    assert git(root, "status", "--porcelain") == ""
    assert git(domain, "rev-parse", "--abbrev-ref", "HEAD") == "HEAD"
    cfg["framework_commit"] = "b" * 40
    with pytest.raises(ValueError, match="reset the environment cache"):
        boot.materialise(cfg, domain)


def test_refuses_foreign_parent_before_writing(estate):
    root, domain, cfg = estate
    (root / "operator.txt").write_text("preserve")
    with pytest.raises(ValueError, match="unrelated"):
        boot.materialise(cfg, domain)
    assert not (root / ".git").exists()
    assert (root / "operator.txt").read_text() == "preserve"


def test_real_setup_maintenance_and_strict_commit_gate(estate):
    root, domain, cfg = estate
    rendered = CODEX.cloud_artifacts(SOURCE, cfg)
    write_artifacts(domain, rendered)
    git(domain, "add", ".")
    git(domain, "commit", "-qm", "cloud configuration")
    before = git(domain, "rev-parse", "HEAD")
    script = domain / ".codex/cloud/bootstrap.sh"
    env = dict(os.environ)
    for mode in ("setup", "maintenance"):
        result = subprocess.run(["bash", str(script), mode], cwd=domain,
                                env=env, text=True, capture_output=True, timeout=180)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "AGENT START REQUIRED" in result.stdout
        assert git(domain, "rev-parse", "HEAD") == before
        assert git(domain, "status", "--porcelain") == ""
        assert not (domain / ".git/mdllm-attest").exists()
    assert git(domain, "config", "--local", "mdllm.publication") == "pr"
    assert not publication_policy(domain).enabled
    assert autopush_repo(domain)["state"] == "off"
    # Existing floor really blocks before receipt, then accepts after actual
    # session-start emission. No setup-only exemption enters the commit hook.
    blocked = subprocess.run(["git", "hook", "run", "pre-commit"], cwd=domain,
                             text=True, capture_output=True, timeout=60)
    assert blocked.returncode != 0
    assert "session gate" in blocked.stdout + blocked.stderr
    python = root / ".venv/bin/python"
    emitted = subprocess.run([str(python), str(root / "tools/mdllm.py"),
                              "session-start", str(domain), "--contract"],
                             text=True, capture_output=True, timeout=60)
    assert emitted.returncode == 0, emitted.stdout + emitted.stderr
    assert "Fixture kernel" in emitted.stdout
    allowed = subprocess.run(["git", "hook", "run", "pre-commit"], cwd=domain,
                             text=True, capture_output=True, timeout=60)
    assert allowed.returncode == 0, allowed.stdout + allowed.stderr
    (domain / "bad.md").write_text("---\nid: invalid\ntype: task\nstatus: impossible\n---\nBad\n")
    git(domain, "add", "bad.md")
    invalid = subprocess.run(["git", "hook", "run", "pre-commit"], cwd=domain,
                             text=True, capture_output=True, timeout=60)
    assert invalid.returncode != 0
    failed_setup = subprocess.run(["bash", str(script), "maintenance"], cwd=domain,
                                  text=True, capture_output=True, timeout=180)
    assert failed_setup.returncode != 0
    assert "Workspace preparation failed validation" in failed_setup.stdout
    assert "Workspace prepared;" not in failed_setup.stdout


def test_clone_restraint_cannot_grant_authority(tmp_path):
    domain = tmp_path / "domain"
    init(domain)
    (domain / "AGENTS.md").write_text("---\ngit:\n  autopush: true\n---\n")
    assert publication_policy(domain).enabled
    for value in ("pr", "true", "", "garbage"):
        git(domain, "config", "--local", "mdllm.publication", value)
        assert not publication_policy(domain).enabled
        assert autopush_repo(domain)["state"] == "off"
    git(domain, "config", "--local", "--unset", "mdllm.publication")
    assert publication_policy(domain).enabled
