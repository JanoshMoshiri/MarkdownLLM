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

Known, documented exception: model.py's corpus-exclusion data (.claude and
.codex in DEFAULT_EXCLUDES, CLAUDE.md in NON_THING_FILES) contains vendor paths
as scan configuration rather than executable adapter policy. model.py remains
deliberately outside this lexical gate rather than being silently passed.

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
    "cli.py", "session.py", "harness_diagnostics.py",
    "lifecycle_runner.py", "adapter_install.py",
    "assemble.py", "publish.py", "bundle_service.py",
]

# Vendor vocabulary that must not appear in neutral CODE (case-insensitive).
FORBIDDEN = [
    ".claude", ".codex", ".github", "sessionstart", "posttooluse",
    "settings.json", "hooks.json", "commandwindows", "copilot",
    "claude", "codex", "cowork",
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


# ---------------------------------------------------- port-only fake adapter
# v1.6 return item 2: a second adapter implementing ONLY declared contracts,
# registered and driven through the REAL scaffold and doctor. If either
# service calls one undeclared method, this crashes — the gate that would have
# caught the shortcut/guidance/doctor_line leak.


class _PortOnlyAdapter:
    name = "port-only-fake"

    def capabilities(self):
        from markdownllm.harness_ports import AdapterCapabilities
        return AdapterCapabilities(harness=self.name)

    def render(self, context):
        return {}  # renders no managed artifacts — a valid, honest answer

    def inspect(self, domain_root, context):
        from markdownllm.harness_ports import (
            InspectionReport, ManagedFragment)
        return InspectionReport(
            harness=self.name,
            fragments=(ManagedFragment(
                path="port-only.cfg", present=False,
                artifact_present=False),))

    def shortcut_sources(self, templates_root):
        return {"port-only.txt": templates_root / "AGENTS.md.template"}

    def scaffold_guidance(self):
        return "port-only-fake scaffold guidance"

    def diagnostic_presentation(self):
        from markdownllm.harness_ports import DiagnosticPresentation
        return DiagnosticPresentation(
            installed="port-only-fake installed",
            absent="port-only-fake absent")


def _ns(**kw):
    import argparse
    return argparse.Namespace(**kw)


def _git_repo(p: Path) -> None:
    import os
    import subprocess
    for k in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
        os.environ.setdefault(k, "floor-tests")
    for k in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
        os.environ.setdefault(k, "floor-tests@local")
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=p, check=True)


def test_port_only_adapter_survives_scaffold_and_doctor(tmp_path, capsys,
                                                        monkeypatch):
    import mdllm
    from markdownllm import adapters
    fake = _PortOnlyAdapter()
    adapters.register(fake)
    try:
        monkeypatch.setattr(adapters, "DEFAULT_HARNESS", fake.name)
        # Doctor: the fake opts into the declared presentation port and must
        # be exercised, rather than merely skipped as capability-less.
        d = tmp_path / "doctor-target"
        d.mkdir()
        _git_repo(d)
        (d / "AGENTS.md").write_text("---\nname: D\n---\n\n# D\n",
                                     encoding="utf-8")
        mdllm.cmd_doctor(_ns(path=str(d)))
        out = capsys.readouterr().out
        assert "port-only-fake absent" in out

        # Scaffold: the fake as DEFAULT harness end-to-end. Every optional
        # capability is reached exclusively through its declared port.
        _git_repo(tmp_path)
        target = tmp_path / "port-only-birth"
        rc = mdllm.cmd_scaffold(_ns(path=str(target)))
        out = capsys.readouterr().out
        assert rc == 0
        assert not (target / ".claude").exists()
        assert not (target / ".github").exists()
        assert "hardened out of the box" not in out
        assert (target / "port-only.txt").is_file()
        assert "port-only-fake scaffold guidance" in out
    finally:
        adapters.unregister(fake.name)
