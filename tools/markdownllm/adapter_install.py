"""Conservative, project-local harness-adapter installation.

This module is the mutation boundary between read-only adapter inspection and
filesystem writes.  It deliberately knows no adapter registry and never looks
at user-global configuration: callers provide selected adapters, a domain
root, and an ownership policy for each rendered artifact.

The operation has two beats:

``preflight_install``
    Reads every selected adapter and returns create/merge/no-op/refuse
    decisions plus an exact unified diff.  It does not write.

``apply_install``
    Refuses the whole plan if *any* selected artifact was ambiguous, verifies
    that none of the inputs changed since preflight, stages every changed file,
    and then replaces them atomically per artifact (rolling earlier replaces
    back if a later replace fails).

The generic default owns a whole artifact.  ``TopLevelJsonFragmentPolicy`` is
the narrow composite-settings seam: it can surgically add one missing
top-level JSON member (for example Claude's ``hooks``) while retaining every
pre-existing byte as an unchanged prefix or suffix.  Existing current or
locally extended managed fragments are no-ops; invalid, stale, duplicated, or
otherwise ambiguous fragments are refusals, never rewrites.
"""

from __future__ import annotations

import difflib
import json
import os
import stat
import tempfile
from dataclasses import dataclass, field, replace
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Literal, Mapping, Protocol, runtime_checkable

from .harness_ports import HarnessContext, InspectionReport, ManagedFragment


InstallAction = Literal["create", "merge", "no-op", "refuse"]


class InstallRefused(RuntimeError):
    """Raised when an all-selected preflight contains any refusal."""


class InstallStateChanged(RuntimeError):
    """Raised when an artifact changes between preflight and apply."""


class AtomicInstallError(RuntimeError):
    """Raised when applying (or rolling back) a preflighted plan fails."""


@dataclass(frozen=True)
class PolicyDecision:
    action: InstallAction
    after: bytes | None
    reason: str


class MergePolicy(Protocol):
    """Decide one rendered artifact without touching the filesystem."""

    def decide(
        self,
        *,
        path: str,
        before: bytes | None,
        desired: bytes,
        inspection: InspectionReport,
    ) -> PolicyDecision: ...


@runtime_checkable
class InstallPolicyPort(Protocol):
    """Adapter-owned schema policy for its rendered artifact paths."""

    def install_policies(self) -> Mapping[str, MergePolicy]: ...


def _matching_fragment(
        inspection: InspectionReport, path: str) -> ManagedFragment | None:
    matches = [fragment for fragment in inspection.fragments
               if fragment.path == path]
    return matches[0] if len(matches) == 1 else None


def _inspection_refusal(
        inspection: InspectionReport, path: str) -> str | None:
    """Return why mutation is unsafe, leaving current extensions admissible."""
    if inspection.findings:
        return "inspection is ambiguous: " + "; ".join(inspection.findings)
    matches = [fragment for fragment in inspection.fragments
               if fragment.path == path]
    if len(matches) != 1:
        return ("inspection did not identify exactly one owned fragment for "
                f"{path!r}")
    fragment = matches[0]
    if fragment.readable is False:
        return "artifact is unreadable"
    if fragment.valid is False:
        detail = "; ".join(fragment.issues) or "schema or syntax invalid"
        return f"artifact is invalid: {detail}"
    if fragment.issues:
        return "managed fragment diverges: " + "; ".join(fragment.issues)
    if fragment.present and fragment.current is False:
        return "managed fragment is stale"
    return None


