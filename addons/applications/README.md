# Add-on: Applications

For anyone applying to something with a deadline: internships, jobs, Master's programmes and scholarships, grants and fellowships, competitions, calls for papers.

**What it gives:**

- **cv-engine:** a CV built to PDF from a plain content file, tailored copies per application with a check that nothing was added, other languages, letters and interview stories, all cut from one record of experience.
- **opportunity-research:** finding offers with search and a browser, screening them against the user's limits, a tracker, a script that verifies every link and deadline, and a weekly watch of pages for new openings.
- **experience.md:** the one home for every fact about what the user has done. Every CV, letter and story is a cut of it.

**Where its files go:**

| From | To |
|---|---|
| `skills/cv-engine/` | `.agents/skills/cv-engine/`, linked from `.claude/skills/cv-engine` |
| `skills/opportunity-research/` | `.agents/skills/opportunity-research/`, linked from `.claude/skills/opportunity-research` |
| `experience.md` | `experience.md` at the workspace root, beside PROFILE.md |

The CV folder and the tracker are created in the user's applications domain during onboarding.

**Rows it adds to AGENTS.md's skills table:**

```markdown
| [cv-engine](.agents/skills/cv-engine/SKILL.md) | Anything about a CV, a letter or interview stories. Facts come from [experience.md](experience.md) |
| [opportunity-research](.agents/skills/opportunity-research/SKILL.md) | Finding, checking or tracking opportunities |
```

The skills need [uv](https://docs.astral.sh/uv/) and nothing else: the CV engine fetches its own Typst on first build, so build once while online.
