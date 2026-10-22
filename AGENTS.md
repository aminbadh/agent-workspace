# Workspace Instructions

The one instructions file for every AI agent that works in this folder, whatever the tool or model. Tools that look for their own file name point here (see [CLAUDE.md](CLAUDE.md)).

## What this workspace is

A folder of plain Markdown files holding the context, reasoning and decisions behind what the user is working on. It is organized by **domain folders**: each has a `CONTEXT.md` saying what is true in it right now and a `DECISIONS.md` logging what was settled and learned. The full spec is [CONVENTIONS.md](.agents/CONVENTIONS.md). Read it before creating or restructuring a domain, rather than copying the shape of a neighbour.

## First, every session

1. **Read [PROFILE.md](PROFILE.md).** It says who the user is and what they are working on. Never ask for something it already answers.
2. **If PROFILE.md still says "Blank template", run the onboard skill before anything else,** whatever the user asked; if it says "Onboarding in progress", resume it. Tell them it takes about fifteen minutes and makes every later answer specific to them.

## Operating rules

1. **Context first.** Before answering anything about a domain, read its `CONTEXT.md`. Do not ask for information that is already written down.
2. **Check freshness before trusting a file.** Every `CONTEXT.md` carries `status` and `last_reviewed` in its frontmatter:
   - `status: dormant`: real, but not being worked. Never present its workstreams as live commitments. Say it is dormant.
   - `status: archived`: finished. It lives under `.archive/`. Do not read it unless the user asks about it directly.
   - `last_reviewed` older than the file's review interval: say so rather than trusting it, for example "last verified on 3 March, treat the dates with caution." [The linter](.agents/scripts/workspace-lint.py) reports what is overdue, so do not keep a threshold in your head.
3. **One fact, one home.** A parent `CONTEXT.md` is an index of its children, not a summary. Never copy a deadline, decision or number from one file into another. Link to where it lives. If two files disagree, the more specific one wins and the other is a bug to fix. Never record state one command reveals (unpushed commits, what is deployed, build status).
4. **Respect closed decisions.** If a `DECISIONS.md` marks something closed, do not reopen or re-analyze it unless the user explicitly asks.
5. **Update what you invalidate.** If work in a session changes something a `CONTEXT.md` asserts, edit that file in the same session and bump its `last_reviewed`. Settled a decision? Append it to `DECISIONS.md`. Stale context is the main way this workspace fails.
6. **Never invent a fact** about the user, their work or the world. Ask, or say you do not know. A plausible default that a plan is then built on is an invented fact.
7. **Search the web for questions about the outside world.** Whether a tool has an MCP server or connector, how to export from an app, the usual way to do something: search before answering or asking the user, and lead with the established solution rather than a homemade one.
8. **Links, not paths.** Refer to other files with real Markdown links, never backticked paths. A link can be checked; a backticked path stays wrong forever.

## What to do now

When the question is open (what should I do now, today or this week, I am stuck, I am behind), use the [one-thing skill](.agents/skills/one-thing/SKILL.md) rather than ranking from memory. When the conversation is already on a topic, "what now" means within that topic. Do not volunteer commentary on the user's priorities when they have not asked.

The weekly pass that keeps these files true is the [weekly-review skill](.agents/skills/weekly-review/SKILL.md). Run it when the user says it is review time or asks to plan the week, never unprompted.

## Tasks

*Not set up yet: the onboard skill writes where tasks live and how to reach them.*

The boundary between tasks and these files is in [CONVENTIONS.md](.agents/CONVENTIONS.md#the-task-home).

## Skills

Procedures the user asks for by name live as skills in `.agents/skills/`, linked into `.claude/skills/` for Claude Code. Use them rather than improvising. Rules that must always hold stay in this file, because a skill only runs when invoked.

| Skill | Use it when |
|---|---|
| [onboard](.agents/skills/onboard/SKILL.md) | PROFILE.md is blank, the user wants to update their setup, or they want an add-on from [addons/](.agents/addons/README.md) |
| [weekly-review](.agents/skills/weekly-review/SKILL.md) | It is review time, or the user asks to plan the week |
| [one-thing](.agents/skills/one-thing/SKILL.md) | The user asks what to do now with no topic in play |
| [upgrade](.agents/skills/upgrade/SKILL.md) | The user asks to upgrade the workspace, or the weekly review reports template changes |

## Working with me

*Not set up yet: the onboard skill writes how the user wants the AI to work and write for them.*

### What the agent may do

A safe default, until onboarding asks the user what to change.

- **Alone:** read anything connected; create and edit files in this workspace; run its scripts and read-only commands; draft anything.
- **Draft only, the user sends:** emails, messages, posts and comments; commits and pushes; anything written to a task app or calendar, until the user says otherwise.
- **Never:** spend money or start paid jobs, enter or store credentials, delete anything outside this workspace.

## Output

- Clean Markdown: headers, bold for key terms, tables for comparisons.
- When updating a document, make the edit directly. Do not describe what you would change.
- **Nothing is committed automatically.** Leave changes in the working tree for the user to review unless they ask for a commit.
