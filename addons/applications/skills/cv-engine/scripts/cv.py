# /// script
# requires-python = ">=3.10"
# dependencies = ["typst==0.15.*", "pyyaml>=6"]
# ///
"""CV engine: YAML content plus a Typst template, built to PDF with nothing to install
beyond uv. The Typst version is pinned above because its syntax changes between releases.

    uv run cv.py init <folder>                  start a CV folder: template, example, applications/
    uv run cv.py build <content.yaml> [...]     build each to <cv folder>/out/<name>.pdf
    uv run cv.py build --png <content.yaml>     also write page images, out/<name>-<n>.png
    uv run cv.py check <cut.yaml> <main.yaml>   list every line in a cut that the main CV lacks

The CV folder is the nearest folder above the YAML file that holds template.typ, so tailored
copies in applications/ build with the same template. Fonts come from the folder's fonts/ and
Typst's built-in set only: system fonts are ignored so a CV looks the same on every machine.
"""
import pathlib
import re
import shutil
import sys

import typst
import yaml

SKILL = pathlib.Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"


def init(folder: pathlib.Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "applications").mkdir(exist_ok=True)
    (folder / "fonts").mkdir(exist_ok=True)
    for src, dst in [("template.typ", "template.typ"), ("example.en.yaml", "cv.en.yaml")]:
        target = folder / dst
        if target.exists():
            print(f"kept     {target} (already there)")
        else:
            shutil.copy(ASSETS / src, target)
            print(f"created  {target}")
    ignore = folder / ".gitignore"
    if not ignore.exists():
        ignore.write_text("out/\n")
    print(f"\nNext: fill in {folder / 'cv.en.yaml'}, then build it.")


def cv_root(content: pathlib.Path) -> pathlib.Path:
    for parent in content.resolve().parents:
        if (parent / "template.typ").exists():
            return parent
    sys.exit(f"error: no template.typ above {content}. Run `init` on the CV folder first.")


def build(content: pathlib.Path, png: bool) -> bool:
    if not content.exists():
        print(f"error: {content} does not exist")
        return False
    root = cv_root(content)
    out = root / "out"
    out.mkdir(exist_ok=True)
    opts = dict(
        root=str(root),
        font_paths=[str(root / "fonts")],
        ignore_system_fonts=True,
        sys_inputs={"content": "/" + content.resolve().relative_to(root).as_posix()},
    )
    template = str(root / "template.typ")
    pdf = out / f"{content.stem}.pdf"
    try:
        _, warnings = typst.compile_with_warnings(template, output=str(pdf), **opts)
        pages = typst.query(template, "<pages>", field="value", one=True, **opts)
        limit = typst.query(template, "<max-pages>", field="value", one=True, **opts)
        if png:
            typst.compile(template, output=str(out / f"{content.stem}-{{p}}.png"),
                          format="png", ppi=110, **opts)
    except typst.TypstError as e:
        print(f"error building {content}:\n{e}")
        return False
    for w in warnings:
        print(f"warning: {w}")
    fits = int(pages) <= int(limit)
    verdict = "fits" if fits else f"OVER the {limit}-page limit"
    print(f"built    {pdf}  ({pages} page{'s' if int(pages) != 1 else ''}, {verdict})")
    return fits


def claims(path: pathlib.Path) -> list[str]:
    """Every line of a CV that states a fact: entry lines, bullets, skill lines, paragraphs.
    The headline is left out, since a cut is meant to rewrite it."""
    data = yaml.safe_load(path.read_text()) or {}
    out = [str(data["summary"])] if "summary" in data else []
    for s in data.get("sections", []):
        if "text" in s:
            out.append(str(s["text"]))
        for e in s.get("entries", []):
            head = " · ".join(str(e[k]) for k in ("title", "role", "date") if k in e)
            out.append(head)
            out += [str(b) for b in e.get("bullets", [])]
        out += [f"{l['label']}: {l['text']}" for l in s.get("lines", [])]
    return [" ".join(c.split()) for c in out]


def check(cut: pathlib.Path, main: pathlib.Path) -> int:
    """Print what a tailored cut says that the main CV does not, word for word. The agent shows
    this to the user, who confirms each line is true before the cut is sent."""
    # Reordering is tailoring, not a new claim: a line whose parts (split on commas and colons) all match a
    # line in the main CV counts as known, whatever their order.
    def key(c: str) -> frozenset[str]:
        return frozenset(part.strip() for part in re.split(r",|: ", c))
    known = {key(c) for c in claims(main)}
    new = [c for c in claims(cut) if key(c) not in known]
    if not new:
        print(f"check    {cut}: every line comes from {main}")
        return 0
    print(f"check    {cut}: {len(new)} line(s) not in {main}. Confirm each is true:")
    for c in new:
        print(f"  NEW    {c}")
    return 1


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "init":
        init(pathlib.Path(argv[1]))
        return 0
    if len(argv) == 3 and argv[0] == "check":
        return check(pathlib.Path(argv[1]), pathlib.Path(argv[2]))
    if argv and argv[0] == "build":
        png = "--png" in argv
        files = [pathlib.Path(a) for a in argv[1:] if a != "--png"]
        if not files:
            print(__doc__)
            return 2
        ok = [build(f, png) for f in files]
        return 0 if all(ok) else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
