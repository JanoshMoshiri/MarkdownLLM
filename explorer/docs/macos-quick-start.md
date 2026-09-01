# Open MarkdownLLM Explorer on a Mac

MarkdownLLM Explorer is a read-only visual window onto a MarkdownLLM framework
and its domains. It runs locally on your Mac and opens in your normal browser.
It does not edit files, run agents, commit changes or publish anything.

The current Mac route is deliberately simple: Claude Code runs the launcher for
you. There is no `.app` or installer to manage yet.

## What you need

- The MarkdownLLM framework checked out on your Mac.
- Claude Code opened at the top-level framework folder.
- Python 3.10 or newer. The launcher checks this and explains if it is missing.
- Internet access on the first launch if Python needs to download the Explorer's
  small runtime dependency.

You do not need administrator access, Node.js or a browser extension.

## Open Explorer for the first time

1. Open the MarkdownLLM framework folder in Claude Code.
2. Make sure the framework is on the latest published `main` branch.
3. Paste this prompt:

   > Open the MarkdownLLM Explorer for this framework. Follow the repository's
   > AGENTS.md instructions and use the tracked macOS launcher. Do not edit any
   > domain files. If it fails, diagnose the Python or launcher problem and
   > report the exact error. Confirm that Explorer opens in my default browser.

4. Wait while Claude prepares the private Explorer environment and opens your
   browser. The first run can take a little longer because it creates the
   environment and installs the package from the current framework checkout.

Claude runs the tracked command:

```bash
bash tools/open-explorer.sh
```

You do not need to remember or type that command yourself.

## What a successful launch looks like

- Your default browser opens MarkdownLLM Explorer.
- The left side lists the **Substrate** followed by the admitted domains on your
  Mac.
- Selecting a source shows its Overview, files, Skills and Memory.
- The right panel says access is **Read-only**.

The Explorer server is available only on your own computer. Its launch
capability stays in memory and is not written into the framework or a log.

## A useful five-minute first look

1. Select **Substrate** and look at its recent commits.
2. Select one of your domains and open its `AGENTS.md` from **Source files**.
3. Open **Memory** and confirm that every populated first-level folder beneath
   `things/` appears, including groups such as plans or working documents.
4. Open a file from the left tree, then follow one rendered Markdown link and
   one related-item button. Each target should visibly replace the document.
5. Use browser Back, Forward and Refresh. The same document and reader layout
   should return.

## Open it again later

With the framework open in Claude Code, say:

> Open the MarkdownLLM Explorer.

The same launcher safely replaces any older Explorer process for this framework
and installs the Explorer code from the current checkout. That means a normal
framework update followed by another launch also updates Explorer.

## Stop Explorer

Explorer stops itself after **30 minutes without genuine browser or
authenticated API activity**. An open but untouched browser tab does not keep
the server running. If it has stopped, ask Claude to open it again.

To stop it immediately, say:

> Stop the MarkdownLLM Explorer.

Claude will use:

```bash
bash tools/open-explorer.sh --stop
```

The launcher checks process ownership before sending a stop signal, so a stale
process record cannot be used to stop an unrelated application.

## If it does not open

Give Claude this prompt:

> Diagnose why the tracked MarkdownLLM Explorer macOS launcher failed. Do not
> edit domain files, bypass the launcher's safety checks or invent a workaround.
> Tell me the exact error, the detected macOS and Python versions, and the
> smallest safe correction.

Common outcomes are:

- **Python is missing or too old** — install Python 3.10 or newer, then ask
  Claude to open Explorer again.
- **The framework checkout is behind** — update it safely, preserving any local
  work, then relaunch.
- **The first installation cannot download a dependency** — reconnect to the
  internet and retry.
- **The browser did not open** — ask Claude to check the owned Explorer process,
  stop it through the tracked launcher and relaunch it. Do not copy or persist a
  capability URL.

If the launcher still fails, send Janosh the exact terminal error rather than
trying a different installation route. The real Mac result is part of the
current acceptance work.

## Send useful first-run feedback

After the first session, ask Claude:

> Summarise this Explorer trial for Janosh. Include the macOS version, CPU
> architecture, Python version, whether launch and relaunch succeeded, whether
> all Memory folders appeared, whether related links opened visibly, and any
> exact error encountered. Confirm whether Explorer changed any served file or
> Git state.

## Further reading

- [Explorer documentation map](README.md)
- [How to use Explorer](user-guide.md)
- [Explorer source and release position](../README.md)
- [Open-source MarkdownLLM repository](https://github.com/JanoshMoshiri/MarkdownLLM)

