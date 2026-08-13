"""Project-local Codex lifecycle adapter.

This is the vendor-shaped outer edge of MarkdownLLM's neutral lifecycle
contract.  Rendering is pure: it returns one ``.codex/hooks.json`` artifact
and never reads or writes project state.  Inspection is read-only and covers
both project hook sources Codex can load (``hooks.json`` and inline hooks in
``config.toml``); global/user configuration is deliberately out of scope.

Codex launches multiple matching command handlers concurrently.  The ordered
``estate-sync`` -> ``session-start`` policy is therefore rendered inside one
SessionStart command handler.  PostToolUse ignores plain stdout, so this
adapter translates neutral runner output into Codex's JSON
``additionalContext`` envelope.  Both commands resolve the domain from Git
rather than the session working directory and use the shared MarkdownLLM
runtime policy.

Static inspection cannot observe project trust or the exact-hook review hash.
Those remain explicitly unknown and are routed to the human ``/hooks`` flow.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from typing import Any

try:  # Python 3.11+; the framework still supports Python 3.10.
    import tomllib
except ImportError:  # pragma: no cover - exercised only on Python 3.10
    tomllib = None  # type: ignore[assignment]

from ..harness_ports import (
    AdapterCapabilities,
    HANDLER_TIMEOUT_SECONDS,
    HarnessContext,
    InspectionReport,
    LifecycleBinding,
    ManagedFragment,
)
from ..harness_diagnostics import (
    AdapterProbe,
    managed_definition_hash,
)
from ..runtime import SH_RESOLVE, powershell_candidate_records
from ..adapter_install import (
    NestedJsonArrayGroupsPolicy,
    load_unique_json,
)

HOOKS_PATH = ".codex/hooks.json"
CONFIG_PATH = ".codex/config.toml"
_SESSION_MATCHER = "startup|resume|clear|compact"
_WRITE_MATCHER = "Edit|Write"
_CONTEXT_LIMIT = 2500
_DESCRIPTION = "MarkdownLLM project lifecycle hardening"
_NON_SEMANTIC_HANDLER_EXTENSIONS = {"statusMessage"}

_EVENT_BY_MOMENT = {
    "session-start": "SessionStart",
    "post-write": "PostToolUse",
}


def _ps_quote(value: str) -> str:
    """Single-quote one literal for an inline PowerShell program."""
    return "'" + value.replace("'", "''") + "'"


def _shell_single_quote(value: str) -> str:
    """Single-quote one literal for the POSIX hook command."""
    return "'" + value.replace("'", "'\"'\"'") + "'"


class CodexAdapter:
    """Pure renderer and conservative project-local inspector for Codex."""

    name = "codex"

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            harness=self.name,
            lifecycle_moments=("session-start", "post-write"),
            notes=("project-local hooks.json; one SessionStart handler owns "
                   "ordered startup; trust/review remain human-observed"),
        )

    def install_policies(self) -> dict[str, NestedJsonArrayGroupsPolicy]:
        """Declare the exact composite fragment this adapter may add."""
        return {HOOKS_PATH: NestedJsonArrayGroupsPolicy(
            container_member="hooks",
            owned_array_members=tuple(_EVENT_BY_MOMENT.values()),
        )}

    # ------------------------------------------------------------- rendering

    @staticmethod
    def _mdllm_posix(context: HarnessContext) -> str:
        rel = context.framework_root_rel.rstrip("/") or "."
        # ROOT must expand, while every byte supplied by the render context
        # stays literal.  In particular, $, backticks, quotes and command
        # substitutions in a legal path must never become shell syntax.
        return '"$ROOT/"' + _shell_single_quote(f"{rel}/tools/mdllm.py")

    @staticmethod
    def _runner_windows(context: HarnessContext) -> str:
        rel = context.framework_root_rel.replace("/", "\\").rstrip("\\")
        rel = rel or "."
        return f"{rel}\\tools\\mdllm.ps1"

    @staticmethod
    def _entry_windows(context: HarnessContext) -> str:
        rel = context.framework_root_rel.replace("/", "\\").rstrip("\\")
        rel = rel or "."
        return f"{rel}\\tools\\mdllm.py"

    @staticmethod
    def _event_name(moment: str) -> str:
        try:
            return _EVENT_BY_MOMENT[moment]
        except KeyError as exc:
            raise ValueError(f"unsupported Codex lifecycle moment: {moment}") \
                from exc

    def format_lifecycle_output(self, moment: str, text: str,
                                passed: bool) -> str:
        """Translate neutral runner output into Codex's JSON hook channel.

        SessionStart always returns structured additional context. PostToolUse
        remains quiet when validation passes and sends model-visible context
        only on failure; plain stdout is ignored for that event.
        """
        if moment == "post-write" and passed:
            return ""
        event = self._event_name(moment)
        return json.dumps({
            "hookSpecificOutput": {
                "hookEventName": event,
                "additionalContext": text,
            },
        }, separators=(",", ":"))

    def _event_posix(self, context: HarnessContext, moment: str,
                     definition_hash: str) -> str:
        unavailable = self.format_lifecycle_output(
            moment,
            f"MarkdownLLM {moment} could not run: no floor-capable Python "
            "or mdllm.py was found.",
            False,
        )
        return (
            'ROOT="$(git rev-parse --show-toplevel)"\n'
            f"MDLLM={self._mdllm_posix(context)}\n"
            f"{SH_RESOLVE}\n"
            'if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then\n'
            f"  printf '%s\\n' {_shell_single_quote(unavailable)}\n"
            "else\n"
            f'  mdllm_python "$MDLLM" harness-event codex {moment} "$ROOT" '
            f'{_shell_single_quote(definition_hash)}\n'
            "fi\n"
            "exit 0"
        )

    def _event_windows(self, context: HarnessContext, moment: str,
                       definition_hash: str) -> str:
        runner_rel = _ps_quote(self._runner_windows(context))
        entry_rel = _ps_quote(self._entry_windows(context))
        event = _ps_quote(self._event_name(moment))
        unavailable = _ps_quote(
            f"MarkdownLLM {moment} could not run: no floor-capable Python "
            "or framework runner was found.")
        failed = _ps_quote(
            f"MarkdownLLM {moment} returned a non-zero status; the lifecycle "
            "failure was surfaced but does not enforce the harness action.")
        script = (
            "$ErrorActionPreference = 'Stop'; "
            "$PSNativeCommandUseErrorActionPreference = $false; "
            "function Write-MdllmFailure([string]$detail) { "
            f"$payload = @{{ hookSpecificOutput = @{{ hookEventName = {event}; "
            "additionalContext = $detail } }; "
            "$payload | ConvertTo-Json -Compress -Depth 3 }; "
            "try { "
            "$root = (& git rev-parse --show-toplevel); "
            "if ($LASTEXITCODE -ne 0 -or -not $root) { "
            "throw 'Git repository root could not be resolved' }; "
            "$hostName = if (Test-Path -LiteralPath "
            "(Join-Path $PSHOME 'pwsh.exe')) { 'pwsh.exe' } "
            "else { 'powershell.exe' }; "
            "$hostExecutable = Join-Path $PSHOME $hostName; "
            f"$entry = Join-Path $root {entry_rel}; "
            f"$runner = Join-Path $root {runner_rel}; "
            "$fw = Split-Path -Parent (Split-Path -Parent $entry); "
            f"$candidates = {powershell_candidate_records()}; "
            "$python = $null; $pythonPrefix = @(); "
            "foreach ($candidate in $candidates) { "
            "$resolved = $null; "
            "if (Test-Path -LiteralPath $candidate.Executable) { "
            "$resolved = $candidate.Executable "
            "} else { "
            "$found = Get-Command $candidate.Executable "
            "-ErrorAction SilentlyContinue; "
            "if ($found) { $resolved = $found.Source } }; "
            "if (-not $resolved) { continue }; "
            "try { & $resolved @($candidate.PrefixArguments) "
            "-c 'import yaml' *> $null } "
            "catch { continue }; "
            "if ($LASTEXITCODE -eq 0) { $python = $resolved; "
            "$pythonPrefix = @($candidate.PrefixArguments); break } }; "
            "$executable = $null; $launchPrefix = @(); "
            "if ($python -and (Test-Path -LiteralPath $entry)) { "
            "$executable = $python; $launchPrefix = @($pythonPrefix) + @($entry) "
            "} elseif (Test-Path -LiteralPath $runner) { "
            # The repository runner calls exit.  Keep it in a child host so
            # its status can never bypass this hook's surface-and-continue
            # finally block.
            "$executable = $hostExecutable; "
            "$launchPrefix = @('-NoProfile', '-File', $runner) }; "
            "if ($executable) { "
            f"& $executable @launchPrefix harness-event codex {moment} "
            f"$root {_ps_quote(definition_hash)}; "
            f"if ($LASTEXITCODE -ne 0) {{ Write-MdllmFailure {failed} }} "
            f"}} else {{ Write-MdllmFailure {unavailable} }} "
            "} catch { Write-MdllmFailure ("
            f"{unavailable} + ' ' + $_.Exception.Message) "
            "} finally { exit 0 }"
        )
        encoded = base64.b64encode(
            script.encode("utf-16-le")).decode("ascii")
        # ``commandWindows`` is entered through stock cmd.exe, which chooses
        # PowerShell 7 only when it is actually discoverable.  The encoded
        # payload keeps every context/path byte out of cmd's metacharacter and
        # percent-expansion grammar.  Delayed expansion carries one payload
        # copy to either host, keeping the command below cmd.exe's 8191-byte
        # limit.  Both the PowerShell finally block and this outer cmd exit
        # preserve the advisory surface-and-continue contract.
        return (
            'cmd.exe /d /v:on /s /c "'
            f'set _MDLLM_HOOK={encoded}'
            '&where.exe pwsh.exe >nul 2>nul'
            '&if errorlevel 1 ('
            'powershell.exe -NoLogo -NoProfile -NonInteractive '
            '-EncodedCommand !_MDLLM_HOOK!) else ('
            'pwsh.exe -NoLogo -NoProfile -NonInteractive '
            '-EncodedCommand !_MDLLM_HOOK!)'
            '&exit /b 0"'
        )

    def _handler(self, context: HarnessContext, moment: str,
                 definition_hash: str) -> dict:
        return {
            "type": "command",
            "command": self._event_posix(
                context, moment, definition_hash),
            "commandWindows": self._event_windows(
                context, moment, definition_hash),
            "timeout": HANDLER_TIMEOUT_SECONDS,
            "additionalContextLimit": _CONTEXT_LIMIT,
        }

    def _definition_hash(self, context: HarnessContext, moment: str) -> str:
        """Hash the complete owned definition with a stable hash placeholder.

        The literal attestation hash is intentionally excluded from its own
        input. An old installed hook therefore keeps its old literal and
        cannot mint current evidence after the renderer evolves.
        """
        event = self._event_name(moment)
        binding = context.binding(moment)
        group = {
            "matcher": (_SESSION_MATCHER if moment == "session-start"
                        else _WRITE_MATCHER),
            "hooks": [self._handler(
                context, moment, "<managed-definition-hash>")],
        }
        return managed_definition_hash({
            "artifact": HOOKS_PATH,
            "binding": json.dumps({
                "moment": binding.moment,
                "steps": [{
                    "operation": step.operation,
                    "argv": list(step.argv),
                    "timeout_seconds": step.timeout_seconds,
                } for step in binding.steps],
                "delivery": binding.delivery,
                "failure": binding.failure,
                "total_timeout_seconds": binding.total_timeout_seconds,
                "runner_reserve_seconds": binding.runner_reserve_seconds,
            }, sort_keys=True, separators=(",", ":")),
            "description": _DESCRIPTION,
            "event": event,
            "group": json.dumps(group, sort_keys=True, separators=(",", ":")),
        })

    def probe(self, domain_root: Path,
              context: HarnessContext) -> AdapterProbe:
        """Return static Codex facts without claiming trust or execution."""
        del domain_root  # Project trust has no stable machine-readable API.
        return AdapterProbe(
            trust="unknown",
            trust_detail=("Codex project trust and exact-hook review are "
                          "human-observed, not inferred from config bytes"),
            definition_hashes={
                moment: self._definition_hash(context, moment)
                for moment in self.capabilities().lifecycle_moments
            },
            remediations=(
                "review project trust and the exact current hook definitions "
                "with `/hooks`",
            ),
            ownership=(
                "MarkdownLLM owns only its lifecycle groups in project "
                ".codex/hooks.json; config.toml and global config remain "
                "operator-owned",
            ),
        )

    def render(self, context: HarnessContext) -> dict[str, bytes]:
        # Fail early if the neutral context omitted a moment this adapter
        # declares. The runner consumes these same bindings at execution.
        context.binding("session-start")
        context.binding("post-write")
        session_hash = self._definition_hash(context, "session-start")
        post_write_hash = self._definition_hash(context, "post-write")
        payload = {
            "description": _DESCRIPTION,
            "hooks": {
                "SessionStart": [{
                    "matcher": _SESSION_MATCHER,
                    "hooks": [self._handler(
                        context, "session-start", session_hash)],
                }],
                "PostToolUse": [{
                    "matcher": _WRITE_MATCHER,
                    "hooks": [self._handler(
                        context, "post-write", post_write_hash)],
                }],
            },
        }
        return {HOOKS_PATH:
                (json.dumps(payload, indent=2) + "\n").encode("utf-8")}

    # ----------------------------------------------------------- inspection

    @staticmethod
    def _absent(path: str) -> ManagedFragment:
        return ManagedFragment(
            path=path, present=False, artifact_present=False)

    @staticmethod
    def _unreadable(path: str, exc: BaseException) -> ManagedFragment:
        return ManagedFragment(
            path=path, present=False, readable=False,
            issues=(type(exc).__name__,))

    @staticmethod
    def _invalid(path: str, issue: str) -> ManagedFragment:
        return ManagedFragment(
            path=path, present=False, readable=True, valid=False,
            issues=(issue,))

    @staticmethod
    def _validate_hook_schema(config: Any) -> str | None:
        if not isinstance(config, dict):
            return "top level is not an object"
        if "description" in config and not isinstance(
                config["description"], str):
            return "description is not a string"
        hooks = config.get("hooks", {})
        if not isinstance(hooks, dict):
            return "hooks is not an object"
        for event, groups in hooks.items():
            if not isinstance(event, str) or not isinstance(groups, list):
                return f"hook event {event!r} is not a list"
            for group in groups:
                if not isinstance(group, dict):
                    return f"hook group under {event!r} is not an object"
                if ("matcher" in group
                        and not isinstance(group["matcher"], str)):
                    return f"matcher under {event!r} is not a string"
                handlers = group.get("hooks")
                if not isinstance(handlers, list):
                    return f"handlers under {event!r} are not a list"
                for handler in handlers:
                    if not isinstance(handler, dict):
                        return f"handler under {event!r} is not an object"
                    if not isinstance(handler.get("type"), str):
                        return f"handler type under {event!r} is not a string"
                    if handler.get("type") == "command":
                        if not isinstance(handler.get("command"), str):
                            return (f"command handler under {event!r} has no "
                                    "string command")
                        if ("commandWindows" in handler and not isinstance(
                                handler["commandWindows"], str)):
                            return (f"commandWindows under {event!r} is not "
                                    "a string")
                    for field in ("timeout", "additionalContextLimit"):
                        if field in handler and (
                                not isinstance(handler[field], (int, float))
                                or isinstance(handler[field], bool)
                                or handler[field] <= 0):
                            return (f"{field} under {event!r} is not a "
                                    "positive number")
        return None

    @staticmethod
    def _contains_mdllm(group: dict) -> bool:
        for handler in group.get("hooks", []):
            for field in ("command", "commandWindows"):
                value = handler.get(field)
                if isinstance(value, str) and (
                        "tools/mdllm.py" in value
                        or "tools\\mdllm.ps1" in value):
                    return True
        return False

    def _compare_managed_group(
            self, moment: str, actual: dict, wanted: dict,
            binding: LifecycleBinding, issues: list[str],
            extensions: list[str], findings: list[str]) -> tuple[str, ...]:
        managed_equal = actual.get("matcher") == wanted.get("matcher")
        if not managed_equal:
            issues.append(
                f"{moment} matcher diverges from the managed form: "
                f"{actual.get('matcher')!r}")
        for key in actual:
            if key not in wanted:
                managed_equal = False
                issues.append(
                    f"{moment} unknown managed group field {key!r} may "
                    "change hook semantics")

        actual_handlers = actual.get("hooks", [])
        wanted_handlers = wanted["hooks"]
        if len(actual_handlers) != len(wanted_handlers):
            managed_equal = False
            issues.append(
                f"{moment} handler count diverges from the managed form "
                f"({len(actual_handlers)} vs {len(wanted_handlers)})")
            if len(actual_handlers) > 1:
                findings.append(
                    f"ambiguous: {moment} has multiple matching command "
                    "handlers; Codex may launch them concurrently")
        if not actual_handlers:
            return ()

        actual_handler = actual_handlers[0]
        wanted_handler = wanted_handlers[0]
        for key, value in wanted_handler.items():
            if actual_handler.get(key) != value:
                managed_equal = False
                issues.append(
                    f"{moment} managed handler field {key!r} diverges")
        for key in actual_handler:
            if key not in wanted_handler:
                if key in _NON_SEMANTIC_HANDLER_EXTENSIONS:
                    extensions.append(
                        f"{moment} handler field {key!r} is operator-owned")
                else:
                    managed_equal = False
                    issues.append(
                        f"{moment} unknown managed handler field {key!r} "
                        "may change hook semantics")
        if managed_equal:
            return tuple(step.operation for step in binding.steps)
        return ()

    def _inspect_hooks_json(
            self, domain_root: Path, context: HarnessContext,
    ) -> tuple[ManagedFragment, tuple[str, ...], tuple[str, ...],
               tuple[str, ...], bool]:
        path = domain_root / HOOKS_PATH
        try:
            if not path.exists():
                return self._absent(HOOKS_PATH), (), (), (), False
            raw = path.read_bytes()
        except OSError as exc:
            return self._unreadable(HOOKS_PATH, exc), (), (), (), False
        try:
            config = load_unique_json(raw)
        except ValueError as exc:
            return self._invalid(HOOKS_PATH, str(exc)), (), (), (), False
        schema_issue = self._validate_hook_schema(config)
        if schema_issue:
            return self._invalid(HOOKS_PATH, schema_issue), (), (), (), False

        hooks = config.get("hooks", {})
        source_active = any(hooks.values())
        desired = json.loads(
            self.render(context)[HOOKS_PATH].decode("utf-8"))
        wanted_hooks = desired["hooks"]
        realised: dict[str, tuple[str, ...]] = {}
        issues: list[str] = []
        extensions: list[str] = []
        findings: list[str] = []

        for moment, event in _EVENT_BY_MOMENT.items():
            groups = hooks.get(event, [])
            wanted = wanted_hooks[event][0]
            exact = [i for i, group in enumerate(groups)
                     if group.get("matcher") == wanted["matcher"]]
            marked = [i for i, group in enumerate(groups)
                      if self._contains_mdllm(group)]
            candidates = exact or marked
            if not candidates:
                for _ in groups:
                    extensions.append(
                        f"{event} group is operator-owned")
                continue
            managed_index = candidates[0]
            if len(candidates) > 1:
                findings.append(
                    f"ambiguous: multiple {event} groups look managed; "
                    "the first is inspected")
            realised[moment] = self._compare_managed_group(
                moment, groups[managed_index], wanted,
                context.binding(moment), issues, extensions, findings)
            for index, _ in enumerate(groups):
                if index != managed_index:
                    extensions.append(
                        f"additional {event} hook group is operator-owned")

        for event in sorted(hooks):
            if event not in wanted_hooks:
                extensions.append(
                    f"hook event {event!r} is operator-owned")

        operator_owned: list[str] = []
        for key in sorted(config):
            if key == "hooks":
                continue
            if key == "description" and config[key] == _DESCRIPTION:
                continue
            operator_owned.append(f"top-level key {key!r} is operator-owned")

        present = bool(realised)
        expected = {
            binding.moment: tuple(step.operation for step in binding.steps)
            for binding in context.bindings
        }
        current = ((realised == expected and not issues and not findings)
                   if present else None)
        fragment = ManagedFragment(
            path=HOOKS_PATH, present=present, readable=True, valid=True,
            current=current, intents_realised=realised,
            issues=tuple(issues),
        )
        return (fragment, tuple(operator_owned), tuple(extensions),
                tuple(findings), source_active)

    def _inspect_config_toml(
            self, domain_root: Path,
    ) -> tuple[ManagedFragment, tuple[str, ...], tuple[str, ...], bool]:
        path = domain_root / CONFIG_PATH
        try:
            if not path.exists():
                return self._absent(CONFIG_PATH), (), (), False
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            return self._unreadable(CONFIG_PATH, exc), (), (), False

        if tomllib is None:  # conservative compatibility path on Python 3.10
            has_hooks = bool(re.search(
                r"(?m)^\s*\[\[?\s*hooks(?:\.|\s*\])", raw))
            fragment = ManagedFragment(
                path=CONFIG_PATH, present=has_hooks, readable=True,
                valid=None, current=None,
                issues=(("inline hooks detected but TOML validity is unknown "
                         "on this Python runtime",) if has_hooks else ()),
            )
            findings = (("config.toml hook ownership/currency is unknown; "
                         "the adapter renders hooks.json only",)
                        if has_hooks else ())
            return fragment, findings, ((CONFIG_PATH,) if has_hooks else ()), \
                has_hooks

        try:
            config = tomllib.loads(raw)
        except (tomllib.TOMLDecodeError, UnicodeError) as exc:
            return self._invalid(CONFIG_PATH, str(exc)), (), (), False
        hooks = config.get("hooks")
        if hooks is not None and not isinstance(hooks, dict):
            return self._invalid(
                CONFIG_PATH, "inline hooks table is not an object"), (), (), False
        if hooks:
            schema_issue = self._validate_hook_schema({"hooks": hooks})
            if schema_issue:
                return self._invalid(CONFIG_PATH, schema_issue), (), (), False
        source_active = bool(hooks)
        fragment = ManagedFragment(
            path=CONFIG_PATH, present=source_active, readable=True, valid=True,
            current=None,
            issues=(("inline hooks are an alternate project source; static "
                     "inspection does not infer MarkdownLLM ownership",)
                    if source_active else ()),
        )
        findings = (("config.toml hook ownership/currency is unknown; the "
                     "adapter renders hooks.json only",)
                    if source_active else ())
        operator = (("project config.toml is operator-owned",)
                    if path.exists() else ())
        return fragment, findings, operator, source_active

    def inspect(self, domain_root: Path,
                context: HarnessContext) -> InspectionReport:
        """Inspect both project hook sources without mutating either one.

        Expected I/O, JSON/TOML, and shape failures become facts.  A final
        broad guard keeps an exotic filesystem/config failure diagnostic too;
        inspection is never allowed to crash doctor or install preflight.
        """
        try:
            (hooks_fragment, hooks_operator, hooks_extensions,
             hooks_findings, hooks_active) = self._inspect_hooks_json(
                 domain_root, context)
        except Exception as exc:  # defensive boundary: inspector never throws
            hooks_fragment = self._unreadable(HOOKS_PATH, exc)
            hooks_operator = hooks_extensions = hooks_findings = ()
            hooks_active = False
        try:
            (toml_fragment, toml_findings,
             toml_operator, toml_active) = self._inspect_config_toml(
                 domain_root)
        except Exception as exc:  # defensive boundary: inspector never throws
            toml_fragment = self._unreadable(CONFIG_PATH, exc)
            toml_findings = toml_operator = ()
            toml_active = False

        findings = [*hooks_findings, *toml_findings]
        if toml_fragment.artifact_present:
            if toml_fragment.readable is False:
                findings.append(
                    "config.toml is unreadable; alternate project hook "
                    "ownership cannot be ruled out")
            elif toml_fragment.valid is False:
                detail = "; ".join(toml_fragment.issues) or "invalid TOML"
                findings.append(
                    "config.toml is invalid; alternate project hook "
                    f"ownership cannot be ruled out: {detail}")
            elif toml_fragment.valid is None:
                findings.append(
                    "config.toml validity is unknown; alternate project "
                    "hook ownership cannot be ruled out")
        if hooks_active and toml_active:
            findings.append(
                "ambiguous: both project hooks.json and inline config.toml "
                "hooks are active; Codex loads both")
        return InspectionReport(
            harness=self.name,
            fragments=(hooks_fragment, toml_fragment),
            operator_owned=(*hooks_operator, *toml_operator),
            extensions=hooks_extensions,
            findings=tuple(findings),
        )


CODEX = CodexAdapter()
