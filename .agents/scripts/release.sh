#!/usr/bin/env bash
# For the maintainer, not for users. Release the generic files from the workspace where they are
# developed and used: the core skills, the applications add-on's skills, the linter, the spec,
# BUILDING.md and the add-ons index. That workspace is their home; these are released copies,
# word for word apart from review dates, so the starter works on its own. Never edit them here.
# It then writes .agents/manifest.json, from which the upgrade skill takes a later release into a
# user's workspace without overwriting their edits. Run it, review the diff, commit.
#
#   ./.agents/scripts/release.sh                    from ~/.links/workspace
#   WORKSPACE=<dir> ./.agents/scripts/release.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
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
CORE="onboard weekly-review one-thing upgrade"
for s in $CORE; do release_skill "$s" .agents/skills; done
for s in cv-engine opportunity-research; do release_skill "$s" .agents/addons/applications/skills; done

# A single file: its workspace path, then its path here.
release_file() {
  [ -f "$SRC/$1" ] || { echo "no $1 in $SRC" >&2; exit 1; }
  mkdir -p "$(dirname "$2")"
  cp "$SRC/$1" "$2"
}
release_file .agents/scripts/workspace-lint.py .agents/scripts/workspace-lint.py
release_file .agents/CONVENTIONS.md .agents/CONVENTIONS.md
release_file .agents/BUILDING.md .agents/addons/building/BUILDING.md
release_file .agents/addons/README.md .agents/addons/README.md

# Released copies carry no review dates: a user cannot review a skill they did not write, so
# their linter must never flag one. Strip status, review_interval and last_reviewed from the
# frontmatter's metadata: block, and drop metadata: itself if nothing is left under it.
for f in .agents/skills/*/SKILL.md .agents/addons/applications/skills/*/SKILL.md; do
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

# The manifest the upgrade skill reads: every file released above with the sha256 of its bytes,
# sorted, then where an add-on's files land once moved in. Released files only, never the
# manifest itself or a starter-owned file, so an unchanged release writes an identical manifest.
{
  find $(printf '.agents/skills/%s ' $CORE) .agents/addons/applications/skills -type f
  printf '%s\n' .agents/scripts/workspace-lint.py .agents/CONVENTIONS.md \
    .agents/addons/building/BUILDING.md .agents/addons/README.md
} | LC_ALL=C sort | tr '\n' '\0' | xargs -0 shasum -a 256 | awk '
  BEGIN { print "{"; print "  \"files\": {" }
  NR > 1 { print line "," }
  { line = "    \"" substr($0, 67) "\": \"" $1 "\"" }
  END {
    print line
    print "  },"
    print "  \"installs\": {"
    print "    \".agents/addons/applications/skills/\": \".agents/skills/\","
    print "    \".agents/addons/building/BUILDING.md\": \".agents/BUILDING.md\""
    print "  }"
    print "}"
  }
' > .agents/manifest.json
git status --short
