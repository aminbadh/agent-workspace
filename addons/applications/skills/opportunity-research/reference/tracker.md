# The Tracker

One row per opportunity. A CSV file by default, which opens in Excel, LibreOffice or Google Sheets. When the workspace already tracks opportunities in an app (Notion, Airtable, a spreadsheet), the rows go there instead, with the same fields.

## Fields

| Field | What goes in it |
|---|---|
| `added` | Set by the script: the day the row was added |
| `org` | The employer or institution, by its usual name |
| `role` | The role or programme title, as posted |
| `location` | City and country, or "Remote" |
| `start` | When it starts, as posted: "Feb 2027", "Sep 2027" |
| `duration` | "6 months", "2 years" |
| `deadline` | `YYYY-MM-DD`, `rolling`, or `unknown`. Never a guess |
| `deadline_source` | The page that states the deadline. Required for a dated deadline |
| `url` | The offer on the employer's or programme's own site |
| `found_via` | Where it was found: "LinkedIn", "Keejob", "a friend at the company" |
| `fit` | `high`, `medium` or `low` |
| `why` | The fit in a few checkable words |
| `status` | `to review`, `applying`, `applied`, `interview`, `offer`, `rejected`, `closed`, `not a fit` |
| `notes` | Anything else: a contact, an assessment, a referral |

## In a CSV

`add` appends a row, refuses one without a real link or with an unsourced date, and skips an offer already tracked. Change a status by editing the file, or ask the agent to.

## In an app

Find the tracker the workspace names (its AGENTS.md, a domain's CONTEXT.md, or a file describing the app). Read a few existing rows first and match their fields and wording rather than imposing these names. Write rows with the app's own tool. Then verify them by passing the open rows as JSON, one object per row with these field names:

```
echo '[{"org": "...", "role": "...", "url": "...", "deadline": "...",
        "deadline_source": "...", "status": "..."}]' | uv run <skill>/scripts/opps.py verify --json -
```
