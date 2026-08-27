"""Generate deterministic application icons from simple vector-like geometry."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def build_icon(size: int = 256) -> Image.Image:
    scale = size / 256
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    def box(values: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return tuple(round(value * scale) for value in values)  # type: ignore[return-value]

    draw.rounded_rectangle(box((12, 12, 244, 244)), radius=round(54 * scale), fill="#171717")
    draw.rounded_rectangle(box((22, 22, 234, 234)), radius=round(46 * scale), outline="#333333", width=max(1, round(3 * scale)))

    stroke = max(2, round(13 * scale))
    points = [(58, 178), (58, 75), (128, 143), (198, 75), (198, 178)]
    scaled = [(round(x * scale), round(y * scale)) for x, y in points]
    draw.line(scaled, fill="#F1EEE8", width=stroke, joint="curve")

    accent = "#9DD9C5"
    radius = round(13 * scale)
    for x, y in (scaled[0], scaled[2], scaled[-1]):
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=accent)
    return image


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--png", type=Path, required=True)
    parser.add_argument("--ico", type=Path, required=True)
    arguments = parser.parse_args()
    arguments.png.parent.mkdir(parents=True, exist_ok=True)
    arguments.ico.parent.mkdir(parents=True, exist_ok=True)
    image = build_icon()
    image.save(arguments.png, format="PNG", optimize=True)
    image.save(
        arguments.ico,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
