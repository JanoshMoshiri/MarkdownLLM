"""Explicit public DTO encoding; adapter tokens never cross this boundary."""

from __future__ import annotations

from enum import Enum
from typing import Mapping

from markdownllm_explorer.core.models import (
    BoundaryToken, CollectionItem, CommitDetail, CommitFile, CommitRecord, DocumentRecord, EstateSnapshot,
    FrontmatterResult, HistoricalDocument, OverviewRecord, Page, RelativePath, RepositoryState, Source,
    ReferenceResolution, SourceCounts, SourceId, SourceIssue, SourceSettingsRecord, TreeNode,
)


def to_wire(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (SourceId, RelativePath)):
        return value.value
    if isinstance(value, BoundaryToken):
        raise TypeError("boundary tokens are not public DTOs")
    if isinstance(value, Source):
        return {
            "id": value.id.value,
            "kind": value.kind.value,
            "display_name": value.display_name,
            "markers": list(value.markers),
            "git_kind": value.git_kind.value,
        }
    if isinstance(value, EstateSnapshot):
        return {"sources": to_wire(value.sources), "issues": to_wire(value.issues), "revision": value.revision}
    if isinstance(value, SourceIssue):
        return _compact({"code": value.code, "message": value.message, "source_id": to_wire(value.source_id)})
    if isinstance(value, Page):
        return {"items": to_wire(value.items)}
    if isinstance(value, SourceCounts):
        return {"eligible_files": value.eligible_files, "skills": value.skills, "memory": value.memory, "partial": value.partial}
    if isinstance(value, RepositoryState):
        return _compact({"kind": value.kind, "head_sha": value.head_sha, "branch": value.branch, "dirty": value.dirty, "issue": value.issue})
    if isinstance(value, OverviewRecord):
        return {"source": to_wire(value.source), "counts": to_wire(value.counts), "repository": to_wire(value.repository), "commits": to_wire(value.commits)}
    if isinstance(value, TreeNode):
        return _compact({"path": value.path.value, "name": value.name, "kind": value.kind.value, "size": value.size, "modified_at": value.modified_at, "expandable": value.expandable})
    if isinstance(value, ReferenceResolution):
        return {
            "source_id": value.source_id.value,
            "resolved": {key: path.value for key, path in value.resolved.items()},
            "unresolved": list(value.unresolved),
            "partial": value.partial,
        }
    if isinstance(value, CommitFile):
        return {"path": value.path.value, "change": value.change, "openable": value.openable}
    if isinstance(value, CommitDetail):
        return {
            "sha": value.sha, "subject": value.subject, "author_name": value.author_name,
            "authored_at": value.authored_at, "files": to_wire(value.files), "partial": value.partial,
        }
    if isinstance(value, HistoricalDocument):
        return {
            "source_id": value.source_id.value, "path": value.path.value, "sha": value.sha,
            "content": value.content, "added_ranges": [list(item) for item in value.added_ranges],
            "size": value.size,
        }
    if isinstance(value, CommitRecord):
        return {"sha": value.sha, "subject": value.subject, "author_name": value.author_name, "authored_at": value.authored_at}
    if isinstance(value, FrontmatterResult):
        return _compact({"state": value.state.value, "values": to_wire(value.values), "error_code": value.error_code})
    if isinstance(value, DocumentRecord):
        return {
            "source_id": value.source_id.value, "path": value.path.value, "mode": value.mode.value,
            "content": value.content, "frontmatter": to_wire(value.frontmatter), "size": value.size,
            "modified_at": value.modified_at, "issues": list(value.issues),
        }
    if isinstance(value, CollectionItem):
        return _compact({
            "path": value.path.value, "title": value.title, "group": value.group, "thing_id": value.thing_id,
            "thing_type": value.thing_type, "issues": list(value.issues),
        })
    if isinstance(value, SourceSettingsRecord):
        return {
            "source_id": value.source_id.value, "source_path": value.source_path, "markers": list(value.markers),
            "kind": value.kind.value, "git_kind": value.git_kind.value,
        }
    if isinstance(value, Mapping):
        return {str(key): to_wire(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_wire(item) for item in value]
    raise TypeError(f"unsupported response value {type(value).__name__}")


def _compact(value: dict[str, object]) -> dict[str, object]:
    """Omit absent optional values instead of publishing JSON nulls."""
    return {key: item for key, item in value.items() if item is not None}
