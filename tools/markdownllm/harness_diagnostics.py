"""Truthful, vendor-neutral lifecycle-adapter diagnostics.

Phase 3 of ``vendor-harness-adapter-foundation`` settles the diagnostic
vocabulary at its first real consumer.  The dimensions deliberately do not
promote one another:

* a supported capability may have no configuration;
* a present configuration may be invalid, ambiguous, or stale;
* a current configuration may still have operator-owned extensions;
* trust is observed (or left unknown), never inferred from installation;
* a runtime probe proves only that the floor command can run;
* execution passes or fails only when a hash-bound real-event attestation is
  available.  Static inspection and runtime success leave it ``untested``.

The module is an application service over the existing render/inspect ports.
It knows no vendor event name or configuration schema.  Adapters may opt into
the narrow ``ProbePort`` to supply machine-observable trust, the fingerprints
of the definitions their real event handlers attest, and vendor-owned
remediation text.  Missing probe capability is an honest ``unknown`` answer.

Attestations are clone-local files beneath the Git directory.  They are
evidence emitted *by a real harness event handler*, not proof that a model
obeyed the injected context and not a substitute for the Git enforcement
boundary.  A changed definition hash invalidates old evidence by returning
``untested`` rather than laundering an earlier run into current verification.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Literal, Mapping, Protocol, runtime_checkable

from .harness_ports import (
    HarnessContext,
    InspectPort,
    InspectionReport,
    RenderPort,
)


SupportState = Literal["supported", "unsupported", "unknown"]
ConfigurationState = Literal[
    "not-applicable", "absent", "present", "invalid", "ambiguous", "unknown"
]
CurrencyState = Literal[
    "not-applicable", "current", "stale", "unknown"
]
TrustState = Literal[
    "not-applicable", "unknown", "review-required", "trusted", "managed"
]
RuntimeState = Literal[
    "not-applicable", "unknown", "unresolved", "dependency-missing",
    "command-failed", "command-runs",
]
ExecutionState = Literal["not-applicable", "untested", "passed", "failed"]


@dataclass(frozen=True)
class AdapterProbe:
    """Adapter-owned observations that the neutral service cannot invent.

    ``definition_hashes`` maps inward lifecycle moments to the fingerprint
    embedded in (and later emitted by) that adapter's real event handler.  A
    renderer should derive it from the complete adapter-owned definition,
    including managed metadata, rather than maintain a second expected list.

    Trust remains ``unknown`` when the harness exposes no stable project API.
    ``remediations`` and ``ownership`` are presentation data only; neither is
    executed by this module.
    """

    trust: TrustState = "unknown"
    trust_detail: str = ""
    definition_hashes: Mapping[str, str] = field(default_factory=dict)
    remediations: tuple[str, ...] = ()
    ownership: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "definition_hashes",
            MappingProxyType(dict(self.definition_hashes)),
        )


@runtime_checkable
class ProbePort(Protocol):
    """Safe, read-only harness observations for diagnostics.

    This port does not fire a lifecycle event.  Real events call
    :func:`record_execution_attestation` after they actually run.
    """

    def probe(self, domain_root: Path,
              context: HarnessContext) -> AdapterProbe: ...


@dataclass(frozen=True)
class RuntimeFact:
    state: RuntimeState
    resolved: str | None = None
    detail: str = ""


@dataclass(frozen=True)
class ExecutionFact:
    state: ExecutionState
    attested_at: str | None = None
    source: str | None = None
    definition_current: bool | None = None
    detail: str = ""


@dataclass(frozen=True)
class CapabilityDiagnostic:
    """Independent facts for one inward lifecycle capability."""

    capability: str
    support: SupportState
    configuration: ConfigurationState
    currency: CurrencyState
    trust: TrustState
    trust_detail: str
    runtime: RuntimeFact
    execution: ExecutionFact
    extensions: tuple[str, ...] = ()
    findings: tuple[str, ...] = ()
    remediations: tuple[str, ...] = ()
    ownership: tuple[str, ...] = ()


@dataclass(frozen=True)
class HarnessDiagnostic:
    harness: str
    capabilities: tuple[CapabilityDiagnostic, ...]
    operator_owned: tuple[str, ...] = ()


def managed_definition_hash(parts: Mapping[str, bytes | str]) -> str:
    """Return a stable hash for adapter-owned definition material.

    Length-prefixing makes the encoding unambiguous; sorting makes it
    independent of mapping insertion order.  Adapters choose the semantic
    parts.  Operator-owned bytes must not be included merely because they
    share a containing file.
    """

    digest = hashlib.sha256()
    digest.update(b"markdownllm-managed-definition-v1\0")
    for name in sorted(parts):
        key = name.encode("utf-8")
        raw = parts[name]
        value = raw.encode("utf-8") if isinstance(raw, str) else bytes(raw)
        digest.update(len(key).to_bytes(8, "big"))
        digest.update(key)
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)
    return "sha256:" + digest.hexdigest()


_SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_ATTESTATION_DIR = "mdllm-harness-attest"
_ATTESTATION_SCHEMA = 1


def _safe_component(value: str, label: str) -> str:
    if not _SAFE_COMPONENT.fullmatch(value):
        raise ValueError(f"{label} must contain only letters, digits, '.', '_' or '-'")
    return value


def _git_dir(root: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"], cwd=root,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return (root / result.stdout.strip()).resolve()


def execution_attestation_path(root: Path, harness: str,
                               capability: str) -> Path | None:
    """Return the clone-local evidence path, or ``None`` outside Git."""

    harness = _safe_component(harness, "harness")
    capability = _safe_component(capability, "capability")
    git_dir = _git_dir(root.resolve())
    if git_dir is None:
        return None
    return git_dir / _ATTESTATION_DIR / harness / f"{capability}.json"


def record_execution_attestation(
        root: Path, harness: str, capability: str, definition_hash: str, *,
        outcome: Literal["passed", "failed"], source: str,
        detail: str = "", observed_at: dt.datetime | None = None) -> Path:
    """Atomically record one *actually fired* lifecycle event.

    Callers must invoke this from the real event handler after the lifecycle
    work has run.  Installation, inspection, and runtime probing must never
    call it.  ``source`` is required so a report can name the evidence rather
    than presenting a bare assertion.
    """

    if not definition_hash.strip():
        raise ValueError("definition_hash must not be empty")
    if outcome not in ("passed", "failed"):
        raise ValueError("outcome must be 'passed' or 'failed'")
    if not source.strip():
        raise ValueError("source must name the real event evidence")
    path = execution_attestation_path(root, harness, capability)
    if path is None:
        raise ValueError("execution attestations require a Git repository")
    when = observed_at or dt.datetime.now(dt.timezone.utc)
    if when.tzinfo is None:
        raise ValueError("observed_at must be timezone-aware")
    payload = {
        "schema": _ATTESTATION_SCHEMA,
        "harness": harness,
        "capability": capability,
        "definition_hash": definition_hash,
        "outcome": outcome,
        "observed_at": when.astimezone(dt.timezone.utc).isoformat(),
        "source": source,
        "detail": detail[:1000],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")
    tmp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="wb", dir=path.parent, prefix=f".{path.name}.",
                suffix=".tmp", delete=False) as tmp:
            tmp.write(raw)
            tmp_name = tmp.name
        os.replace(tmp_name, path)
    finally:
        if tmp_name is not None and os.path.exists(tmp_name):
            os.unlink(tmp_name)
    return path


def read_execution_attestation(root: Path, harness: str, capability: str,
                               expected_definition_hash: str) -> ExecutionFact:
    """Read current real-event evidence without promoting stale evidence."""

    path = execution_attestation_path(root, harness, capability)
    if path is None:
        return ExecutionFact(
            state="untested",
            detail="not a Git repository; no clone-local execution evidence",
        )
    if not path.is_file():
        return ExecutionFact(
            state="untested",
            detail="no real-event execution attestation for this definition",
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("attestation root is not an object")
        if data.get("schema") != _ATTESTATION_SCHEMA:
            raise ValueError("unsupported attestation schema")
        if data.get("harness") != harness or data.get("capability") != capability:
            raise ValueError("attestation identity does not match its path")
        recorded_hash = data.get("definition_hash")
        outcome = data.get("outcome")
        stamp = data.get("observed_at")
        source = data.get("source")
        if not all(isinstance(v, str) and v for v in
                   (recorded_hash, stamp, source)):
            raise ValueError("attestation evidence fields are incomplete")
        parsed = dt.datetime.fromisoformat(stamp)
        if parsed.tzinfo is None:
            raise ValueError("attestation timestamp has no timezone")
        if outcome not in ("passed", "failed"):
            raise ValueError("attestation outcome is invalid")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return ExecutionFact(
            state="untested",
            detail=f"execution attestation is unreadable or invalid: {exc}",
        )
    if recorded_hash != expected_definition_hash:
        return ExecutionFact(
            state="untested", attested_at=stamp, source=source,
            definition_current=False,
            detail="stale execution attestation ignored: managed definition changed",
        )
    return ExecutionFact(
        state=outcome, attested_at=stamp, source=source,
        definition_current=True, detail=str(data.get("detail") or ""),
    )


def runtime_fact(result: Mapping[str, object] | None) -> RuntimeFact:
    """Translate the shared runtime probe without claiming event execution."""

    if result is None:
        return RuntimeFact("unknown", detail="runtime was not probed")
    resolved = result.get("resolved")
    ran = result.get("command_executed")
    if isinstance(resolved, str) and resolved:
        if ran is True:
            return RuntimeFact("command-runs", resolved=resolved)
        if ran is False:
            return RuntimeFact(
                "command-failed", resolved=resolved,
                detail="dependency loaded but the floor command did not run",
            )
        return RuntimeFact(
            "unknown", resolved=resolved,
            detail="interpreter resolved but command execution was not observed",
        )
    candidates = result.get("candidates")
    if isinstance(candidates, list) and any(
            isinstance(item, Mapping) and item.get("interpreter_found") is True
            for item in candidates):
        return RuntimeFact(
            "dependency-missing",
            detail="an interpreter was found but none loaded the floor dependency",
        )
    return RuntimeFact("unresolved", detail="no floor-capable interpreter resolved")


def _configuration_fact(report: InspectionReport, capability: str,
                        supported: bool) -> tuple[
                            ConfigurationState, CurrencyState,
                            tuple[str, ...], tuple[str, ...]]:
    if not supported:
        return "not-applicable", "not-applicable", (), ()
    fragments = report.fragments
    if not fragments:
        return "unknown", "unknown", report.extensions, report.findings

    # An unreadable or structurally invalid active artifact cannot be called
    # absent: bytes exist, but their lifecycle meaning is not safely known.
    if any(f.artifact_present and
           (f.readable is False or f.valid is False) for f in fragments):
        return "invalid", "unknown", report.extensions, report.findings

    # Inspect reports carry cross-fragment warnings/findings rather than a
    # second hidden ambiguity flag.  Treating a finding as ambiguous is the
    # conservative answer: diagnostics must never choose one competing
    # managed definition on the operator's behalf.
    realised = [f for f in fragments
                if capability in f.intents_realised]
    if report.findings or len(realised) > 1:
        return "ambiguous", "unknown", report.extensions, report.findings

    if not realised:
        if all(not f.artifact_present for f in fragments):
            return "absent", "not-applicable", report.extensions, report.findings
        # Artifacts may be wholly operator-owned; the managed capability is
        # still absent, not installed by mere file presence.
        if all(f.readable is not None for f in fragments):
            return "absent", "not-applicable", report.extensions, report.findings
        return "unknown", "unknown", report.extensions, report.findings

    fragment = realised[0]
    if fragment.current is True:
        currency: CurrencyState = "current"
    elif fragment.current is False:
        currency = "stale"
    else:
        currency = "unknown"
    return "present", currency, report.extensions, report.findings


def _default_remediations(harness: str, capability: str,
                          configuration: ConfigurationState,
                          currency: CurrencyState,
                          runtime: RuntimeFact,
                          execution: ExecutionFact) -> tuple[str, ...]:
    out: list[str] = []
    if configuration in ("absent", "invalid", "ambiguous") or currency == "stale":
        out.append(
            f"review `mdllm adapter-install . --harness {harness}`; the command "
            "must show its owned diff and may refuse ambiguity"
        )
    if runtime.state not in ("command-runs", "not-applicable"):
        out.append("run `mdllm runtime-probe .` and repair the reported runtime")
    if execution.state == "untested":
        out.append(
            f"fire a real {capability} event in {harness}, then rerun doctor; "
            "static probes do not count as event execution"
        )
    return tuple(out)


def diagnose_harness(
        adapter: object, domain_root: Path, context: HarnessContext, *,
        runtime_result: Mapping[str, object] | None = None,
        moments: tuple[str, ...] | None = None) -> HarnessDiagnostic:
    """Aggregate read-only adapter, runtime, trust, and execution facts.

    The caller owns whether/when to execute the shared runtime probe and passes
    its raw result here.  This keeps deterministic unit tests possible and,
    more importantly, makes it impossible for a static probe's successful
    return to be mistaken for a lifecycle event.
    """

    if not isinstance(adapter, RenderPort) or not isinstance(adapter, InspectPort):
        raise TypeError("diagnostics require the declared render and inspect ports")
    root = domain_root.resolve()
    caps = adapter.capabilities()
    inspection = adapter.inspect(root, context)
    probe = (adapter.probe(root, context)
             if isinstance(adapter, ProbePort) else AdapterProbe())
    wanted = moments or tuple(binding.moment for binding in context.bindings)
    shared_runtime = runtime_fact(runtime_result)
    diagnostics: list[CapabilityDiagnostic] = []

    for capability in wanted:
        supported = capability in caps.lifecycle_moments
        support: SupportState = "supported" if supported else "unsupported"
        configuration, currency, extensions, findings = _configuration_fact(
            inspection, capability, supported)
        if supported:
            trust = probe.trust
            rt = shared_runtime
        else:
            trust = "not-applicable"
            rt = RuntimeFact("not-applicable")

        expected_hash = probe.definition_hashes.get(capability)
        if not supported:
            execution = ExecutionFact("not-applicable")
        elif configuration != "present" or currency != "current":
            # Even a matching leftover file cannot verify a definition which
            # inspection says is absent, invalid, ambiguous, or stale now.
            execution = ExecutionFact(
                "untested",
                detail="current managed configuration is not established",
            )
        elif not expected_hash:
            execution = ExecutionFact(
                "untested",
                detail="adapter supplied no current definition fingerprint",
            )
        else:
            execution = read_execution_attestation(
                root, caps.harness, capability, expected_hash)

        remediation = list(_default_remediations(
            caps.harness, capability, configuration, currency, rt, execution))
        remediation.extend(probe.remediations)
        diagnostics.append(CapabilityDiagnostic(
            capability=capability,
            support=support,
            configuration=configuration,
            currency=currency,
            trust=trust,
            trust_detail=(probe.trust_detail if supported else ""),
            runtime=rt,
            execution=execution,
            extensions=extensions,
            findings=findings,
            remediations=tuple(dict.fromkeys(remediation)),
            ownership=probe.ownership,
        ))

    return HarnessDiagnostic(
        harness=caps.harness,
        capabilities=tuple(diagnostics),
        operator_owned=inspection.operator_owned,
    )
