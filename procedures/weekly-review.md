---
domain: Weekly Review
parent: procedures
status: active
review_interval: 90
last_reviewed: 2026-09-30
---

# The Weekly Review

**The recurring pass that keeps every other file true.** [AGENTS.md](../AGENTS.md) says how to
work, [CONVENTIONS.md](../CONVENTIONS.md) says how files are shaped, [COMPASS.md](../COMPASS.md)
ranks the areas. This keeps all three from going stale.

**The order matters.** Leftover work first, because reviewing uncommitted changes means
reviewing something nobody has agreed to. Domains before the Compass, because picking what to
do next requires knowing what actually moved. The Compass last, always.

Nothing here is fully automated on purpose. The linter catches shape; the rot that matters is a
sentence that is still grammatical and no longer true.

Ask your agent to walk through it with you. Budget thirty minutes.

## 1. Leftover work

- `git status` and read the diff. **Do not commit it unread.** Work left from a previous
  session is usually mid-thought, and the reason it was left is part of the review.

## 2. The automated pass

- `uv run scripts/workspace-lint.py`. Warnings are the agenda, not the verdict.
- **Dates in live files.** Dates to act on live in the task app, so a date in forward-looking
  language (deadline, due, before, next, target) inside a `CONTEXT.md` is either a task that was
  copied or one that was never created. Move it or delete it. A met deadline still written as
  pending reads exactly like an unmet one.
- **Claims that something is built.** A sentence saying software does something is the one kind
  of rot rereading never catches. A claim that something is built should name what implements
  it, so checking costs one search.

## 3. Freshness: verified, not touched

For every `active` file past its review interval:

- **Read it. Do not just bump the date.** Bumping without checking is worse than the warning,
  because it turns a stale file into one that looks fresh.
- If nothing rotted, say so and bump.
- If the file is stable by nature, give it a longer `review_interval` instead of rereading it
  every fortnight.

## 4. Cross-domain rot

Where the expensive mistakes live, because no tool sees them.

- **Anything finished or archived this week: search for it in prose, not just in links.** A
  link fix misses every mention that was never a link.
- **Anything decided this week: does another domain say the opposite?** A decision in one
  domain routinely invalidates a sentence in another.
- **Anything a decision rested on: is it still true?**

## 5. Per domain

A domain includes its projects in the task app, not just its folder.

- **Its dated tasks: still dated against something real?** A plan built around a launch that
  moved describes a plan nobody is following.
- **Its open tasks: is each one an action?** "Improve marketing" is a feeling with a due date.
  A task you cannot start without first deciding what it means is a decision in disguise.
- `CONTEXT.md` over 120 lines: move settled material to `DECISIONS.md`.
- Next Up items that are not actions, or are already done.
- Next Up items that are blocked: name the blocker. If it is a person, the item is the unblock.
- **Pending actions buried in closed decisions.** "Do X once Y lands" inside a closed entry is
  invisible. Lift X into Next Up.
- Facts stated in two places. The more specific file wins; fix the other.

## 6. Dormant and archived

- Every `dormant` domain: waiting on something real, or finished? Archive it or wake it.
- Anything `active` that has not moved in a month and has no trigger is dormant. Say so.

## 7. The Compass

Last, and only once the domains are true.

- **Done ONE Things:** replace them from that area's ladder.
- **Blocked ONE Things:** blocked on a person means the action is the unblock. Blocked on a date
  means the area sits out this week, said plainly.
- **Weekly rungs:** achieved ones get raised; a rung describing a habit that is already
  automatic is not pulling anything.
- **The scores:** re-rate them instead of carrying them forward.
- **Pick this week's one thing.** Not by score: closing windows first, then whether the next
  step is in your hands, then what is in season.

## 8. Close

- Bump `last_reviewed` on everything actually verified.
- Commit in small, coherent chunks.