@dataclass(frozen=True)
class WholeArtifactPolicy:
    """Own a complete file, while preserving a current local extension.

    A non-existent file can be created and exact bytes are naturally a no-op.
    If inspection says a present fragment is semantically current, a byte
    difference is treated as formatting or a reported local extension and is
    deliberately left untouched.  Every other existing shape is refused.
    """

    def decide(
        self,
        *,
        path: str,
        before: bytes | None,
        desired: bytes,
        inspection: InspectionReport,
    ) -> PolicyDecision:
        unsafe = _inspection_refusal(inspection, path)
        if unsafe:
            return PolicyDecision("refuse", desired, unsafe)
        fragment = _matching_fragment(inspection, path)
        assert fragment is not None  # established by _inspection_refusal
        if before is None:
            if fragment.artifact_present:
                return PolicyDecision(
                    "refuse", desired,
                    "inspection and filesystem disagree about artifact presence")
            return PolicyDecision("create", desired,
                                  "managed artifact is absent")
        if not fragment.artifact_present:
            return PolicyDecision(
                "refuse", desired,
                "inspection and filesystem disagree about artifact presence")
        if before == desired:
            return PolicyDecision("no-op", before,
                                  "managed artifact is already exact")
        if fragment.present and fragment.current is True:
            return PolicyDecision(
                "no-op", before,
                "managed fragment is current; formatting or local extensions "
                "are preserved")
        return PolicyDecision(
            "refuse", desired,
            "existing artifact has no safely replaceable managed fragment")


class _DuplicateJsonKey(ValueError):
    pass


def _unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise _DuplicateJsonKey(f"duplicate JSON key {key!r}")
        out[key] = value
    return out


