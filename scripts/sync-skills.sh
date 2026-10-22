#!/usr/bin/env bash
# For the maintainer, not for users. Refresh the applications add-on's copies of cv-engine and
# opportunity-research from the workspace where they are developed and used. That workspace is
# their home; these are released copies, so the starter works on its own. Run it, review the
# diff, commit.
#
#   ./scripts/sync-skills.sh                    from ~/.links/workspace/.agents/skills
#   WORKSPACE_SKILLS=<dir> ./scripts/sync-skills.sh
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="${WORKSPACE_SKILLS:-$HOME/.links/workspace/.agents/skills}"
DEST="addons/applications/skills"
mkdir -p "$DEST"
for s in cv-engine opportunity-research; do
  [ -d "$SRC/$s" ] || { echo "no $s in $SRC" >&2; exit 1; }
  rm -rf "${DEST:?}/$s"
  cp -R "$SRC/$s" "$DEST/"
done
find "$DEST" \( -name __pycache__ -o -name .DS_Store \) -prune -exec rm -rf {} +
git status --short "$DEST"
