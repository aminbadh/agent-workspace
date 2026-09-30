#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Check the workspace for the failure modes that mislead agents.

Rot in a workspace like this is never loud. A replaced deadline reads exactly like a current
one, so this script makes staleness and contradiction visible without anyone having to
remember to look. The rules it enforces are written out in CONVENTIONS.md.

Usage:  uv run scripts/workspace-lint.py [--quiet]
        (or: python3 scripts/workspace-lint.py, with Python 3.11 or newer)
Exit:   0 if clean or warnings only, 1 if any error was found.
"""
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date.today()
STALE_DAYS = 14            # default review interval; a file can declare its own
MAX_CONTEXT_LINES = 120    # CONVENTIONS.md aims for 100 and warns here
VALID_STATUS = {"active", "dormant", "archived"}

# Folders rewritten by their own tooling. Linting them produces notes nobody can act on.
SKIP = (".claude/", ".agents/", ".cursor/", "node_modules/")

errors, warnings, notes = [], [], []


def markdown_files():
    """Every Markdown file git knows about or would add: tracked plus untracked, minus
    anything .gitignore excludes. Falls back to a plain walk outside a git repository."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        files = [ROOT / f for f in out.split("\0") if f]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = [p for p in ROOT.rglob("*") if ".git" not in p.parts]
    return sorted({f for f in files
                   if f.suffix == ".md" and f.exists()
                   and not rel(f).startswith(SKIP)}, key=rel)


def rel(p):
    return p.relative_to(ROOT).as_posix()


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def archived(p):
    return rel(p).startswith(".archive/")


FILES = markdown_files()
CONTEXTS = [p for p in FILES if p.name == "CONTEXT.md"]
LIVE = [p for p in CONTEXTS if not archived(p)]

# Every live CONTEXT.md is checked and must carry frontmatter. Any other file opts in by
# carrying frontmatter itself, so this script never keeps a list of exceptions.
REVIEWED = LIVE + [p for p in FILES
                   if p not in LIVE and not archived(p)
                   and p.read_text().startswith("---\n")]

# --- 1. frontmatter, status, freshness ---------------------------------------
for p in REVIEWED:
    text = p.read_text()
    fm = frontmatter(text)
    if fm is None:
        errors.append(f"{rel(p)}: no frontmatter (see CONVENTIONS.md, Frontmatter)")
        continue
    status = fm.get("status")
    if status not in VALID_STATUS:
        errors.append(f"{rel(p)}: status is {status!r}, expected one of {sorted(VALID_STATUS)}")

    raw = fm.get("last_reviewed")
    try:
        reviewed = dt.date.fromisoformat(raw)
    except (TypeError, ValueError):
        errors.append(f"{rel(p)}: last_reviewed is {raw!r}, expected YYYY-MM-DD")
        continue
    interval = STALE_DAYS
    if "review_interval" in fm:
        try:
            interval = int(fm["review_interval"])
            if interval < 1:
                raise ValueError
        except ValueError:
            errors.append(f"{rel(p)}: review_interval is {fm['review_interval']!r}, "
                          f"expected a positive whole number of days")
            interval = STALE_DAYS
    age = (TODAY - reviewed).days
    if age < 0:
        errors.append(f"{rel(p)}: last_reviewed {raw} is in the future")
    elif status == "active" and age > interval:
        detail = "" if interval == STALE_DAYS else f", its interval is {interval}"
        warnings.append(f"{rel(p)}: active but last verified {age} days ago ({raw}{detail}). "
                        f"Read it, fix what rotted, then bump the date")
    if p.name == "CONTEXT.md":
        n = len(text.splitlines())
        if n > MAX_CONTEXT_LINES:
            warnings.append(f"{rel(p)}: {n} lines, over the {MAX_CONTEXT_LINES}-line limit. "
                            f"Move settled material to DECISIONS.md")

