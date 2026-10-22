# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Opportunity tracker tools: record offers, verify them against the web, watch sources.

    uv run opps.py add <tracker.csv> --org X --role Y --url U [--deadline 2026-11-15
                       --deadline-source U] [--location --start --duration --found-via
                       --fit high|medium|low --why --status --notes]
    uv run opps.py verify <tracker.csv>          check every open row
    uv run opps.py verify --json -               the same, for rows piped in as JSON
                                                 (a tracker in Notion or another app)
    uv run opps.py watch <sources.json>          report what changed on watched pages

The model finds and judges offers; this script checks the facts it cannot be trusted to
grade itself: that each link opens and is about that organisation, that the offer is not
closed, and that a deadline appears on the page it was taken from.
Exit codes: 0 all clear, 1 something to look at, 2 usage error.
"""
import csv
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import ssl
import urllib.error
import urllib.request

COLUMNS = ["added", "org", "role", "location", "start", "duration", "deadline",
           "deadline_source", "url", "found_via", "fit", "why", "status", "notes"]
STATUSES = ["to review", "applying", "applied", "interview", "offer", "rejected", "closed",
            "not a fit"]
DONE = {"rejected", "closed", "not a fit"}
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Sites that copy postings from employers. Fine for finding a name; the row should carry
# the employer's own posting, since copies go stale and drop the real deadline.
AGGREGATORS = ("indeed.", "glassdoor.", "jooble.", "talent.com", "optioncarriere.",
               "careerjet.", "simplyhired.", "adzuna.", "neuvoo.", "jobrapido.",
               "mastersportal.", "findamasters.", "scholarshipportal.")
# Sites that refuse plain requests. A row on them can only be confirmed in a browser.
BLOCKING = ("linkedin.com", "indeed.", "glassdoor.", "welcometothejungle.com", "tanitjobs.com",
            "emploitunisie.com", "apec.fr")
CLOSED = ("no longer accepting applications", "this job is no longer available",
          "this position has been filled", "job has expired", "posting has expired",
          "no longer available", "applications are closed", "this job has been closed",
          "n'est plus disponible", "offre expirée", "cette offre a expiré",
          "offre n'est plus en ligne", "candidatures sont closes")
MONTHS_EN = ["january", "february", "march", "april", "may", "june", "july", "august",
             "september", "october", "november", "december"]
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
             "septembre", "octobre", "novembre", "décembre"]


# ---- Fetching -----------------------------------------------------------------------

class Page(HTMLParser):
    """Visible text and links of a page. Script and style carry no news."""
    SKIP = {"script", "style", "noscript", "svg", "head"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._skip = 0
        self._href: str | None = None
        self._label: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._label = []

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        if tag == "a" and self._href:
            self.links.append((self._href, " ".join(self._label).strip()))
            self._href = None

    def handle_data(self, data):
        if not self._skip and data.strip():
            self.text.append(data.strip())
            if self._href is not None:
                self._label.append(data.strip())


def _curl(url: str) -> tuple[int | None, str, Page | None, str]:
    """Fallback for servers that omit an intermediate certificate: curl's trust store often
    completes the chain where Python's cannot. Verification stays on in both."""
    try:
        out = subprocess.run(["curl", "-sS", "--location", "--max-time", "30", "-A", UA,
                              "-w", "\n%{http_code} %{url_effective}", url],
                             capture_output=True, text=True, errors="replace", timeout=45)
    except (OSError, subprocess.TimeoutExpired):
        return None, url, None, "certificate error"
    if out.returncode != 0:
        return None, url, None, "certificate error"
    body, _, tail = out.stdout.rpartition("\n")
    code, _, final = tail.partition(" ")
    page = Page()
    page.feed(body)
    return int(code), final or url, page, ""


