"""Pure Explorer domain and application values."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
from typing import Generic, Mapping, TypeVar
from urllib.parse import quote

from .errors import ExplorerError


class SourceKind(str, Enum):
    SUBSTRATE = "substrate"
    DOMAIN = "domain"


class GitKind(str, Enum):
    REPOSITORY = "repository"
    NON_GIT = "non-git"
    EXTERNAL_STORE = "external-store"
    UNAVAILABLE = "unavailable"


class EntryKind(str, Enum):
    DIRECTORY = "directory"
    FILE = "file"


class DocumentMode(str, Enum):
    RAW = "raw"
    RENDERED = "rendered"


class CollectionKind(str, Enum):
    SKILLS = "skills"
    MEMORY = "memory"


class FrontmatterState(str, Enum):
    ABSENT = "absent"
    VALID = "valid"
    INVALID = "invalid"


class LinkKind(str, Enum):
    RELATIVE = "relative"
    EXTERNAL = "external"
    INERT = "inert"


@dataclass(frozen=True, order=True)
class SourceId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or "\\" in self.value or "\x00" in self.value:
            raise ExplorerError("invalid_request")


@dataclass(frozen=True, order=True)
class BoundaryToken:
    value: str


@dataclass(frozen=True, order=True)
class RelativePath:
    value: str = ""

    @classmethod
    def parse(cls, raw: str | None) -> "RelativePath":
        value = raw or ""
        if "\x00" in value or "\\" in value or value.startswith(("/", "//")):
            raise ExplorerError("invalid_path", relative_path=None)
        if ":" in value:
            raise ExplorerError("invalid_path", relative_path=None)
        parts = value.split("/") if value else []
        if any(part in {"", ".", ".."} for part in parts):
            raise ExplorerError("invalid_path", relative_path=None)
        normalised = PurePosixPath(*parts).as_posix() if parts else ""
        return cls(normalised)

    @property
    def parts(self) -> tuple[str, ...]:
        return tuple(self.value.split("/")) if self.value else ()

    @property
    def depth(self) -> int:
        return len(self.parts)

    @property
    def name(self) -> str:
        return self.parts[-1] if self.parts else ""

    @property
    def parent(self) -> "RelativePath":
        return RelativePath("/".join(self.parts[:-1]))

    def child(self, name: str) -> "RelativePath":
        return RelativePath.parse("/".join((*self.parts, name)))

    def quoted(self) -> str:
        return quote(self.value, safe="/")


@dataclass(frozen=True)
class Source:
    id: SourceId
    kind: SourceKind
    display_name: str
    boundary_token: BoundaryToken
    markers: tuple[str, ...]
    git_kind: GitKind


@dataclass(frozen=True)
class SourceIssue:
    code: str
    message: str
    source_id: SourceId | None = None


@dataclass(frozen=True)
class EstateSnapshot:
    sources: tuple[Source, ...]
    issues: tuple[SourceIssue, ...]
    revision: str
    observed_at: str


@dataclass(frozen=True)
class TreeNode:
    path: RelativePath
    name: str
    kind: EntryKind
    size: int | None = None
    modified_at: str | None = None
    expandable: bool = False


T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    items: tuple[T, ...]
    next_cursor: str | None
    partial: bool
    observed_at: str


@dataclass(frozen=True)
class SourceCounts:
    eligible_files: int
    skills: int
    memory: int
    partial: bool


@dataclass(frozen=True)
class RepositoryState:
    kind: str
    head_sha: str | None = None
    branch: str | None = None
    dirty: bool | None = None
    issue: str | None = None


@dataclass(frozen=True)
class CommitRecord:
    sha: str
    subject: str
    author_name: str
    authored_at: str


@dataclass(frozen=True)
class FrontmatterResult:
    state: FrontmatterState
    values: Mapping[str, object] = field(default_factory=dict)
    error_code: str | None = None


@dataclass(frozen=True)
class RawDocument:
    source_id: SourceId
    path: RelativePath
    text: str
    size: int
    modified_at: str


@dataclass(frozen=True)
class LinkCandidate:
    label: str
    raw_target: str
    kind: LinkKind


@dataclass(frozen=True)
class ResolvedLink:
    label: str
    kind: LinkKind
    href: str | None = None


@dataclass(frozen=True)
class InlineNode:
    kind: str
    text: str = ""
    children: tuple["InlineNode", ...] = ()
    link_index: int | None = None


@dataclass(frozen=True)
class MarkdownBlock:
    kind: str
    inlines: tuple[InlineNode, ...] = ()
    level: int = 0
    text: str = ""
    items: tuple[tuple[InlineNode, ...], ...] = ()
    rows: tuple[tuple[tuple[InlineNode, ...], ...], ...] = ()


@dataclass(frozen=True)
class MarkdownTree:
    blocks: tuple[MarkdownBlock, ...]
    links: tuple[LinkCandidate, ...]


@dataclass(frozen=True)
class ParsedDocument:
    frontmatter: FrontmatterResult
    body: str


@dataclass(frozen=True)
class DocumentRecord:
    source_id: SourceId
    path: RelativePath
    mode: DocumentMode
    content: str
    frontmatter: FrontmatterResult
    size: int
    modified_at: str
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class CollectionItem:
    path: RelativePath
    title: str
    group: str
    thing_id: str | None = None
    thing_type: str | None = None
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class SourceSettingsRecord:
    source_id: SourceId
    source_path: str
    markers: tuple[str, ...]
    kind: SourceKind
    git_kind: GitKind


@dataclass(frozen=True)
class OverviewRecord:
    source: Source
    counts: SourceCounts
    repository: RepositoryState
    commits: Page[CommitRecord]
