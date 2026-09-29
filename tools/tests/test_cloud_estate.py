"""Multi-repository cloud contracts, with real isolated Git remotes."""
import copy
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from test_cloud_workspace import SOURCE, estate, git, init
from markdownllm import cloud_bootstrap as boot
from markdownllm.adapters.codex import CODEX
from markdownllm.cloud_repositories import assemble_extra, complete_history, layout, provision_boundary
from markdownllm.cloud_service import write_artifacts
from markdownllm.sync import SyncState, autopush_repo, publication_policy, sync_repo


def config_v2(old):
    return {"schema_version": 2, "framework_repo": old["framework_repo"],
            "framework_commit": old["framework_commit"], "workspace_directory": old["workspace_directory"],
            "primary": {"repo": old["domain_repo"], "kind": "domain", "credential_env": None,
                        "boundary_terms_env": None}, "repositories": []}


def entry(name="reference", kind="domain", access="read", publication="manual"):
    return dict(name=name, repo=f"https://github.com/fixture/{name}.git", kind=kind,
                revision={"branch": "trunk"}, access=access, publication=publication,
                credential_env=None, boundary_terms_env=None)


def source_repo(tmp_path, spec):
    source = tmp_path / (spec["name"] + "-source")
    init(source)
    if spec["kind"] == "domain":
        (source / "AGENTS.md").write_text("---\nname: Fixture\nframework_root: ../..\n"
                                         "git:\n  autopush: true\n---\n# Fixture\n")
        (source / "_schema.yaml").write_text("options:\n  session_gate: strict\n")
        (source / ".gitignore").write_text(".boundary-terms\n")
    else:
        # Would be invalid if this were incorrectly treated as a domain thing.
        (source / "README.md").write_text("---\nid: not-a-domain\n---\n# Code\n")
    git(source, "add", ".")
    git(source, "commit", "-qm", "fixture")
    remote = tmp_path / (spec["name"] + "-remote.git")
    subprocess.run(["git", "clone", "--bare", str(source), str(remote)], check=True, capture_output=True)
    subprocess.run(["git", "config", "--global", f"url.{remote.as_uri()}.insteadOf", spec["repo"]], check=True)
    return source, remote


def test_manifest_rejects_ambiguous_or_unsafe_estates():
    from test_cloud_workspace import config
    cfg = config_v2(config())
    cfg["repositories"] = [entry()]
    boot.validate_config(cfg)
    mutations = [
        ("name", "../escape"), ("name", "engineering"), ("kind", "unknown"),
        ("repo", "https://secret@github.com/fixture/private.git"),
        ("credential_env", "token; echo secret"), ("credential_env", "github_pat_literal"),
        ("revision", {"branch": "main", "commit": "a" * 40}),
        ("revision", {"branch": "--upload-pack=evil"}), ("revision", {"commit": "main"}),
        ("publication", "declared"), ("access", True),
    ]
    for key, value in mutations:
        changed = copy.deepcopy(cfg)
        changed["repositories"][0][key] = value
        with pytest.raises(ValueError):
            boot.validate_config(changed)
    changed = copy.deepcopy(cfg)
    changed["repositories"] *= 2
    with pytest.raises(ValueError):
        boot.validate_config(changed)
    changed = copy.deepcopy(cfg)
    changed["repositories"][0].update(access="write", revision={"commit": "a" * 40})
    with pytest.raises(ValueError):
        boot.validate_config(changed)


@pytest.mark.parametrize("protocol,host,path,operation,allowed", [
    ("https", "github.com", "fixture/reference.git", "get", True),
    ("https", "github.com", "fixture/reference", "get", True),
    ("http", "github.com", "fixture/reference.git", "get", False),
    ("https", "evil.invalid", "fixture/reference.git", "get", False),
    ("https", "github.com", "fixture/other.git", "get", False),
    ("https", "github.com", "fixture/reference.git", "store", False),
])
def test_credential_protocol_is_exact_repo_scoped(monkeypatch, capsys, protocol, host, path, operation, allowed):
    monkeypatch.setenv("MDLLM_TEST_AUTH", "fixture-credential-do-not-log")
    monkeypatch.setattr(sys, "stdin", io.StringIO(f"protocol={protocol}\nhost={host}\npath={path}\n\n"))
    boot.credential_response("MDLLM_TEST_AUTH", entry()["repo"], operation)
    output = capsys.readouterr().out
    assert ("password=fixture-credential-do-not-log" in output) is allowed


def test_missing_token_is_a_phase_failure_without_persistence(monkeypatch):
    spec = entry()
    spec["credential_env"] = "MDLLM_TEST_MISSING"
    monkeypatch.delenv(spec["credential_env"], raising=False)
    with pytest.raises(ValueError, match="unavailable in this phase"):
        boot.auth_options(spec)
    monkeypatch.setenv(spec["credential_env"], "fixture-private-token")
    assert "fixture-private-token" not in " ".join(boot.auth_options(spec))


