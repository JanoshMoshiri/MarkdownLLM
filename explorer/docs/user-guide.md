# Explore a MarkdownLLM estate

MarkdownLLM Explorer turns a substrate and its domains into a calm, visual
map. Files and git remain the source of truth; Explorer gives you a way to see
and read them without using the command line.

> Explorer is currently a **Windows preview**. It is for inspection only: it
> does not change files, run an agent, synchronise repositories or publish
> anything.

All images in this guide come from **Northstar Studio**, a completely fictional
estate created for public demonstrations.

![The fictional Northstar estate with Product Studio selected](images/estate-overview.jpg)

## Start with the whole

The left side always shows two levels:

- **Substrate** — the shared MarkdownLLM framework at the top.
- **Domain estate** — the independent domains beneath it.

Choose any name to make it the active source. The centre changes immediately;
the right side confirms what you are looking at and that access is read-only.

## See what changed

**Overview** is the front door to a source. It shows the number of files,
skills and memory things, followed by recent commits from that source's own git
history.

Read the subjects from top to bottom to get a quick sense of movement. Choose a
different domain and the history changes with it.

## Read any file

Use **Source files** on the left to open folders and files. Markdown opens as a
styled document by default, with its frontmatter kept separately and clearly
labelled.

![A domain AGENTS file opened as a styled document](images/file-reader.jpg)

Choose **Raw** when you need to see the exact Markdown source. Choose
**Styled** to return to the reading view. Explorer never edits the file.

The search box filters by file path. It is useful when you know part of a file
or folder name but not where it lives.

## Find the reusable skills

Open **Skills** to see the Markdown files in the active source's `skills`
folder. Choose a skill to read it without losing the estate around you. Refresh,
Back and Forward restore both the skill and the surrounding Skills collection.

![A fictional discovery skill rendered inside Explorer](images/styled-skill.jpg)

## Follow the memory

Open **Memory** to see decisions, insights, conflicts and retrospectives. Items
are grouped by kind, so you can move from a decision to the learning that
informed it. A refreshed or restored Memory link keeps the grouped collection
visible beside the selected item.

![Fictional decisions, insights and retrospectives in the Memory view](images/memory-view.jpg)

Memory is not a chat transcript. It is the durable Markdown that helps a domain
carry reasoning across sessions.

## Make it comfortable

Use the small theme button beside search to move between **system**, **light**
and **dark**. Explorer remembers the choice in your browser without changing
the source or document you have open.

![The same fictional domain in the light theme](images/light-theme.jpg)

## A useful first journey

If this is your first visit:

1. Choose **Substrate** and read the latest commits.
2. Choose one domain and open its `AGENTS.md`.
3. Read one item under **Skills**.
4. Read one item under **Memory**.

You will have seen the whole estate, the purpose of one domain, one reusable
capability and one piece of durable learning.

## What Explorer will not do

Explorer cannot edit, create, delete, commit, pull or push. It does not run
skills or talk to an LLM. That boundary is intentional: the interface is a
window onto the accepted local state, not another place where state can change.

For installation or update help, see the
[Windows installation guide](installation-guide.md).
