"""The architecture fitness gate — Phase 2C of vendor-harness-adapter-foundation.

Mechanically enforces the allowed vendor boundary (handoff acceptance
condition 3): vendor vocabulary may appear only in the vendor adapters
(markdownllm/adapters/), their fixtures/tests, and explicitly vendor-specific
documentation. Neutrality is **total by construction** (floor-structure-residue
item 1, landed sprint 2): every package module outside ``adapters/`` is
neutral — a newly added module is born gated, never born exempt. Exceptions
are declared per module with a reason, and must stay exact: an exception
whose module no longer trips the gate fails the suite.

Docstrings and comments are exempt (they are documentation; e.g. session.py
factually names the harnesses whose hooks feed it). The registry package
front (markdownllm/adapters/__init__.py) is the one aggregation point where
adapters are known by name — importing IT from a neutral module is the
sanctioned seam; importing a vendor module directly is not, and that rule
has no exceptions at all.

Run: python -m pytest tools/tests/test_architecture_fitness.py -q
"""

import ast
import io
import sys
import tokenize
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PKG = Path(__file__).resolve().parents[1] / "markdownllm"

ADAPTER_PACKAGE = PKG / "adapters"


def _neutral_modules() -> dict[str, Path]:
    """Every package module OUTSIDE adapters/ — neutral by construction."""
    return {
        path.relative_to(PKG).as_posix(): path
        for path in sorted(PKG.rglob("*.py"))
        if ADAPTER_PACKAGE not in path.parents
    }


# Modules whose PURPOSE is vendor-facing, excepted from the lexical vocabulary
# gate by declaration-with-reason. Exactness is itself tested below: a stale
# entry (module gone, or no longer tripping the gate) fails the suite — the
# same-builder blindness floor-structure-residue names must not accumulate
# here.
VENDOR_VOCABULARY_EXCEPTIONS = {
    "model.py":
        "corpus-exclusion scan data (.claude/.codex in DEFAULT_EXCLUDES, "
        "CLAUDE.md in NON_THING_FILES) — configuration, not adapter policy",
    "evals.py":
        "drives the vendor CLI as its eval subject (`claude -p` headless "
        "agent); the vocabulary is the module's purpose, not leaked policy",
}

# Vendor vocabulary that must not appear in neutral CODE (case-insensitive).
FORBIDDEN = [
    ".claude", ".codex", ".github", "sessionstart", "posttooluse",
    "settings.json", "hooks.json", "commandwindows", "copilot",
    "claude", "codex", "cowork",
]


def _package_modules() -> dict[str, Path]:
    modules: dict[str, Path] = {}
    for path in PKG.rglob("*.py"):
        relative = path.relative_to(PKG)
        parts = list(relative.with_suffix("").parts)
        if parts[-1] == "__init__":
            parts.pop()
        name = "markdownllm" + ("." + ".".join(parts) if parts else "")
        modules[name] = path
    return modules


def _local_imports(module: str, path: Path,
                   known: set[str]) -> tuple[set[str], list[tuple[str, str]]]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    package = module if path.name == "__init__.py" else module.rpartition(".")[0]
    dependencies: set[str] = set()
    private: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in known:
                    dependencies.add(alias.name)
            continue
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level:
            anchor = package.split(".")
            if node.level > 1:
                anchor = anchor[:-(node.level - 1)]
            target = ".".join(anchor + (node.module or "").split(".")).rstrip(".")
        else:
            target = node.module or ""
        if target in known:
            dependencies.add(target)
        if not node.module:
            for alias in node.names:
                candidate = f"{target}.{alias.name}" if target else alias.name
                if candidate in known:
                    dependencies.add(candidate)
        if target.startswith("markdownllm"):
            private.extend((target, alias.name) for alias in node.names
                           if alias.name.startswith("_") and alias.name != "__future__")
    return dependencies, private


def _import_sccs(graph: dict[str, set[str]]) -> list[tuple[str, ...]]:
    """Tarjan SCCs, returned only when they contain an actual cycle."""
    counter = 0
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    active: set[str] = set()
    cycles: list[tuple[str, ...]] = []

    def visit(node: str) -> None:
        nonlocal counter
        indices[node] = low[node] = counter
        counter += 1
        stack.append(node)
        active.add(node)
        for dependency in graph[node]:
            if dependency not in indices:
                visit(dependency)
                low[node] = min(low[node], low[dependency])
            elif dependency in active:
                low[node] = min(low[node], indices[dependency])
        if low[node] != indices[node]:
            return
        component: list[str] = []
        while True:
            item = stack.pop()
            active.remove(item)
            component.append(item)
            if item == node:
                break
        if len(component) > 1 or node in graph[node]:
            cycles.append(tuple(sorted(component)))

    for name in sorted(graph):
        if name not in indices:
            visit(name)
    return sorted(cycles)


def test_package_import_graph_is_acyclic():
    modules = _package_modules()
    known = set(modules)
    graph = {name: _local_imports(name, path, known)[0]
             for name, path in modules.items()}
    assert not _import_sccs(graph), (
        "package import cycle(s) make initialization order observable: "
        f"{_import_sccs(graph)}")


def test_package_has_no_cross_module_private_imports():
    modules = _package_modules()
    known = set(modules)
    found: set[tuple[str, str, str]] = set()
    for consumer, path in modules.items():
        _, imports = _local_imports(consumer, path, known)
        found.update((consumer, provider, symbol)
                     for provider, symbol in imports)
    assert not found, "cross-module private imports: " + repr(sorted(found))


def test_hook_execution_layers_do_not_depend_on_scaffold():
    # Executors (runtime, repository_transaction) and diagnosers (doctor,
    # session) consume the leaf contract; none may reach back into the
    # producer. doctor and session joined the set when sprint 2's F4 move
    # deleted their scaffold edges — this pins them deleted.
    modules = _package_modules()
    known = set(modules)
    for name in ("markdownllm.hook_contract", "markdownllm.runtime",
                 "markdownllm.repository_transaction",
                 "markdownllm.doctor", "markdownllm.session"):
        dependencies, _ = _local_imports(name, modules[name], known)
        assert "markdownllm.scaffold" not in dependencies, (
            f"{name} imports the hook producer instead of its leaf contract")


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
    for name, path in _neutral_modules().items():
        if name in VENDOR_VOCABULARY_EXCEPTIONS:
            continue
        code = _code_only(path).lower()
        for token in FORBIDDEN:
            if token in code:
                violations.append(f"{name}: {token!r}")
    assert not violations, (
        "vendor vocabulary leaked into neutral modules:\n  "
        + "\n  ".join(violations))


def test_vendor_vocabulary_exceptions_are_exact():
    neutral = _neutral_modules()
    stale = []
    for name in VENDOR_VOCABULARY_EXCEPTIONS:
        path = neutral.get(name)
        if path is None:
            stale.append(f"{name}: not a neutral module (moved or deleted)")
            continue
        code = _code_only(path).lower()
        if not any(token in code for token in FORBIDDEN):
            stale.append(f"{name}: no longer trips the gate — remove it")
    assert not stale, (
        "stale vendor-vocabulary exceptions:\n  " + "\n  ".join(stale))


def test_neutral_modules_import_only_the_registry():
    # `from .adapters import ...` (the registry front) is the sanctioned seam;
    # `from .adapters.claude_code import ...` (a vendor module) is not.
    # No exceptions: even vocabulary-excepted modules must not import one.
    for name, path in _neutral_modules().items():
        tree = ast.parse(path.read_text(encoding="utf-8"))
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
