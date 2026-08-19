"""The Claude Code adapter — Phase 2C of vendor-harness-adapter-foundation.

Everything Claude-shaped that used to live inline in scaffold and doctor:
the `.claude/settings.json` lifecycle projection, the deliberate-shortcut
projections (`.claude/commands/` for Claude Code and `.github/prompts/` for VS
Code Copilot), the scaffold completion guidance, and the doctor advisory line.
Those shortcut projections share a renderer for compatibility; Claude Code
lifecycle execution and Copilot lifecycle compatibility remain separate
evidence claims.

Thin by construction: this module translates the inward lifecycle bindings
into Claude's config format and reads that format back. It contains no domain
reasoning, no thing schema, no validation logic.

Byte-compatibility is a release gate, not an aspiration: `render()` must
reproduce `tools/tests/fixtures/claude_golden/settings.json.golden` exactly
(Phase 0 freeze), derived from the bindings — never pasted.

Current Claude launches all matching command handlers in parallel.  The frozen
two-handler SessionStart bytes below are therefore a legacy migration input,
not proof that the inward ordered lifecycle was realised.  The Phase 5R
projection replaces them with one managed handler entering the neutral runner;
until then scaffold/install remains held at the reopened gate.

Inspection semantics (accepted at the Phase 2B challenge):
- currency derives from THIS adapter's renderer — no second expected list;
- formatting-only differences are semantically current;
- a wrong framework path, matcher, argument, ordering, or managed field is
  stale; an added trailing argument on a managed command is an extension and
  does NOT break currency; extra sibling hook groups are extensions;
- absent, unreadable, malformed, and schema-invalid artifacts return honest
  reports, never exceptions, and inspection never writes a byte.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..adapter_install import LegacyDefinition, TopLevelJsonFragmentPolicy
from ..harness_diagnostics import AdapterProbe, managed_definition_hash
from ..harness_ports import (
    HANDLER_TIMEOUT_SECONDS, AdapterCapabilities, DiagnosticPresentation,
    HarnessContext, InspectionReport, LifecycleBinding, ManagedFragment,
)
from ..runtime import SH_RESOLVE


def _unique_json_object(pairs):
    """Reject duplicate keys instead of accepting json.loads' last value.

    Duplicate settings keys have no single operator-owned meaning.  Treating
    the last ``hooks`` member as authoritative could certify ambiguous bytes
    as the current managed fragment, while another JSON consumer selects a
    different occurrence.
    """
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key {key!r}")
        out[key] = value
    return out

SETTINGS_PATH = ".claude/settings.json"
LOCAL_SETTINGS_PATH = ".claude/settings.local.json"

# Inward delivery semantics -> Claude event vocabulary. Lives here and only
# here; a neutral module never names these.
_DELIVERY_EVENT = {"context": "SessionStart", "feedback": "PostToolUse"}
_DELIVERY_EVENT_BY_MOMENT = {
    "session-start": "SessionStart",
    "post-write": "PostToolUse",
}
_FEEDBACK_MATCHER = "Write|Edit"
_HASH_PLACEHOLDER = "<managed-definition-hash>"
_ROOT_POWERSHELL_SESSION = (
    'python "$env:CLAUDE_PROJECT_DIR/tools/mdllm.py" estate-sync .; '
    'python "$env:CLAUDE_PROJECT_DIR/tools/mdllm.py" session-start .')
_ROOT_POWERSHELL_POST_WRITE = (
    'python "$env:CLAUDE_PROJECT_DIR/tools/mdllm.py" validate . --quiet')
_LEGACY_ROOT_FIXED_STEP_V1 = Path(__file__).with_name("legacy") / \
    "claude-hooks-root-fixed-step-v1.json"


def _shell_single_quote(value: str) -> str:
    """Single-quote one literal for the POSIX hook command.

    Every byte the render context supplies stays literal: `$`, backticks,
    quotes and command substitutions inside a legal path must never become
    shell syntax.
    """
    return "'" + value.replace("'", "'\"'\"'") + "'"


class ClaudeCodeAdapter:
    """Render/inspect Claude Code lifecycle plus compatible shortcut files.

    The `.github/prompts/` projection is inert until Copilot invokes it. It
    does not make a Claude lifecycle transcript evidence for Copilot.
    """

    name = "claude-code"

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            harness=self.name,
            lifecycle_moments=("session-start", "post-write"),
            notes="Claude Code lifecycle projection; Copilot shortcut output "
                  "is separate and its lifecycle remains unverified")

    def install_policies(self):
        """Own only the top-level hooks member in composite settings."""
        return {SETTINGS_PATH: TopLevelJsonFragmentPolicy("hooks")}

    def _legacy_hooks(self, context: HarnessContext) -> dict[str, object]:
        rel = context.framework_root_rel.rstrip("/") or "."
        prefix = f"python {rel}/tools/mdllm.py "
        return {
            "SessionStart": [{"hooks": [
                {"type": "command", "command":
                 f"{prefix}{step.operation} ."}
                for step in context.binding("session-start").steps
            ]}],
            "PostToolUse": [{
                "matcher": _FEEDBACK_MATCHER,
                "hooks": [{"type": "command", "command":
                           f"{prefix}validate . --quiet"}],
            }],
        }

    def _root_powershell_legacy_hooks(self) -> dict[str, object]:
        return {
            "SessionStart": [{"hooks": [{
                "type": "command", "shell": "powershell",
                "command": _ROOT_POWERSHELL_SESSION,
            }]}],
            "PostToolUse": [{
                "matcher": _FEEDBACK_MATCHER,
                "hooks": [{
                    "type": "command", "shell": "powershell",
                    "command": _ROOT_POWERSHELL_POST_WRITE,
                }],
            }],
        }

    def legacy_definitions(
            self, context: HarnessContext) -> tuple[LegacyDefinition, ...]:
        """Exact historical managed fragments; recognition data only."""
        output_tail_hooks: dict = {}
        for binding in context.bindings:
            event = _DELIVERY_EVENT[binding.delivery]
            handler = self._handler(
                context, binding.moment,
                self._definition_hash(
                    context, binding, include_output=False))
            group: dict = {"hooks": [handler]}
            if binding.delivery != "context":
                group = {"matcher": _FEEDBACK_MATCHER, "hooks": [handler]}
            output_tail_hooks.setdefault(event, []).append(group)
        output_tail_definition = LegacyDefinition(
            legacy_id="legacy-output-tail-v1",
            path=SETTINGS_PATH,
            owned_fragment=(json.dumps(
                {"hooks": output_tail_hooks}, separators=(",", ":"))
                + "\n").encode("utf-8"),
        )
        definitions = [LegacyDefinition(
            legacy_id="legacy-v1",
            path=SETTINGS_PATH,
            owned_fragment=(json.dumps(
                {"hooks": self._legacy_hooks(context)},
                separators=(",", ":")) + "\n").encode("utf-8"),
        )]
        if (context.framework_root_rel.rstrip("/") or ".") == ".":
            definitions.append(LegacyDefinition(
                legacy_id="legacy-root-powershell-v1",
                path=SETTINGS_PATH,
                owned_fragment=(json.dumps(
                    {"hooks": self._root_powershell_legacy_hooks()},
                    separators=(",", ":")) + "\n").encode("utf-8"),
            ))
            historical = json.loads(
                _LEGACY_ROOT_FIXED_STEP_V1.read_text(encoding="utf-8"),
                object_pairs_hook=_unique_json_object)
            if not isinstance(historical, dict) or not isinstance(
                    historical.get("hooks"), dict):
                raise ValueError(
                    "Claude fixed-step legacy definition is invalid")
            definitions.append(LegacyDefinition(
                legacy_id="legacy-root-fixed-step-v1",
                path=SETTINGS_PATH,
                owned_fragment=(json.dumps(
                    {"hooks": historical["hooks"]},
                    separators=(",", ":")) + "\n").encode("utf-8"),
            ))
        definitions.append(output_tail_definition)
        return tuple(definitions)

    def _definition_hash(self, context: HarnessContext,
                         binding: LifecycleBinding, *,
                         include_output: bool = True) -> str:
        """Hash the complete owned definition with a stable hash placeholder.

        The literal attestation hash is excluded from its own input, so an
        already-installed handler keeps its old literal and cannot mint
        current evidence once the renderer evolves.
        """
        event = _DELIVERY_EVENT[binding.delivery]
        group: dict = {"hooks": [
            self._handler(context, binding.moment, _HASH_PLACEHOLDER)]}
        if binding.delivery != "context":
            group = {"matcher": _FEEDBACK_MATCHER, "hooks": group["hooks"]}
        binding_payload = {
            "moment": binding.moment,
            "delivery": binding.delivery,
            "failure": binding.failure,
            "steps": [{
                "operation": step.operation,
                "argv": list(step.argv),
                "protected_seconds": step.protected_seconds,
                **({"protected_characters": step.protected_characters}
                   if include_output else {}),
            } for step in binding.steps],
            "total_timeout_seconds": binding.total_timeout_seconds,
            "runner_reserve_seconds": binding.runner_reserve_seconds,
        }
        if include_output:
            binding_payload.update({
                "output_limit_characters": binding.output_limit_characters,
                "output_reserve_characters":
                    binding.output_reserve_characters,
            })
        return managed_definition_hash({
            "artifact": SETTINGS_PATH,
            "binding": json.dumps(
                binding_payload, sort_keys=True, separators=(",", ":")),
            "event": event,
            "group": json.dumps(group, sort_keys=True, separators=(",", ":")),
        })

    def probe(self, domain_root: Path,
              context: HarnessContext) -> AdapterProbe:
        """Return only facts static Claude project config can establish.

        Trust is a real Claude surface, not an absent one: project-level hook
        configuration is reviewed and approved by the human through Claude's
        own trust flow, and no stable machine-readable API exposes that
        decision. It is therefore reported `unknown` — the honest answer —
        rather than `not-applicable`, which the first adapter asserted only
        because it did not model the surface at all.
        """
        del domain_root  # No stable machine-readable project-trust API.
        return AdapterProbe(
            trust="unknown",
            definition_hashes={
                binding.moment: self._definition_hash(context, binding)
                for binding in context.bindings
            },
            trust_detail=(
                "Claude project hook review and approval are human-observed; "
                "configuration bytes never establish that decision"),
            ownership=(
                "the adapter owns only the managed lifecycle hook groups",
                "permissions, unrelated settings, and local extensions remain "
                "operator-owned",
            ),
        )

    # -------------------------------------------------------- lifecycle output

    def format_lifecycle_output(self, moment: str, text: str,
                                passed: bool) -> str:
        """Translate one neutral execution into Claude's hook output channel.

        SessionStart always returns model-visible context. A passing
        post-write is quiet: silence is the correct feedback when nothing is
        wrong, and it keeps the model's context free of routine noise. A
        failing post-write returns context only — never a blocking decision —
        because the Git pre-commit hook is the whole enforcement boundary and
        a harness hook must stay advisory (`surface-and-continue`).
        """
        if moment == "post-write" and passed:
            return ""
        try:
            event = _DELIVERY_EVENT_BY_MOMENT[moment]
        except KeyError as exc:
            raise ValueError(
                f"unsupported Claude lifecycle moment: {moment}") from exc
        return json.dumps({
            "hookSpecificOutput": {
                "hookEventName": event,
                "additionalContext": text,
            },
        }, separators=(",", ":"))

    # ------------------------------------------------------------- rendering

    def _command(self, ctx: HarnessContext, moment: str,
                 definition_hash: str) -> str:
        """One sh command entering the neutral ordered runner exactly once.

        Shell form in sh dialect is the portable carrier established by live
        dispatch (2026-08-13): POSIX runs these bytes natively, and on Windows
        Claude self-locates Git Bash even when PATH carries no Git entry, so
        the PowerShell branch is not reachable where Git for Windows exists.

        Root resolution prefers Claude's documented `$CLAUDE_PROJECT_DIR`
        because a hook's cwd is not guaranteed to be the project root — the
        exact defect that forced the framework root's own 2026-07-01 fix —
        and falls back to Git so the command still works if the variable is
        ever absent. Ordering is the runner's job, not this schema's: Claude
        launches matching handlers in parallel, so one handler is the only
        construction that can honour an ordered binding.
        """
        rel = ctx.framework_root_rel.rstrip("/") or "."
        mdllm = '"$ROOT/"' + _shell_single_quote(f"{rel}/tools/mdllm.py")
        unavailable = self.format_lifecycle_output(
            moment,
            f"MarkdownLLM {moment} could not run: no floor-capable Python "
            "or mdllm.py was found.",
            False,
        )
        return (
            'ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"\n'
            f"MDLLM={mdllm}\n"
            f"{SH_RESOLVE}\n"
            'if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then\n'
            f"  printf '%s\\n' {_shell_single_quote(unavailable)}\n"
            "else\n"
            f'  mdllm_python "$MDLLM" harness-event {self.name} {moment} '
            f'"$ROOT" {_shell_single_quote(definition_hash)}\n'
            "fi\n"
            "exit 0"
        )

    def _handler(self, ctx: HarnessContext, moment: str,
                 definition_hash: str) -> dict:
        return {
            "type": "command",
            "command": self._command(ctx, moment, definition_hash),
            "timeout": HANDLER_TIMEOUT_SECONDS,
        }

    def render(self, ctx: HarnessContext) -> dict[str, bytes]:
        hooks: dict = {}
        for binding in ctx.bindings:
            event = _DELIVERY_EVENT[binding.delivery]
            handler = self._handler(
                ctx, binding.moment, self._definition_hash(ctx, binding))
            group: dict = {"hooks": [handler]}
            if binding.delivery != "context":
                group = {"matcher": _FEEDBACK_MATCHER, "hooks": [handler]}
            hooks.setdefault(event, []).append(group)
        payload = json.dumps({"hooks": hooks}, indent=2) + "\n"
        return {SETTINGS_PATH: payload.encode("utf-8")}

    # ------------------------------------------------- shortcut projections

    def shortcut_sources(self, templates_root: Path) -> dict[str, Path]:
        """Deliberate-ritual shortcuts: destination relpath -> template file.
        A separate projection from lifecycle hooks — these are inert until
        the operator invokes them. The caller owns placeholder substitution
        and writing; this adapter owns only where each file belongs."""
        out: dict[str, Path] = {}
        if (templates_root / "commands").is_dir():
            for src in sorted((templates_root / "commands").glob("*.md")):
                out[f".claude/commands/{src.name}"] = src
        if (templates_root / "copilot-prompts").is_dir():
            for src in sorted(
                    (templates_root / "copilot-prompts").glob("*.prompt.md")):
                out[f".github/prompts/{src.name}"] = src
        return out

    # --------------------------------------------------------- presentation
    # Pinned strings (Phase 0 golden / doctor tests). Phase 3 owns replacing
    # this vocabulary; until then the bytes must not drift.

    def scaffold_guidance(self) -> str:
        return ("  - Claude Code lifecycle hardened out of the box: "
                ".claude/settings.json fires session-start + post-write "
                "validation automatically; /end-session + /retrospective "
                "shortcuts are installed. VS Code Copilot lifecycle remains "
                "separately unverified. Delete .claude/ to fall back to "
                "interpretation-only — the domain kernel still drives both.")

    def diagnostic_presentation(self) -> DiagnosticPresentation:
        """Display strings only (DiagnosticPresentationPort) — the install
        decision and extension surfacing are doctor's neutral logic."""
        return DiagnosticPresentation(
            installed="SessionStart adapter installed (.claude/settings.json)",
            absent="no SessionStart adapter — session-start runs by "
                   "interpretation (opt-in: "
                   "mdllm adapter-install . --harness claude)")

    # ----------------------------------------------------------- inspection

    def inspect(self, domain_root: Path,
                ctx: HarnessContext) -> InspectionReport:
        primary = self._inspect_primary(domain_root, ctx)
        overlay = domain_root / ".claude" / "settings.local.json"
        if not overlay.exists():
            return primary
        findings = list(primary.findings)
        operator_owned = list(primary.operator_owned)
        try:
            raw = overlay.read_text(encoding="utf-8")
            cfg = json.loads(raw, object_pairs_hook=_unique_json_object)
            if not isinstance(cfg, dict):
                raise ValueError("top level is not an object")
            hooks = cfg.get("hooks")
            if hooks not in (None, {}):
                findings.append(
                    "ambiguous: project-local .claude/settings.local.json "
                    "also defines hooks; the overlay is read-only and must "
                    "be resolved by the operator")
            else:
                operator_owned.append(
                    ".claude/settings.local.json is operator-owned and "
                    "contains no competing hooks")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError,
                TypeError) as exc:
            findings.append(
                "ambiguous: project-local .claude/settings.local.json "
                f"cannot be safely inspected: {type(exc).__name__}: {exc}")
        return InspectionReport(
            harness=primary.harness, fragments=primary.fragments,
            operator_owned=tuple(operator_owned),
            extensions=primary.extensions, findings=tuple(findings))

    def _inspect_primary(self, domain_root: Path,
                         ctx: HarnessContext) -> InspectionReport:
        path = domain_root / ".claude" / "settings.json"
        if not path.exists():
            return self._report(ManagedFragment(
                path=SETTINGS_PATH, present=False, artifact_present=False))
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            return self._report(ManagedFragment(
                path=SETTINGS_PATH, present=False, readable=False,
                issues=(type(exc).__name__,)))
        try:
            cfg = json.loads(raw, object_pairs_hook=_unique_json_object)
            if not isinstance(cfg, dict):
                raise ValueError("top level is not an object")
            hooks = cfg.get("hooks", {})
            if hooks is None:
                hooks = {}
            if not isinstance(hooks, dict):
                raise ValueError("hooks is not an object")
            return self._inspect_valid(cfg, hooks, ctx)
        except (json.JSONDecodeError, ValueError, KeyError, IndexError,
                TypeError, AttributeError) as exc:
            return self._report(ManagedFragment(
                path=SETTINGS_PATH, present=False, readable=True,
                valid=False, issues=(str(exc),)))

    def _realised_operations(self, command: str, moment: str,
                             ctx: HarnessContext) -> tuple[str, ...]:
        """What one installed handler actually realises.

        A current handler delegates the whole ordered binding to the neutral
        runner, so it realises every step of that moment — the runner owns
        the loop. A legacy handler names one floor operation directly, and
        that single operation is all it realises. Anything else is reported
        as its own leading token rather than silently mapped onto an intent.
        """
        if f"harness-event {self.name} {moment} " in command:
            return tuple(step.operation
                         for step in ctx.binding(moment).steps)
        if "tools/mdllm.py " in command:
            return (command.split("tools/mdllm.py ", 1)[1].split()[0],)
        return ((command.split() or [command])[0],)

    def _compare_group(self, moment: str, actual_hooks: list,
                       wanted_hooks: list, extensions: list[str],
                       issues: list[str],
                       ctx: HarnessContext) -> tuple[str, ...]:
        """Compare one managed hook group against the renderer's desired form.
        Extensions are TOKEN-BOUNDARY-safe: an added argument extends the
        managed command only across a space — `--quiet` mutating into
        `--quietly` is a divergence, never an extension (v1.6 return item 3).
        Managed hook counts are exact: a missing or appended command inside
        the managed group is a divergence, not silently ignored."""
        acts = []
        for actual, want in zip(actual_hooks, wanted_hooks):
            cmd, want_cmd = actual.get("command", ""), want["command"]
            # The renderer owns the complete managed hook entry, not only its
            # command string.  A retained command under a different hook type
            # (or with an unrecognised managed field) is not the same hook and
            # must never be certified current.  Command-tail extensions remain
            # the one explicit local-extension seam below.
            actual_shape = {k: v for k, v in actual.items() if k != "command"}
            wanted_shape = {k: v for k, v in want.items() if k != "command"}
            if actual_shape != wanted_shape:
                issues.append(
                    f"{moment} managed hook fields diverge from the managed "
                    f"form: {actual_shape!r} vs {wanted_shape!r}")
            if cmd == want_cmd:
                pass
            elif cmd.startswith(want_cmd + " "):
                extensions.append(
                    f"{moment} command carries {cmd[len(want_cmd):].strip()}")
            else:
                issues.append(f"{moment} command diverges from the managed "
                              f"form: {cmd!r}")
            acts.extend(self._realised_operations(cmd, moment, ctx))
        if len(actual_hooks) != len(wanted_hooks):
            issues.append(f"{moment} hook count diverges from the managed "
                          f"form ({len(actual_hooks)} vs "
                          f"{len(wanted_hooks)})")
        return tuple(acts)

    def _legacy_match(self, hooks: dict, ctx: HarnessContext
                      ) -> tuple[str | None, tuple[str, ...]]:
        """Name one exact legacy definition, or expose command-tail mixing."""

        def compare(actual, wanted, trail: tuple[str, ...]) -> tuple[bool, list[str]]:
            if isinstance(wanted, dict):
                if not isinstance(actual, dict) or set(actual) != set(wanted):
                    return False, []
                tails: list[str] = []
                for key in wanted:
                    if (key == "command" and isinstance(wanted[key], str)
                            and isinstance(actual[key], str)
                            and actual[key].startswith(wanted[key] + " ")):
                        tails.append(
                            f"{'/'.join(trail)} command carries "
                            f"{actual[key][len(wanted[key]):].strip()}")
                        continue
                    matched, nested = compare(
                        actual[key], wanted[key], trail + (str(key),))
                    if not matched:
                        return False, []
                    tails.extend(nested)
                return True, tails
            if isinstance(wanted, list):
                if not isinstance(actual, list) or len(actual) != len(wanted):
                    return False, []
                tails: list[str] = []
                for index, (actual_item, wanted_item) in enumerate(
                        zip(actual, wanted)):
                    matched, nested = compare(
                        actual_item, wanted_item, trail + (str(index),))
                    if not matched:
                        return False, []
                    tails.extend(nested)
                return True, tails
            return actual == wanted, []

        for definition in self.legacy_definitions(ctx):
            payload = json.loads(definition.owned_fragment)
            wanted = payload["hooks"]
            if hooks == wanted:
                return definition.legacy_id, ()
            matched, tails = compare(hooks, wanted, (definition.legacy_id,))
            if matched and tails:
                return None, tuple(tails)
        return None, ()

    def _inspect_valid(self, cfg: dict, hooks: dict,
                       ctx: HarnessContext) -> InspectionReport:
        desired = json.loads(self.render(ctx)[SETTINGS_PATH].decode("utf-8"))
        realised: dict[str, tuple[str, ...]] = {}
        extensions: list[str] = []
        issues: list[str] = []
        findings: list[str] = []

        # session-start: the FIRST SessionStart group is the managed one;
        # extra sibling groups are operator-owned (2B-accepted semantics).
        ss = hooks.get("SessionStart") or []
        if ss:
            wanted = desired["hooks"]["SessionStart"][0]["hooks"]
            realised["session-start"] = self._compare_group(
                "session-start", ss[0]["hooks"], wanted, extensions, issues,
                ctx)
            for _ in ss[1:]:
                extensions.append(
                    "additional SessionStart hook group is operator-owned")

        # post-write: the FIRST group with the managed matcher is managed;
        # a SECOND group repeating the managed matcher is ambiguity — a
        # finding, never a silent overwrite (v1.6 return item 3).
        want_pw = desired["hooks"]["PostToolUse"][0]
        managed_pw_seen = False
        for g in hooks.get("PostToolUse") or []:
            if g.get("matcher") != want_pw["matcher"]:
                extensions.append(
                    f"PostToolUse group with matcher {g.get('matcher')!r} "
                    "is operator-owned")
                continue
            if managed_pw_seen:
                findings.append(
                    "ambiguous: duplicate PostToolUse group repeats the "
                    f"managed matcher {want_pw['matcher']!r} — first group "
                    "treated as managed, this one not inspected")
                continue
            managed_pw_seen = True
            realised["post-write"] = self._compare_group(
                "post-write", g["hooks"], want_pw["hooks"],
                extensions, issues, ctx)

        for event in sorted(hooks):
            if event not in _DELIVERY_EVENT.values():
                extensions.append(
                    f"hook event {event!r} is not adapter-managed")

        operator_owned = tuple(
            f"top-level key {k!r} is operator-owned"
            for k in sorted(cfg) if k != "hooks")
        # A managed fragment is PRESENT only when a managed moment was
        # genuinely located — an artifact carrying only operator-owned hook
        # events has no managed fragment (v1.6 return item 3).
        present = bool(realised)
        expected = {b.moment: tuple(s.operation for s in b.steps)
                    for b in ctx.bindings}
        current = ((realised == expected and not issues and not findings)
                   if present else None)
        # A recognised legacy form is named only when it is genuinely NOT
        # current and carries no local extension: mixed ownership must stay
        # unknown so it remains a refusal rather than an inference.
        legacy_id = None
        if present and current is False:
            matched_id, tails = self._legacy_match(hooks, ctx)
            extensions.extend(tails)
            if matched_id and not tails and not extensions and not findings:
                legacy_id = matched_id
        return self._report(
            ManagedFragment(
                path=SETTINGS_PATH, present=present, readable=True,
                valid=True, current=current, legacy_id=legacy_id,
                intents_realised=realised, issues=tuple(issues)),
            operator_owned=operator_owned,
            extensions=tuple(extensions),
            findings=tuple(findings))

    def _report(self, fragment: ManagedFragment,
                operator_owned: tuple[str, ...] = (),
                extensions: tuple[str, ...] = (),
                findings: tuple[str, ...] = ()) -> InspectionReport:
        return InspectionReport(
            harness=self.name, fragments=(fragment,),
            operator_owned=operator_owned, extensions=extensions,
            findings=findings)


CLAUDE_CODE = ClaudeCodeAdapter()
