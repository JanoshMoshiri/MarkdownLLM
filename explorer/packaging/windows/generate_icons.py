"""Prepare native assets from the committed MarkdownLLM brand icon.

The multi-resolution ICO shares Desktop's authored vector mark. Preserve its
individual size renderings and derive the tray PNG from its largest frame.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image


BRAND_ICON = Path(__file__).parent / "assets" / "markdownllm-explorer.ico"

def build_icon() -> Image.Image:
    with Image.open(BRAND_ICON) as icon:
        return icon.convert("RGBA")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--png", type=Path, required=True)
    parser.add_argument("--ico", type=Path, required=True)
    arguments = parser.parse_args()
    arguments.png.parent.mkdir(parents=True, exist_ok=True)
    arguments.ico.parent.mkdir(parents=True, exist_ok=True)
    build_icon().save(arguments.png, format="PNG", optimize=True)
    if arguments.ico.resolve() != BRAND_ICON.resolve():
        shutil.copyfile(BRAND_ICON, arguments.ico)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
