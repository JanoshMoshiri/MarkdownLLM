"""Pure curated-collection grouping rules."""

from __future__ import annotations

from .models import RelativePath


def memory_group_for(relative: RelativePath) -> str | None:
    """Return the first-level ``things`` group for an eligible Markdown path."""
    if (
        len(relative.parts) < 3
        or relative.parts[0].casefold() != "things"
        or not relative.name.casefold().endswith((".md", ".markdown"))
    ):
        return None
    return relative.parts[1].replace("-", " ").replace("_", " ").title()
