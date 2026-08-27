from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


EXPLORER_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = EXPLORER_ROOT / "docs"
GUIDES = (DOCS_ROOT / "installation-guide.md", DOCS_ROOT / "user-guide.md")
PRIVATE_TERMS = (
    "canna" + "bias",
    "jano" + "sh",
    "ja" + "mos",
    "c:\\" + "users\\",
    "app" + "data",
)


def test_public_demo_estate_is_fictional_clean_and_repeatable(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    script = EXPLORER_ROOT / "tools" / "build_public_demo_estate.py"

    for destination in (first, second):
        subprocess.run(
            [sys.executable, str(script), str(destination)],
            check=True,
            capture_output=True,
            text=True,
        )

    for estate in (first, second):
        assert (estate / ".public-demo-estate").is_file()
        assert (estate / "AGENTS.md").is_file()
        assert sorted(path.name for path in (estate / "domain").iterdir()) == [
            "Product Studio",
            "Research Library",
            "Service Operations",
        ]
        for repository in (estate, *(path for path in (estate / "domain").iterdir())):
            status = subprocess.run(
                ["git", "-C", str(repository), "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True,
            )
            assert status.stdout == ""

    first_text = _estate_text(first)
    second_text = _estate_text(second)
    assert first_text == second_text
    lowered = first_text.lower()
    assert "northstar studio" in lowered
    assert not any(term in lowered for term in PRIVATE_TERMS)

    for relative in (Path("."), Path("domain/Product Studio"), Path("domain/Research Library"), Path("domain/Service Operations")):
        assert _head(first / relative) == _head(second / relative)


def test_guides_reference_existing_public_screenshots() -> None:
    referenced: set[Path] = set()
    for guide in GUIDES:
        content = guide.read_text(encoding="utf-8")
        lowered = content.lower()
        assert "northstar studio" in lowered
        assert not any(term in lowered for term in PRIVATE_TERMS)
        for target in re.findall(r"!\[[^\]]*\]\(([^)]+\.jpg)\)", content):
            image = (guide.parent / target).resolve()
            assert image.is_relative_to(DOCS_ROOT.resolve())
            assert image.is_file()
            referenced.add(image)
            width, height = _jpeg_size(image)
            assert width >= 1000
            assert height >= 650

    committed = set((DOCS_ROOT / "images").glob("*.jpg"))
    assert referenced == committed


def _estate_text(root: Path) -> str:
    return "\n".join(
        path.relative_to(root).as_posix() + "\n" + path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    )


def _head(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:2] == b"\xff\xd8"
    position = 2
    start_of_frame = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while position + 8 < len(data):
        if data[position] != 0xFF:
            position += 1
            continue
        marker = data[position + 1]
        position += 2
        if marker in {0xD8, 0xD9}:
            continue
        segment_length = int.from_bytes(data[position : position + 2], "big")
        if marker in start_of_frame:
            height = int.from_bytes(data[position + 3 : position + 5], "big")
            width = int.from_bytes(data[position + 5 : position + 7], "big")
            return width, height
        position += segment_length
    raise AssertionError("JPEG dimensions were not found")
