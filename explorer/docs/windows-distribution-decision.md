---
id: markdownllm-explorer-windows-distribution
type: decision
status: made
version: 1.0
created: 2026-08-27
decided_by: Janosh Moshiri
origin: stated
exposed: false
tags: [explorer, windows, distribution, packaging]
---

# Decision: Native Windows Distribution for MarkdownLLM Explorer

## Context

The first Explorer increment was technically installable as a Python package, but the operator's actual Windows path failed before the product opened: the console command did not exist, the repository root was not a Python package, and the user was expected to understand Python, `pip`, package location and `PATH`. That recreates the black-box access problem at the installation boundary.

## Decision

Windows is the first native distribution target. Explorer will ship as one NSIS setup executable containing a PyInstaller one-folder runtime. Setup will install per user without elevation, validate and remember the substrate root, create Desktop and Start Menu shortcuts and register an uninstaller. The installed windowless launcher will open the default browser automatically and provide notification-area **Open Explorer** and **Exit Explorer** actions. Python remains the implementation language but is no longer an end-user prerequisite.

The portable Python package and CLI remain supported for development, automation and later non-Windows work. Linux and macOS native packaging are deferred until their own captured runtime evidence is available.

## Alternatives Considered

| Alternative | Reason rejected |
|---|---|
| Document the correct `pip install ...\explorer` command | Still makes Python, `pip`, package layout and `PATH` part of the user experience. |
| Ship a raw PyInstaller one-file executable | Adds repeated temporary extraction but still lacks root selection, stable upgrade identity, shortcuts and uninstall. |
| Rewrite the product in Go | Changes the implementation stack without solving the installer/desktop lifecycle by itself; no current performance evidence justifies the rewrite. |
| Use an administrator-wide installer | Creates an unnecessary elevation and machine-governance boundary for a local per-user viewer. |

## Consequences

The installer becomes a separately tested release artefact built on Windows. PyInstaller and NSIS are build-time dependencies; they do not enter core/application code or the end-user machine as separate tools. The selected substrate root is the only application setting retained outside the browser. The capability remains process-memory-only.

The build is structurally ready for Authenticode but cannot be publicly trusted as a known publisher until an authorised code-signing certificate is supplied. Unsigned local builds may therefore trigger Windows reputation warnings.

## Review Condition

Revisit the packaging choice if the frozen application fails the measured startup/support boundary, if public distribution requires Microsoft Store/MSIX governance, or when Linux/macOS native packaging becomes a prioritised operator requirement.

## Exposure

No. This is a project-specific distribution decision; another domain should not treat it as a general architectural rule.
