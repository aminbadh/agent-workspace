---
name: opportunity-research
description: "Find, screen and track opportunities with a deadline (internships, jobs, funded Master's programmes and scholarships, grants and fellowships, competitions and hackathons, calls for papers or speakers) using web search and a browser, record them in a tracker, verify every link and deadline with a script, and watch sources for new offers. Use when the user wants to find opportunities, check whether one fits, add them to their tracker, check their tracker is still accurate, or watch pages for openings."
---

# Opportunity Research

Find offers that fit the user, record them, and prove each one is real. The model searches and judges; the script `scripts/opps.py` in this skill's folder checks what a model cannot be trusted to grade itself. Run it with `uv run`; it needs nothing else installed.

| Guide | Read it for |
|---|---|
| [guide.md](reference/guide.md) | Any opportunity: criteria, local guides, sources, screening, watching |
| [tracker.md](reference/tracker.md) | The tracker's fields, and using an app instead of a CSV |

**Local guides** hold what differs by country, school or field: the boards a country uses, a school's rules. Look for one in the workspace first (the domain's CONTEXT.md links it). When the search needs one and none exists, write it as [the guide](reference/guide.md#local-guides) describes.

## Ground rules

- **Never invent a fact.** Every row's link is a page you opened. A deadline is copied from a page and that page is recorded; otherwise it is `unknown`.
- **Read only.** Never apply, submit a form, message anyone or log in on the user's behalf. A browser is for reading pages the user can already see.
- **Verify before reporting.** Run `verify` after adding rows and show the user its flags word for word. Never describe a flagged row as confirmed.

## 1. Criteria

Read the user's profile, [the guide](reference/guide.md) and any local guide that applies. If criteria are missing (dates, places, role families, languages, hard limits), ask for them once and write them into the profile, so the next search does not ask again.

## 2. Find

Use every tool available, best first:

1. **Web search** for postings and programme pages, with the patterns in the guide.
2. **A browser tool**, when one is connected (Claude in Chrome, Codex's browser, a Playwright server): for LinkedIn, many national job boards and other sites that block scripts, and for careers pages that only render in a browser. Use the user's existing session; read, do not act. When a site asks to sign in, stop and ask the user to sign in themselves in that browser; never enter credentials. From a list of results, find each promising offer's own page on the employer's site rather than reading every posting inside the board.
3. **What the user pastes**: a link, a screenshot, or the text of a posting. This always works, whatever tools are missing, and is enough on its own.

Always end on the employer's or programme's own page, and record that page, not the board where it was found.

**Cover the sources before concluding.** Work through the guide's sources, not just the first search results. A repost on a third-party site is a lead: look for the employer's own page before dropping it. When fewer offers turn up than the user asked for, say so plainly and report the coverage: which sources were searched, which could not be read without a browser, and any leads the user can confirm themselves. Fewer real offers beats padding the list.

## 3. Screen

Judge each offer against the criteria with the guide's rules. Drop anything that fails a hard limit and tell the user in one line why. Rate the rest `high`, `medium` or `low`, with a short checkable reason.

## 4. Record

Find the tracker: the one the workspace names, or `opportunities.csv` beside the user's applications if there is none. For a CSV:

```
uv run <skill>/scripts/opps.py add <tracker.csv> --org "Criteo" --role "BI Analyst Intern" \
  --url https://... --location "Barcelona" --start "Feb 2027" --duration "6 months" \
  --deadline unknown --found-via "LinkedIn" --fit high --why "dates fit, names Business Analytics"
```

For an app, see [tracker.md](reference/tracker.md).

## 5. Verify

```
uv run <skill>/scripts/opps.py verify <tracker.csv>
```

It opens every open row and flags: a dead or missing page, a page that does not name the organisation, an offer marked closed, an aggregator link, a deadline that is past, unsourced, or absent from its source page, and sites it cannot read (`BLOCKED`, `UNCHECKED`). Fix what you can: replace aggregator links, open blocked pages in a browser and confirm them, set closed offers to `closed`. Show the user the rest.

## 6. Watch

For pages that will change (a careers page, a catalogue, a programme with no dates yet), add an entry to a sources file beside the tracker, following [the example](assets/sources.example.json), then:

```
uv run <skill>/scripts/opps.py watch <sources.json>
```

The first run records a baseline. Later runs report links or dates that appeared or vanished. It runs every week through the Weekly section below.

## 7. Apply

When the user picks an offer, hand it to the cv-engine skill to tailor a CV, and set the row's status as the application moves.

## Weekly

Run in the user's weekly review. Read only, as everywhere in this skill.

1. **Watch:** run `watch` on each sources file the workspace keeps beside its trackers. Report what appeared or vanished, and add or update rows for anything new.
2. **Waiting for a reply:** list rows at `applied`, oldest first, with how long each has waited (from `added` and its notes). Whether to follow up is the user's call; never message anyone.
3. **Replies, when the workspace has email access** (an MCP server, a connector or a CLI): read messages from the organisations with open rows since the last review, and propose each status change (`interview`, `rejected`, `offer`) with the message it rests on. Update the tracker once the user agrees. Never reply, archive or label.
4. **Closing soon:** list rows at `to review` or `applying` whose deadline falls in the next two weeks.
