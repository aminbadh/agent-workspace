# Finding and Judging Opportunities

How to find, screen and watch any opportunity with a deadline: internships, jobs, Master's programmes and scholarships, grants and fellowships, competitions and hackathons, calls for papers or speakers. They share one pattern: an official page, an eligibility rule, a window that opens and closes. The sections below cover that pattern once, with notes where a type differs.

## Criteria to settle first

Write these into the user's profile before searching, so every screen uses the same rules and the next search does not ask again:

- **The window:** when they can start or submit, and for how long they are available.
- **Places:** cities or countries, and whether remote counts.
- **Fields:** two or three families (for example data analysis, marketing analytics, product), not one exact title.
- **Languages** they can work or study in, honestly rated, and any tests they hold.
- **Eligibility facts** that offers screen on: nationality and residence, degree and year of study, career stage.
- **Hard limits:** anything that rules an offer out before it is read (a place they cannot go, a minimum stipend or funding level, paperwork their school or visa requires).

| Type | Also settle |
|---|---|
| Internship | Type (end-of-studies, summer, either) and the minimum and maximum length the school allows |
| Job | Contract type, seniority, salary floor if they have one |
| Master's or scholarship | Funding need: full (tuition and living costs), tuition only, or self-funded. Intake year and the degree held by then. Visa risk per country, in their own judgement |
| Grant or fellowship | What it would fund, and whether they apply alone, with a team or through an organisation |
| Competition or hackathon | Solo or team, online or on site, and whether travel is possible |
| Call for papers or speakers | Topics they can speak or write on, and whether they can travel or pay a fee |

## Local guides

Where to look and how things work differ by country, school and field: the job boards a country uses, a school's internship rules, a field's usual venues. When a search needs that knowledge and the workspace has no guide for it, **build one with the tools you have**: search for the country's boards and groups, read the school's official rules, try each source in a browser to see whether it can be read. Write what you found as a short guide in the workspace, where that domain's knowledge lives, with a source for each rule, and link it from that domain's CONTEXT.md. Read it on every later search instead of rediscovering it. A guide holds where to look and how it works, never the offers themselves: those go in the tracker.

## Where opportunities are

**The official page is always the row's link:** the employer's careers page, the programme's or funder's own page, the organiser's call. Everything else is a way of finding it.

| Type | Good sources |
|---|---|
| Internships and jobs | Company careers pages; LinkedIn Jobs (blocks scripts: in a browser, search results show signed out, add `&f_JT=I` to the search URL for internships only, and opening a posting needs the user signed in); the country's own boards (see the local guide); large companies' early-careers pages, whose windows open months ahead and close early; the school's career office, which is not on the web, so ask |
| Master's and scholarships | **Official catalogues are the source**, because the funder keeps the list: the [Erasmus Mundus catalogue](https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en) (it also lists programmes whose funding has ended, so confirm on each consortium's site), the [DAAD database](https://www2.daad.de/deutschland/stipendium/datenbank/en/21148-scholarship-database/) (passing its country filter means "not obviously excluded", not "eligible"), and country portals such as Campus France, Study in Japan and Study in Korea |
| Grants and fellowships | The funder's own call page; national research and arts councils; foundations in the field. Many repeat yearly at about the same time |
| Competitions and hackathons | The organiser's page; university and community event listings; platforms such as Devpost or Kaggle for technical ones |
| Calls for papers or speakers | The conference's own call page; field mailing lists; aggregators such as WikiCFP or Sessionize for discovery |
| Any type | **Warm leads:** people the user knows. Often the fastest route; record who in `found_via` |

**Aggregators give names only.** Indeed, Glassdoor, MastersPortal, ScholarshipPortal, opportunity channels on Telegram or Facebook, and similar: fine for discovering that something exists, never the fact. Find the official page and record that.

## Search patterns

Combine a field, the type and a place or year, in the language of the place:

- `"business analyst intern" 6 months 2027 Barcelona`
- `"stage de fin d'études" data analyst Paris 2027`
- `"fully funded" master data science 2027 scholarship`
- `site:careers.<company>.com intern 2027`

Search organisations the user already admires by name, not only by keyword.

## Screening

Read the official page itself, then rate the fit:

- **high:** the window, place, language and eligibility all fit, and it matches a field family.
- **medium:** one soft mismatch, such as a start a few weeks off or a stretch on eligibility.
- **low:** worth keeping only for a reason the user gave.
- **Fails a hard limit:** do not add it. Tell the user in one line why it was skipped, so it is not screened twice.

Write the reason in `why`, in a few words the user can check: "dates fit, names Business Analytics", not "great fit".

| Type | Also check on the official page |
|---|---|
| Internship | Whether the role is open to their year of study, and whether the company will sign the school's agreement |
| Master's or scholarship | What the funding covers, for how long and whether it renews (count what is left to pay); eligibility (degree, grades, language scores); documents that take weeks (referees, translations, certified copies) |
| Grant or fellowship | What it funds and what it does not; reporting duties; whether an institution must apply for them |
| Competition or hackathon | Who owns what is built; team rules; prizes and what they depend on |
| Call for papers or speakers | Format and length; fees, travel support, and whether talks are recorded |

A page with no published window gets `deadline: unknown` and a watch entry, never a guessed date.

## Red flags

- Asking for money to apply, train or "secure" a place (a conference registration fee is not this; a fee to be considered usually is).
- No organisation name, or a free email address as the only contact.
- A role or call described only in buzzwords, with no team, task or criteria.
- A deadline that appears nowhere on the official pages.

## Watching

Official pages change without notice when a window opens. Add a `dates` watch for each page whose dates are unpublished, and a `links` watch for any listing or catalogue already swept, so new entries surface. The format is in [the example](../assets/sources.example.json).
