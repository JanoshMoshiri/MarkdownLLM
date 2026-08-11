"""Phase 2A of vendor-harness-adapter-foundation: the draft ports vs the freeze.

The implementations in THIS FILE are draft evidence, not production code —
they exist to prove the port signatures in markdownllm/harness_ports.py can
express the frozen Claude behaviour without importing any vendor schema into
the contract. Production scaffold/doctor still run their inline Claude paths;
moving them onto the ports is Phase 2C, after the Codex-owned 2B challenge.

What is proven here:
- the context object carries ENOUGH to reproduce the golden Claude bytes
  (rendering is derived from the lifecycle intents, not pasted);
- the inspect signature can report every estate shape read-only — standard,
  composite, locally extended, permissions-only, absent — without flattening
  extensions or touching operator-owned content;
- the drafted intents equal the Phase 0 freeze, byte for byte.

Run: python -m pytest tools/tests/test_harness_ports.py -q
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import harness_ports as hp  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


# ------------------------------------------------------------ contract equality


def test_lifecycle_intents_match_the_phase0_freeze():
    import test_adapter_contract as frozen
    assert hp.LIFECYCLE_INTENTS == frozen.LIFECYCLE_INTENTS


# ------------------------------------------- draft renderer (test-local only)


class _DraftClaudeRenderer:
    """2B challenge evidence: the Claude settings artifact derived from the
    intent data through the port signature — no pasted JSON."""

    def capabilities(self) -> hp.AdapterCapabilities:
        return hp.AdapterCapabilities(
            harness="claude-code",
            lifecycle_events=("session-start", "post-write"),
            shortcuts=True,
            notes="ordering via a single sequential hook group")

    def render(self, ctx: hp.HarnessContext) -> dict[str, bytes]:
        rel = ctx.framework_root_rel
        mdllm = f"python {rel}/tools/mdllm.py"
        ss = [{"type": "command", "command": f"{mdllm} {act} ."}
              for act in ctx.intents["session-start"]]
        pw = [{"type": "command", "command": f"{mdllm} {act} . --quiet"}
              for act in ctx.intents["post-write"]]
        settings = {
            "hooks": {
                "SessionStart": [{"hooks": ss}],
                "PostToolUse": [{"matcher": "Write|Edit", "hooks": pw}],
            }
        }
        return {".claude/settings.json":
                (json.dumps(settings, indent=2) + "\n").encode("utf-8")}


def test_draft_renderer_reproduces_the_golden_bytes(tmp_path):
    renderer = _DraftClaudeRenderer()
    assert isinstance(renderer, hp.RenderPort)
    ctx = hp.HarnessContext(domain_root=tmp_path, framework_root_rel="../..")
    out = renderer.render(ctx)
    golden = (FIXTURES / "claude_golden" / "settings.json.golden").read_text(
        encoding="utf-8").replace("{rel_fw}", "../..")
    assert out[".claude/settings.json"].decode("utf-8") == golden, \
        "the context object does not carry enough to derive the golden bytes"


# ------------------------------------------ draft inspector (test-local only)


class _DraftClaudeInspector:
    """2B challenge evidence: every estate shape reported read-only, local
    extensions surfaced rather than normalised."""

    _EXPECTED = {"session-start": ("estate-sync", "session-start"),
                 "post-write": ("validate",)}

    def capabilities(self) -> hp.AdapterCapabilities:
        return _DraftClaudeRenderer().capabilities()

    def inspect(self, domain_root: Path) -> hp.InspectionReport:
        path = domain_root / ".claude" / "settings.json"
        if not path.is_file():
            return hp.InspectionReport(
                harness="claude-code",
                fragments=(hp.ManagedFragment(
                    path=".claude/settings.json", present=False),))
        cfg = json.loads(path.read_text(encoding="utf-8"))
        hooks = cfg.get("hooks") or {}
        realised: dict[str, tuple[str, ...]] = {}
        extensions: list[str] = []
        ss = hooks.get("SessionStart") or []
        if ss:
            acts = []
            for h in ss[0]["hooks"]:
                tail = h["command"].split("tools/mdllm.py ", 1)[1]
                parts = tail.split()
                acts.append(parts[0])
                extra = [p for p in parts[1:] if p != "."]
                if extra:
                    extensions.append(
                        f"session-start command carries {' '.join(extra)}")
            realised["session-start"] = tuple(acts)
        for g in hooks.get("PostToolUse") or []:
            if g.get("matcher") == "Write|Edit":
                realised["post-write"] = tuple(
                    h["command"].split("tools/mdllm.py ", 1)[1].split()[0]
                    for h in g["hooks"])
        operator_owned = tuple(
            f"top-level key {k!r} is operator-owned"
            for k in sorted(cfg) if k != "hooks")
        return hp.InspectionReport(
            harness="claude-code",
            fragments=(hp.ManagedFragment(
                path=".claude/settings.json", present=bool(hooks),
                current=(realised == self._EXPECTED and not extensions),
                intents_realised=realised),),
            operator_owned=operator_owned,
            extensions=tuple(extensions))


def _inspect_shape(tmp_path, shape):
    if shape is not None:
        dst = tmp_path / ".claude" / "settings.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(
            (FIXTURES / "estate_shapes" / f"{shape}.json").read_bytes())
    inspector = _DraftClaudeInspector()
    assert isinstance(inspector, hp.InspectPort)
    before = (hashlib.sha256(dst.read_bytes()).hexdigest()
              if shape is not None else None)
    report = inspector.inspect(tmp_path)
    if shape is not None:
        assert hashlib.sha256(dst.read_bytes()).hexdigest() == before, \
            "inspection mutated the source document"
    return report


def test_inspect_standard_shape(tmp_path):
    r = _inspect_shape(tmp_path, "hooks-only")
    frag = r.fragments[0]
    assert frag.present and frag.current
    assert frag.intents_realised == hp.LIFECYCLE_INTENTS
    assert not r.extensions and not r.operator_owned


def test_inspect_extended_startup_reports_not_flattens(tmp_path):
    r = _inspect_shape(tmp_path, "extended-startup")
    frag = r.fragments[0]
    assert frag.present and frag.current is False
    assert frag.intents_realised == hp.LIFECYCLE_INTENTS  # intent still met
    assert any("--assistant" in e for e in r.extensions)


def test_inspect_composite_preserves_operator_content(tmp_path):
    r = _inspect_shape(tmp_path, "permissions-plus-hooks")
    assert r.fragments[0].present
    assert any("permissions" in o for o in r.operator_owned)


def test_inspect_permissions_only(tmp_path):
    r = _inspect_shape(tmp_path, "permissions-only")
    assert not r.fragments[0].present
    assert any("permissions" in o for o in r.operator_owned)


def test_inspect_absent(tmp_path):
    r = _inspect_shape(tmp_path, None)
    assert not r.fragments[0].present


# ----------------------------------------------------- vendor-neutral boundary


def test_ports_module_names_no_vendor_config():
    # The contract module may mention vendors only in prose examples; it must
    # contain no vendor config path, key, or schema assumption as CODE.
    src = Path(hp.__file__).read_text(encoding="utf-8")
    code_lines = [l for l in src.splitlines()
                  if l.strip() and not l.strip().startswith("#")
                  and '"""' not in l and "'''" not in l]
    joined = "\n".join(code_lines)
    for token in (".claude", "settings.json", "SessionStart", "PostToolUse",
                  ".codex", "hooks.json"):
        assert token not in joined, f"vendor artifact {token!r} leaked into " \
                                    "the application contract"
