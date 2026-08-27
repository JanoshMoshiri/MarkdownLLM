"""Pure file and directory eligibility policy."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import PurePosixPath


ELIGIBLE_EXTENSIONS = frozenset(
    {
        ".md", ".markdown", ".txt", ".yaml", ".yml", ".json", ".toml",
        ".ini", ".cfg", ".csv", ".tsv", ".py", ".js", ".mjs", ".cjs",
        ".ts", ".tsx", ".jsx", ".css", ".html", ".xml", ".sh", ".ps1", ".bat",
    }
)
ELIGIBLE_EXTENSIONLESS = frozenset({"agents", "readme", "license", "changelog"})
IGNORED_DIRECTORIES = frozenset(
    {
        ".git", ".hg", ".svn", ".venv", "venv", "node_modules", ".next", "dist",
        "build", "coverage", ".coverage", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        "__pycache__", ".bundle-build", ".test-tmp", ".uv-cache",
    }
)
SECRET_PATTERNS = (
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*",
    "id_ed25519*", "*credential*", "*secret*", "*token*", "*.kdbx",
)


@dataclass(frozen=True)
class EligibilityPolicy:
    eligible_extensions: frozenset[str] = ELIGIBLE_EXTENSIONS
    eligible_extensionless: frozenset[str] = ELIGIBLE_EXTENSIONLESS
    ignored_directories: frozenset[str] = IGNORED_DIRECTORIES
    secret_patterns: tuple[str, ...] = SECRET_PATTERNS

    def is_ignored_directory(self, name: str) -> bool:
        folded = name.casefold()
        return name.startswith(".") or folded in self.ignored_directories or self.is_secret_name(name)

    def is_secret_name(self, name: str) -> bool:
        folded = name.casefold()
        return any(fnmatchcase(folded, pattern) for pattern in self.secret_patterns)

    def is_eligible_file(self, name: str) -> bool:
        folded = name.casefold()
        if self.is_secret_name(name):
            return False
        if folded == ".markdownllm":
            return True
        if name.startswith("."):
            return False
        suffix = PurePosixPath(folded).suffix
        if suffix:
            return suffix in self.eligible_extensions
        return folded in self.eligible_extensionless