def test_real_helper_is_idempotent_and_never_stores_token(estate, monkeypatch):
    _, domain, _ = estate
    spec = dict(entry(), repo="https://github.com/fixture/engineering.git", credential_env="MDLLM_TEST_AUTH")
    monkeypatch.setenv("MDLLM_TEST_AUTH", "fixture-private-token")
    boot.install_credentials(domain, spec)
    boot.install_credentials(domain, spec)
    assert "fixture-private-token" not in (domain / ".git/config").read_text()
    request = "protocol=https\nhost=github.com\npath=fixture/engineering.git\n\n"
    result = subprocess.run(["git", "credential", "fill"], cwd=domain, input=request,
                            text=True, capture_output=True, check=True)
    assert "password=fixture-private-token" in result.stdout
    monkeypatch.delenv("MDLLM_TEST_AUTH")
    result = subprocess.run(["git", "credential", "fill"], cwd=domain, input=request,
                            text=True, capture_output=True, env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    assert result.returncode != 0
    assert "fixture-private-token" not in result.stdout + result.stderr


def test_history_repair_restores_origin_but_preserves_host_head(estate, tmp_path):
    root, domain, old = estate
    spec = dict(entry("history"), repo=old["domain_repo"])
    source, remote = source_repo(tmp_path, spec)
    (source / "later.txt").write_text("later")
    git(source, "add", ".")
    git(source, "commit", "-qm", "later")
    git(source, "push", str(remote), "trunk")
    clone = tmp_path / "shallow"
    subprocess.run(["git", "clone", "--depth=1", remote.as_uri(), str(clone)], check=True, capture_output=True)
    git(clone, "remote", "remove", "origin")
    git(clone, "checkout", "--detach")
    head = git(clone, "rev-parse", "HEAD")
    complete_history(clone, spec, primary=True)
    assert git(clone, "rev-parse", "--is-shallow-repository") == "false"
    assert git(clone, "rev-parse", "HEAD") == head
    assert git(clone, "rev-parse", "--abbrev-ref", "HEAD") == "HEAD"


def test_multi_repo_real_setup_resume_and_publication(estate, tmp_path, monkeypatch):
    root, primary, old = estate
    cfg = config_v2(old)
    references = entry("reference")
    writable = entry("working", access="write", publication="declared")
    code = entry("product", kind="repository", access="write")
    sources = {}
    for spec in (references, writable, code):
        sources[spec["name"]] = source_repo(tmp_path, spec)
    references["revision"] = {"commit": git(sources["reference"][0], "rev-parse", "HEAD")}
    writable["credential_env"] = "MDLLM_TEST_AUTH"
    writable["boundary_terms_env"] = "MDLLM_TEST_BOUNDARY"
    monkeypatch.setenv("MDLLM_TEST_AUTH", "fixture-private-token")
    monkeypatch.setenv("MDLLM_TEST_BOUNDARY", "private-fixture-term\n")
    cfg["repositories"] = [references, writable, code]
    boot.validate_config(cfg)
    write_artifacts(primary, CODEX.cloud_artifacts(SOURCE, cfg))
    git(primary, "add", ".")
    git(primary, "commit", "-qm", "configure cloud")
    git(primary, "checkout", "--detach")
    head = git(primary, "rev-parse", "HEAD")
    for mode in ("setup", "maintenance"):
        result = subprocess.run(["bash", str(primary / ".codex/cloud/bootstrap.sh"), mode], cwd=primary,
                                text=True, capture_output=True, timeout=180)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "fixture-private-token" not in result.stdout + result.stderr
        assert "private-fixture-term" not in result.stdout + result.stderr
        assert git(primary, "rev-parse", "HEAD") == head
        assert git(primary, "status", "--porcelain") == ""
        assert not (primary / ".git/mdllm-attest").exists()
    read_repo, write_repo, code_repo = [p for _, p in layout(cfg, primary)[1:]]
    assert not publication_policy(primary).enabled
    assert not publication_policy(read_repo).enabled
    assert publication_policy(write_repo).enabled
    assert not publication_policy(code_repo).enabled
    assert (write_repo / ".boundary-terms").read_text() == "private-fixture-term\n"
    assert not (code_repo / ".git/hooks/pre-commit").exists()
    assert git(root, "status", "--porcelain") == ""
    assert git(root, "rev-parse", "--is-shallow-repository") == "false"
    python = root / ".venv/bin/python"
    cli = root / "tools/mdllm.py"
    emitted = subprocess.run([str(python), str(cli), "cloud", "start", str(primary), "--repository", "working"],
                             text=True, capture_output=True, timeout=60)
    assert emitted.returncode == 0, emitted.stdout + emitted.stderr
    assert "Fixture kernel" in emitted.stdout
    assert "full triggers" in emitted.stdout
    assert "imports coverage" in emitted.stdout
    git(write_repo, "config", "user.name", "Fixture")
    git(write_repo, "config", "user.email", "fixture@example.invalid")
    (write_repo / "accepted.md").write_text("---\nid: accepted\ntype: task\nstatus: completed\ncreated: 2026-09-27\n---\n# Accepted\n")
    git(write_repo, "add", "accepted.md")
    git(write_repo, "commit", "-m", "complete: fixture")
    assert git(sources["working"][1], "rev-parse", "trunk") == git(write_repo, "rev-parse", "HEAD")
    git(write_repo, "checkout", "-qb", "wrong-branch")
    assert autopush_repo(write_repo)["state"] == "wrong-branch"
    assert git(sources["working"][1], "rev-parse", "trunk") == git(write_repo, "rev-parse", "HEAD")
    # The substrate's corpus does not ingest ordinary repositories' markdown.
    from markdownllm.model import scan
    corpus, _ = scan(root)
    assert all(thing.id != "not-a-domain" for thing in corpus.things)


def test_cached_drafts_and_pin_changes_are_never_overwritten(estate, tmp_path):
    root, primary, old = estate
    spec = entry()
    source_repo(tmp_path, spec)
    boot.materialise(old, primary)
    target = root / "domains" / spec["name"]
    assemble_extra(root, spec, target, maintenance=False)
    (target / "draft.txt").write_text("preserve")
    with pytest.raises(ValueError, match="drafts"):
        assemble_extra(root, spec, target, maintenance=True)
    assert (target / "draft.txt").read_text() == "preserve"
    cfg = config_v2(old)
    boot.materialise(cfg, primary)
    cfg["repositories"] = [spec]
    with pytest.raises(ValueError, match="configuration changed"):
        boot.materialise(cfg, primary)


def test_boundary_requires_ignored_path_and_preserves_existing_bytes(estate, monkeypatch):
    _, domain, _ = estate
    spec = dict(entry(), boundary_terms_env="MDLLM_TEST_BOUNDARY")
    monkeypatch.setenv("MDLLM_TEST_BOUNDARY", "private-term\n")
    with pytest.raises(ValueError):
        provision_boundary(domain, spec)
    (domain / ".gitignore").write_text(".boundary-terms\n")
    provision_boundary(domain, spec)
    monkeypatch.setenv("MDLLM_TEST_BOUNDARY", "different-term\n")
    with pytest.raises(ValueError, match="differs"):
        provision_boundary(domain, spec)
    assert (domain / ".boundary-terms").read_text() == "private-term\n"


def test_host_selected_branch_is_observed_without_fast_forward(estate, tmp_path):
    _, _, _ = estate
    spec = entry("hostbranch", kind="repository")
    source, remote = source_repo(tmp_path, spec)
    clone = tmp_path / "hostbranch"
    subprocess.run(["git", "clone", "--quiet", remote.as_uri(), str(clone)], check=True)
    git(clone, "config", "mdllm.sync", "observe")
    selected = git(clone, "rev-parse", "HEAD")
    (source / "later.txt").write_text("remote state")
    git(source, "add", "later.txt")
    git(source, "commit", "-qm", "later")
    git(source, "push", str(remote), "trunk")
    state = sync_repo(clone)
    assert state.state is SyncState.PINNED
    assert "+0 local / +1 remote" in state.detail
    assert git(clone, "rev-parse", "HEAD") == selected


def test_primary_ordinary_code_keeps_its_own_hooks(estate, tmp_path):
    root, domain, old = estate
    boot.materialise(old, domain)
    primary = root / "repositories" / "product-primary"
    spec = entry("product-primary", kind="repository", access="write")
    init(primary)
    git(primary, "remote", "add", "origin", spec["repo"])
    (primary / "README.md").write_text("# Ordinary product\n")
    git(primary, "add", ".")
    git(primary, "commit", "-qm", "product")
    cfg = config_v2(old)
    cfg["workspace_directory"] = primary.parent.as_posix()
    cfg["primary"] = dict(repo=spec["repo"], kind="repository",
                          credential_env=None, boundary_terms_env=None)
    write_artifacts(primary, CODEX.cloud_artifacts(SOURCE, cfg))
    git(primary, "add", ".")
    git(primary, "commit", "-qm", "cloud files")
    before = git(primary, "rev-parse", "HEAD")
    result = subprocess.run(["bash", str(primary / ".codex/cloud/bootstrap.sh")], cwd=primary,
                            text=True, capture_output=True, timeout=180)
    assert result.returncode == 0, result.stdout + result.stderr
    assert git(primary, "rev-parse", "HEAD") == before
    assert not (primary / ".git/hooks/pre-commit").exists()
    assert git(primary, "config", "--local", "mdllm.publication") == "pr"
    assert git(primary, "config", "--local", "mdllm.sync") == "observe"


def test_declared_publication_requires_remote_default(estate, tmp_path):
    root, primary, old = estate
    boot.materialise(old, primary)
    spec = entry("feature-domain", access="write", publication="declared")
    source, remote = source_repo(tmp_path, spec)
    git(source, "checkout", "-qb", "feature")
    git(source, "push", str(remote), "feature")
    spec["revision"] = {"branch": "feature"}
    target = root / "domains" / spec["name"]
    with pytest.raises(ValueError, match="remote default branch"):
        assemble_extra(root, spec, target, maintenance=False)
    assert git(target, "rev-parse", "--abbrev-ref", "HEAD") == "feature"
