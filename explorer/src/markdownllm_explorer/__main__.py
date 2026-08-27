"""Command-line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from .composition import build_runtime
from .delivery.http_server import serve


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore a MarkdownLLM substrate and domain estate")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="substrate root (default: current directory)")
    parser.add_argument("--domain-dir", default="domain", help="one-level domain directory relative to root")
    parser.add_argument("--port", type=int, default=0, help="loopback port (default: choose an available port)")
    arguments = parser.parse_args()
    resolved_root = arguments.root.expanduser().resolve(strict=True)
    runtime = build_runtime(resolved_root, arguments.domain_dir)
    server, url = serve(runtime, arguments.port)
    print(f"Root: {resolved_root}", flush=True)
    print(f"MarkdownLLM Explorer: {url}", flush=True)
    print("Read-only local service. Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
