# Workspace Starter

**Tell your AI once.** A folder of plain Markdown files your AI assistant works in, so it knows who you are, what you are working on and what you already decided, and stops asking you to explain yourself every session. It stays useful instead of confidently wrong, because every file says how old it is and every fact lives in one place.

You do not set it up by hand. Open it in your AI tool and say hello: it interviews you for about fifteen minutes, creates your first areas of work from your answers, connects to where your notes and tasks already live, offers a weekly rhythm that fits how you plan, and finishes by doing one real task for you with what it just learned.

## How to start

1. **Get your own copy.** Press "Use this template" on GitHub (keep the new repository private: it will hold your life), then clone it. Or download the zip.
2. **Open the folder in your AI tool.** Claude Code, Codex and OpenCode all work; so does any tool that reads AGENTS.md.
3. **Say hello.** Onboarding starts by itself and asks what you are here for.

You need [uv](https://docs.astral.sh/uv/) for the linter and the add-on scripts (or Python 3.11 or newer for the linter alone). Nothing else to install.

## What it does for you

- **Your context, written down once.** Each area of your work or life is a folder with a `CONTEXT.md` (what is true now) and a `DECISIONS.md` (what was settled, so it stays settled).
- **Honest about its age.** Every file says when it was last verified, and the AI tells you when something is too old to trust instead of planning on it.
- **One fact, one home.** Everything else links to it, so there is no second copy to go stale.
- **Tasks stay in your task app.** If it can connect, the AI uses it; if not, a TASKS.md file. These files hold the reasoning, the task home holds the dates.
- **A weekly review** that keeps it all true, with the planning rhythm you choose: GTD, Agile Results, 12 Week Year, multi-scale planning, a Bullet Journal, or the Compass.
- **"What should I do now?"** has an answer, worked out from your plan and what actually moved.

## Core and add-ons

The core is small on purpose:

| File | What it is |
|---|---|
| [AGENTS.md](AGENTS.md) | The rules every agent follows. Onboarding adds how you want it to work and write for you |
| [CONVENTIONS.md](CONVENTIONS.md) | The full spec: frontmatter, freshness, folders, links, dates, the task home, skills |
| [PROFILE.md](PROFILE.md) | Who you are. Blank until onboarding fills it |
| [scripts/workspace-lint.py](scripts/workspace-lint.py) | The linter: stale files, broken links, dates where they do not belong. No dependencies |
| [onboard](.agents/skills/onboard/SKILL.md) | The first-session interview, later updates, and adding an add-on |
| [weekly-review](.agents/skills/weekly-review/SKILL.md) | Upkeep, then your own planning rhythm |
| [one-thing](.agents/skills/one-thing/SKILL.md) | Picks the single thing to do now |

[Add-ons](addons/README.md) wait in `addons/` until onboarding moves in the ones you pick, so an unused one never clutters your workspace:

- **Applications:** for applying to internships, jobs, Master's programmes, scholarships and more. A CV engine (plain content file to PDF, tailored copies, letters, interview stories) and opportunity research (find, screen, track, and verify every link and deadline).
- **Building:** for writing code with AI agents. One session plans and keeps the docs true; short-lived builders work in each repo from a written brief.

## Tools

- **Claude Code** reads [CLAUDE.md](CLAUDE.md), which imports AGENTS.md, and finds skills through the links in `.claude/skills/`.
- **Codex** and **OpenCode** read AGENTS.md and `.agents/skills/` directly.
- **Any other tool** that looks for its own file name: add that file with the same one-line import as CLAUDE.md, or point the tool's settings at AGENTS.md.

A browser your AI can drive helps (to read sites that block scripts, for example), and onboarding checks whether you have one rather than assuming.

## Where this came from

The workspace its maintainer has run their own work and studies from since March 2026, refined through daily use with AI agents and stripped back to the core. The story, and how each rule earned its place, is at [aminbadh.me/workspace](https://aminbadh.me/workspace).

## For the maintainer

This repository is a release of the maintainer's own workspace. The generic files (the three core skills, the applications add-on's skills, the linter, CONVENTIONS.md, the building add-on's BUILDING.md and [addons/README.md](addons/README.md)) are edited only there and copied here word for word by the release script, minus review dates. Never edit them here. The starter owns only PROFILE.md and AGENTS.md (blank templates), this README, LICENSE, .gitignore, CLAUDE.md and the add-on READMEs other than the index. To release, run the script, review the diff and commit.

```bash
./scripts/release.sh                   # from ~/.links/workspace
WORKSPACE=<dir> ./scripts/release.sh   # from anywhere else
```
