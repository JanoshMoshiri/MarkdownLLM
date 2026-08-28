# Install MarkdownLLM Explorer on Windows

MarkdownLLM Explorer is a small, read-only window into your substrate. The
Windows installer includes everything it needs: you do not have to install
Python, Node or a browser extension.

> Explorer is currently a **Windows preview candidate**. The reviewed product
> is accepted as a read-only viewer, but an unsigned local build is not a public
> release asset. Publish only after the application and setup are signed and the
> signed installer has completed the native lifecycle verification.

## Install in three steps

### 1. Open the installer

Get `MarkdownLLM-Explorer-Installer-0.3.0.exe` from your trusted MarkdownLLM
release source, then double-click it.

Windows may warn about or, under Smart App Control or enterprise code-integrity
policy, fully block an unsigned build. A public release must carry a trusted
publisher signature; source trust alone does not override those policies.
The release evidence must identify the signed installer by SHA-256; do not
rename an unsigned local build and treat it as the verified release.

### 2. Choose your substrate

When asked for the **MarkdownLLM folder**, choose the top-level folder that
contains your substrate's `AGENTS.md` file.

For example:

```text
C:\MarkdownLLM
├── AGENTS.md
├── skills
├── things
└── domain
```

Select **Install**. Explorer creates shortcuts on the Desktop and in the Start
Menu for the current Windows user.

### 3. Open Explorer

Double-click **MarkdownLLM Explorer** on the Desktop. Explorer starts quietly
in the notification area and opens in your default browser.

![MarkdownLLM Explorer showing a fictional Product Studio domain](images/estate-overview.jpg)

The screenshot uses **Northstar Studio**, a fictional estate made only for
public demonstrations.

That is it. Choose a domain from the left and start exploring.

## Open it again

Use the Desktop or Start Menu shortcut. If Explorer is already running, the
shortcut simply opens another browser view of the same local service.

The notification-area icon has two commands:

- **Open Explorer** — reopen the browser.
- **Exit Explorer** — stop the local service.

Closing the browser tab does not stop Explorer. Use **Exit Explorer** when you
are finished.

## Update or remove it

Run a newer installer to update Explorer. Your selected substrate folder is
kept. If Explorer is running, setup closes the local service, waits for it to
finish active work, and only then replaces the installed files.

To remove it, open **Installed apps** in Windows, find **MarkdownLLM Explorer**
and choose **Uninstall**. The uninstaller closes a running Explorer before
removing its files. Uninstalling Explorer does not change or remove your
substrate.

## If Explorer does not open

- Check that the chosen folder still exists and contains `AGENTS.md` or
  `.markdownllm`.
- Look for the Explorer icon in the Windows notification area and choose
  **Open Explorer**.
- If the folder moved, reinstall Explorer and choose its new location.

Explorer stays on your computer, binds only to the local loopback address and
does not need an internet connection after installation.
