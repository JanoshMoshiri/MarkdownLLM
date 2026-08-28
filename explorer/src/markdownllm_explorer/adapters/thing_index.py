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
* Walking the source to check whether the index is still valid measured between
  0.3s and 2.2s on the same machine, varying run to run.  That is too much to
  spend on every reference lookup, so the walk is spaced rather than repeated:
  within a short window the cached mapping is served directly, and after it the
  walk decides whether a rebuild is owed.

The index is therefore allowed to be briefly stale, which is a deliberate trade
rather than an oversight.  Its worst failure is a reference that will not open —
visible to the reader and recoverable by reopening — so it does not warrant the
per-request cost that a pagination cursor legitimately does.

Three properties are not optional, and each was absent in the first version:

* The cache is keyed on **source identity**, not on the boundary token.  Tokens
  are minted fresh on every estate discovery, so keying on one meant a browser
  reload silently forfeited the index and retained the old one for ever.
* Builds are **single-flight**.  Without it, N concurrent cold lookups ran N
  full source walks, each holding one of the server's 16 request permits.
* A source that is *being written while it is read* — an agent session working
  in the estate — must not turn every reference into a false "not found".  A
  walk interrupted by a concurrent write yields a partial answer, never an
  error that the browser would render as absence.
"""

from __future__ import annotations

import hashlib
import threading
import time
from dataclasses import dataclass, replace

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import BoundaryToken, RelativePath

from .confined_source_reader import ConfinedSourceReader
from .filesystem_catalogue import BoundaryRegistry

MARKDOWN_SUFFIXES = (".md", ".markdown")
FRONTMATTER_FENCES = {"---", "..."}
# An identifier declared past this many frontmatter lines is not an identifier
# this reader will find; the bound keeps a hostile file from being scanned far.
MAX_FRONTMATTER_LINES = 200
# Only the head of a file can hold its frontmatter, and splitting a whole
# hundred-kilobyte document into lines to read its fourth one is waste.
FRONTMATTER_HEAD_BYTES = 8 * 1024
# How long a mapping is served without rechecking that the source still agrees.
REVALIDATE_SECONDS = 30.0
# How long a follower waits for the in-flight build it is sharing.
BUILD_WAIT_SECONDS = 30.0


@dataclass(frozen=True)
class _Entry:
    revision: str
    mapping: dict[str, str]
    partial: bool
    checked_at: float


class ThingIndex:
    def __init__(self, filesystem: ConfinedSourceReader, registry: BoundaryRegistry, limits: ExplorerLimits) -> None:
        self._filesystem = filesystem
        self._registry = registry
        self._limits = limits
        self._lock = threading.Lock()
        self._cached: dict[str, _Entry] = {}
        self._building: dict[str, threading.Event] = {}

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
        key = self._registry.by_token(token).source.id.value
        fresh = self._fresh(key)
        if fresh is not None:
            return fresh

        event, leading = self._claim(key)
        if not leading:
            # Someone else is already walking this source. Waiting for their
            # answer is cheaper than duplicating a multi-second walk, and it
            # keeps concurrent openers from consuming every request permit.
            event.wait(BUILD_WAIT_SECONDS)
            with self._lock:
                entry = self._cached.get(key)
            if entry is not None:
                return entry.mapping, entry.partial
            event, leading = self._claim(key)
            if not leading:
                raise ExplorerError("source_unreadable")

        try:
            listing, revision, partial = self._listing(token)
            with self._lock:
                entry = self._cached.get(key)
                if entry is not None and entry.revision == revision:
                    self._cached[key] = replace(entry, checked_at=time.monotonic())
                    return entry.mapping, entry.partial
            mapping = self._build(token, listing)
            with self._lock:
                self._cached[key] = _Entry(revision, mapping, partial, time.monotonic())
            return mapping, partial
        except ExplorerError:
            # Unreadable now does not mean unknown: a mapping already built is
            # still a better answer than declaring every reference missing.
            with self._lock:
                entry = self._cached.get(key)
            if entry is not None:
                return entry.mapping, True
            raise
        finally:
            with self._lock:
                self._building.pop(key, None)
            event.set()

    def _fresh(self, key: str) -> tuple[dict[str, str], bool] | None:
        with self._lock:
            entry = self._cached.get(key)
        if entry is None or time.monotonic() - entry.checked_at >= REVALIDATE_SECONDS:
            return None
        return entry.mapping, entry.partial

    def _claim(self, key: str) -> tuple[threading.Event, bool]:
        with self._lock:
            existing = self._building.get(key)
            if existing is not None:
                return existing, False
            event = threading.Event()
            self._building[key] = event
            return event, True

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
            # A source being written while it is read is the normal case here,
            # not an exceptional one: an agent session edits the estate while an
            # operator browses it. A walk cut short yields a partial index, the
            # same way hitting the scan limit does.
            if error.code not in {"directory_limit", "source_changed"}:
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

    Two rules earn their keep. The block must actually *close*: a prose page
    that opens with a horizontal rule and later quotes `id:` inside a fenced
    example would otherwise claim that identifier and, by contesting it, put out
    a working reference elsewhere in the estate. And an unquoted trailing
    comment is stripped, because `id: settled  # canonical` is valid YAML that
    the rest of the application reads correctly; disagreeing with it here would
    silently unindex the thing.
    """
    lines = text[:FRONTMATTER_HEAD_BYTES].splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    found: str | None = None
    for line in lines[1:MAX_FRONTMATTER_LINES]:
        if line.strip() in FRONTMATTER_FENCES:
            return found
        if found is not None or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if not separator or key.strip() != "id":
            continue
        found = _scalar(value)
    # The block never closed within the scanned head, so nothing here is
    # frontmatter this reader is willing to trust.
    return None


def _scalar(value: str) -> str | None:
    text = value.strip()
    if text[:1] in {"'", '"'}:
        quote = text[0]
        closing = text.find(quote, 1)
        return text[1:closing] or None if closing > 0 else None
    comment = text.find(" #")
    if comment >= 0:
        text = text[:comment].strip()
    if text[:1] in {"|", ">", "&", "*", "!"}:
        return None
    return text or None
