---
name: weekly-review
description: "The weekly review: upkeep that keeps the workspace true (leftover work, the linter worked against reality, each installed skill's Weekly step), then the user's own planning rhythm, which puts the week's plan in the task home. Use when the user says it is review time, asks to plan the week, or asks what needs attention across the whole workspace. Never unprompted, and not for routine work inside one domain."
---

# The Weekly Review

Two jobs, kept apart. **Upkeep** is the same for everyone and keeps the files true. **The rhythm** is the user's own way of planning and reflecting, chosen at onboarding and written in [PROFILE.md](../../../PROFILE.md#weekly-rhythm), so this skill stays the same in every workspace. Upkeep runs first, because planning from stale files means planning against something that is no longer true.

**The linter is the agenda.** A domain being worked stays fresh, because work updates what it invalidates ([AGENTS.md](../../../AGENTS.md), rule 5). A quiet domain goes stale and the linter flags it. So the review never sweeps every domain: it works what is flagged, and nothing else.

## Upkeep

### 1. Leftover work

- **If the workspace has a remote of the user's own** (`git remote -v`; the upstream named on README.md's `Upstream:` line, the template this workspace was made from, does not count), pull first with `git pull --ff-only`, to pick up work from another machine. With no remote, skip this. With no git at all, skip this whole step.
- **A dirty tree is normal, not a blocker.** Work is committed by the user when it is done, never by the review.
- **Flag only stale dirty files:** uncommitted and untouched for a week or more. That is abandoned work rather than live work; ask whether to finish, commit or drop it.

### 2. Work the linter

`uv run .agents/scripts/workspace-lint.py`. Fix the errors. Then, for each warned file:

- **Read it and check it against reality**: the task home, the sources it was filled from, the user. **Do not just bump the date.** Bumping without verifying turns a stale file into one that looks fresh.
- Look for: Next Up items already done, blocked (name the blocker; if it is a person, the item is the unblock) or not actions at all; dates written as pending that have passed, or that belong in the task home ([CONVENTIONS.md](../../CONVENTIONS.md#dates)); facts stated in two places (the more specific file wins).
- Fix what rotted, then bump `last_reviewed`. If nothing rotted, say so and bump.
- **Stable by nature** rather than unreviewed: give it a longer `review_interval` instead of rereading it every fortnight.
- **Dormant and flagged:** archive it or wake it. Dormant is a holding state, not a graveyard.
- **Active but not moved in a month, with no trigger:** it is dormant. Say so.

### 3. Each skill's Weekly step

Read every `SKILL.md` in `.agents/skills/` and run each one's `## Weekly` section, if it has one. A skill declares its own weekly step there, so this list never needs editing when an add-on is moved in.

### 4. The task home

If the task home is TASKS.md, clear the ticked tasks and empty last week's This week section. In a task app, leave its own housekeeping to it.

### 5. The rhythm, after a few weeks

If the rhythm in PROFILE.md was chosen four or more weeks ago and has not been checked since, ask whether it is working: is the review getting done, and does the plan get followed? If not, the onboard skill's update mode swaps it. Note the answer under the rhythm, with the date, either way.

## The rhythm

Read the rhythm named in [PROFILE.md](../../../PROFILE.md#weekly-rhythm)'s "Weekly rhythm" section, and run its planning and reflection steps from its entry in [the rhythms reference](reference/rhythms.md). What PROFILE.md adds is the user's own: their day, steps they skip or add, and weekly steps of theirs that belong to no skill. Where the two differ, PROFILE.md wins.

Until one is chosen: read each active domain's Next Up, ask the user which one to three to do this week, and put them in the task home.

## Close

- Bump `last_reviewed` on everything actually verified, and nothing else.
- Say in a few lines what changed and what the week's plan is.
- Do not commit: the user reviews and commits ([AGENTS.md](../../../AGENTS.md#output)).
