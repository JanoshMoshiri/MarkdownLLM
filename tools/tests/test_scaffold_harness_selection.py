"""Phase 5 scaffold selection: common domain core, variable outer edge."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm import adapters  # noqa: E402


_FRAMEWORK_ROOT = Path(mdllm.__file__).resolve().parents[1]
_FRAMEWORK_BOUNDARY = _FRAMEWORK_ROOT / ".boundary-terms"


@pytest.fixture(autouse=True)
def _restore_framework_boundary_terms():
    """Scaffold birth registers a private name; tests must leave no local state."""
    existed = _FRAMEWORK_BOUNDARY.is_file()
    before = _FRAMEWORK_BOUNDARY.read_bytes() if existed else None
    try:
        yield
    finally:
        if existed:
            _FRAMEWORK_BOUNDARY.write_bytes(before)
        elif _FRAMEWORK_BOUNDARY.exists():
            _FRAMEWORK_BOUNDARY.unlink()


for _key in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_key, "floor-tests")
for _key in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_key, "floor-tests@local")


def _git_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"],
                   cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "t"],
                   cwd=path, check=True)


def _scaffold(parent: Path, harness_marker=Ellipsis) -> Path:
    _git_repo(parent)
    target = parent / "adapter-selection-fixture"
    values = {"path": str(target)}
    if harness_marker is not Ellipsis:
        values["harness"] = harness_marker
    assert mdllm.cmd_scaffold(argparse.Namespace(**values)) == 0
    # New domains intentionally gate their second commit onward; establish
    # the clone-local Tier-0 attestation before asserting clean validation.
    assert mdllm.cmd_session_start(argparse.Namespace(
        path=str(target))) == 0
    assert mdllm.cmd_validate(argparse.Namespace(
        path=str(target), quiet=True)) == 0
    return target


def _common_tree(root: Path) -> dict[str, bytes]:
    outer = {".claude", ".codex", ".github", ".git"}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and not outer.intersection(
            path.relative_to(root).parts)
    }


def test_scaffold_selection_changes_only_outer_projection(tmp_path):
    targets = {
        "default": _scaffold(tmp_path / "default"),
        "claude": _scaffold(tmp_path / "claude", "claude"),
        "codex": _scaffold(tmp_path / "codex", "codex"),
        "all": _scaffold(tmp_path / "all", "all"),
        "none": _scaffold(tmp_path / "none", "none"),
    }

    baseline = _common_tree(targets["default"])
    assert all(_common_tree(target) == baseline
               for target in targets.values())
    assert (targets["default"] / ".claude" / "settings.json").is_file()
    assert not (targets["default"] / ".codex").exists()
    assert (targets["claude"] / ".claude" / "settings.json").is_file()
    assert not (targets["claude"] / ".codex").exists()
    assert (targets["codex"] / ".codex" / "hooks.json").is_file()
    assert not (targets["codex"] / ".claude").exists()
    assert not (targets["codex"] / ".github").exists()
    assert (targets["all"] / ".claude" / "settings.json").is_file()
    assert (targets["all"] / ".codex" / "hooks.json").is_file()
    assert not (targets["none"] / ".claude").exists()
    assert not (targets["none"] / ".codex").exists()
    assert not (targets["none"] / ".github").exists()


def test_entry_pointers_are_born_in_every_selection(tmp_path):
    """Phase 6 finding: a harness that auto-loads a differently named entry
    file found nothing in a `--harness none` domain, so removing the adapter
    removed the only automatic route in. Entry pointers are core surface —
    present in every selection, routing back to the one entry file, holding no
    content of their own."""
    pointers = sorted(
        p.stem for p in (_FRAMEWORK_ROOT / "templates" / "entry")
        .glob("*.template"))
    assert pointers, "templates/entry must declare at least one entry pointer"

    for marker in (Ellipsis, "claude", "codex", "all", "none"):
        label = "default" if marker is Ellipsis else marker
        target = _scaffold(tmp_path / f"entry-{label}", marker)
        for pointer in pointers:
            body = (target / pointer).read_text(encoding="utf-8")
            assert "@AGENTS.md" in body, (
                f"{pointer} must route to the entry file in {label}")
            # It points; it does not restate. Anything the domain says twice
            # is a second thing to keep in sync.
            assert "framework_root" not in body
            assert "Session Start" not in body


def _installer_wrapper_body(installer: str, opener: str, closer: str) -> str:
    """Extract the CLAUDE.md wrapper body an installer writes."""
    text = (_FRAMEWORK_ROOT / installer).read_text(encoding="utf-8")
    section = text.split("# --- 7. Claude Code wrapper", 1)[1]
    return section.split(opener, 1)[1].split(closer, 1)[0]


def test_root_wrapper_routes_both_positions_and_no_surface_drifts():
    """The root CLAUDE.md is read from two positions: as the framework
    workspace's own entry pointer, and inherited into every nested-domain
    session by the harness's documented ancestor walk (observed live
    2026-08-17: the QMS session received it unexpanded as item 1). The
    wrapper must route both positions, and the three surfaces that write it —
    the tracked root file and both installer heredocs — must not drift; a
    restated wording is a walk step per restatement, forever."""
    root = (_FRAMEWORK_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    surfaces = {
        "CLAUDE.md": root,
        "install.sh": _installer_wrapper_body(
            "install.sh", "<<'EOF'\n", "\nEOF\n"),
        "install.ps1": _installer_wrapper_body(
            "install.ps1", "@'\n", "\n'@"),
    }
    for name, body in surfaces.items():
        assert body.strip() == root.strip(), (
            f"{name} wrapper drifted from the tracked root CLAUDE.md")
        # The two positions, routed explicitly — the inherited case must not
        # depend on the external-import gate staying unapproved.
        assert "Your workspace is this directory" in body, name
        assert "inherited from a parent directory" in body, name
        assert "Do not read or follow the framework" in body, name
        assert "@AGENTS.md" in body, name


def test_unknown_selection_refuses_before_target_creation(tmp_path):
    _git_repo(tmp_path)
    target = tmp_path / "unknown-selection"
    with pytest.raises(KeyError):
        mdllm.cmd_scaffold(argparse.Namespace(
            path=str(target), harness="not-registered"))
    assert not target.exists()


class _CollidingAdapter:
    name = "collision-test"

    def capabilities(self):
        from markdownllm.harness_ports import AdapterCapabilities
        return AdapterCapabilities(harness=self.name)

    def render(self, context):
        del context
        return {".claude/settings.json": b"collision\n"}


def test_cross_adapter_path_collision_refuses_before_target_creation(tmp_path):
    _git_repo(tmp_path)
    target = tmp_path / "adapter-collision-fixture"
    adapters.register(_CollidingAdapter())
    try:
        with pytest.raises(SystemExit, match="projection collision"):
            mdllm.cmd_scaffold(argparse.Namespace(
                path=str(target), harness="all"))
    finally:
        adapters.unregister("collision-test")
    assert not target.exists()


class _ProjectedPathsAdapter(_CollidingAdapter):
    def __init__(self, name, paths):
        self.name = name
        self.paths = paths

    def render(self, context):
        del context
        return {path: b"projected\n" for path in self.paths}


@pytest.mark.parametrize("relpath", [
    "agents.md",                 # case-folded root core file
    "things\\_schema.yaml",    # separator-normalised core namespace
    ".GIT/hooks/pre-commit",    # core git namespace, case-folded
])
def test_adapter_core_collision_refuses_before_target_creation(
        tmp_path, relpath):
    _git_repo(tmp_path)
    target = tmp_path / "core-collision"
    adapter = _ProjectedPathsAdapter("core-collision-test", [relpath])
    adapters.register(adapter)
    try:
        with pytest.raises(SystemExit, match="projection collision"):
            mdllm.cmd_scaffold(argparse.Namespace(
                path=str(target), harness=adapter.name))
    finally:
        adapters.unregister(adapter.name)
    assert not target.exists()


def test_portable_case_and_separator_collision_refuses_before_creation(
        tmp_path):
    _git_repo(tmp_path)
    target = tmp_path / "portable-collision"
    adapter = _ProjectedPathsAdapter(
        "portable-collision-test",
        [".codex/hooks.json", ".CODEX\\hooks.json"],
    )
    adapters.register(adapter)
    try:
        with pytest.raises(SystemExit, match="projection collision"):
            mdllm.cmd_scaffold(argparse.Namespace(
                path=str(target), harness=adapter.name))
    finally:
        adapters.unregister(adapter.name)
    assert not target.exists()


@pytest.mark.parametrize("relpath", [
    "C:AGENTS.md", "safe/file:stream", "CON", "safe/NUL.txt",
    "safe/trailing.", "safe/*.json", "./safe.json", "safe//file.json",
])
def test_drive_relative_and_colon_projection_refuses_before_creation(
        tmp_path, relpath):
    _git_repo(tmp_path)
    target = tmp_path / "unsafe-projection"
    adapter = _ProjectedPathsAdapter("unsafe-projection-test", [relpath])
    adapters.register(adapter)
    try:
        with pytest.raises(SystemExit, match="unsafe path"):
            mdllm.cmd_scaffold(argparse.Namespace(
                path=str(target), harness=adapter.name))
    finally:
        adapters.unregister(adapter.name)
    assert not target.exists()
