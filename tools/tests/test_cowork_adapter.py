"""Phase 0 of the ``cowork-adapter`` plan: the third registered harness.

Cowork is estate-level and run-time bound — an account-level bundle
assembles the workspace after the session starts, so no per-domain artifact
ever exists. The honest diagnostic states pinned here are the port stretch
that registration forced:

- project configuration is **not-applicable** (never "absent", which would
  prescribe `adapter-install` toward a harness with no place for it);
- execution is **untested** until a real bootstrap attests against a
  probe-supplied fingerprint (Phase 3) — installation is not activation;
- post-write feedback is **unsupported**, stated rather than implied:
  writes meet the floor at commit time.

Run: python -m pytest tools/tests/test_cowork_adapter.py -q
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402  (registers tools/ on sys.path side effects)
from markdownllm import adapters  # noqa: E402
from markdownllm.adapters.cowork import COWORK  # noqa: E402
from markdownllm.harness_diagnostics import diagnose_harness  # noqa: E402
from markdownllm.harness_ports import (  # noqa: E402
    HarnessContext, InspectPort, RenderPort,
)


def _ns(**kw):
    import argparse
    defaults = {"harness": None}
    defaults.update(kw)
    return argparse.Namespace(**defaults)


def _git_repo(p: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=p, check=True)


CTX = HarnessContext(framework_root_rel="../..")


# ----------------------------------------------------------------- registry

def test_registered_with_honest_capabilities():
    assert "cowork" in adapters.names()
    adapter = adapters.get("cowork")
    assert isinstance(adapter, RenderPort)
    assert isinstance(adapter, InspectPort)
    caps = adapter.capabilities()
    assert caps.harness == "cowork"
    # session-start is bound (at run time, by the bundle); post-write is NOT —
    # nothing in Cowork fires validation on individual writes.
    assert caps.lifecycle_moments == ("session-start",)
    assert "run time" in caps.notes
    assert "post-write" in caps.notes or "commit time" in caps.notes


def test_default_harness_unchanged():
    # Registering a third adapter is not a product decision about defaults
    # (that is the foundation plan's Phase 8, owner: operator).
    assert adapters.DEFAULT_HARNESS == "claude-code"
    assert "cowork" in adapters.selection_choices()


# ------------------------------------------------------- honest emptiness

def test_renders_no_project_artifacts():
    assert COWORK.render(CTX) == {}
    assert COWORK.render(HarnessContext(framework_root_rel=".")) == {}


def test_inspect_reports_nothing_to_find(tmp_path):
    report = COWORK.inspect(tmp_path, CTX)
    assert report.harness == "cowork"
    assert report.fragments == ()
    # No fragment can ever satisfy doctor's presence detection —
    # `any(fragment.artifact_present ...)` over an empty tuple is False —
    # so repo contents can never claim a Cowork installation exists.
    assert not any(f.artifact_present for f in report.fragments)


# ------------------------------------------------------------- diagnostics

def test_diagnose_session_start_is_not_applicable_configuration(tmp_path):
    diagnostic = diagnose_harness(COWORK, tmp_path, CTX)
    facts = {f.capability: f for f in diagnostic.capabilities}

    ss = facts["session-start"]
    assert ss.support == "supported"
    assert ss.configuration == "not-applicable"
    assert ss.currency == "not-applicable"
    assert ss.legacy_id is None
    assert ss.launch_currency == "not-applicable"
    assert ss.trust == "unknown"  # Cowork exposes no project-trust surface
    # Untested until a real bootstrap attests against a Phase 3 fingerprint.
    assert ss.execution.state == "untested"
    assert "fingerprint" in ss.execution.detail
    # The absent-configuration remediation must NOT fire: there is nothing
    # to adapter-install toward this harness.
    assert not any("adapter-install" in r for r in ss.remediations)
    # The honest remediation that does fire: a real event, not a static probe.
    assert any("real session-start event" in r for r in ss.remediations)


def test_diagnose_post_write_is_unsupported(tmp_path):
    diagnostic = diagnose_harness(COWORK, tmp_path, CTX)
    facts = {f.capability: f for f in diagnostic.capabilities}

    pw = facts["post-write"]
    assert pw.support == "unsupported"
    assert pw.configuration == "not-applicable"
    assert pw.currency == "not-applicable"
    assert pw.execution.state == "not-applicable"
    assert pw.trust == "not-applicable"


def test_render_time_adapters_unaffected_by_the_stretch(tmp_path):
    # The not-applicable branch keys on an empty render, so the render-time
    # adapters must keep their existing absent-configuration reading on an
    # empty domain (their renderers emit artifacts; configuration facts stay
    # derived from inspection).
    claude = adapters.get("claude-code")
    diagnostic = diagnose_harness(claude, tmp_path, CTX)
    facts = {f.capability: f for f in diagnostic.capabilities}
    assert facts["session-start"].configuration != "not-applicable"


# ------------------------------------------------------------------ scaffold

def test_scaffold_cowork_selection_equals_none_selection(tmp_path):
    """`--harness cowork` must add not one byte over `--harness none`:
    the entry pointers are neutral scaffold surface, and Cowork's projection
    is honestly empty."""
    # Same domain basename in two parents: scaffold derives skill filenames
    # from the domain name, and this comparison is about adapter surface only.
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    _git_repo(tmp_path / "a")
    _git_repo(tmp_path / "b")
    none_target = tmp_path / "a" / "parity-domain"
    cowork_target = tmp_path / "b" / "parity-domain"
    assert mdllm.cmd_scaffold(_ns(path=str(none_target), harness="none")) == 0
    assert mdllm.cmd_scaffold(
        _ns(path=str(cowork_target), harness="cowork")) == 0

    def tree(root: Path) -> set[str]:
        return {p.relative_to(root).as_posix()
                for p in root.rglob("*")
                if p.is_file() and ".git" not in p.relative_to(root).parts}

    assert tree(cowork_target) == tree(none_target)


def test_harness_event_refuses_cowork_without_output_port(tmp_path):
    # Phase 0 deliberately does not bind the neutral runner: the bundle
    # integration (and its output envelope) is Phase 3's decision. Until
    # then the CLI must refuse honestly, not crash.
    from markdownllm.lifecycle_runner import cmd_harness_event
    rc = cmd_harness_event(_ns(
        harness="cowork", moment="session-start", path=str(tmp_path),
        definition_hash="unused"))
    assert rc == 2
