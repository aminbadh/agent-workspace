# Workspace Conventions

The rules that keep this workspace readable by agents and honest about its own age. [AGENTS.md](AGENTS.md) carries the short version every agent follows. This file is the full spec, read when creating or restructuring a domain.

## The problem these rules solve

Every file here is written in the present tense. Without a freshness signal, a note written in April and a note written today read as equally current, and an agent will happily plan against a deadline that was replaced months ago. Worse, when the same fact is written in two places, one copy goes stale silently and both still look authoritative.

Two rules follow from that, and everything else is detail:

1. **Every domain declares its own status and age.**
2. **One fact, one home.** Everywhere else points at that home.

## The top level is organized by life context

Top-level folders (for example `work/`, `studies/`, `personal/`) are **areas of life**, not statuses. Whether something is being worked on lives in frontmatter (`status`), because changing a status is a one-line edit while moving a folder breaks every link to it and every `parent:` field.

**Growth rule.** A domain moves up to the top level when it stops belonging to its parent's context, not when it gets big. A side project under `work/` earns its own top-level folder when it becomes a company with its own money and team. Until then, nesting is correct.

## Frontmatter (required on every CONTEXT.md)

```yaml
---
domain: Newsletter
parent: work
status: active
last_reviewed: 2026-10-21
---
```

| Field | Meaning |
|---|---|
| `domain` | Display name. Matches the `# Domain:` heading |
| `parent` | The folder the domain sits in, or `root`. Checked by the linter, since moving a file does not update it |
| `status` | `active`, `dormant` or `archived`. See below |
| `last_reviewed` | The date the content was last **verified** as true, not the date it was last edited |
| `review_interval` | Optional. Days before `active` content is treated as suspect. Defaults to 14. Declare it only where 14 is wrong |

`last_reviewed` is the important one, and it means verified rather than touched. Fixing a typo does not refresh it. Confirming that the workstreams and facts still hold does.

**Files that are not domains use the same block**, which is how they opt into the freshness check: the linter checks every live `CONTEXT.md` plus any other file that carries frontmatter. For those, `domain` is just a display name and `parent` is the folder they sit in, or `root`. A file with no frontmatter is not checked, which is the right default for most working notes. The exception is a working file that asserts live state someone will act on, such as a runbook for a server: it opts in, because otherwise nothing notices when it stops being true.

### Status values

- **`active`**: being worked on now. Its workstreams are real commitments.
- **`dormant`**: real but not being worked. **Never present a dormant domain's workstreams as live work.** Say it is dormant and offer to revive it.
- **`archived`**: finished, or rarely needed. Lives under `.archive/`. Not read unless asked about directly, and never treated as current.

### Staleness

An `active` file whose `last_reviewed` is older than its review interval is suspect. Say so rather than trusting it: "this was last verified on X, treat the dates with caution." `uv run scripts/workspace-lint.py` reports these.

The interval is 14 days unless the file says otherwise. A file that knows its own rhythm declares it in `review_interval` rather than the tooling keeping a list of exceptions: a profile might declare 60, because a name and a graduation year do not move, and a Compass 30, because it is reviewed monthly. A `dormant` file inherits 90 instead, so it surfaces to be archived or woken rather than sitting forever.

## CONTEXT.md structure

`CONTEXT.md` is an **index of what is true now**, not an archive of how it got that way. Aim for under 100 lines. If it grows past that, the overflow belongs in `DECISIONS.md` or a `_working/` document. The linter leaves slack and warns at 120, so a file between the two is drifting rather than broken.

Required sections, in order:

1. **Title**: `# Domain: [Name]`
2. **Overview**: what this is and why it exists. A few sentences.
3. **Status & Priorities**: `### Active Workstreams` and `### Next Up`. The part agents read first and the part that rots fastest. A domain with no live workstreams is `dormant`, not an active domain with an empty list.
4. **Operating Context**: `### Constraints & Boundaries` and `### Key People & Orgs`. Hard limits only. No dates section: see [Dates](#dates).
5. **Pointer to DECISIONS.md**: one line.

Optional: **Key Resources** (links, accounts, where the original notes live) and a **Folder Map** for domains with enough files to need one. A folder map that disagrees with the filesystem is worse than none.

## DECISIONS.md

Append-only, one per domain. Everything settled and everything learned.

```markdown
## Open
- **Whether to move the newsletter to a paid tier.** Kept open because...

## Closed Decisions
- **Weekly on Tuesdays, 12 Sep 2026.** Readers open more on weekdays, and...

## Key Learnings & Principles
- **Write the subject line first.** Every issue that started from the subject...
```

One bullet per entry, led by a bold one-line statement of what was decided.

Open items go at the top under `## Open`, above everything closed, so all decision state lives in one place. `CONTEXT.md` carries only a one-line pointer.

Date closed decisions. Learnings rarely need a date. **Never delete an entry.** When a decision is replaced, add the new one and mark the old with `**Superseded 2026-11-02 by:** ...`. That is what stops the same ground being argued twice, and it is why `CONTEXT.md` can stay short.

## Folder vocabulary

```
[domain]/
├── CONTEXT.md          the hub: what is true now
├── DECISIONS.md        append-only log of what was settled and learned
├── _working/           internal analysis and living documents
├── _deliverables/      anything that goes to another person, prefixed YYYY-MM
├── _meetings/          call and meeting notes, prefixed YYYY-MM-DD
└── _sources/           documents someone else wrote, kept unedited
```

Only create the subfolders you need, when there is something to put in them.

**The underscore marks a folder as this level's own material rather than a child domain.** A parent such as `studies/` holds both, and without the prefix they interleave alphabetically. With it they sort above the child domains in every file browser. The linter rejects the unprefixed names.

**The line between `_working/` and `_deliverables/` matters most.** An agent may rewrite internal notes freely; something that already went to another person is a record.

`_sources/` holds documents somebody else wrote: a handbook, a contract, a published calendar. A derived document is only auditable if what it was derived from is still there. Three rules keep it from becoming a second home for facts:

- **Never edited.** A source is a snapshot. Record errors in the document derived from it.
- **Date-prefixed by the version it is,** not the day it was obtained, so a newer edition sits beside the old one.
- **A README.md indexing each file** and what was derived from it.

Other documents link to the derivation, not the source. Reading a source in place of its derivation is how an error that was already caught gets copied back in.

**Date-prefix anything point-in-time** so it sorts chronologically. Living documents that get revised in place stay undated.

## Linking

Use real Markdown links, relative to the file: `[strategy draft](_working/strategy-draft.md)`.

Not backticked paths. A backticked path is invisible to every tool: nothing checks it, nothing follows it, and it stays wrong forever. A real link is checked by the linter and opens in any editor.

**Not `[[wikilinks]]` either.** Only Obsidian resolves them; every other tool sees literal text. The linter warns if any appear.

**Material outside the workspace** (notes in another app, a folder of documents, a shared drive) is linked from the domain's Key Resources rather than copied in: the app's own link when it has one, otherwise a link to the folder. A domain filled from those notes says where they came from, so the source can be reread. When the workspace is used on more than one machine or reached from code repos, the building add-on's paths section covers how to write those links so they resolve everywhere.

When a document refers to a code repository, name the repository rather than writing its path. A name survives the folder moving; a path does not.

## The single-source rule

A parent `CONTEXT.md` is an **index**, not a summary. One row per child: name, status, one line of what it is, and a link. No dates, no decisions, no workstream detail.

The moment a parent restates a child's deadline, there are two copies of that deadline and one of them will be wrong. The linter warns when an index file carries dates.

The same rule holds across domains. Identity lives in [PROFILE.md](PROFILE.md), money in one finance domain, and so on. Reference them; do not copy them.

## The task home

**The task home holds anything row-shaped with a live status**: tasks, projects, trackers, content calendars, and every date to act on. **This repo holds reasoning, decisions and context.** A task home is either a task app the agent can reach (through an MCP server, a connector or a command-line tool) or a TASKS.md file at the root, started from [the template](.agents/skills/onboard/assets/TASKS.md). Onboarding sets it up, and [AGENTS.md](AGENTS.md#tasks) says which one this workspace uses and how to write to it.

Why the split works: a task app is good at surfacing what is due and bad at holding why. A folder of Markdown is the opposite. Each does the job it is good at, and the link between them is one line: a `CONTEXT.md` links to its project in the task home rather than copying its tasks, because a copied task is a stale task.

Rules for writing tasks:

- **Task names are short actions**, verb first: "Draft launch email", not "the launch email thing".
- **A task body stays nearly empty.** A constraint or a step order that would otherwise be forgotten, nothing more. Reasoning goes in the domain's files, and the task can say where.
- **Search before creating.** Check the task or project does not already exist under another name.
- **Targets sit before deadlines.** A due date is a target with slack, never the real deadline.

## Dates

**Dates you act on live in the task home**: due dates, deadlines, launch dates, application windows. A task app surfaces an overdue item by itself, and a second copy here goes stale the first time the plan moves. So a `CONTEXT.md` has no dates section, there is no date field in frontmatter, and a Next Up item links to its project in the task home instead of restating when.

A date belongs in these files in two cases only: **as history** inside a `DECISIONS.md` entry, where it records when something was settled and cannot go stale, and **as a stable fact** that is not a commitment, such as a graduation year or a contract's term. `last_reviewed` is metadata about the file, not a plan, and stays.

## Skills

A skill is a **procedure the user asks for by name**: a recurring pass with an order, or a workflow run on request. Each is a folder in `.agents/skills/` holding a `SKILL.md`, which Codex, OpenCode, Cursor and others read from there. Claude Code reads `.claude/skills/` only, so each skill is linked there too: `.claude/skills/<name>` is a symlink to `../../.agents/skills/<name>`.

**What goes where.** A skill only runs when invoked, and agents often fail to invoke one on their own. So:

- **Rules that must always hold** stay in [AGENTS.md](AGENTS.md), which every session loads.
- **Procedures and workflows** are skills, called by name or pointed to from AGENTS.md's skills table.
- **Steps that must come out the same every time** are scripts, run by the skill.
- **Specs and boundaries** that a skill or rule refers to, like this file, stay plain files.

**Write one the third time** the same sequence gets explained. The first time is work; the third time it is a procedure that has been costing the rediscovery. A one-off does not qualify, however involved, and neither does anything scoped to one domain: that is a runbook in the domain's `_working/` folder.

**Shape.** The frontmatter carries `name` and a `description` written as what it does plus when to use it, since the description is all an agent sees before deciding. A skill restates no rule: it applies them and links to where they live. A skill can add `status`, `last_reviewed` and `review_interval` under `metadata:`, which opts it into the linter's freshness check; skills without them are skipped.

**Add-ons** are optional sets of skills and files in [addons/](addons/README.md). The onboard skill moves one in when the user picks it, and the folder stays so another can be added later.

**Third-party skills** are installed only for a named gap, after reading every file they contain.

## Archive

Two kinds of material move to `.archive/[original-path]/`, keeping their structure, with `status: archived` and an `archived:` date added to the frontmatter:

- **Finished work**: a project that ended, a course that completed.
- **Rarely needed reference**: a setup that works and needs nothing. It is pulled back into the live tree when it needs changing.

Either way, **nothing active links into the archive.** If a live document still needs something, that thing is not archived, or the part still needed stays live. A loose working file gets its own folder with a short `CONTEXT.md` when archived, so it says what it is.

Archiving is not deletion: git keeps the history. The point is a lighter live tree, so an agent scanning for commitments does not surface one that ended in April. **Agents do not read `.archive/` unless the user asks about something in it.**

## Adding a domain

1. Create the folder at the right level.
2. Write `CONTEXT.md` with full frontmatter and the required sections ([the template](.agents/skills/onboard/assets/CONTEXT.md)).
3. Add a row to the parent's index table.
4. Create `_working/` when there is something to put in it, not before.
5. Run `uv run scripts/workspace-lint.py`.
