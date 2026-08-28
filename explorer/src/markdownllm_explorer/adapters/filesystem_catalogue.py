"""Estate discovery and adapter-private source boundary registry."""

from __future__ import annotations

import hashlib
import os
import secrets
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from markdownllm_explorer.core.eligibility import EligibilityPolicy
from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import (
    BoundaryToken, EstateSnapshot, GitKind, Source, SourceId, SourceIssue, SourceKind,
)


@dataclass(frozen=True)
class SourceBoundary:
    source: Source
    root: Path
    excluded_root: Path | None = None


class BoundaryRegistry:
    """The only component that maps public identities to filesystem roots."""

    def __init__(self) -> None:
        self._by_token: dict[str, SourceBoundary] = {}
        self._by_id: dict[str, SourceBoundary] = {}

    def replace(self, boundaries: list[SourceBoundary]) -> None:
        self._by_token = {item.source.boundary_token.value: item for item in boundaries}
        self._by_id = {item.source.id.value: item for item in boundaries}

    def by_token(self, token: BoundaryToken) -> SourceBoundary:
        try:
            return self._by_token[token.value]
        except KeyError:
            raise ExplorerError("source_not_found") from None

    def by_id(self, source_id: str) -> SourceBoundary:
        try:
            return self._by_id[source_id]
        except KeyError:
            raise ExplorerError("source_not_found") from None


class FilesystemSourceCatalogue:
    def __init__(
        self, root: Path, domain_dir: str, registry: BoundaryRegistry,
        policy: EligibilityPolicy, limits: ExplorerLimits | None = None,
    ) -> None:
        requested = root.expanduser().absolute()
        if not requested.exists() or not requested.is_dir():
            raise ExplorerError("source_unreadable", detail="Configured root is not a readable directory")
        if _is_reparse(requested):
            raise ExplorerError("source_unreadable", detail="Configured root cannot be a link or reparse point")
        self._root = requested.resolve(strict=True)
        self._domain_relative = _safe_domain_dir(domain_dir)
        self._domain_root = self._root.joinpath(*self._domain_relative.parts)
        self._registry = registry
        self._policy = policy
        self._limits = limits or ExplorerLimits()
        self._snapshot: EstateSnapshot | None = None

    @property
    def root(self) -> Path:
        return self._root

    def discover(self) -> EstateSnapshot:
        boundaries: list[SourceBoundary] = []
        issues: list[SourceIssue] = []
        # The substrate is the MarkdownLLM framework in every estate, so it is
        # named rather than described.  The navigation group heading above it
        # already carries the role (FR-EST-002, amended 2026-08-28).
        substrate = self._make_source("substrate", "MarkdownLLM", SourceKind.SUBSTRATE, self._root)
        boundaries.append(SourceBoundary(substrate, self._root, self._domain_root))
        candidates: list[tuple[str, Path, str]] = []
        if self._domain_root.exists() and self._domain_root.is_dir() and not _is_reparse(self._domain_root):
            try:
                entries = []
                with os.scandir(self._domain_root) as iterator:
                    for entry in iterator:
                        entries.append(entry)
                        if len(entries) > self._limits.candidate_scan:
                            issues.append(SourceIssue("domain_scan_limit", "The domain directory exceeded the discovery scan limit."))
                            break
            except OSError:
                issues.append(SourceIssue("domain_directory_unreadable", "The configured domain directory cannot be read."))
                entries = []
            for entry in entries:
                try:
                    if self._policy.is_ignored_directory(entry.name):
                        continue
                    path = Path(entry.path)
                    if entry.is_symlink() or _is_reparse(path):
                        issues.append(SourceIssue("domain_boundary_invalid", "A domain candidate is a link or reparse point."))
                        continue
                    if not entry.is_dir(follow_symlinks=False):
                        continue
                    marker_paths = tuple(path / marker for marker in ("AGENTS.md", ".markdownllm"))
                    if any(marker.exists() and not marker.is_file() for marker in marker_paths):
                        issues.append(SourceIssue("domain_marker_invalid", "A domain candidate has an invalid marker shape."))
                        continue
                    markers = tuple(marker.name for marker in marker_paths if marker.is_file())
                except OSError:
                    issues.append(SourceIssue("domain_candidate_unreadable", "A domain candidate could not be inspected."))
                    continue
                if not markers:
                    issues.append(SourceIssue("domain_marker_missing", "A domain candidate has no readable admission marker."))
                    continue
                folded = unicodedata.normalize("NFC", entry.name).casefold()
                source_id = _normalised_domain_id(entry.name)
                candidates.append((folded, path, source_id))
        collisions = _collision_ids(source_id for _, _, source_id in candidates)
        for folded, path, source_id in sorted(candidates, key=lambda item: (item[0], item[1].name)):
            if source_id in collisions:
                issues.append(SourceIssue("source_id_collision", "Two domain directories normalise to the same identity.", SourceId(source_id)))
                continue
            try:
                canonical = path.resolve(strict=True)
                canonical.relative_to(self._domain_root.resolve(strict=True))
            except (OSError, ValueError):
                issues.append(SourceIssue("domain_boundary_invalid", "A marked domain did not resolve inside the domain directory.", SourceId(source_id)))
                continue
            source = self._make_source(source_id, path.name, SourceKind.DOMAIN, canonical)
            boundaries.append(SourceBoundary(source, canonical))
        self._registry.replace(boundaries)
        revision_input = "\n".join(f"{item.source.id.value}\0{item.root}" for item in boundaries).encode()
        self._snapshot = EstateSnapshot(
            tuple(item.source for item in boundaries), tuple(issues), hashlib.sha256(revision_input).hexdigest(),
            datetime.now(timezone.utc).isoformat(),
        )
        return self._snapshot

    def source(self, source_id: str) -> Source:
        if self._snapshot is None:
            self.discover()
        return self._registry.by_id(source_id).source

    def _make_source(self, source_id: str, display_name: str, kind: SourceKind, root: Path) -> Source:
        markers = tuple(marker for marker in ("AGENTS.md", ".markdownllm") if (root / marker).is_file())
        git_path = root / ".git"
        git_kind = GitKind.REPOSITORY if git_path.exists() else GitKind.NON_GIT
        return Source(SourceId(source_id), kind, display_name, BoundaryToken(secrets.token_urlsafe(24)), markers, git_kind)


def _safe_domain_dir(value: str) -> Path:
    if not value or "\x00" in value or ":" in value:
        raise ExplorerError("invalid_path")
    candidate = Path(value)
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise ExplorerError("invalid_path")
    return candidate


def _normalised_domain_id(name: str) -> str:
    folded = unicodedata.normalize("NFC", name).casefold()
    return "domain/" + quote(folded, safe="")


def _collision_ids(source_ids) -> set[str]:
    seen: set[str] = set()
    collisions: set[str] = set()
    for source_id in source_ids:
        if source_id in seen:
            collisions.add(source_id)
        seen.add(source_id)
    return collisions


def _is_reparse(path: Path) -> bool:
    try:
        return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())
    except OSError:
        return True