# --- 2. `parent` must name the folder the file actually sits in ---------------
# Nothing else reads `parent`, so a file moved between folders keeps a wrong one forever.
for p in REVIEWED:
    fm = frontmatter(p.read_text())
    if not fm or "parent" not in fm:
        continue
    folder = p.parent if p.name != "CONTEXT.md" else p.parent.parent
    expected = "root" if folder == ROOT else folder.name
    if fm["parent"] != expected:
        errors.append(f"{rel(p)}: parent is {fm['parent']!r} but the file sits in "
                      f"{expected!r}. Moving a file does not update its frontmatter")

# --- 3. archived files must say so --------------------------------------------
for p in CONTEXTS:
    if archived(p):
        fm = frontmatter(p.read_text()) or {}
        if fm.get("status") != "archived":
            errors.append(f"{rel(p)}: under .archive/ but status is {fm.get('status')!r}")

# --- 4. broken links, and live links into the archive -------------------------
LINK = re.compile(r'\[[^\]]*\]\(([^)#]+?)\)')
CODE = re.compile(r'```.*?```|`[^`]*`', re.S)
for p in FILES:
    if archived(p):
        continue
    for target in LINK.findall(CODE.sub("", p.read_text())):   # code spans are examples
        if re.match(r'^(https?:|mailto:|#)', target):
            continue
        dest = p.parent / target
        if not dest.exists():
            errors.append(f"{rel(p)}: link points at nothing: {target}")
        elif (ROOT / ".archive") in dest.resolve().parents:
            warnings.append(f"{rel(p)}: links into .archive/ ({target}). Nothing active links "
                            f"there: unarchive what is still needed, or drop the link")

# --- 5. index files must not restate their children's dates -------------------
# An index is a CONTEXT.md with at least one live CONTEXT.md beneath it.
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE = re.compile(rf'\b(?:\d{{4}}-\d{{2}}-\d{{2}}|\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}}'
                  rf'|(?:{MONTHS})\s+\d{{1,2}},\s+\d{{4}})\b')
for p in LIVE:
    if not any(c != p and c.is_relative_to(p.parent) for c in LIVE):
        continue
    body = p.read_text()
    end = body.find("\n---\n", 3)
    found = sorted(set(DATE.findall(body[end + 5:] if end != -1 else body)))
    if found:
        warnings.append(f"{rel(p)}: index file carries date(s) that likely belong to a child: "
                        f"{', '.join(found[:4])}. Link instead of restating")

# --- 6. wikilinks, which only Obsidian resolves --------------------------------
WIKI = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]')
for p in FILES:
    if archived(p):
        continue
    for target in set(WIKI.findall(CODE.sub("", p.read_text()))):
        warnings.append(f"{rel(p)}: [[{target}]] is an Obsidian wikilink. Use a Markdown link "
                        f"so other tools and this linter can follow it")

# --- 7. real files written as code, which nothing can check -------------------
BACKTICK = re.compile(r'`([A-Za-z0-9._][A-Za-z0-9._/-]*\.(?:md|pdf|docx|pptx))`')
GENERIC = {"CONTEXT.md", "DECISIONS.md", "AGENTS.md", "CLAUDE.md", "CONVENTIONS.md",
           "README.md", "TASKS.md", "COMPASS.md"}
for p in FILES:
    if archived(p) or p.name in ("CONVENTIONS.md", "AGENTS.md", "README.md"):
        continue
    for m in set(BACKTICK.findall(p.read_text())):
        if m not in GENERIC and ((p.parent / m).exists() or (ROOT / m).exists()):
            notes.append(f"{rel(p)}: `{m}` is a real file written as code. Make it a link")

# --- report --------------------------------------------------------------------
quiet = "--quiet" in sys.argv
for label, items, colour in (("ERROR", errors, "31"), ("WARN", warnings, "33"),
                             ("NOTE", notes, "36")):
    if not items or (quiet and label == "NOTE"):
        continue
    print(f"\n\033[{colour}m{label}\033[0m ({len(items)})")
    for i in items:
        print(f"  {i}")

if not (errors or warnings or notes):
    print(f"\033[32mClean.\033[0m {len(LIVE)} live domain(s), "
          f"{len(CONTEXTS) - len(LIVE)} archived.")
else:
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s), {len(notes)} note(s) "
          f"across {len(LIVE)} live domain(s).")
sys.exit(1 if errors else 0)