def load_unique_json(raw: bytes) -> object:
    """Decode one UTF-8 JSON document while refusing duplicate keys.

    The ordinary ``json.loads`` last-key-wins rule is unsafe at a mutation
    boundary: two visually present ownership keys would otherwise collapse
    into one value before either an inspector or merge policy could report
    the ambiguity.  Adapters may use this same reader for duplicate-aware
    inspection; mutation policies always use it before calculating spans.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("artifact is not UTF-8") from exc
    try:
        return json.loads(text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, _DuplicateJsonKey) as exc:
        raise ValueError(str(exc)) from exc


# Compatibility alias for the first composite policy.  New adapter-facing
# code uses the public, intentionally neutral name above.
_load_unique_json = load_unique_json


@dataclass(frozen=True)
class _JsonValueSpan:
    start: int
    end: int


def _skip_json_space(text: str, offset: int) -> int:
    while offset < len(text) and text[offset] in " \t\r\n":
        offset += 1
    return offset


def _json_object_members(
        text: str, span: _JsonValueSpan) -> dict[str, _JsonValueSpan]:
    """Locate direct object-member value spans in an already valid document."""
    decoder = json.JSONDecoder()
    position = _skip_json_space(text, span.start)
    if position >= span.end or text[position] != "{":
        raise ValueError("JSON path does not identify an object")
    position = _skip_json_space(text, position + 1)
    members: dict[str, _JsonValueSpan] = {}
    if position < span.end and text[position] == "}":
        return members
    while position < span.end:
        try:
            key, key_end = decoder.raw_decode(text, position)
        except json.JSONDecodeError as exc:  # defensive: whole doc was valid
            raise ValueError(f"cannot locate JSON object key: {exc}") from exc
        if not isinstance(key, str):
            raise ValueError("JSON object key is not a string")
        position = _skip_json_space(text, key_end)
        if position >= span.end or text[position] != ":":
            raise ValueError("JSON object member has no colon")
        value_start = _skip_json_space(text, position + 1)
        try:
            _, value_end = decoder.raw_decode(text, value_start)
        except json.JSONDecodeError as exc:  # defensive: whole doc was valid
            raise ValueError(f"cannot locate JSON member value: {exc}") from exc
        members[key] = _JsonValueSpan(value_start, value_end)
        position = _skip_json_space(text, value_end)
        if position >= span.end:
            raise ValueError("unterminated JSON object")
        if text[position] == "}":
            return members
        if text[position] != ",":
            raise ValueError("JSON object members are not comma-separated")
        position = _skip_json_space(text, position + 1)
    raise ValueError("unterminated JSON object")


def _json_span_at_path(text: str, path: tuple[str, ...]) -> _JsonValueSpan:
    decoder = json.JSONDecoder()
    start = _skip_json_space(text, 0)
    try:
        _, end = decoder.raw_decode(text, start)
    except json.JSONDecodeError as exc:
        raise ValueError(str(exc)) from exc
    span = _JsonValueSpan(start, end)
    for member in path:
        members = _json_object_members(text, span)
        try:
            span = members[member]
        except KeyError as exc:
            raise ValueError(f"JSON path member {member!r} is absent") from exc
    return span


def insert_json_object_member(
        raw: bytes, object_path: tuple[str, ...], member: str,
        value: object) -> bytes:
    """Add one missing member without replacing any existing source byte.

    ``object_path`` is a tuple of member names from the document root to the
    containing object.  New bytes use a compact JSON representation; all old
    bytes remain in the same order, which is the ownership guarantee needed
    for composite configuration files.
    """
    document = load_unique_json(raw)
    current: object = document
    for part in object_path:
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"JSON path member {part!r} is absent")
        current = current[part]
    if not isinstance(current, dict):
        raise ValueError("JSON insertion path does not identify an object")
    if member in current:
        raise ValueError(f"JSON member {member!r} already exists")

    text = raw.decode("utf-8")
    span = _json_span_at_path(text, object_path)
    close = span.end - 1
    if close < span.start or text[close] != "}":
        raise ValueError("JSON insertion path has no closing object brace")
    encoded = json.dumps(member) + ":" + json.dumps(
        value, separators=(",", ":"))
    prefix = "," if current else ""
    return (text[:close] + prefix + encoded + text[close:]).encode("utf-8")


def append_json_array_value(
        raw: bytes, array_path: tuple[str, ...], value: object) -> bytes:
    """Append one array value while preserving every pre-existing byte."""
    document = load_unique_json(raw)
    current: object = document
    for part in array_path:
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"JSON path member {part!r} is absent")
        current = current[part]
    if not isinstance(current, list):
        raise ValueError("JSON append path does not identify an array")

    text = raw.decode("utf-8")
    span = _json_span_at_path(text, array_path)
    close = span.end - 1
    if close < span.start or text[close] != "]":
        raise ValueError("JSON append path has no closing array bracket")
    encoded = json.dumps(value, separators=(",", ":"))
    prefix = "," if current else ""
    return (text[:close] + prefix + encoded + text[close:]).encode("utf-8")


def _top_level_member_bytes(desired: bytes, member: str) -> bytes:
    """Extract one renderer-formatted member without inventing its bytes."""
    data = _load_unique_json(desired)
    if not isinstance(data, dict) or set(data) != {member}:
        raise ValueError(
            f"renderer must emit exactly one top-level {member!r} member")
    # Render only the outer one-member object using the same stdlib contract
    # used by the adapters, then remove its braces.  Keeping the two-space
    # indentation makes the inserted managed fragment byte-stable.
    one = json.dumps({member: data[member]}, indent=2).splitlines()
    return "\n".join(one[1:-1]).encode("utf-8")


def _insert_top_level_member(
        before: bytes, desired: bytes, member: str) -> bytes:
    """Surgically add ``member`` while retaining every input byte in order."""
    existing = _load_unique_json(before)
    if not isinstance(existing, dict):
        raise ValueError("top-level JSON value is not an object")
    if member in existing:
        raise ValueError(f"top-level {member!r} member already exists")
    managed = _top_level_member_bytes(desired, member)

    whitespace = b" \t\r\n"
    close = len(before) - 1
    while close >= 0 and before[close] in whitespace:
        close -= 1
    if close < 0 or before[close:close + 1] != b"}":
        raise ValueError("JSON object has no terminal closing brace")

    if existing:
        # The final non-whitespace token before the root close is the end of
        # the last existing member value.  Insert there: original prefix and
        # suffix remain exact byte slices of ``before``.
        insert_at = close - 1
        while insert_at >= 0 and before[insert_at] in whitespace:
            insert_at -= 1
        insert_at += 1
        insertion = b",\n" + managed
    else:
        opening = 0
        while opening < close and before[opening] in whitespace:
            opening += 1
        if before[opening:opening + 1] != b"{":
            raise ValueError("JSON object has no opening brace")
        insert_at = opening + 1
        insertion = b"\n" + managed

    suffix = before[insert_at:]
    if not suffix or suffix[0] not in whitespace:
        insertion += b"\n"
    return before[:insert_at] + insertion + suffix


@dataclass(frozen=True)
class TopLevelJsonFragmentPolicy:
    """Own one top-level JSON member inside a composite settings file."""

    member: str

    def decide(
        self,
        *,
        path: str,
        before: bytes | None,
        desired: bytes,
        inspection: InspectionReport,
    ) -> PolicyDecision:
        unsafe = _inspection_refusal(inspection, path)
        if unsafe:
            return PolicyDecision("refuse", desired, unsafe)
        fragment = _matching_fragment(inspection, path)
        assert fragment is not None
        if before is None:
            if fragment.artifact_present:
                return PolicyDecision(
                    "refuse", desired,
                    "inspection and filesystem disagree about artifact presence")
            return PolicyDecision("create", desired,
                                  "managed artifact is absent")
        if not fragment.artifact_present:
            return PolicyDecision(
                "refuse", desired,
                "inspection and filesystem disagree about artifact presence")
        # Inspection is adapter-defined and may use an ordinary JSON parser
        # that cannot see duplicate object keys.  Mutation must use the
        # stricter reader even on a semantically current/no-op artifact: a
        # duplicate owned key is ambiguous and must be made visible.
        try:
            _load_unique_json(before)
            _load_unique_json(desired)
        except ValueError as exc:
            return PolicyDecision("refuse", desired,
                                  f"JSON ownership is ambiguous: {exc}")
        if before == desired:
            return PolicyDecision("no-op", before,
                                  "managed artifact is already exact")
        if fragment.present:
            if fragment.current is True:
                return PolicyDecision(
                    "no-op", before,
                    "managed fragment is current; local extensions and "
                    "operator-owned bytes are preserved")
            return PolicyDecision("refuse", desired,
                                  "managed fragment is not current")
        if fragment.readable is not True or fragment.valid is not True:
            return PolicyDecision(
                "refuse", desired,
                "missing managed fragment is not in a readable valid artifact")
        try:
            merged = _insert_top_level_member(before, desired, self.member)
        except ValueError as exc:
            return PolicyDecision("refuse", desired,
                                  f"safe surgical merge is unavailable: {exc}")
        return PolicyDecision(
            "merge", merged,
            f"add missing top-level {self.member!r} managed fragment")


@dataclass(frozen=True)
class NestedJsonArrayGroupsPolicy:
    """Own named array groups below one top-level JSON object member.

    This is deliberately schema-shaped but vendor-neutral.  An adapter names
    the containing member and the array members it owns.  For an existing,
    valid composite document the policy either adds the missing containing
    object, adds a missing owned array, or appends the renderer's groups to an
    existing operator-owned array.  It never serializes the existing object.

    Inspection remains authoritative about discovery and currency: a partly
    present or stale managed fragment is refused, as are duplicate keys and
    cross-artifact findings.  Only a genuinely absent managed fragment can be
    merged into an existing artifact.
    """

    container_member: str
    owned_array_members: tuple[str, ...]

    def decide(
        self,
        *,
        path: str,
        before: bytes | None,
        desired: bytes,
        inspection: InspectionReport,
    ) -> PolicyDecision:
        unsafe = _inspection_refusal(inspection, path)
        if unsafe:
            return PolicyDecision("refuse", desired, unsafe)
        fragment = _matching_fragment(inspection, path)
        assert fragment is not None
        if before is None:
            if fragment.artifact_present:
                return PolicyDecision(
                    "refuse", desired,
                    "inspection and filesystem disagree about artifact presence")
            return PolicyDecision("create", desired,
                                  "managed artifact is absent")
        if not fragment.artifact_present:
            return PolicyDecision(
                "refuse", desired,
                "inspection and filesystem disagree about artifact presence")

        try:
            existing = load_unique_json(before)
            wanted = load_unique_json(desired)
        except ValueError as exc:
            return PolicyDecision("refuse", desired,
                                  f"JSON ownership is ambiguous: {exc}")
        if before == desired:
            return PolicyDecision("no-op", before,
                                  "managed artifact is already exact")
        if fragment.present:
            if fragment.current is True:
                return PolicyDecision(
                    "no-op", before,
                    "managed fragment is current; local extensions and "
                    "operator-owned bytes are preserved")
            return PolicyDecision("refuse", desired,
                                  "managed fragment is not current")
        if fragment.readable is not True or fragment.valid is not True:
            return PolicyDecision(
                "refuse", desired,
                "missing managed fragment is not in a readable valid artifact")
        if not isinstance(existing, dict) or not isinstance(wanted, dict):
            return PolicyDecision(
                "refuse", desired, "top-level JSON value is not an object")
        wanted_container = wanted.get(self.container_member)
        if not isinstance(wanted_container, dict):
            return PolicyDecision(
                "refuse", desired,
                f"renderer has no object member {self.container_member!r}")
        if set(wanted_container) != set(self.owned_array_members):
            return PolicyDecision(
                "refuse", desired,
                "renderer-owned JSON arrays do not match the policy schema")
        for member in self.owned_array_members:
            groups = wanted_container.get(member)
            if not isinstance(groups, list) or not groups:
                return PolicyDecision(
                    "refuse", desired,
                    f"renderer member {member!r} is not a non-empty array")

        try:
            merged = before
            existing_container = existing.get(self.container_member)
            if existing_container is None:
                merged = insert_json_object_member(
                    merged, (), self.container_member, wanted_container)
            else:
                if not isinstance(existing_container, dict):
                    raise ValueError(
                        f"existing {self.container_member!r} is not an object")
                for member in self.owned_array_members:
                    groups = wanted_container[member]
                    if member not in existing_container:
                        merged = insert_json_object_member(
                            merged, (self.container_member,), member, groups)
                    else:
                        if not isinstance(existing_container[member], list):
                            raise ValueError(
                                f"existing {member!r} is not an array")
                        for group in groups:
                            merged = append_json_array_value(
                                merged, (self.container_member, member), group)
            # Reparse the result before returning bytes to the transaction.
            load_unique_json(merged)
        except ValueError as exc:
            return PolicyDecision(
                "refuse", desired, f"safe surgical merge is unavailable: {exc}")
        return PolicyDecision(
            "merge", merged,
            "add missing managed JSON array groups without replacing "
            "operator-owned bytes")


@dataclass(frozen=True)
class AdapterInstallTarget:
    """One selected adapter plus explicit ownership for its rendered files."""

    adapter: object
    context: HarnessContext
    policies: Mapping[str, MergePolicy] = field(default_factory=dict)
    default_policy: MergePolicy = field(default_factory=WholeArtifactPolicy)


def target_for_adapter(adapter: object,
                       context: HarnessContext) -> AdapterInstallTarget:
    """Compose a target through the optional schema-policy port."""
    policies = (adapter.install_policies()
                if isinstance(adapter, InstallPolicyPort) else {})
    return AdapterInstallTarget(adapter, context, policies=policies)


@dataclass(frozen=True)
class ArtifactDecision:
    harness: str
    path: str
    action: InstallAction
    reason: str
    before: bytes | None
    after: bytes | None

    @property
    def changes_bytes(self) -> bool:
        return (self.action in ("create", "merge")
                and self.after is not None and self.after != self.before)

    def unified_diff(self) -> str:
        if self.after is None or self.after == self.before:
            return ""
        old = (self.before or b"").decode("utf-8", errors="replace")
        new = self.after.decode("utf-8", errors="replace")
        return "".join(difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"a/{self.path}",
            tofile=f"b/{self.path}",
        ))


@dataclass(frozen=True)
class InstallPlan:
    domain_root: Path
    decisions: tuple[ArtifactDecision, ...] = ()
    findings: tuple[str, ...] = ()

    @property
    def refused(self) -> bool:
        return bool(self.findings or any(
            decision.action == "refuse" for decision in self.decisions))

    def owned_diff(self) -> str:
        """Exact byte changes this plan could apply after a clean preflight."""
        return "".join(
            decision.unified_diff() for decision in self.decisions
            if decision.action in ("create", "merge"))

    def refusal_diff(self) -> str:
        """Renderer comparison for refused state; never an apply candidate."""
        return "".join(
            decision.unified_diff() for decision in self.decisions
            if decision.action == "refuse")


@dataclass(frozen=True)
class ApplyResult:
    written: tuple[str, ...]
    unchanged: tuple[str, ...]


def portable_artifact_parts(relpath: str) -> tuple[str, ...]:
    """Return a portable project-relative path, or reject it.

    Adapter artifacts are shared through git, so a path that is only safe on
    the current host is not safe enough.  In particular, ``C:foo`` is drive
    relative on Windows (despite not being absolute), and a colon can name an
    alternate data stream there.  Backslashes are likewise refused at this
    mutation boundary so one rendered spelling always identifies one file.
    """
    if not isinstance(relpath, str):
        raise ValueError("artifact path must be a string")
    pure = PurePosixPath(relpath)
    windows = PureWindowsPath(relpath)
    invalid_windows = set('<>"|?*')
    if (not relpath or pure.is_absolute() or not pure.parts
            or ".." in pure.parts or "\\" in relpath or ":" in relpath
            or pure.as_posix() != relpath
            or windows.is_absolute() or windows.drive
            or any(
                PureWindowsPath(part).is_reserved()
                or part.endswith((" ", "."))
                or any(ord(char) < 32 or char in invalid_windows
                       for char in part)
                for part in pure.parts)):
        raise ValueError(f"artifact path must be project-relative: {relpath!r}")
    return pure.parts


def portable_artifact_key(relpath: str) -> str:
    """Canonical ownership key with Windows' case semantics everywhere."""
    return "/".join(
        part.casefold() for part in portable_artifact_parts(relpath))