def fetch(client: None, url: str) -> tuple[int | None, str, Page | None, str]:
    """Status code, final URL, parsed page, and an error message when there is no page.
    Standard library only, so the script needs nothing downloaded to run."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as r:
            status, final, ctype, raw = r.status, r.geturl(), r.headers.get("content-type", "html"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, url, Page(), ""
    except urllib.error.URLError as e:
        if isinstance(getattr(e, "reason", None), ssl.SSLError):
            return _curl(url)
        return None, url, None, type(e.reason).__name__ if hasattr(e, "reason") else "URLError"
    except (TimeoutError, OSError) as e:
        return None, url, None, type(e).__name__
    page = Page()
    if "html" in ctype:
        page.feed(raw.decode("utf-8", "replace"))
    return status, final, page, ""


def client():
    """Kept so call sites read the same; the standard library needs no session object."""
    import contextlib
    return contextlib.nullcontext(None)


# ---- Tracker ------------------------------------------------------------------------

def read_rows(path: pathlib.Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_rows(path: pathlib.Path, rows: list[dict]) -> None:
    # utf-8-sig so Excel opens accented text correctly.
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def norm_url(u: str) -> str:
    p = urlparse(u.strip())
    return f"{p.netloc.lower().removeprefix('www.')}{p.path.rstrip('/')}"


def add(argv: list[str]) -> int:
    path = pathlib.Path(argv[0])
    row = {c: "" for c in COLUMNS}
    args = argv[1:]
    for flag, value in zip(args[::2], args[1::2]):
        key = flag.removeprefix("--").replace("-", "_")
        if key not in COLUMNS:
            print(f"error: unknown field {flag}. Fields: {', '.join(COLUMNS[1:])}")
            return 2
        row[key] = value.strip()
    problems = []
    if not row["org"] or not row["role"]:
        problems.append("--org and --role are required")
    if not re.match(r"https?://", row["url"]):
        problems.append("--url must be the offer's own web address")
    d = row["deadline"].lower()
    if d and d not in ("rolling", "unknown"):
        try:
            dt.date.fromisoformat(row["deadline"])
        except ValueError:
            problems.append("--deadline must be YYYY-MM-DD, 'rolling' or 'unknown'")
        if not re.match(r"https?://", row["deadline_source"]):
            problems.append("a dated --deadline needs --deadline-source: the page that states it")
    if not d:
        row["deadline"] = "unknown"
    if row["fit"] and row["fit"] not in ("high", "medium", "low"):
        problems.append("--fit is high, medium or low")
    row["status"] = row["status"] or "to review"
    if row["status"] not in STATUSES:
        problems.append(f"--status is one of: {', '.join(STATUSES)}")
    if problems:
        for p in problems:
            print(f"error: {p}")
        return 2
    rows = read_rows(path)
    if any(norm_url(r["url"]) == norm_url(row["url"]) for r in rows):
        print(f"skipped  {row['org']} · {row['role']}: already in {path}")
        return 0
    row["added"] = dt.date.today().isoformat()
    rows.append(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_rows(path, rows)
    print(f"added    {row['org']} · {row['role']} to {path} ({len(rows)} rows)")
    return 0


# ---- Verify -------------------------------------------------------------------------

def date_forms(d: dt.date) -> list[str]:
    en, fr = MONTHS_EN[d.month - 1], MONTHS_FR[d.month - 1]
    return [d.isoformat(), f"{d.day} {en} {d.year}", f"{en} {d.day}, {d.year}",
            f"{en} {d.day} {d.year}", f"{d.day} {fr} {d.year}", f"{d.day:02d}/{d.month:02d}/{d.year}",
            f"{d.day}/{d.month}/{d.year}", f"{d.day:02d}.{d.month:02d}.{d.year}",
            f"{d.day} {en[:3]} {d.year}", f"{en[:3]} {d.day}, {d.year}"]


# Words that appear on any careers page, so finding one proves nothing about the employer.
GENERIC = {"analytics", "group", "company", "groupe", "inc", "ltd", "sarl", "the", "and",
           "consulting", "solutions", "technologies", "technology", "international", "global",
           "services", "digital", "data", "tunisia", "tunisie", "france", "school", "university",
           "careers", "jobs", "bank", "banque", "systems", "labs", "partners", "holding"}
NOT_FOUND = ("page not found", "page introuvable", "page n'existe pas", "404 error",
             "error 404", "we couldn't find", "can't find the page", "cannot be found")


def mentions(text: str, org: str) -> bool:
    """True when the page names the organisation by a word that is its own, not one any
    careers page would contain. An organisation named only in generic words passes."""
    words = [w for w in re.findall(r"\w+", org.lower()) if len(w) >= 3 and w not in GENERIC]
    return not words or any(re.search(rf"\b{re.escape(w)}\b", text) for w in words)


def verify_row(c: None, row: dict) -> list[str]:
    flags = []
    url, host = row.get("url", ""), urlparse(row.get("url", "")).netloc.lower()
    if any(a in host for a in AGGREGATORS):
        flags.append("AGGREGATOR: replace with the employer's own posting")
    if any(b in host for b in BLOCKING):
        flags.append("BLOCKED: this site refuses scripts; confirm it in a browser")
    else:
        status, final, page, err = fetch(c, url)
        text = " ".join(page.text).lower() if page else ""
        if status is None:
            flags.append(f"UNREACHABLE: {err}")
        elif status in (404, 410):
            flags.append(f"DEAD: the page returns {status}")
        elif status >= 400:
            flags.append(f"ERROR {status}: open it in a browser")
        elif len(text) < 400:
            flags.append("UNCHECKED: the page builds itself with JavaScript; confirm in a browser")
        else:
            if any(m in text for m in NOT_FOUND):
                flags.append("NOT FOUND: the page says it does not exist")
            if any(m in text for m in CLOSED):
                flags.append("CLOSED: the page says the offer is no longer open")
            if not mentions(text, row.get("org", "")):
                flags.append(f"MISMATCH: the page never mentions {row.get('org')!r}")
            if norm_url(final) != norm_url(url) and urlparse(final).path in ("", "/"):
                flags.append("REDIRECTED to a home page: the offer is probably gone")
    deadline = row.get("deadline", "").strip().lower()
    if deadline and deadline not in ("rolling", "unknown"):
        try:
            d = dt.date.fromisoformat(deadline)
        except ValueError:
            flags.append(f"BAD DEADLINE {deadline!r}: use YYYY-MM-DD, rolling or unknown")
            return flags
        if d < dt.date.today():
            flags.append(f"PAST DEADLINE: {d}")
        src = row.get("deadline_source", "")
        if not src:
            flags.append("UNSOURCED DEADLINE: no page states it")
        elif not any(b in urlparse(src).netloc for b in BLOCKING):
            status, _, page, _ = fetch(c, src)
            text = " ".join(page.text).lower() if page else ""
            if status and status < 400 and len(text) >= 400 and \
                    not any(f.lower() in text for f in date_forms(d)):
                flags.append(f"DEADLINE NOT FOUND: {d} does not appear on its source page")
    return flags


def verify(argv: list[str]) -> int:
    if argv[:2] == ["--json", "-"]:
        rows = json.load(sys.stdin)
    else:
        rows = read_rows(pathlib.Path(argv[0]))
    live = [r for r in rows if (r.get("status") or "").lower() not in DONE]
    if not live:
        print("verify   nothing open to check")
        return 0
    flagged = 0
    with client() as c:
        for r in live:
            flags = verify_row(c, r)
            label = f"{r.get('org', '?')} · {r.get('role', '?')}"
            if flags:
                flagged += 1
                print(f"FLAG     {label}")
                for f in flags:
                    print(f"           {f}")
            else:
                print(f"ok       {label}")
    print(f"\nverify   {len(live)} open row(s), {flagged} need a look")
    return 1 if flagged else 0


# ---- Watch --------------------------------------------------------------------------

DATE_RE = re.compile(
    r"\b\d{1,2}\s+(?:" + "|".join(MONTHS_EN + MONTHS_FR) + r")\s+\d{4}\b|"
    r"\b(?:" + "|".join(MONTHS_EN) + r")\s+\d{1,2},?\s+\d{4}\b|"
    r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[./]\d{1,2}[./]\d{4}\b", re.I)


def watch(argv: list[str]) -> int:
    """Each source is {"label", "url", "kind": "links" or "dates", "match": optional,
    "pages": optional}. links: report links (filtered by `match`) that appeared or vanished,
    for career pages and catalogues; `pages` reads a paginated listing as url?page=0 to
    pages-1 (set it one above the current count, so growth is not cut off). dates: report
    dates that appeared or vanished, for a page whose window has not been announced yet.
    State is kept beside the sources file."""
    src_path = pathlib.Path(argv[0])
    sources = json.loads(src_path.read_text())
    state_path = src_path.with_name(src_path.stem + ".state.json")
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    changed = False
    with client() as c:
        for s in sources:
            key = hashlib.sha1(s["url"].encode()).hexdigest()[:12]
            status, final, page, err = fetch(c, s["url"])
            if not page or (status and status >= 400):
                print(f"FAILED   {s['label']}: {err or status}")
                changed = True
                continue
            if s.get("kind", "links") == "dates":
                now = sorted({m.group(0).lower() for m in DATE_RE.finditer(" ".join(page.text))})
            else:
                pages = [(final, page)]
                sep = "&" if "?" in s["url"] else "?"
                for p in range(1, int(s.get("pages", 1))):
                    _, f_p, pg_p, _ = fetch(c, f"{s['url']}{sep}page={p}")
                    if pg_p:
                        pages.append((f_p, pg_p))
                now = sorted({f"{l or '(no text)'} | {urljoin(f, h)}" for f, pg in pages
                              for h, l in pg.links if s.get("match", "") in urljoin(f, h)})
                if not now:
                    print(f"EMPTY    {s['label']}: no matching links; the page may need a browser")
            before = state.get(key)
            state[key] = now
            if before is None:
                print(f"baseline {s['label']}: {len(now)} item(s) recorded")
                continue
            added, gone = set(now) - set(before), set(before) - set(now)
            if added or gone:
                changed = True
                print(f"CHANGED  {s['label']}  ({s['url']})")
                for a in sorted(added):
                    print(f"  + {a}")
                for g in sorted(gone):
                    print(f"  - {g}")
            else:
                print(f"same     {s['label']}")
    state_path.write_text(json.dumps(state, indent=1, ensure_ascii=False))
    return 1 if changed else 0


def main(argv: list[str]) -> int:
    commands = {"add": add, "verify": verify, "watch": watch}
    if len(argv) >= 2 and argv[0] in commands:
        return commands[argv[0]](argv[1:])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
