# MarkdownLLM Explorer

MarkdownLLM Explorer is a standalone, read-only browser for a MarkdownLLM substrate and its nested domain estate. It shows each repository's commits, file tree, skills and memory, and renders Markdown as a styled document.

## Windows install and run

Run `MarkdownLLM-Explorer-Installer-0.2.0.exe`. The installer asks for the
MarkdownLLM folder, installs the complete application for the current user,
and creates Desktop and Start Menu shortcuts. No separate Python or Node
installation is required.

Open **MarkdownLLM Explorer** from either shortcut. It starts in the notification
area and opens the Explorer in your default browser. Use the tray menu to reopen
the browser or exit the local service. Windows may identify an unsigned local
development build as coming from an unknown publisher; release signing can be
added without changing the package layout.

To build the Windows installer from source:

```powershell
.\packaging\windows\build.ps1
```

The build requires Python 3.10+ and NSIS 3.12, but the resulting installer and
installed application do not. The output is written to `dist/`.

## Python development route

For source development or automation, from any working directory using Python
3.10+:

```powershell
python -m pip install C:\path\to\MarkdownLLM\explorer
mdllm-explorer --root C:\path\to\MarkdownLLM
```

The command prints a loopback URL containing an in-memory launch capability in
its URL fragment. Open that URL in a browser. Explorer binds only to `127.0.0.1`,
performs no repository writes and needs no Node runtime, CDN or internet
connection after installation.

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
