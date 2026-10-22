---
name: onboard
description: "Set up this workspace for its user by interviewing them: what they are here for, who they are, what they are working on and how the AI should work with them; then create their first domains, connect where their notes and tasks already live, choose a weekly rhythm, move in the add-ons that fit, and finish with one real task. Use when PROFILE.md is still the blank template, when the user wants to update their setup because something changed, or when they want to add an add-on."
---

# Onboarding

The first session decides whether the workspace makes sense to the user. They came for an outcome, not for a system, and they may never have used an AI this way. So: short, warm, plain words, and something real at the end.

**Three modes.** If [PROFILE.md](../../../PROFILE.md) still says "Blank template", run the full onboarding below. Otherwise run [update mode](#update-mode). If the user only wants an add-on, go straight to [moving an add-on in](#moving-an-add-on-in).

## Ground rules

- **A conversation, not a form.** Two or three questions per message. Follow up on vague answers ("data stuff": "analysing data, building dashboards, or something else?"). If they want to skip something, skip it and note it as unknown.
- **Save after every answer, not at the end.** A session can end at any moment, and the user should never have to answer twice. Write what each message told you into the right file before asking the next questions.
- **Never invent.** Write their words, not a plausible version of them. Mark anything they were unsure of "(to confirm)".
- **Search for the outside world** ([AGENTS.md](../../../AGENTS.md), rule 7): whether their task app has an MCP server, how to export from their notes app. Lead with the established route.
- **Get today's date from the machine** (`date +%Y-%m-%d`), never from memory.

## Before the first question

Say, in two or three sentences, in the language they wrote in:

- This folder is theirs, on their computer. The AI reads and writes its files; nothing is uploaded.
- A few questions now, about fifteen minutes, mean they never have to explain themselves again.
- At the end you will do one real thing for them with what they told you.

## 1. What are you here for?

Ask one open question: what do they want this workspace to help with? The answer picks the paths that run. Everyone gets the core (steps 2 to 7). Then:

- **Applying to something** (internships, jobs, a Master's, scholarships, grants, competitions): the [applications path](#the-applications-path).
- **Writing code**, for a project of their own or at work: the [building path](#the-building-path).
- Anything else: the core is enough. Offer the add-ons at step 7 only if something they said fits one.

## 2. Who they are

Ask who they are (name, what they do, where they are based, languages), what they are working on (the two to five big things), and **how they want the AI to work and write for them**: the language for replies, the tone (brief or detailed, formal or casual), and anything they want or never want in its writing (jargon, emoji, long lists, a phrase that annoys them).

Write it down:

- **PROFILE.md:** fill the fields from their answers. Add frontmatter at the top (`domain: Profile`, `parent: root`, `status: active`, `review_interval: 60`, `last_reviewed:` today) and remove the "Blank template" line, which is how AGENTS.md knows onboarding has run.
- **AGENTS.md, "Working with me":** replace the "Not set up yet" line with their preferences, as short bold-led bullets in the second person ("**Replies in French.** Code and file names stay in English."). Their writing rules go here and nowhere else.

## 3. Their first domains

Create a domain for each thing they are working on, rather than explaining the pattern and leaving it empty. Read [CONVENTIONS.md](../../../CONVENTIONS.md) first.

- **Place each one in an area of life**: a top-level folder such as `studies/`, `work/` or `personal/`, named in their words. One domain in an area can sit straight in the area folder's place (`studies/` as the domain itself). Two or more in one area: the area gets its own index `CONTEXT.md` with one row per child, as CONVENTIONS.md describes, and each child gets a folder inside it.
- **Write each from the templates** in [assets/](assets/CONTEXT.md): `CONTEXT.md` and `DECISIONS.md`. Fill the overview and current picture from what they said, and ask for what is missing: what is being done now, what is next, any hard limits, who matters. A domain they are not working on now is `dormant`.
- **No dates in domain files.** A deadline they mention goes to the task home once it exists (step 5); until then, note it and carry it over.
- Link each domain from PROFILE.md's "What I am working on".

## 4. Where things already live

Ask where their notes, documents and plans live today: a notes app, a folder of files, Notion, Google Docs, a paper notebook, their head.

- **What you can reach** (a folder on this computer, an app with a connected tool): read it, fill the domains from it, and link the source from each domain's Key Resources rather than copying everything in. Copy only what the domain needs to say what is true now.
- **What you cannot reach yet:** search for the way in (an MCP server or connector for the app, an export format, a sync to a folder) and offer it, with the steps. If they set it up now, read it and fill the domains; if not, note in PROFILE.md where it lives and that it is not connected.
- Record in PROFILE.md's Setup where their notes live.

## 5. Tools and the task home

- **Which AI tool** they use, written in PROFILE.md.
- **Whether you have a browser.** Check, do not assume: web search is not a browser. If a browser tool is listed, open one page with it. Write down what you actually have, so later work knows its limits.
- **Git.** If `git remote -v` shows the starter's own repository (`workspace-starter` on GitHub), say so: a weekly pull would pull the starter's changes into their workspace. Offer to remove that remote (`git remote remove origin`), or to point it at a private repository of their own. If the folder is not a git repository, offer `git init`, so every version of every file is kept; their choice.
- **Where tasks live.** Ask what they use for tasks and dates: an app (Todoist, Things, TickTick, Notion, Linear, a calendar), a file, paper, nothing.
  - **An app:** search whether it has an MCP server, a connector for their AI tool, or a command-line tool. If one exists and is connected, test it by listing a few of their tasks. If it exists but is not connected, give them the setup steps and offer to wait. Once it works, write AGENTS.md's "Tasks" section: the app, how the agent reaches it, the projects or lists that matter, how "done" and "this week" are marked. If no route exists, say so and suggest a TASKS.md instead.
  - **Anything else:** copy [the TASKS.md template](assets/TASKS.md) to the workspace root. If they already keep tasks in a file or a notebook, move the open ones into it (verb first, dates kept) with their agreement, so there is one list, not two. Then write AGENTS.md's "Tasks" section: `Tasks live in [TASKS.md](TASKS.md).`, with one line on how it is used.
  - Either way, replace the "Not set up yet" line, then move any deadline noted in step 3 into the task home.

## 6. A weekly rhythm

The [weekly-review skill](../weekly-review/SKILL.md) does the same upkeep for everyone; the planning and reflection part is theirs to choose.

1. Ask about their habits, using the questions at the top of [the rhythms reference](../weekly-review/reference/rhythms.md): do they plan now and how, which day suits a review and how long, numbers or not, one big goal or several areas.
2. Suggest one or two methods from the reference that fit, with a line each on why. If they name a method that is not there, search for it and write its steps in the same shape. If they want none, leave it: the review falls back to each domain's Next Up.
3. Write the chosen method into the weekly-review skill's "The rhythm" section, replacing the "Not chosen yet" text: its name and today's date as a line, its planning steps, its reflection steps, and where its plan lives. Keep it to what they will actually do.
4. **The Compass** also installs [COMPASS.md](../weekly-review/assets/COMPASS.md) at the root: show the life areas from the reference, let them pick, rename and merge, write one section per area, and fill the ladders with them, marking anything you suggested *(proposed)*. Scores stay off for a first setup.

## 7. Add-ons

Each folder in [addons/](../../../addons/README.md) is an add-on, with a README saying what it gives. Offer the ones their answers point to, in one line each, and move in the ones they pick (see [moving an add-on in](#moving-an-add-on-in)). Never move one in unasked. Then run its path below.

### The applications path

When they are applying to something. Move the **applications** add-on in, then:

1. **What they want:** the type (internship, end-of-studies internship, job, Master's, scholarship, grant, competition), when it starts and for how long, where, and two or three fields or role families. For a type with school or funder rules (an internship's length, a scholarship's eligibility), ask what they know, then read the opportunity-research skill's guide.
2. **Hard limits:** anything that rules an offer out (a place they cannot go, a language they cannot work in, a minimum stipend or funding level, constraints they choose to share).
3. **Languages,** honestly rated: native, fluent, working, basic.
4. **Their experience.** Ask for an existing CV first: a file in the folder, a PDF, a Word document, pasted text, or a LinkedIn profile saved as PDF. Read it. Then go section by section (education, work, projects, clubs and volunteering, awards, skills) asking for **what they did and what came of it**, with numbers where they exist. Most people undersell: "I helped with events" often hides "ran a 200-person event". Ask once, kindly, for the result. Write every fact into experience.md under its heading, newest first.
5. **Where it lives:** the criteria from 1 to 3 go in PROFILE.md under a new "## What I am looking for" section, where the opportunity-research skill reads them. Create an applications domain (for example `career/` or `studies/applications/`) in step 3's shape, whose Constraints link to that section rather than restating it. The tracker is the task home if it is an app that can hold rows with fields, otherwise `opportunities.csv` in the domain folder; name it in the domain's Key Resources.
6. **What to watch:** ask which careers pages, catalogues or programme pages they want watched for new openings. If they name some, start `sources.json` beside the tracker from the opportunity-research skill's [example](../opportunity-research/assets/sources.example.json), with one entry per page, and run `watch` once to record the baseline. If they decline, say plainly that the weekly watch is off until they add a page, and that they can say "watch this page" any time.
7. **First CV:** use the cv-engine skill to start the CV folder at `cv/` inside the applications domain, write the main CV from experience.md, build it and look at the page image. Ask whether they want another language.
8. Show them experience.md and the CV, and ask them to correct anything wrong now.

### The building path

When they write code. Move the **building** add-on in, then ask which code repositories the workspace plans for, and give each one a domain in step 3's shape (the domain holds the reasoning; the repo holds the code). Then offer BUILDING.md's "Paths across machines", since builders reach their briefs through `~/.links/workspace`. **It changes their home folder, so nothing is created without a yes:**

1. Explain in two lines what it creates: a hidden `~/.links` folder holding two links, one to this workspace and one to the folder holding their code repos.
2. Ask where their code repos live. Do not guess a folder.
3. Check what is already there (`ls -la ~/.links`). If a link exists and points elsewhere, say where, and ask before changing it.
4. Only once they agree, run the commands from BUILDING.md with their folder, and show the result with `ls -la ~/.links`. If they decline, say that briefs then need full paths on this machine, and move on.

Then walk through "Setting up a repo" with them for the first one.

## 8. One real thing

Finish with a task that matches what they came for, using what they just told you, and point out that you did not need to ask anything again. Pick from what they said:

- **Applications:** find two or three real offers that fit with the opportunity-research skill, record and verify them; or tailor the CV to an offer they already have in mind.
- **A domain with a clear next step:** do it, or draft it (an email, a plan, a summary of the notes you read).
- **"What should I do now?":** run the one-thing skill.
- **Building:** write the first brief for their repo, as BUILDING.md describes.

## 9. Close

Run `uv run scripts/workspace-lint.py` and fix anything it reports. Then end with a few lines:

- what was created and where (their domains, the task home, the rhythm, any add-on);
- two or three things they can say next time ("what should I do now?", "it's review time", something from their add-on);
- that they can update their setup any time by saying what changed.

Do not commit: they review and commit ([AGENTS.md](../../../AGENTS.md#output)).

## Update mode

When PROFILE.md is already filled in, do not re-run the interview. Ask what changed (a new goal, a finished project, a move, a new tool), and update only what it touches: PROFILE.md, the domains (a new one, one gone dormant, one to archive), AGENTS.md's "Tasks" or "Working with me", experience.md and the CV if their facts changed. Bump `last_reviewed` on what you verified.

- **The rhythm, after a few weeks:** if the weekly review reports that the rhythm is not working, ask what got in the way, suggest another from the reference, and replace the rhythm section with it. Installing or removing the Compass follows step 6.
- **A new add-on:** offer it if what changed points to one, and move it in as below.

## Moving an add-on in

An add-on's README says what it gives, where each of its files goes, and the row it adds to AGENTS.md's skills table. To move one in:

1. **Its skills:** move each folder in the add-on's `skills/` into `.agents/skills/` (with `git mv` if the folder is a git repository).
2. **The Claude Code links:** for each skill, `ln -s ../../.agents/skills/<name> .claude/skills/<name>`, then `ls -la .claude/skills` to check every link resolves. On a system where links fail (some Windows setups), copy the folder instead and say so.
3. **Its files:** move each to where its README says.
4. **AGENTS.md:** add its row or rows to the skills table.
5. **Remove the add-on's now-empty folder**, README included, so [addons/](../../../addons/README.md) holds only what is not yet installed. The folder itself stays, so another add-on can be added later.
6. Run `uv run scripts/workspace-lint.py`.
