"""Read-only, root-confined browsing over registered sources."""

from __future__ import annotations

import hashlib
import os
import stat
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote

from markdownllm_explorer.core.eligibility import EligibilityPolicy
from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import (
    BoundaryToken, CollectionItem, DocumentMode, DocumentRecord, EntryKind, FrontmatterResult, FrontmatterState,
    LinkKind, Page, RelativePath, ResolvedLink, SourceCounts, SourceSettingsRecord, TreeNode,
)

from .cursors import CursorCodec, CursorState
from .document_presenter import DocumentPresenter
from .filesystem_catalogue import BoundaryRegistry, SourceBoundary, _is_reparse
from .frontmatter_parser import FrontmatterParser
from .safe_markdown_parser import SafeMarkdownParser


class ConfinedSourceReader:
    def __init__(
        self, registry: BoundaryRegistry, policy: EligibilityPolicy, limits: ExplorerLimits,
        cursors: CursorCodec, frontmatter: FrontmatterParser, markdown: SafeMarkdownParser,
        presenter: DocumentPresenter,
    ) -> None:
        self._registry = registry
        self._policy = policy
        self._limits = limits
        self._cursors = cursors
        self._frontmatter = frontmatter
        self._markdown = markdown
        self._presenter = presenter

    def counts(self, token: BoundaryToken) -> SourceCounts:
        boundary = self._registry.by_token(token)
        eligible = skills = memory = 0
        partial = False
        for relative, _ in self._walk(boundary):
            eligible += 1
            if relative.parts and relative.parts[0].casefold() == "skills" and relative.name.casefold().endswith((".md", ".markdown")):
                skills += 1
            if self._memory_group(relative):
                memory += 1
            if eligible >= self._limits.candidate_scan:
                partial = True
                break
        return SourceCounts(eligible, skills, memory, partial)

    def tree(self, token: BoundaryToken, path: RelativePath, cursor: str | None) -> Page[TreeNode]:
        boundary = self._registry.by_token(token)
        if path.depth > self._limits.directory_depth:
            raise ExplorerError("directory_limit")
        directory = self._resolve_directory(boundary, path)
        nodes: list[TreeNode] = []
        try:
            before_directory = directory.stat(follow_symlinks=False)
            entries = list(os.scandir(directory))
            after_directory = directory.stat(follow_symlinks=False)
        except FileNotFoundError:
            raise ExplorerError("file_not_found") from None
        except OSError:
            raise ExplorerError("source_unreadable") from None
        if not _same_file(before_directory, after_directory) or before_directory.st_mtime_ns != after_directory.st_mtime_ns:
            raise ExplorerError("source_changed")
        for entry in entries:
            child = path.child(entry.name)
            if self._excluded(boundary, child, entry.name) or (entry.is_dir(follow_symlinks=False) and self._policy.is_ignored_directory(entry.name)):
                continue
            try:
                if entry.is_symlink() or _is_reparse(Path(entry.path)):
                    continue
                info = entry.stat(follow_symlinks=False)
                if entry.is_dir(follow_symlinks=False):
                    nodes.append(TreeNode(child, entry.name, EntryKind.DIRECTORY, expandable=True))
                elif entry.is_file(follow_symlinks=False) and self._policy.is_eligible_file(entry.name):
                    nodes.append(TreeNode(child, entry.name, EntryKind.FILE, info.st_size, _iso(info.st_mtime)))
            except OSError:
                continue
        nodes.sort(key=lambda item: (item.kind is EntryKind.FILE, item.name.casefold(), item.name))
        revision = self._revision(nodes)
        state = self._cursors.decode(cursor, operation="tree", source=boundary.source.id.value, context=path.value)
        if state.revision and state.revision != revision:
            raise ExplorerError("source_changed")
        return self._page(nodes, state.offset, self._limits.directory_page, "tree", boundary, path.value, revision)

    def search(self, token: BoundaryToken, query: str, cursor: str | None) -> Page[TreeNode]:
        boundary = self._registry.by_token(token)
        query = query.strip()
        if not query or len(query) > 200:
            raise ExplorerError("invalid_query")
        folded = query.casefold()
        matches: list[TreeNode] = []
        scanned = 0
        partial = False
        for relative, info in self._walk(boundary):
            scanned += 1
            if folded in relative.value.casefold():
                matches.append(TreeNode(relative, relative.name, EntryKind.FILE, info.st_size, _iso(info.st_mtime)))
            if scanned >= self._limits.candidate_scan:
                partial = True
                break
        matches.sort(key=lambda item: item.path.value.casefold())
        revision = self._revision(matches) + ("-partial" if partial else "")
        state = self._cursors.decode(cursor, operation="search", source=boundary.source.id.value, context=folded)
        if state.revision and state.revision != revision:
            raise ExplorerError("source_changed")
        page = self._page(matches, state.offset, self._limits.search_page, "search", boundary, folded, revision)
        return Page(page.items, page.next_cursor, page.partial or partial, page.observed_at)

    def collection(self, token: BoundaryToken, kind: str, cursor: str | None) -> Page[CollectionItem]:
        boundary = self._registry.by_token(token)
        if kind not in {"skills", "memory"}:
            raise ExplorerError("invalid_request")
        candidates: list[CollectionItem] = []
        ids: dict[str, list[int]] = {}
        scanned = 0
        partial = False
        for relative, _ in self._walk(boundary):
            group = ""
            if kind == "skills":
                if not (relative.parts and relative.parts[0].casefold() == "skills" and relative.name.casefold().endswith((".md", ".markdown"))):
                    continue
                group = "Skills"
            else:
                group = self._memory_group(relative) or ""
                if not group:
                    continue
            scanned += 1
            issues: list[str] = []
            title = relative.name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
            thing_id = thing_type = None
            try:
                raw = self._read_text(boundary, relative)
                parsed = self._frontmatter.parse(raw[0])
                if parsed.frontmatter.state is FrontmatterState.VALID:
                    values = parsed.frontmatter.values
                    thing_id = _string(values.get("id"))
                    thing_type = _string(values.get("type"))
                    title = self._title(parsed.body) or title
                    if kind == "memory" and thing_type and thing_type.casefold() != group.rstrip("s").casefold():
                        issues.append("frontmatter_type_mismatch")
                elif parsed.frontmatter.state is FrontmatterState.INVALID:
                    issues.append("frontmatter_invalid")
                elif kind == "memory":
                    issues.append("frontmatter_missing")
            except ExplorerError as error:
                issues.append(error.code)
            item_index = len(candidates)
            candidates.append(CollectionItem(relative, title, group, thing_id, thing_type, tuple(issues)))
            if thing_id:
                ids.setdefault(thing_id, []).append(item_index)
            if scanned >= self._limits.memory_candidates:
                partial = True
                break
        for indexes in ids.values():
            if len(indexes) > 1:
                for item_index in indexes:
                    item = candidates[item_index]
                    candidates[item_index] = CollectionItem(item.path, item.title, item.group, item.thing_id, item.thing_type, (*item.issues, "duplicate_id"))
        candidates.sort(key=lambda item: (item.group.casefold(), item.title.casefold(), item.path.value))
        revision = self._revision(candidates) + ("-partial" if partial else "")
        state = self._cursors.decode(cursor, operation="collection", source=boundary.source.id.value, context=kind)
        if state.revision and state.revision != revision:
            raise ExplorerError("source_changed")
        page = self._page(candidates, state.offset, self._limits.search_page, "collection", boundary, kind, revision)
        return Page(page.items, page.next_cursor, page.partial or partial, page.observed_at)

    def document(self, token: BoundaryToken, path: RelativePath, mode: DocumentMode) -> DocumentRecord:
        boundary = self._registry.by_token(token)
        text, size, modified = self._read_text(boundary, path)
        is_markdown = PurePosixPath(path.value.casefold()).suffix in {".md", ".markdown"}
        parsed = self._frontmatter.parse(text) if is_markdown else None
        frontmatter = parsed.frontmatter if parsed else FrontmatterResult(FrontmatterState.ABSENT)
        issues = (frontmatter.error_code,) if frontmatter.error_code else ()
        actual_mode = mode if is_markdown else DocumentMode.RAW
        if actual_mode is DocumentMode.RAW:
            content = text
        else:
            tree = self._markdown.parse(parsed.body if parsed else text)
            resolved = tuple(self._resolve_link(boundary, path, link) for link in tree.links)
            content = self._presenter.render(tree, resolved)
        return DocumentRecord(boundary.source.id, path, actual_mode, content, frontmatter, size, modified, tuple(issue for issue in issues if issue))

    def settings(self, token: BoundaryToken) -> SourceSettingsRecord:
        boundary = self._registry.by_token(token)
        return SourceSettingsRecord(boundary.source.id, str(boundary.root), boundary.source.markers, boundary.source.kind, boundary.source.git_kind)

    def _read_text(self, boundary: SourceBoundary, relative: RelativePath) -> tuple[str, int, str]:
        if not relative.name or not self._policy.is_eligible_file(relative.name) or self._excluded(boundary, relative, relative.name):
            raise ExplorerError("path_excluded")
        candidate = boundary.root.joinpath(*relative.parts)
        self._reject_reparse_components(boundary, relative)
        try:
            before = candidate.lstat()
        except FileNotFoundError:
            raise ExplorerError("file_not_found") from None
        except OSError:
            raise ExplorerError("source_unreadable") from None
        if not stat.S_ISREG(before.st_mode) or _is_reparse(candidate):
            raise ExplorerError("path_type_changed")
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(boundary.root)
            if boundary.excluded_root is not None and _inside(resolved, boundary.excluded_root):
                raise ExplorerError("path_excluded")
        except ValueError:
            raise ExplorerError("path_outside_source") from None
        try:
            with candidate.open("rb") as handle:
                opened = os.fstat(handle.fileno())
                if not _same_file(before, opened):
                    raise ExplorerError("source_changed")
                opened_path = _opened_final_path(handle)
                if opened_path is not None:
                    try:
                        opened_path.relative_to(boundary.root)
                    except ValueError:
                        raise ExplorerError("path_outside_source") from None
                    if boundary.excluded_root is not None and _inside(opened_path, boundary.excluded_root):
                        raise ExplorerError("path_excluded")
                payload = handle.read(self._limits.file_bytes + 1)
                if len(payload) > self._limits.file_bytes:
                    raise ExplorerError("file_too_large")
                after = os.fstat(handle.fileno())
            final = candidate.lstat()
        except ExplorerError:
            raise
        except FileNotFoundError:
            raise ExplorerError("source_changed") from None
        except PermissionError:
            raise ExplorerError("source_unreadable") from None
        except OSError:
            raise ExplorerError("source_changed") from None
        if not (_same_file(opened, after) and _same_file(after, final) and opened.st_size == after.st_size == final.st_size and opened.st_mtime_ns == after.st_mtime_ns == final.st_mtime_ns):
            raise ExplorerError("source_changed")
        if b"\x00" in payload:
            raise ExplorerError("binary_unsupported")
        try:
            text = payload.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ExplorerError("encoding_unsupported") from None
        return text, len(payload), _iso(final.st_mtime)

    def _resolve_directory(self, boundary: SourceBoundary, relative: RelativePath) -> Path:
        if any(self._policy.is_ignored_directory(part) for part in relative.parts) or self._excluded(boundary, relative, relative.name):
            raise ExplorerError("path_excluded")
        candidate = boundary.root.joinpath(*relative.parts)
        self._reject_reparse_components(boundary, relative)
        try:
            if _is_reparse(candidate) or not candidate.is_dir():
                raise ExplorerError("file_not_found")
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(boundary.root)
            if boundary.excluded_root is not None and _inside(resolved, boundary.excluded_root):
                raise ExplorerError("path_excluded")
            return resolved
        except ValueError:
            raise ExplorerError("path_outside_source") from None

    def _walk(self, boundary: SourceBoundary):
        stack: list[tuple[Path, RelativePath, int]] = [(boundary.root, RelativePath(), 0)]
        while stack:
            directory, relative_dir, depth = stack.pop()
            if depth >= self._limits.directory_depth:
                continue
            try:
                before_directory = directory.stat(follow_symlinks=False)
                entries = list(os.scandir(directory))
                after_directory = directory.stat(follow_symlinks=False)
            except OSError:
                continue
            if not _same_file(before_directory, after_directory) or before_directory.st_mtime_ns != after_directory.st_mtime_ns:
                raise ExplorerError("source_changed")
            for entry in sorted(entries, key=lambda item: item.name.casefold(), reverse=True):
                child = relative_dir.child(entry.name)
                if self._excluded(boundary, child, entry.name):
                    continue
                try:
                    path = Path(entry.path)
                    if entry.is_symlink() or _is_reparse(path):
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        if not self._policy.is_ignored_directory(entry.name):
                            stack.append((path, child, depth + 1))
                    elif entry.is_file(follow_symlinks=False) and self._policy.is_eligible_file(entry.name):
                        yield child, entry.stat(follow_symlinks=False)
                except OSError:
                    continue

    def _excluded(self, boundary: SourceBoundary, relative: RelativePath, name: str) -> bool:
        if self._policy.is_secret_name(name) or any(self._policy.is_ignored_directory(part) for part in relative.parts[:-1]):
            return True
        if boundary.excluded_root is not None:
            candidate = boundary.root.joinpath(*relative.parts)
            return _inside(candidate, boundary.excluded_root)
        return False

    def _reject_reparse_components(self, boundary: SourceBoundary, relative: RelativePath) -> None:
        current = boundary.root
        for part in relative.parts:
            current = current / part
            if _is_reparse(current):
                raise ExplorerError("path_outside_source")

    def _memory_group(self, relative: RelativePath) -> str | None:
        if len(relative.parts) < 3 or relative.parts[0].casefold() != "things" or not relative.name.casefold().endswith((".md", ".markdown")):
            return None
        groups = {"insights": "Insights", "conflicts": "Conflicts", "retrospectives": "Retrospectives", "decisions": "Decisions"}
        return groups.get(relative.parts[1].casefold())

    def _resolve_link(self, boundary: SourceBoundary, document: RelativePath, link) -> ResolvedLink:
        if link.kind is LinkKind.EXTERNAL:
            return ResolvedLink(link.label, link.kind, link.raw_target)
        if link.kind is not LinkKind.RELATIVE:
            return ResolvedLink(link.label, LinkKind.INERT)
        target_text = link.raw_target.split("#", 1)[0].split("?", 1)[0]
        try:
            combined = PurePosixPath(document.parent.value) / target_text
            parts: list[str] = []
            for part in combined.parts:
                if part == "..":
                    if not parts:
                        raise ValueError
                    parts.pop()
                elif part not in {"", "."}:
                    parts.append(part)
            target = RelativePath.parse("/".join(parts))
            candidate = boundary.root.joinpath(*target.parts)
            if self._excluded(boundary, target, target.name) or not candidate.is_file() or _is_reparse(candidate) or not self._policy.is_eligible_file(target.name):
                return ResolvedLink(link.label, LinkKind.INERT)
            candidate.resolve(strict=True).relative_to(boundary.root)
            href = f"#source={quote(boundary.source.id.value, safe='')}&path={target.quoted()}"
            return ResolvedLink(link.label, LinkKind.RELATIVE, href)
        except (ValueError, OSError, ExplorerError):
            return ResolvedLink(link.label, LinkKind.INERT)

    def _page(self, items, offset: int, limit: int, operation: str, boundary: SourceBoundary, context: str, revision: str):
        selected = tuple(items[offset:offset + limit])
        next_cursor = None
        if offset + limit < len(items):
            next_cursor = self._cursors.encode(CursorState(operation, boundary.source.id.value, context, offset + limit, revision))
        return Page(selected, next_cursor, False, datetime.now(timezone.utc).isoformat())

    @staticmethod
    def _revision(items) -> str:
        content = "\n".join(repr(item) for item in items).encode()
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def _title(body: str) -> str | None:
        for line in body.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return None


