# Workspace Instructions

The single instructions file for every AI agent that works in this folder, whatever the tool
or model. Tools that look for their own file name point here (see [CLAUDE.md](CLAUDE.md)).

## What this workspace is

A folder of plain Markdown files that holds the context, reasoning and decisions behind
everything I am working on. It is organized by **domain folders**. Each domain has a
`CONTEXT.md` saying what is true in it right now, and a `DECISIONS.md` logging what was
settled and learned. The full spec is [CONVENTIONS.md](CONVENTIONS.md): read it before
creating or restructuring a domain, rather than copying the shape of a neighbour.

Tasks and dates do not live here. They live in my task app; see [TASKS.md](TASKS.md).

## Operating rules

1. **Context first.** Before answering anything about a domain, read its `CONTEXT.md`. Do not
   ask me for information that is already written down.
2. **Check freshness before trusting a file.** Every `CONTEXT.md` carries `status` and
   `last_reviewed` in its frontmatter:
   - `status: dormant`: real, but not being worked. Never present its workstreams as live
     commitments. Say it is dormant.
   - `status: archived`: finished. It lives under `.archive/`. Do not read it unless I ask
     about it directly.
   - `last_reviewed` older than the file's review interval: say so rather than trusting it,
     for example "last verified on 3 March, treat the dates with caution." The
     [linter](scripts/workspace-lint.py) reports what is overdue, so do not keep a threshold
     in your head.
3. **One fact, one home.** A parent `CONTEXT.md` is an index of its children, not a summary.
   Never copy a deadline, decision or number from one file into another. Link to where it
   lives. If two files disagree, the more specific one wins and the other is a bug to fix.
4. **Respect closed decisions.** If a `DECISIONS.md` marks something closed, do not reopen or
   re-analyze it unless I explicitly ask.
5. **Update what you invalidate.** If work in a session changes something a `CONTEXT.md`
   asserts, edit that file in the same session and bump its `last_reviewed`. Settled a
   decision? Append it to `DECISIONS.md`. Stale context is the main way this workspace fails.
6. **Links, not paths.** Refer to other files with real Markdown links, never backticked
   paths. A link can be checked; a backticked path stays wrong forever.
7. **Arbitrate with the Compass.** Domain files say what is true inside a domain. They never
   say which domain matters most. When that is the question, read [COMPASS.md](COMPASS.md).

## The Compass

[COMPASS.md](COMPASS.md) is the only file with authority across domains: a few life areas,
each with a goal ladder from someday down to this week.

**Read it when** the question is what to do now, today or this week; when I say I am stuck,
behind or overwhelmed; when a plan trades one domain off against another; and when something
new is being considered. A new commitment is a priority decision in disguise, drawn from the
same fixed hours as everything else.

**Do not read it** for routine work inside one domain, and do not volunteer commentary on my
priorities when I have not asked.

**Picking one thing to do now.** Read the board, check each candidate's domain for what
actually moved, and name one. Weigh closing deadlines first, then whether the next step is in
my hands, then what is in season. If the top candidate is blocked on a person, the action is
the unblock. If it is blocked by a date, say that area sits out rather than inventing a
substitute.

## The weekly review

[procedures/weekly-review.md](procedures/weekly-review.md) is the recurring pass that keeps
these files true. Follow it when I say it is review time. Do not run it unprompted, and do
not run half of it during ordinary work.

## Working with me

*Replace these with your own. They are examples of the kind of preference worth writing down
once instead of repeating in every session.*

- **Ask before assuming.** When context is missing, read the file or ask. Never fill a gap
  with a plausible default and build a plan on it.
- **Targets sit before deadlines.** "By X" is the outer bound. Plan the work with slack.
- **On a decision, give a recommendation**, not an exhaustive survey of options.

## Output

- Clean Markdown: headers, bold for key terms, tables for comparisons.
- When updating a document, make the edit directly. Do not describe what you would change.
- **Nothing is committed automatically.** Leave changes in the working tree for me to review
  unless I ask for a commit.
