# Workspace Starter

A folder structure and a small set of rules that keep an AI assistant useful instead of
confidently wrong, when you run your work or life from plain Markdown files.

Works with any tool that reads files: Claude Code, Codex, Cursor, OpenCode, or whatever comes
next. The instructions live in [AGENTS.md](AGENTS.md), the shared format most agents read.

## The problem

Every note you write sounds current forever. An assistant cannot tell a note from April from one
written this morning, and when the same fact lives in two files, one copy goes stale while both
still look right. The assistant then plans against the stale one, confidently.

## The idea

- **Domains.** One folder per area of your work or life, each with a `CONTEXT.md` that says what
  is true in it right now.
- **Every file declares its age.** A status (active, dormant, archived) and the date it was last
  verified. Old means suspect, and the assistant says so.
- **One fact, one home.** Everything else links to it. Parent folders are indexes, not summaries.
- **Decisions are logged, not remembered.** Each domain keeps an append-only `DECISIONS.md`, so
  settled questions stay settled.
- **A linter catches the rot.** Stale files, broken links, dates copied where they do not belong.
- **A Compass for priorities.** One file ranks the areas of your life against each other, so
  "what should I do now?" has an answer.
- **Tasks stay in your task app.** These files hold reasoning; your app holds dates.

## What is in here

| File | What it is |
|---|---|
| [AGENTS.md](AGENTS.md) | The rules every agent follows. Edit the "Working with me" section |
| [CLAUDE.md](CLAUDE.md) | One line pointing Claude Code at AGENTS.md |
| [CONVENTIONS.md](CONVENTIONS.md) | The full spec: frontmatter, freshness, folders, links, dates |
| [COMPASS.md](COMPASS.md) | Your areas of life, each with a goal ladder. Blank, for you to fill |
| [TASKS.md](TASKS.md) | Where the line sits between these files and your task app |
| [procedures/weekly-review.md](procedures/weekly-review.md) | The 30-minute weekly pass that keeps it all true |
| [work/](work/CONTEXT.md) | An invented example domain. Read it, copy its shape, delete it |
| [scripts/workspace-lint.py](scripts/workspace-lint.py) | The linter. No dependencies |

## Getting started

1. **Copy this repository.** Press "Use this template" on GitHub, or download the zip.
2. **Open the folder in your AI tool** and ask it: *"Read AGENTS.md and CONVENTIONS.md, then
   help me set up my first domain."* Start with one area you are actively working on.
3. **Run the linter:** `uv run scripts/workspace-lint.py` (or `python3 scripts/workspace-lint.py`
   with Python 3.11+). Within two weeks it will flag the example domain as stale. That is the
   point: delete it once your own domains exist.

Then fill in the Compass when you next plan a week, and run the weekly review when you do.

### Tool notes

- **Claude Code** reads [CLAUDE.md](CLAUDE.md), which imports AGENTS.md.
- **Codex**, **Cursor** and **OpenCode** read AGENTS.md directly.
- **Any other tool** that looks for its own file name: add that file with the same one-line
  import as CLAUDE.md, or point the tool's settings at AGENTS.md.

## Where this came from

This is the skeleton of the workspace I have run my own work and studies from since March 2026,
refined through daily use with AI agents. The full story, and how each rule earned its place, is at
[aminbadh.me/workspace](https://aminbadh.me/workspace).
