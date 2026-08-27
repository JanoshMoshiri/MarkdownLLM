"""PyInstaller entry point for the windowed Windows application."""

from __future__ import annotations

import multiprocessing

from markdownllm_explorer.windows_app import main


if __name__ == "__main__":
    multiprocessing.freeze_support()
    raise SystemExit(main())