def _same_file(left: os.stat_result, right: os.stat_result) -> bool:
    return (left.st_dev, left.st_ino, stat.S_IFMT(left.st_mode)) == (right.st_dev, right.st_ino, stat.S_IFMT(right.st_mode))


def _inside(candidate: Path, root: Path) -> bool:
    try:
        candidate.absolute().relative_to(root.absolute())
        return True
    except ValueError:
        return False


def _iso(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def _string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _opened_final_path(handle) -> Path | None:
    if os.name != "nt":
        return None
    try:
        import ctypes
        import msvcrt

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        function = kernel32.GetFinalPathNameByHandleW
        function.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32]
        function.restype = ctypes.c_uint32
        native_handle = msvcrt.get_osfhandle(handle.fileno())
        size = function(native_handle, None, 0, 0)
        if not size:
            raise OSError(ctypes.get_last_error())
        buffer = ctypes.create_unicode_buffer(size + 1)
        written = function(native_handle, buffer, len(buffer), 0)
        if not written or written >= len(buffer):
            raise OSError(ctypes.get_last_error())
        value = buffer.value
        if value.startswith("\\\\?\\UNC\\"):
            value = "\\\\" + value[8:]
        elif value.startswith("\\\\?\\"):
            value = value[4:]
        return Path(value).resolve(strict=True)
    except (AttributeError, OSError, ValueError):
        raise ExplorerError("source_unreadable") from None