def _artifact_path(root: Path, relpath: str) -> Path:
    parts = portable_artifact_parts(relpath)
    root_real = root.resolve()
    candidate = root.joinpath(*parts)
    # Resolve existing symlinked parents as well as the final path.  A project
    # adapter must never escape into user-global configuration through a link.
    candidate_real = candidate.resolve(strict=False)
    try:
        candidate_real.relative_to(root_real)
    except ValueError as exc:
        raise ValueError(f"artifact path escapes project root: {relpath!r}") from exc
    if candidate.is_symlink():
        raise ValueError(f"artifact path is a symlink: {relpath!r}")
    return candidate


def _read_existing(path: Path) -> bytes | None:
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError("artifact path exists but is not a regular file")
    return path.read_bytes()


def preflight_install(
        domain_root: Path,
        targets: tuple[AdapterInstallTarget, ...] | list[AdapterInstallTarget],
        ) -> InstallPlan:
    """Read every selected adapter and decide the entire operation first."""
    root = Path(domain_root).resolve()
    decisions: list[ArtifactDecision] = []
    findings: list[str] = []

    for target in targets:
        adapter = target.adapter
        harness = str(getattr(adapter, "name", type(adapter).__name__))
        try:
            rendered = adapter.render(target.context)
            inspection = adapter.inspect(root, target.context)
        except Exception as exc:  # adapters report expected shapes; bugs refuse
            findings.append(
                f"{harness}: adapter preflight failed: "
                f"{type(exc).__name__}: {exc}")
            continue
        if not isinstance(rendered, dict):
            findings.append(f"{harness}: renderer did not return a path map")
            continue
        for relpath in sorted(rendered):
            desired = rendered[relpath]
            if not isinstance(relpath, str) or not isinstance(desired, bytes):
                findings.append(
                    f"{harness}: rendered artifact must be str -> bytes")
                continue
            try:
                path = _artifact_path(root, relpath)
                before = _read_existing(path)
                policy = target.policies.get(relpath, target.default_policy)
                outcome = policy.decide(
                    path=relpath, before=before, desired=desired,
                    inspection=inspection)
                decisions.append(ArtifactDecision(
                    harness=harness, path=relpath, action=outcome.action,
                    reason=outcome.reason, before=before, after=outcome.after))
            except (OSError, ValueError) as exc:
                findings.append(f"{harness} {relpath!r}: {exc}")

    # Two selected adapters owning one path is ambiguous even if their desired
    # bytes happen to match today.  Convert every claimant into a refusal.
    owners: dict[str, list[int]] = {}
    for index, decision in enumerate(decisions):
        owners.setdefault(portable_artifact_key(decision.path), []).append(index)
    for _key, indices in owners.items():
        if len(indices) < 2:
            continue
        names = ", ".join(decisions[index].harness for index in indices)
        spellings = ", ".join(repr(decisions[index].path)
                              for index in indices)
        for index in indices:
            decisions[index] = replace(
                decisions[index], action="refuse",
                reason=(f"ambiguous ownership: {names} render the same "
                        f"portable path ({spellings})"))

    return InstallPlan(root, tuple(decisions), tuple(findings))


