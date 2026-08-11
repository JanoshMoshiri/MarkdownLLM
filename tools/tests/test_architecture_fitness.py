"""The architecture fitness gate — Phase 2C of vendor-harness-adapter-foundation.

Mechanically enforces the allowed vendor boundary (handoff acceptance
condition 3): vendor vocabulary may appear only in the vendor adapters
(markdownllm/adapters/), their fixtures/tests, and explicitly vendor-specific
documentation. The declared NEUTRAL modules — lifecycle contract, runtime,
scaffold, diagnostics, CLI, session — must contain no vendor config path,
event name, artifact filename, or direct vendor-adapter import in CODE.

Docstrings and comments are exempt (they are documentation; e.g. session.py
factually names the harnesses whose hooks feed it). The registry package
front (markdownllm/adapters/__init__.py) is the one aggregation point where
adapters are known by name — importing IT from a neutral module is the
sanctioned seam; importing a vendor module directly is not.

Known, documented exception: model.py's corpus-exclusion data (.claude in
DEFAULT_EXCLUDES, CLAUDE.md in NON_THING_FILES) is vendor paths as scan
configuration. Phase 4 adds .codex there; whether that data moves behind the
registry is a Phase 4 design question, so model.py is deliberately outside
this gate's scope for now rather than silently passed.

Run: python -m pytest tools/tests/test_architecture_fitness.py -q
"""

import ast
import io
import sys
import tokenize
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PKG = Path(__file__).resolve().parents[1] / "markdownllm"

NEUTRAL_MODULES = [
    "harness_ports.py", "runtime.py", "scaffold.py", "doctor.py",
    "cli.py", "session.py",
]

# Vendor vocabulary that must not appear in neutral CODE (case-insensitive).
FORBIDDEN = [
    ".claude", ".codex", ".github", "sessionstart", "posttooluse",
    "settings.json", "hooks.json", "commandwindows", "copilot",
    "claude", "codex",
]


def _code_only(path: Path) -> str:
    """Source minus comments and minus docstrings — what executes."""
    src = path.read_text(encoding="utf-8")
    doc_lines: set[int] = set()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list):
            continue  # Lambda/IfExp carry a single node, not a statement list
        if (body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            doc_lines.update(range(body[0].lineno, body[0].end_lineno + 1))
    out: list[str] = []
    tokens = tokenize.generate_tokens(io.StringIO(src).readline)
    for tok in tokens:
        if tok.type == tokenize.COMMENT:
            continue
        if tok.start[0] in doc_lines or tok.end[0] in doc_lines:
            continue
        out.append(tok.string)
    return " ".join(out)


def test_neutral_modules_carry_no_vendor_vocabulary():
    violations = []
    for name in NEUTRAL_MODULES:
        code = _code_only(PKG / name).lower()
        for token in FORBIDDEN:
            if token in code:
                violations.append(f"{name}: {token!r}")
    assert not violations, (
        "vendor vocabulary leaked into neutral modules:\n  "
        + "\n  ".join(violations))


def test_neutral_modules_import_only_the_registry():
    # `from .adapters import ...` (the registry front) is the sanctioned seam;
    # `from .adapters.claude_code import ...` (a vendor module) is not.
    for name in NEUTRAL_MODULES:
        tree = ast.parse((PKG / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                assert not (mod.startswith("adapters.")
                            or ".adapters." in mod), \
                    f"{name} imports a vendor adapter directly: {mod}"
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "adapters." not in alias.name, \
                        f"{name} imports a vendor adapter directly: " \
                        f"{alias.name}"


def test_every_registered_adapter_satisfies_the_ports():
    from markdownllm import adapters
    from markdownllm.harness_ports import InspectPort, RenderPort
    assert adapters.names(), "registry is empty"
    assert adapters.DEFAULT_HARNESS in adapters.names()
    for name in adapters.names():
        a = adapters.get(name)
        assert isinstance(a, RenderPort) and isinstance(a, InspectPort)
        caps = a.capabilities()
        assert caps.harness == name
