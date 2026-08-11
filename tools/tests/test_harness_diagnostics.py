"""Phase 3: independent, truthful harness-diagnostic dimensions."""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import harness_diagnostics as hd  # noqa: E402
from markdownllm import harness_ports as hp  # noqa: E402


CURRENT_HASH = hd.managed_definition_hash({
    "managed-command": "ordered lifecycle definition",
    "managed-metadata": b"timeout=120",
})


def _current_fragment(**kw) -> hp.ManagedFragment:
    values = dict(
        path="adapter.config", present=True, artifact_present=True,
        readable=True, valid=True, current=True,
        intents_realised={
            "session-start": ("estate-sync", "session-start"),
            "post-write": ("validate",),
        },
    )
    values.update(kw)
    return hp.ManagedFragment(**values)


class _Adapter:
    name = "test-harness"

    def __init__(self, report: hp.InspectionReport, *,
                 trust: hd.TrustState = "unknown",
                 hashes=None, remediations=(), ownership=()):
        self.report = report
        self.observation = hd.AdapterProbe(
            trust=trust,
            definition_hashes=hashes or {},
            remediations=remediations,
            ownership=ownership,
        )

    def capabilities(self):
        return hp.AdapterCapabilities(
            harness=self.name,
            lifecycle_moments=("session-start", "post-write"),
        )

    def render(self, context):
        return {"adapter.config": b"managed projection\n"}

    def inspect(self, domain_root, context):
        return self.report

    def probe(self, domain_root, context):
        return self.observation


class _NoProbeAdapter:
    """The required render/inspect ports, and deliberately nothing more."""

    name = "no-probe-harness"

    def capabilities(self):
        return hp.AdapterCapabilities(
            harness=self.name, lifecycle_moments=("session-start",))

    def render(self, context):
        return {"adapter.config": b"managed projection\n"}

    def inspect(self, domain_root, context):
        return hp.InspectionReport(
            harness=self.name, fragments=(_current_fragment(),))


def _report(fragment: hp.ManagedFragment, **kw) -> hp.InspectionReport:
    return hp.InspectionReport(
        harness=_Adapter.name, fragments=(fragment,), **kw)


def _runtime_runs():
    return {
        "resolved": "floor-python",
        "command_executed": True,
        "candidates": [{
            "candidate": "floor-python",
            "interpreter_found": True,
            "dependency_loaded": True,
        }],
    }


def _diag(tmp_path: Path, adapter: _Adapter,
          runtime=None) -> hd.CapabilityDiagnostic:
    result = hd.diagnose_harness(
        adapter, tmp_path, hp.HarnessContext(".."),
        runtime_result=runtime, moments=("session-start",),
    )
    assert result.harness == adapter.name
    return result.capabilities[0]


def _git_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)


def test_invalid_configuration_does_not_become_absent_or_stale(tmp_path):
    fragment = hp.ManagedFragment(
        path="adapter.config", present=True, artifact_present=True,
        readable=True, valid=False,
    )
    fact = _diag(tmp_path, _Adapter(_report(fragment)), _runtime_runs())
    assert fact.support == "supported"
    assert fact.configuration == "invalid"
    assert fact.currency == "unknown"
    assert fact.runtime.state == "command-runs"
    assert fact.execution.state == "untested"


def test_current_but_untrusted_remains_two_independent_facts(tmp_path):
    adapter = _Adapter(
        _report(_current_fragment()), trust="review-required",
        hashes={"session-start": CURRENT_HASH},
        remediations=("complete the harness's human trust review",),
        ownership=("the operator owns the trust decision",),
    )
    fact = _diag(tmp_path, adapter, _runtime_runs())
    assert (fact.configuration, fact.currency) == ("present", "current")
    assert fact.trust == "review-required"
    assert fact.runtime.state == "command-runs"
    assert fact.execution.state == "untested"
    assert "complete the harness's human trust review" in fact.remediations
    assert fact.ownership == ("the operator owns the trust decision",)


def test_runtime_success_never_claims_a_real_event_fired(tmp_path):
    _git_repo(tmp_path)
    fact = _diag(
        tmp_path,
        _Adapter(_report(_current_fragment()), trust="managed",
                 hashes={"session-start": CURRENT_HASH}),
        _runtime_runs(),
    )
    assert fact.runtime.state == "command-runs"
    assert fact.execution.state == "untested"
    assert "no real-event" in fact.execution.detail
    path = hd.execution_attestation_path(
        tmp_path, _Adapter.name, "session-start")
    assert path is not None and not path.exists(), \
        "diagnosis must never manufacture its own execution evidence"


def test_adapter_without_probe_port_reports_unknown_not_exception(tmp_path):
    result = hd.diagnose_harness(
        _NoProbeAdapter(), tmp_path, hp.HarnessContext(".."),
        runtime_result=_runtime_runs(), moments=("session-start",),
    ).capabilities[0]
    assert result.support == "supported"
    assert result.trust == "unknown"
    assert result.execution.state == "untested"
    assert "no current definition fingerprint" in result.execution.detail


def test_extensions_are_explicit_without_becoming_staleness(tmp_path):
    fact = _diag(
        tmp_path,
        _Adapter(_report(
            _current_fragment(),
            extensions=("operator added a trailing argument",),
        )),
        _runtime_runs(),
    )
    assert fact.configuration == "present"
    assert fact.currency == "current"
    assert fact.extensions == ("operator added a trailing argument",)


