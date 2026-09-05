# MarkdownLLM Explorer

MarkdownLLM Explorer is a standalone, read-only browser for a MarkdownLLM substrate and its nested domain estate. It shows each repository's commits, file tree, skills and memory, and renders Markdown as a styled document.

> **Current release position — operator-accepted Windows preview candidate.**
> Independent review corrections are implemented. Public Windows publication
> is still gated by Authenticode signing and a final native lifecycle run on the
> signed bytes; the unsigned local build is not the release asset.

## Start here

- [Install Explorer on Windows](docs/installation-guide.md)
- [Open Explorer on macOS](docs/macos-quick-start.md)
- [Explore a MarkdownLLM estate](docs/user-guide.md)
- [See all Explorer documentation](docs/README.md)

## macOS quick route

With the MarkdownLLM framework checkout open in Claude Code, ask:

> Open the MarkdownLLM Explorer.

The framework instructions route Claude to:

```bash
bash tools/open-explorer.sh
```

The script checks for macOS and Python 3.10+, creates an Explorer-only virtual
environment in the user's Application Support directory, installs the Explorer
from the current checkout, starts the loopback service and opens the default
browser. It needs no administrator rights and never writes into a served
repository. The service keeps running until explicitly stopped, including when
the browser is idle or closed. Stop it with `bash tools/open-explorer.sh --stop`.

This portable route is the immediate Mac handoff. A native `.app`/DMG remains a
later lane requiring an actual Mac build host and separate signing/notarization
evidence.

## Windows install and run

Run `MarkdownLLM-Explorer-Installer-0.4.1.exe`. The installer asks for the
MarkdownLLM folder, installs the complete application for the current user,
and creates Desktop and Start Menu shortcuts. No separate Python or Node
installation is required.

Open **MarkdownLLM Explorer** from either shortcut. It starts in the notification
area and opens the Explorer in your default browser. Use the tray menu to reopen
the browser or exit the local service. Windows may warn about or fully block an
unsigned local development build. The public release must sign both the frozen
application and setup before the final native verification run; signing does
not change the package layout.

To build the Windows installer from source:

```powershell
.\packaging\windows\build.ps1
```

For a public build, pass all three signing inputs together:

```powershell
.\packaging\windows\build.ps1 `
  -SignToolPath 'C:\path\to\signtool.exe' `
  -SignCertificateThumbprint '40_HEXADECIMAL_CHARACTERS' `
  -TimestampUrl 'https://your-ca.example/rfc3161'
```

The build signs the frozen application first, then uses NSIS signing hooks for
the generated uninstaller and final setup. It fails closed if any signing step
or RFC 3161 timestamp fails.

The build requires Python 3.10+ and NSIS 3.12, but the resulting installer and
installed application do not. The output is written to the ignored `dist/`
directory. A public installer must be rebuilt from the final immutable
candidate, verified and attached as a release asset; it is not tracked in Git.

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
--open-browser      open the capability URL in the default browser
```

Press Ctrl+C to stop the server. Explorer has no inactivity timeout on any
launch surface; use the Mac stop command or Windows tray Exit when finished.

## Development

```powershell
Set-Location C:\path\to\MarkdownLLM\explorer
python -m pip install -e .
python -m pytest
```

The explicit working-directory step keeps Explorer's local test tools distinct
from the framework root's `tools` package. The governing requirements, design
and test ledger also live in `docs/`.
