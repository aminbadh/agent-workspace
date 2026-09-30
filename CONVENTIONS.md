# Workspace Conventions

The rules that keep this workspace readable by agents and honest about its own age.
[AGENTS.md](AGENTS.md) carries the short version every agent follows. This file is the full
spec, read when creating or restructuring a domain.

## The problem these rules solve

Every file here is written in the present tense. Without a freshness signal, a note written in
April and a note written today read as equally current, and an agent will happily plan against
a deadline that was replaced months ago. Worse, when the same fact is written in two places,
one copy goes stale silently and both still look authoritative.

Two rules follow from that, and everything else is detail:

1. **Every domain declares its own status and age.**
2. **One fact, one home.** Everywhere else points at that home.

## The top level is organized by life context

Top-level folders (for example `work/`, `personal/`, `education/`) are **areas of life**, not
statuses. Whether something is being worked on lives in frontmatter (`status`), because
changing a status is a one-line edit while moving a folder breaks every link to it.

**Growth rule.** A domain moves up to the top level when it stops belonging to its parent's
context, not when it gets big. A side project under `work/` earns its own top-level folder
when it becomes a company with its own money and team. Until then, nesting is correct.

## Frontmatter (required on every CONTEXT.md)

```yaml
---
domain: Newsletter
parent: work
status: active
last_reviewed: 2026-09-30
---
```

| Field | Meaning |
|---|---|
| `domain` | Display name. Matches the `# Domain:` heading |
| `parent` | The folder the domain sits in, or `root`. Checked by the linter, since moving a file does not update it |
| `status` | `active`, `dormant` or `archived`. See below |
| `last_reviewed` | The date the content was last **verified** as true, not the date it was last edited |
| `review_interval` | Optional. Days before `active` content is treated as suspect. Defaults to 14. Declare it only where 14 is wrong |

`last_reviewed` is the important one, and it means verified rather than touched. Fixing a typo
does not refresh it. Confirming that the workstreams and facts still hold does.

**Files that are not domains can use the same block** to opt into the freshness check: the
linter checks every live `CONTEXT.md` plus any other file that carries frontmatter.
[COMPASS.md](COMPASS.md) does, and declares `review_interval: 7` because weekly goals are the
first thing to rot. A reference file that barely changes can declare 60. A file with no
frontmatter is not checked, which is the right default for most working notes.

### Status values

- **`active`**: being worked on now. Its workstreams are real commitments.
- **`dormant`**: real but not being worked. **Never present a dormant domain's workstreams as
  live work.** Say it is dormant and offer to revive it.
- **`archived`**: finished, or rarely needed. Lives under `.archive/`. Not read unless asked
  about directly, and never treated as current.

### Staleness

An `active` file whose `last_reviewed` is older than its review interval is suspect. Say so
rather than trusting it: "this was last verified on X, treat the dates with caution."
`uv run scripts/workspace-lint.py` reports these.

## CONTEXT.md structure

`CONTEXT.md` is an **index of what is true now**, not an archive of how it got that way.
Aim for under 100 lines. If it grows past that, the overflow belongs in `DECISIONS.md` or a
`working/` document. The linter warns at 120.

Required sections, in order:

1. **Title**: `# Domain: [Name]`
2. **Overview**: what this is and why it exists. A few sentences.
3. **Status & Priorities**: `### Active Workstreams` and `### Next Up`. The part agents read
   first and the part that rots fastest. A domain with no live workstreams is `dormant`, not an
   active domain with an empty list.
4. **Operating Context**: `### Constraints & Boundaries` and `### Key People & Orgs`. Hard
   limits only. No dates section: see [Dates](#dates).
5. **Pointer to DECISIONS.md**: one line.

Optional: **Key Resources** (links, accounts, IDs) and a **Folder Map** for domains with enough
files to need one.

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

Open items go at the top, above everything closed, so all decision state lives in one place.
`CONTEXT.md` carries only a one-line pointer.

Date closed decisions. Learnings rarely need a date. **Never delete an entry.** When a
decision is replaced, add the new one and mark the old with
`**Superseded 2026-11-02 by:** ...`. That is what stops the same ground being argued twice,
and it is why `CONTEXT.md` can stay short.

## Folder vocabulary

```
[domain]/
├── CONTEXT.md          the hub: what is true now
├── DECISIONS.md        append-only log of what was settled and learned
├── working/            internal analysis and living documents
├── deliverables/       anything that goes to another person, prefixed YYYY-MM
├── meetings/           call and meeting notes, prefixed YYYY-MM-DD
└── sources/            documents someone else wrote, kept unedited
```

Only create the subfolders you need, when there is something to put in them.

**The line between `working/` and `deliverables/` matters most.** An agent may rewrite your
internal notes freely; something that already went to another person is a record.

`sources/` holds documents somebody else wrote: a handbook, a contract, a published calendar.
Three rules keep it from becoming a second home for facts:

- **Never edited.** A source is a snapshot. Record errors in the document derived from it.
- **Date-prefixed by the version it is,** so a newer edition sits beside the old one.
- **A README.md indexing each file** and what was derived from it.

**Date-prefix anything point-in-time** so it sorts chronologically. Living documents that get
revised in place stay undated.

## Linking

Use real Markdown links, relative to the file: `[strategy draft](working/strategy-draft.md)`.

Not backticked paths. A backticked path is invisible to every tool: nothing checks it, nothing
follows it, and it stays wrong forever. A real link is checked by the linter and opens in any
editor.

**Not `[[wikilinks]]` either.** Only Obsidian resolves them; every other tool sees literal
text. The linter warns if any appear.

When a document refers to a code repository elsewhere on your machine, name the repository
rather than writing its path. A name survives the folder moving; a path does not.

## The single-source rule

A parent `CONTEXT.md` is an **index**, not a summary. One row per child: name, status, one line
of what it is, and a link. No dates, no decisions, no workstream detail.

The moment a parent restates a child's deadline, there are two copies of that deadline and one
of them will be wrong. The linter warns when an index file carries dates.

The same rule holds across domains. Identity facts live in one profile file, money in one
finance domain. Reference them; do not copy them.

## Dates

**Dates you act on live in your task app**: due dates, deadlines, launch dates, application
windows. The app surfaces an overdue item by itself, and a second copy here goes stale the first
time the plan moves. So a `CONTEXT.md` has no dates section, and a Next Up item links to its
project in the task app instead of restating when. See [TASKS.md](TASKS.md).

A date belongs in these files in two cases only: **as history** inside a `DECISIONS.md` entry,
where it records when something was settled and cannot go stale, and **as a stable fact** that
is not a commitment, like a graduation year. `last_reviewed` is metadata about the file, not a
plan, and stays.

## Archive

Two kinds of material move to `.archive/[original-path]/`, keeping their structure, with
`status: archived` and an `archived:` date added to the frontmatter:

- **Finished work**: a project that ended, a course that completed.
- **Rarely needed reference**: a setup that works and needs nothing.

Either way, **nothing active links into the archive.** If a live document still needs
something, that thing is not archived. Archiving is not deletion: git keeps the history. The
point is a lighter live tree, so an agent scanning for commitments does not surface one that
ended in April.

## Adding a domain

1. Create the folder at the right level.
2. Write `CONTEXT.md` with full frontmatter and the required sections.
3. Add a row to the parent's index table.
4. Create `working/` when there is something to put in it, not before.
5. Run `uv run scripts/workspace-lint.py`.
