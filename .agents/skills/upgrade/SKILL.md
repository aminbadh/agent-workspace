---
name: upgrade
description: "Take the fixes and new versions the template has released since this workspace was made, file by file, without overwriting anything the user changed. Use when the user asks to upgrade or update the workspace, asks whether the template has changed, or when the weekly review reports that it has."
---

# Upgrade

The template this workspace was made from keeps improving: its skills, the linter, CONVENTIONS.md. This skill brings those changes in **one file at a time, with the user's yes**, and never touches their content (PROFILE.md, their domains, their answers in AGENTS.md).

The template's URL is on README.md's `Upstream:` line. What this workspace last received is `.agents/manifest.json`, which the template writes on every release. The script `scripts/upgrade.py` in this skill's folder compares the two; run it with `uv run`.

## 1. Plan

`uv run .agents/skills/upgrade/scripts/upgrade.py plan` fetches the template into a temporary folder and lists every file it changed since this workspace last took it, with what that means here:

| It says | Meaning | What to do |
|---|---|---|
| `update` | Only the template changed it | Offer it, with a one-line summary of the change |
| `new` | The template added it | Offer it, saying what it is |
| `conflict: both changed` | The user edited it too | Show the diff both ways and ask: take theirs, keep yours, or merge by hand |
| `removed upstream` | The template dropped it | Ask before removing; keep it if they still use it |

**Read each change before offering it** (`git diff --no-index <their file> <template copy>`), and say in plain words what it does for them. Never offer a batch as "updates available".

## 2. Apply

`uv run .agents/skills/upgrade/scripts/upgrade.py apply <path> ...` takes the template's version of the files the user agreed to. Give each file's template path: for an installed add-on, the path `plan` shows after "from". It saves each replaced file to a backup folder first and prints where. For a conflict they want merged, edit the file by hand instead, keeping both sides' intent, and show them the result.

Then, by hand:

- **A new skill:** link it for Claude Code (`ln -s ../../.agents/skills/<name> .claude/skills/<name>`) and add its row to AGENTS.md's skills table.
- **AGENTS.md:** it is the user's file, so it is never in the manifest. Compare the template copy's general sections (from "What this workspace is" through "What to do now", and "Output") with theirs, and offer any rule the template added or changed, one at a time. Their "Tasks", "Working with me" and "What the agent may do" stay theirs.
- **An add-on they have installed:** its files arrive through the same plan. A new add-on appears in `.agents/addons/`; mention it, and leave moving it in to the onboard skill.

## 3. Finish

`uv run .agents/skills/upgrade/scripts/upgrade.py finish` records the template's manifest as received, including for files they chose to keep as theirs (they have seen that version, so it is not offered again), and removes the temporary copy. Run the linter, say what changed in a few lines, and leave everything uncommitted for them to review.

## No manifest yet

A workspace made before the template shipped a manifest has no `.agents/manifest.json`. `plan` then treats nothing as received and lists every file that differs from the template, so the user looks at each once; `finish` writes the manifest, and later upgrades are file by file as above.

## Weekly

If README.md has no `Upstream:` line, skip this: the workspace has no template above it. Otherwise run `plan` and report in one line whether the template has anything new, naming the files. Do not apply anything in the review; the user says when.
