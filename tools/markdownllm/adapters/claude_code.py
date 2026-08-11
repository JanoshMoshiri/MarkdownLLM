"""The Claude Code adapter — Phase 2C of vendor-harness-adapter-foundation.

Everything Claude-shaped that used to live inline in scaffold and doctor:
the `.claude/settings.json` lifecycle projection, the deliberate-shortcut
projections (`.claude/commands/` for Claude Code, `.github/prompts/` for VS
Code Copilot agent mode — one adapter because one settings file serves both
harnesses), the scaffold completion guidance, and the doctor advisory line.

Thin by construction: this module translates the inward lifecycle bindings
into Claude's config format and reads that format back. It contains no domain
reasoning, no thing schema, no validation logic.

Byte-compatibility is a release gate, not an aspiration: `render()` must
reproduce `tools/tests/fixtures/claude_golden/settings.json.golden` exactly
(Phase 0 freeze), derived from the bindings — never pasted.

Claude's ordering mechanism (the fact the ports must not generalise away):
the ordered session-start policy is expressed as ONE hook group whose
commands run sequentially. A harness that launches matching hooks
concurrently needs a different mechanism for the same intent.

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

from ..harness_ports import (
    DOMAIN_ROOT_ARG, AdapterCapabilities, DiagnosticPresentation,
    HarnessContext, InspectionReport, ManagedFragment,
)

SETTINGS_PATH = ".claude/settings.json"

# Inward delivery semantics -> Claude event vocabulary. Lives here and only
# here; a neutral module never names these.
_DELIVERY_EVENT = {"context": "SessionStart", "feedback": "PostToolUse"}
_FEEDBACK_MATCHER = "Write|Edit"


class ClaudeCodeAdapter:
    """Render + inspect + shortcut projections for Claude Code (and, via the
    same artifacts, VS Code Copilot agent mode)."""

    name = "claude-code"

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            harness=self.name,
            lifecycle_moments=("session-start", "post-write"),
            notes="one settings file also serves VS Code Copilot agent mode; "
                  "ordering via a single sequential hook group")

    # ------------------------------------------------------------- rendering

    def _command(self, ctx: HarnessContext, operation: str,
                 argv: tuple[str, ...]) -> str:
        args = " ".join("." if a == DOMAIN_ROOT_ARG else a for a in argv)
        return (f"python {ctx.framework_root_rel}/tools/mdllm.py "
                f"{operation} {args}")

    def render(self, ctx: HarnessContext) -> dict[str, bytes]:
        hooks: dict = {}
        for binding in ctx.bindings:
            entries = [{"type": "command",
                        "command": self._command(ctx, s.operation, s.argv)}
                       for s in binding.steps]
            if binding.delivery == "context":
                # Claude's ordering guarantee: one group, sequential commands.
                hooks.setdefault("SessionStart", []).append({"hooks": entries})
            else:
                hooks.setdefault("PostToolUse", []).append(
                    {"matcher": _FEEDBACK_MATCHER, "hooks": entries})
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
        return ("  - hardened out of the box: .claude/settings.json fires "
                "session-start + post-write validation automatically (Claude "
                "Code / VS Code Copilot agent mode), and /end-session + "
                "/retrospective are installed. Delete .claude/ to fall back "
                "to interpretation-only — the domain kernel still drives "
                "both.")

    def diagnostic_presentation(self) -> DiagnosticPresentation:
        """Display strings only (DiagnosticPresentationPort) — the install
        decision and extension surfacing are doctor's neutral logic."""
        return DiagnosticPresentation(
            installed="SessionStart adapter installed (.claude/settings.json)",
            absent="no SessionStart adapter — session-start runs by "
                   "interpretation (opt-in: "
                   "adapters/claude-code.settings.example.json)")

    # ----------------------------------------------------------- inspection

    def inspect(self, domain_root: Path,
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
            cfg = json.loads(raw)
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

    def _compare_group(self, moment: str, actual_hooks: list,
                       wanted_hooks: list, extensions: list[str],
                       issues: list[str]) -> tuple[str, ...]:
        """Compare one managed hook group against the renderer's desired form.
        Extensions are TOKEN-BOUNDARY-safe: an added argument extends the
        managed command only across a space — `--quiet` mutating into
        `--quietly` is a divergence, never an extension (v1.6 return item 3).
        Managed hook counts are exact: a missing or appended command inside
        the managed group is a divergence, not silently ignored."""
        acts = []
        for actual, want in zip(actual_hooks, wanted_hooks):
            cmd, want_cmd = actual.get("command", ""), want["command"]
            if cmd == want_cmd:
                pass
            elif cmd.startswith(want_cmd + " "):
                extensions.append(
                    f"{moment} command carries {cmd[len(want_cmd):].strip()}")
            else:
                issues.append(f"{moment} command diverges from the managed "
                              f"form: {cmd!r}")
            acts.append(cmd.split("tools/mdllm.py ", 1)[1].split()[0]
                        if "tools/mdllm.py " in cmd else (cmd.split() or [cmd])[0])
        if len(actual_hooks) != len(wanted_hooks):
            issues.append(f"{moment} hook count diverges from the managed "
                          f"form ({len(actual_hooks)} vs "
                          f"{len(wanted_hooks)})")
        return tuple(acts)

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
                "session-start", ss[0]["hooks"], wanted, extensions, issues)
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
                extensions, issues)

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
        return self._report(
            ManagedFragment(
                path=SETTINGS_PATH, present=present, readable=True,
                valid=True, current=current, intents_realised=realised,
                issues=tuple(issues)),
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
