---
name: cv-engine
description: "Create, update, tailor, translate and restyle a CV or résumé, built to PDF from a plain YAML content file and a Typst template, with nothing to install beyond uv; write motivation and cover letters and interview stories from the same facts. Use when the user wants to make or edit a CV, tailor one to a job, internship or programme, make a version in another language, change how it looks, get it to fit one page, write a motivation or cover letter, or prepare stories for an interview."
metadata:
  status: active
  review_interval: 90
  last_reviewed: 2026-10-21
---

# CV Engine

A CV here is two files: **content** (a YAML file of facts, one per version) and **look** (`template.typ`, shared by every version). The script `scripts/cv.py`, in this skill's folder, builds content into a PDF and reports whether it fits its page limit. Run it with `uv run`; it fetches its own pinned Typst, so nothing else needs installing.

```
cv/
├── cv.en.yaml          the main CV
├── cv.fr.yaml          another language, when needed
├── template.typ        the look: theirs to restyle
├── fonts/              extra fonts, if the look needs them
├── applications/       one tailored copy per application, YYYY-MM-org-role.yaml
└── out/                built PDFs, never edited by hand
```

## Ground rules

- **Never invent a fact.** Every title, date, number and result comes from the user or from where their workspace records experience: `experience.md` by default, or the log or profile the workspace names. That record is the one home for facts, and the main CV, each tailored CV, every letter and every interview story is a cut of it. Ask for a missing number rather than estimating one, and write a new fact there first, so no CV or letter is the only place it lives.
- **Look before saying done.** Build with `--png` and view the page image after any change to the look, and before handing over a CV that will be sent.
- **The user's template is theirs.** Never overwrite `template.typ` with the default once it exists. `init` refuses to.

## Starting a CV

1. Ask where the CV folder should live. Default: `cv/` in the area of the workspace that holds applications.
2. `uv run <skill>/scripts/cv.py init <folder>` copies the template and an example.
3. Replace the example with the user's facts, following [the content format](reference/content-format.md) and [the writing guide](reference/writing.md). Interview for what is missing: results, numbers, dates.
4. Build, view the page image, and fix until it fits.

An existing CV in another format (Word, HTML, a PDF) is a source of facts: copy them into the YAML, then build. Do not try to reproduce its layout unless the user asks for that look.

## Building

```
uv run <skill>/scripts/cv.py build cv/cv.en.yaml            # the PDF
uv run <skill>/scripts/cv.py build --png cv/cv.en.yaml      # plus page images to look at
```

Each build prints the page count against `max_pages`. When it runs over, cut in this order: weakest bullets, then older or less relevant entries, then wordy phrasing. Shrinking the text or margins in the template is the last resort, and only with the user's agreement, since it changes every version.

## Tailoring to an application

1. Read the posting. Note the role's title, the skills and tools it screens for, and its language.
2. Copy the main CV to `applications/YYYY-MM-org-role.yaml`, with the year and month from today's date (run `date +%Y-%m`; do not guess it). It is a snapshot of what was sent, so it is allowed to differ from the main CV.
3. Reorder entries and skill items so the most relevant come first, and pick the bullets that prove what the posting asks for. Keep Education first for students and graduates (see [the writing guide](reference/writing.md)). Use the posting's wording only where it is true. **A skill or result the posting wants and the user does not have stays out**: say so to the user instead.
4. Set `headline` to what this application is for.
5. Build it, then, from the CV folder, run the check against the main CV: `uv run <skill>/scripts/cv.py check applications/<name>.yaml cv.en.yaml`. It lists every line of the cut that the main CV does not contain.
6. Give the user the PDF path, a short list of what changed, and **the check's output word for word**. Each line it lists is a claim the user must confirm is true before sending. Never summarise it away or call the cut "nothing new" yourself.

## Letters

A motivation letter, cover letter or statement is written from the same facts as the CV.

1. Read the offer, and **what the application asks of the letter**: its length (words, characters or pages), the questions it must answer, its language. A form's limits win over any habit.
2. Save it beside the tailored CV as `applications/YYYY-MM-org-role.letter.md`, or where the workspace keeps that application's documents. One paragraph per line, so it pastes cleanly into a form or an email.
3. Write from the experience record and the offer only: why this, what they bring (two or three results that prove what the offer asks for), and why now. Specific beats eloquent. Follow [the writing guide](reference/writing.md#letters).
4. **Check its claims.** No script can compare prose with the record, so do it by hand and show the result: list every factual claim in the letter (a role, a number, a result, a skill) beside the line of the experience record it rests on. A claim with no line is marked `NOT IN RECORD`. Give the user that list word for word; each marked claim is theirs to confirm, add to the record, or cut before sending.
5. Give the user the file path, the word or character count against the limit, and the claims list.

## Interview stories

A short bank of stories for the questions interviews keep asking. Start it when the first interview is booked, not before: the interview says which stories matter.

1. Keep it beside the experience record as `stories.md`, so every application reuses it.
2. Six to ten stories, each from the experience record only, in four lines: the situation, what they had to do, what they did, and what came of it (with its number). Tag each with the questions it answers: a project they are proud of, a failure, a conflict, leading without authority, a hard deadline, why this field.
3. Before each interview, pick the three or four stories that best prove what the role or programme asks for, and rehearse them out loud with the user: short, specific, and theirs. Add the questions that came up afterwards, so the bank grows.

## Another language

Copy to `cv.fr.yaml` (or the language's code), set `lang`, and translate section titles, roles and bullets. Keep names of organisations, schools and products as they are. Dates follow the language's convention ("juin – août 2026").

## Changing the look

Most changes are the "Look" block at the top of `template.typ`: font, size, colours, margins, spacing. For anything beyond that, read [the Typst cheat-sheet](reference/typst-cheatsheet.md) first. Build with `--png` after each change and look at it. A new font needs its .ttf files in `fonts/`; system fonts are ignored on purpose so the CV renders the same on every machine.
