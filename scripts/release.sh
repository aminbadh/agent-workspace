#!/usr/bin/env bash
# For the maintainer, not for users. Release the generic files from the workspace where they are
# developed and used: the core skills, the applications add-on's skills, the linter, the spec,
# BUILDING.md and the add-ons index. That workspace is their home; these are released copies,
# word for word apart from review dates, so the starter works on its own. Never edit them here.
# Run it, review the diff, commit.
#
#   ./scripts/release.sh                    from ~/.links/workspace
#   WORKSPACE=<dir> ./scripts/release.sh
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="${WORKSPACE:-$HOME/.links/workspace}"
[ -d "$SRC" ] || { echo "no workspace at $SRC" >&2; exit 1; }

# A skill folder, replaced whole. The workspace's gws-* skills are vendored and personal: never
# released.
release_skill() {
  [ -d "$SRC/.agents/skills/$1" ] || { echo "no $1 in $SRC/.agents/skills" >&2; exit 1; }
  mkdir -p "$2"
  rm -rf "${2:?}/$1"
  cp -R "$SRC/.agents/skills/$1" "$2/"
  find "$2/$1" \( -name __pycache__ -o -name .DS_Store \) -prune -exec rm -rf {} +
}
for s in onboard weekly-review one-thing; do release_skill "$s" .agents/skills; done
for s in cv-engine opportunity-research; do release_skill "$s" addons/applications/skills; done

# A single file: its workspace path, then its path here.
release_file() {
  [ -f "$SRC/$1" ] || { echo "no $1 in $SRC" >&2; exit 1; }
  mkdir -p "$(dirname "$2")"
  cp "$SRC/$1" "$2"
}
release_file scripts/workspace-lint.py scripts/workspace-lint.py
release_file CONVENTIONS.md CONVENTIONS.md
release_file BUILDING.md addons/building/BUILDING.md
release_file addons/README.md addons/README.md

# Released copies carry no review dates: a user cannot review a skill they did not write, so
# their linter must never flag one. Strip status, review_interval and last_reviewed from the
# frontmatter's metadata: block, and drop metadata: itself if nothing is left under it.
for f in .agents/skills/*/SKILL.md addons/applications/skills/*/SKILL.md; do
  awk '
    NR == 1 && $0 == "---" { fm = 1; print; next }
    fm && $0 == "---"      { if (held) held = ""; fm = 0; print; next }
    fm && /^metadata:[[:space:]]*$/ { held = $0; next }
    fm && /^[[:space:]]+(status|review_interval|last_reviewed):/ { next }
    fm && held && /^[[:space:]]/ { print held; held = "" }
    fm && held               { held = "" }
    { print }
  ' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done
git status --short
