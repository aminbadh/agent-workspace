# CV Content Format

One YAML file per version of the CV: `cv.en.yaml`, `cv.fr.yaml`, and one per application in `applications/`. The template reads every field below; anything else is ignored.

## Top level

| Field | Required | What it is |
|---|---|---|
| `name` | yes | The person's name, the title of the page |
| `headline` | no | One line under the name: who they are and what they are looking for |
| `contact` | no | A list. Each item is plain text, or `text:` plus `url:` to make it a link |
| `lang` | no | `en` (default), `fr`, `de`... Sets hyphenation and quotation marks |
| `paper` | no | `a4` (default) or `us-letter` |
| `max_pages` | no | Default 1. The build reports when the CV runs longer |
| `sections` | yes | The body, in the order it prints |

## A section

Every section has a `title` and any of these, printed in this order:

- `text`: a paragraph, for a summary or profile.
- `entries`: a list of jobs, degrees, projects or roles. Each entry:

| Field | What it is |
|---|---|
| `title` | Organisation, school or project name, in bold. Required |
| `role` | Job title or degree, in italics after the title |
| `url` | Makes the title a link |
| `date` | Right-aligned, written as it should appear: `Jun – Aug 2026`, `2023 – 2027` |
| `place` | City, country, or "Remote", on the line below |
| `note` | A short grey aside after the place, such as "part-time" |
| `bullets` | The results, one per line |

- `lines`: label and text pairs, for skills, languages or certifications. Each has `label` and `text`.

## Text

- Text prints exactly as written, so `C#`, `$`, `@` and `%` need no escaping.
- Wrap words in `*stars*` to make them bold, and write a link as `[label](https://...)`. Nothing else is formatted. Straight apostrophes print as typographic ones.
- Quote a value that contains a colon followed by a space, or starts with a special character: `- "Relevant courses: statistics, databases"`.
- Numbers such as a bare year are fine unquoted.