def _current_bytes(root: Path, decision: ArtifactDecision) -> bytes | None:
    path = _artifact_path(root, decision.path)
    return _read_existing(path)


def _write_staged(path: Path, payload: bytes, mode: int) -> Path:
    fd, raw_name = tempfile.mkstemp(
        prefix=f".{path.name}.mdllm-", suffix=".tmp", dir=path.parent)
    staged = Path(raw_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(staged, mode)
        return staged
    except Exception:
        try:
            staged.unlink(missing_ok=True)
        finally:
            raise


def _restore(
        path: Path,
        before: bytes | None,
        mode: int | None,
        expected_after: bytes,
        ) -> None:
    # Never turn rollback into a second lost update.  Another process may have
    # changed an already-applied artifact while a later replace was failing;
    # in that case its bytes belong to that process and must remain untouched.
    if _read_existing(path) != expected_after:
        raise InstallStateChanged(
            "rollback conflict: artifact changed after adapter write")
    if before is None:
        path.unlink(missing_ok=True)
        return
    assert mode is not None
    staged = _write_staged(path, before, mode)
    try:
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def _ensure_parent_dirs(
        root: Path, parent: Path, created: list[Path]) -> None:
    """Create parents one at a time, recording only directories we created."""
    relative = parent.relative_to(root)
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        try:
            cursor.mkdir()
        except FileExistsError:
            if not cursor.is_dir():
                raise
        else:
            created.append(cursor)


def _remove_empty_dirs(created: list[Path]) -> None:
    """Remove transaction-created directories only while they remain empty."""
    for path in reversed(created):
        try:
            path.rmdir()
        except OSError:
            pass


def apply_install(plan: InstallPlan) -> ApplyResult:
    """Apply a successful plan, with state recheck and best-effort rollback."""
    if plan.refused:
        reasons = list(plan.findings) + [
            f"{d.harness} {d.path}: {d.reason}"
            for d in plan.decisions if d.action == "refuse"]
        raise InstallRefused("adapter install refused: " + "; ".join(reasons))

    changes = [decision for decision in plan.decisions
               if decision.changes_bytes]
    unchanged = tuple(decision.path for decision in plan.decisions
                      if not decision.changes_bytes)

    # Verify *all* input states before making even the first project write.
    for decision in plan.decisions:
        try:
            current = _current_bytes(plan.domain_root, decision)
        except (OSError, ValueError) as exc:
            raise InstallStateChanged(
                f"{decision.path} cannot be rechecked: {exc}") from exc
        if current != decision.before:
            raise InstallStateChanged(
                f"{decision.path} changed after adapter-install preflight")

    staged: list[tuple[Path, Path, ArtifactDecision, int | None]] = []
    created_dirs: list[Path] = []
    try:
        for decision in changes:
            path = _artifact_path(plan.domain_root, decision.path)
            _ensure_parent_dirs(plan.domain_root, path.parent, created_dirs)
            old_mode = (stat.S_IMODE(path.stat().st_mode)
                        if decision.before is not None else None)
            mode = old_mode if old_mode is not None else 0o644
            assert decision.after is not None
            temp_path = _write_staged(path, decision.after, mode)
            staged.append((temp_path, path, decision, old_mode))
    except Exception as exc:
        for temp_path, _, _, _ in staged:
            temp_path.unlink(missing_ok=True)
        _remove_empty_dirs(created_dirs)
        raise AtomicInstallError(f"could not stage adapter artifacts: {exc}") from exc

    applied: list[tuple[Path, ArtifactDecision, int | None]] = []
    try:
        for temp_path, path, decision, old_mode in staged:
            # Close the widest practical TOCTOU window before each replace.
            if _read_existing(path) != decision.before:
                raise InstallStateChanged(
                    f"{decision.path} changed while artifacts were staged")
            os.replace(temp_path, path)
            applied.append((path, decision, old_mode))
    except Exception as exc:
        rollback_errors: list[str] = []
        for path, decision, old_mode in reversed(applied):
            try:
                assert decision.after is not None
                _restore(path, decision.before, old_mode, decision.after)
            except Exception as rollback_exc:  # report a damaged transaction
                rollback_errors.append(f"{decision.path}: {rollback_exc}")
        for temp_path, _, _, _ in staged:
            temp_path.unlink(missing_ok=True)
        _remove_empty_dirs(created_dirs)
        suffix = ("; rollback failures: " + "; ".join(rollback_errors)
                  if rollback_errors else "")
        if isinstance(exc, InstallStateChanged) and not rollback_errors:
            raise exc
        raise AtomicInstallError(f"adapter install failed: {exc}{suffix}") from exc
    finally:
        for temp_path, _, _, _ in staged:
            temp_path.unlink(missing_ok=True)

    return ApplyResult(
        written=tuple(decision.path for decision in changes),
        unchanged=unchanged,
    )


def cmd_adapter_install(args) -> int:
    """Show the complete owned diff, then apply only an unambiguous plan."""
    from . import adapters
    from .scaffold import MDLLM_ENTRY

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"mdllm: adapter-install target is not a directory: {root}")
        return 2
    try:
        framework_rel = Path(os.path.relpath(
            MDLLM_ENTRY.parents[1], root)).as_posix()
    except ValueError:
        print("mdllm: framework and target have no relative path; refusing "
              "to embed an absolute machine-specific adapter command")
        return 2
    context = HarnessContext(framework_root_rel=framework_rel)
    selected = adapters.selection(args.harness)
    targets = tuple(target_for_adapter(adapters.get(name), context)
                    for name in selected)
    plan = preflight_install(root, targets)

    print(f"## Adapter Install — {root}\n")
    for decision in plan.decisions:
        print(f"  {decision.action.upper():7s}  {decision.harness}:"
              f"{decision.path} — {decision.reason}")
    for finding in plan.findings:
        print(f"  REFUSE   {finding}")
    diff = plan.owned_diff()
    print("\nOwned apply diff:")
    print(diff.rstrip() if diff else "  (no applicable byte changes)")
    refusal_diff = plan.refusal_diff()
    if refusal_diff:
        print("\nRefusal comparison (diagnostic only; never applied):")
        print(refusal_diff.rstrip())

    if plan.refused:
        print("\nREFUSED — no adapter artifact was written.")
        return 1
    if getattr(args, "dry_run", False):
        print("\nDRY RUN — preflight complete; no adapter artifact was written.")
        return 0
    try:
        result = apply_install(plan)
    except (InstallRefused, InstallStateChanged, AtomicInstallError) as exc:
        print(f"\nREFUSED — no incomplete adapter install accepted: {exc}")
        return 1
    print(f"\nApplied: {len(result.written)} written; "
          f"{len(result.unchanged)} unchanged.")
    return 0