def test_findings_make_configuration_ambiguous_not_current(tmp_path):
    fact = _diag(
        tmp_path,
        _Adapter(_report(
            _current_fragment(),
            findings=("two managed groups compete",),
        )),
        _runtime_runs(),
    )
    assert fact.configuration == "ambiguous"
    assert fact.currency == "unknown"
    assert fact.execution.state == "untested"


def test_matching_real_event_attestation_is_the_only_pass_path(tmp_path):
    _git_repo(tmp_path)
    when = dt.datetime(2026, 8, 11, 9, 30, tzinfo=dt.timezone.utc)
    hd.record_execution_attestation(
        tmp_path, _Adapter.name, "session-start", CURRENT_HASH,
        outcome="passed", source="real lifecycle handler",
        detail="ordered steps completed", observed_at=when,
    )
    fact = _diag(
        tmp_path,
        _Adapter(_report(_current_fragment()), trust="trusted",
                 hashes={"session-start": CURRENT_HASH}),
        _runtime_runs(),
    )
    assert fact.execution.state == "passed"
    assert fact.execution.definition_current is True
    assert fact.execution.attested_at == "2026-08-11T09:30:00+00:00"
    assert fact.execution.source == "real lifecycle handler"
    assert fact.execution.detail == "ordered steps completed"


def test_failed_real_event_is_executed_but_not_passing(tmp_path):
    _git_repo(tmp_path)
    hd.record_execution_attestation(
        tmp_path, _Adapter.name, "session-start", CURRENT_HASH,
        outcome="failed", source="real lifecycle handler",
        detail="second ordered step failed",
    )
    fact = _diag(
        tmp_path,
        _Adapter(_report(_current_fragment()),
                 hashes={"session-start": CURRENT_HASH}),
        _runtime_runs(),
    )
    assert fact.execution.state == "failed"
    assert fact.execution.definition_current is True


def test_changed_definition_hash_invalidates_old_execution(tmp_path):
    _git_repo(tmp_path)
    old_hash = hd.managed_definition_hash({"definition": "old"})
    new_hash = hd.managed_definition_hash({"definition": "new"})
    hd.record_execution_attestation(
        tmp_path, _Adapter.name, "session-start", old_hash,
        outcome="passed", source="real lifecycle handler",
    )
    fact = _diag(
        tmp_path,
        _Adapter(_report(_current_fragment()),
                 hashes={"session-start": new_hash}),
        _runtime_runs(),
    )
    assert fact.execution.state == "untested"
    assert fact.execution.definition_current is False
    assert "stale" in fact.execution.detail


def test_invalid_attestation_is_not_execution_evidence(tmp_path):
    _git_repo(tmp_path)
    path = hd.execution_attestation_path(
        tmp_path, _Adapter.name, "session-start")
    assert path is not None
    path.parent.mkdir(parents=True)
    path.write_text("not json\n", encoding="utf-8")
    fact = _diag(
        tmp_path,
        _Adapter(_report(_current_fragment()),
                 hashes={"session-start": CURRENT_HASH}),
        _runtime_runs(),
    )
    assert fact.execution.state == "untested"
    assert "invalid" in fact.execution.detail


def test_stale_configuration_cannot_reuse_even_matching_evidence(tmp_path):
    _git_repo(tmp_path)
    hd.record_execution_attestation(
        tmp_path, _Adapter.name, "session-start", CURRENT_HASH,
        outcome="passed", source="real lifecycle handler",
    )
    stale = _current_fragment(current=False)
    fact = _diag(
        tmp_path,
        _Adapter(_report(stale), hashes={"session-start": CURRENT_HASH}),
        _runtime_runs(),
    )
    assert (fact.configuration, fact.currency) == ("present", "stale")
    assert fact.execution.state == "untested"
    assert "not established" in fact.execution.detail


def test_runtime_states_keep_resolution_dependency_and_command_separate(tmp_path):
    adapter = _Adapter(_report(_current_fragment()))
    missing = _diag(tmp_path, adapter, {
        "resolved": None, "command_executed": None,
        "candidates": [{"interpreter_found": True,
                        "dependency_loaded": False}],
    })
    assert missing.runtime.state == "dependency-missing"

    failed = _diag(tmp_path, adapter, {
        "resolved": "floor-python", "command_executed": False,
        "candidates": [{"interpreter_found": True,
                        "dependency_loaded": True}],
    })
    assert failed.runtime.state == "command-failed"

    unresolved = _diag(tmp_path, adapter, {
        "resolved": None, "command_executed": None,
        "candidates": [{"interpreter_found": False,
                        "dependency_loaded": False}],
    })
    assert unresolved.runtime.state == "unresolved"


def test_unsupported_capability_uses_not_applicable_not_failure(tmp_path):
    result = hd.diagnose_harness(
        _Adapter(_report(_current_fragment())), tmp_path,
        hp.HarnessContext(".."), runtime_result=_runtime_runs(),
        moments=("deliberate-session-end",),
    ).capabilities[0]
    assert result.support == "unsupported"
    assert result.configuration == "not-applicable"
    assert result.currency == "not-applicable"
    assert result.trust == "not-applicable"
    assert result.runtime.state == "not-applicable"
    assert result.execution.state == "not-applicable"


def test_definition_hash_is_order_stable_and_content_sensitive():
    first = hd.managed_definition_hash({"b": b"two", "a": "one"})
    reordered = hd.managed_definition_hash({"a": "one", "b": b"two"})
    changed = hd.managed_definition_hash({"a": "one", "b": b"three"})
    assert first == reordered
    assert first != changed
