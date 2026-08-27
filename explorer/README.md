# MarkdownLLM Explorer

MarkdownLLM Explorer is a standalone, read-only browser for a MarkdownLLM substrate and its nested domain estate. It shows each repository's commits, file tree, skills and memory, and renders Markdown as a styled document.

## Install and run

From any working directory, using Python 3.10+:

```powershell
python -m pip install C:\path\to\MarkdownLLM\explorer
mdllm-explorer --root C:\path\to\MarkdownLLM
```

The command prints a loopback URL containing an in-memory launch capability in its URL fragment. Open that URL in a browser. Explorer binds only to `127.0.0.1`, performs no repository writes and needs no Node runtime, CDN or internet connection after installation.

Options:

```text
--root PATH         substrate root (required)
--domain-dir PATH   source-relative domain directory (default: domain)
--port PORT         loopback port; 0 selects an available port (default: 0)
```

Press Ctrl+C to stop the server.

## Development

```powershell
python -m pip install -e C:\path\to\MarkdownLLM\explorer
python -m pytest C:\path\to\MarkdownLLM\explorer\tests
```

The governing requirements, design and test ledger live in `docs/`.

