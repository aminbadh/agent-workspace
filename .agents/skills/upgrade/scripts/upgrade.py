#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Take the template's fixes into this workspace without touching what the user changed.

The template ships `.agents/manifest.json`: every generic file it releases, with a hash of its
content. This workspace's copy records what it last received. Comparing three versions of each
file (this workspace's, the last received, the template's current) tells "the template changed
it" from "the user changed it" from "both did", so a clean update is never mistaken for a
conflict and a user's edit is never overwritten silently.

Usage:  uv run upgrade.py plan            fetch the template and report, change nothing
        uv run upgrade.py apply PATH...   take the template's version of these files
        uv run upgrade.py finish          record the new manifest, remove the fetched copy

Exit:   0 done, 1 something to fix first (no Upstream line, no manifest, fetch failed).
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MANIFEST = ".agents/manifest.json"
FETCHED = Path(tempfile.gettempdir()) / f"agent-workspace-upgrade-{hashlib.sha1(str(ROOT).encode()).hexdigest()[:8]}"


def sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def upstream() -> str:
    readme = ROOT / "README.md"
    m = re.search(r"^Upstream:\s*(\S+)", readme.read_text() if readme.exists() else "", re.M)
    if not m:
        sys.exit("upgrade: README.md has no `Upstream:` line, so there is no template to upgrade from.")
    return m.group(1)


def manifest(base: Path, required: bool = True) -> dict[str, str]:
    f = base / MANIFEST
    if f.exists():
        return json.loads(f.read_text())["files"]
    if required:
        sys.exit(f"upgrade: the template at {upstream()} has no {MANIFEST} to compare against.")
    # Made before manifests existed: nothing counts as received, so every file that differs
    # from the template is shown once, and the user decides.
    print(f"upgrade: no {MANIFEST} here yet; every file that differs from the template is listed.\n")
    return {}


def installs(base: Path) -> dict[str, str]:
    """Where an add-on's files live once it is moved in, as the template's manifest declares:
    a path prefix inside .agents/addons/<name>/ mapped to its installed prefix."""
    f = base / MANIFEST
    return json.loads(f.read_text()).get("installs", {}) if f.exists() else {}


def local(path: str, moves: dict[str, str]) -> str:
    """This workspace's path for a template file: inside the add-on folder while the add-on is
    not installed, and where the manifest says once it is (its folder is then gone)."""
    for prefix, target in moves.items():
        addon = Path(*Path(prefix).parts[:3])  # .agents/addons/<name>
        if path.startswith(prefix) and not (ROOT / addon).exists():
            return target + path[len(prefix):]
    return path


def fetch() -> Path:
    if not FETCHED.exists():
        url = upstream()
        r = subprocess.run(["git", "clone", "--quiet", "--depth", "1", url, str(FETCHED)],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"upgrade: could not fetch {url}: {r.stderr.strip()}")
    return FETCHED


def plan() -> int:
    old, new_dir = manifest(ROOT, required=False), fetch()
    new, moves = manifest(new_dir), installs(new_dir)
    rows = []
    for path in sorted(set(old) | set(new)):
        here = local(path, moves)
        mine, was, now = sha(ROOT / here), old.get(path), new.get(path)
        if was == now:
            continue  # the template did not change it: nothing to take, whatever the user did
        if now is None:
            kind = "removed upstream" if mine == was else "removed upstream, yours changed"
        elif mine == now:
            kind = "already current"
        elif was is None:
            kind = "new" if mine is None else "new upstream, yours differs"
        elif mine == was:
            kind = "update"
        elif mine is None:
            kind = "update, yours deleted"
        else:
            kind = "conflict: both changed"
        rows.append((kind, here if here == path else f"{here}  (from {path})"))
    rows = [r for r in rows if r[0] != "already current"]
    if not rows:
        shutil.rmtree(new_dir)
        print("upgrade: nothing changed in the template since this workspace last took it.")
        return 0
    for kind, path in rows:
        print(f"{kind:34} {path}")
    print(f"\nTemplate copy: {new_dir}  (compare with `git diff --no-index <yours> <copy>`)")
    return 0


def apply(paths: list[str]) -> int:
    """PATHs are template paths, as `plan` prints them in brackets for installed add-ons."""
    new_dir = fetch()
    moves = installs(new_dir)
    backup = Path(tempfile.gettempdir()) / f"{FETCHED.name}-backup-{date.today()}"
    for path in paths:
        src, dst = new_dir / path, ROOT / local(path, moves)
        if dst.exists():
            (backup / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup / path)
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"took     {dst.relative_to(ROOT)}")
        elif dst.exists():
            dst.unlink()
            print(f"removed  {dst.relative_to(ROOT)}")
            folder = dst.parent
            while folder != ROOT and not any(folder.iterdir()):
                folder.rmdir()
                folder = folder.parent
    if backup.exists():
        print(f"\nPrevious versions saved in {backup}")
    return 0


def finish() -> int:
    new_dir = fetch()
    shutil.copy2(new_dir / MANIFEST, ROOT / MANIFEST)
    shutil.rmtree(new_dir)
    print(f"upgrade: {MANIFEST} now records the template as received; fetched copy removed.")
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["plan"]:
        return plan()
    if argv[:1] == ["apply"] and len(argv) > 1:
        return apply(argv[1:])
    if argv[:1] == ["finish"]:
        return finish()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
