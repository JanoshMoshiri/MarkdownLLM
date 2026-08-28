"""Resolve thing identifiers to paths within one source.

Structural references in frontmatter (`informed_by`, `linked_things`,
`dependencies`, …) name *identifiers*, not paths, and the thing they name can
live anywhere in the source.  Answering "where is this id" therefore needs a
whole-source view, which is expensive to build and cheap to reuse.

Measurements over a 1,519-file source shaped this adapter:

* Reading its 1,076 markdown files costs ~2.3s; parsing their frontmatter as
  YAML costs ~2.9s.  The parse — not the I/O — was the largest single cost, so
  the identifier is lifted from the frontmatter block's own `id:` line rather
  than by parsing YAML at all.
* Walking the source to check whether the index is still valid measured
  between 0.3s and 2.2s on the same machine, varying run to run.  That is too
  much to spend on every reference lookup, so the walk is spaced rather than
  repeated: within a short window the cached mapping is served directly, and
  after it the walk decides whether a rebuild is owed.

The index is therefore allowed to be briefly stale, which is a deliberate
trade rather than an oversight.  Its worst failure is a reference that will
not open — visible to the reader and recoverable by reopening — so it does not
warrant the per-request cost that a pagination cursor legitimately does.
"""

from __future__ import annotations

import hashlib
import threading
import time

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import BoundaryToken, RelativePath

from .confined_source_reader import ConfinedSourceReader

MARKDOWN_SUFFIXES = (".md", ".markdown")
FRONTMATTER_FENCES = {"---", "..."}
# An identifier declared past this many frontmatter lines is not an identifier
# this reader will find; the bound keeps a hostile file from being scanned far.
MAX_FRONTMATTER_LINES = 200
# Only the head of a file can hold its frontmatter, and splitting a whole
# hundred-kilobyte document into lines to read its fourth one is waste.
FRONTMATTER_HEAD_BYTES = 8 * 1024
# The walk that revalidates the cache costs about a second on a large source
# and its timing is noisy. Paying it on every reference lookup would put that
# second between a reader and every document they open. Staleness here can
# only produce a reference that fails to open — recoverable and visible —
# so the walk is spaced out rather than run every time.
REVALIDATE_SECONDS = 30.0


class ThingIndex:
    def __init__(self, filesystem: ConfinedSourceReader, limits: ExplorerLimits) -> None:
        self._filesystem = filesystem
        self._limits = limits
        self._lock = threading.Lock()
        self._cached: dict[str, tuple[str, dict[str, str], bool, float]] = {}

    def resolve(self, token: BoundaryToken, ids: tuple[str, ...]) -> tuple[dict[str, RelativePath], tuple[str, ...], bool]:
        mapping, partial = self._mapping(token)
        found: dict[str, RelativePath] = {}
        missing: list[str] = []
        for identifier in ids:
            path = mapping.get(identifier)
            if path is None:
                missing.append(identifier)
            else:
                found[identifier] = RelativePath(path)
        return found, tuple(missing), partial

    def _mapping(self, token: BoundaryToken) -> tuple[dict[str, str], bool]:
        now = time.monotonic()
        with self._lock:
            cached = self._cached.get(token.value)
            if cached and now - cached[3] < REVALIDATE_SECONDS:
                return cached[1], cached[2]
        listing, revision, partial = self._listing(token)
        with self._lock:
            cached = self._cached.get(token.value)
            if cached and cached[0] == revision:
                self._cached[token.value] = (revision, cached[1], cached[2], time.monotonic())
                return cached[1], cached[2]
        mapping = self._build(token, listing)
        with self._lock:
            self._cached[token.value] = (revision, mapping, partial, time.monotonic())
        return mapping, partial

    def _listing(self, token: BoundaryToken) -> tuple[list[RelativePath], str, bool]:
        listing: list[RelativePath] = []
        digest = hashlib.sha256()
        partial = False
        try:
            for relative, info in self._filesystem.iter_files(token):
                if not relative.name.casefold().endswith(MARKDOWN_SUFFIXES):
                    continue
                listing.append(relative)
                digest.update(f"{relative.value}|{info.st_size}|{info.st_mtime_ns}".encode("utf-8"))
                if len(listing) >= self._limits.candidate_scan:
                    partial = True
                    break
        except ExplorerError as error:
            if error.code != "directory_limit":
                raise
            partial = True
        if partial:
            digest.update(b"|partial")
        return listing, digest.hexdigest(), partial

    def _build(self, token: BoundaryToken, listing: list[RelativePath]) -> dict[str, str]:
        mapping: dict[str, str] = {}
        contested: set[str] = set()
        for relative in listing:
            try:
                raw = self._filesystem.read(token, relative)
            except ExplorerError:
                # A file this source will not read is simply not indexed.
                continue
            identifier = thing_identifier(raw.text)
            if not identifier:
                continue
            if identifier in mapping and mapping[identifier] != relative.value:
                # Two files claiming one identifier cannot be resolved to a
                # single destination, so neither is offered.
                contested.add(identifier)
                continue
            mapping[identifier] = relative.value
        for identifier in contested:
            mapping.pop(identifier, None)
        return mapping


def thing_identifier(text: str) -> str | None:
    """Lift a top-level `id:` out of a leading frontmatter block.

    Deliberately conservative, and deliberately not a YAML parse.  Anything it
    is unsure of returns None, which surfaces to the reader as a reference that
    could not be resolved rather than as a link to the wrong file.
    """
    lines = text[:FRONTMATTER_HEAD_BYTES].splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:MAX_FRONTMATTER_LINES]:
        if line.strip() in FRONTMATTER_FENCES:
            return None
        if not line.startswith("id:"):
            continue
        value = line[3:].strip()
        if len(value) > 1 and value[0] in "'\"" and value[-1] == value[0]:
            value = value[1:-1]
        return value or None
    return None
