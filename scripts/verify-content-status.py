#!/usr/bin/env python3
"""
verify-content-status.py — assert the docs still describe the live site.

Compares the post status recorded in `content/content-calendar.md`, `STATE.json`
and `NEXT.md` against what is actually published on WordPress, read live from the
public REST API.

WHY THIS EXISTS
    The other gates check doctrine (`verify-imports.py`) and content quality
    (`verify-malay-voice.py`). Nothing checked whether the docs still match
    reality.

    On 2026-08-05 that gap produced real waste: the breadcrumb files still
    described Post #4 as having outstanding Phase 7 work months after it was
    finished, and an agent read that stale record and told the operator to redo
    completed work. The fix was applied by hand; nothing prevented a recurrence.

    `write-post/SKILL.md` Phase 7 ends with "update the docs" as a manual,
    unenforced step. Manual steps rot. This makes the rot loud.

WHAT IS DERIVABLE
    Published status, post ID, slug, URL, publish date, and the total post count
    all come from the WordPress REST API and are checked automatically.

WHAT IS NOT
    ClickRank and Screpy tracking checkboxes have no reliable API and are read
    off dashboards by hand. This script deliberately does NOT check them, and
    does not pretend to. Do not add a fake check for them.

USAGE
    python scripts/verify-content-status.py            # human-readable
    python scripts/verify-content-status.py --quiet    # only failures
    python scripts/verify-content-status.py --fix      # rewrite derivable fields
    python scripts/verify-content-status.py --offline  # skip the live fetch

EXIT CODES
    0 = docs agree with the live site    1 = drift found (or the fetch failed)
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The calendar is full of emoji ("PUBLISHED OK-tick") and middle dots, and those
# strings end up quoted inside failure messages. The Windows console is cp1252,
# so printing one raised UnicodeEncodeError and killed the run *while reporting
# drift* -- the gate crashed instead of reporting the very thing it exists to
# catch. Degrade unencodable characters instead of dying.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # non-tty or already-wrapped stream
        pass

SITE = "https://digitrustlab.com"
API = f"{SITE}/wp-json/wp/v2/posts?per_page=100&status=publish&_fields=id,slug,date,link"
TIMEOUT = 20

CALENDAR = "content/content-calendar.md"
STATE = "STATE.json"
NEXT = "NEXT.md"

# Table rows we treat as authoritative claims about a post. Matched on the FIRST
# column only, exact (case-insensitive) — so prose rows like
# "Optimized version | Duplicate draft created (Post ID 320)" are NOT mistaken
# for the post's own ID. That row exists in Post #1 and broke an earlier draft
# of this parser.
FIELD_ALIASES = {
    "post id": "post_id",
    "wp post id": "post_id",
    "url": "url",
    "slug": "slug",
    "status": "status",
    "date": "date",
    "published date": "date",
}

POST_HEADING = re.compile(r"^##\s*Post\s*#(\d+)\s*(?:—|-|–)?\s*(.*)$", re.IGNORECASE)
TABLE_ROW = re.compile(r"^\|([^|]+)\|(.*)\|\s*$")


def rel(p):
    return os.path.relpath(p, REPO).replace("\\", "/")


def strip_md(text):
    """Drop bold/code/emphasis markers so values compare cleanly."""
    return re.sub(r"[*`_]", "", text).strip()


def first_int(text):
    m = re.search(r"\d+", text or "")
    return int(m.group()) if m else None


def slug_from(value):
    """Pull a slug out of either a full URL or a bare /slug/ path."""
    if not value:
        return None
    m = re.search(r"digitrustlab\.com/([^/\s)]+)", value)
    if m:
        return m.group(1).strip("/")
    m = re.match(r"^/?([a-z0-9-]+)/?$", value.strip())
    return m.group(1) if m else None


def iso_date(text):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", text or "")
    return m.group(1) if m else None


def ascii_safe(text):
    """The Windows console is cp1252 and mangles the middle dots used in tables."""
    return (text or "").encode("ascii", "replace").decode("ascii")


# How to reduce a raw cell to its comparable essence before deciding whether two
# entries for the same field actually disagree.
#
# WHY: the calendar mixes bare values with annotated ones. Post #4 records the ID
# twice -- once as `536`, once as `536 - slug cara-buat-gambar-ai - category ...`.
# Those are the SAME claim. Comparing raw strings flagged it as a contradiction,
# which is a false positive that would train the operator to ignore this gate.
NORMALIZERS = {
    "post_id": first_int,
    "date": iso_date,
    "url": slug_from,
    "slug": slug_from,
}


def normalize(field, value):
    fn = NORMALIZERS.get(field)
    if fn:
        got = fn(value)
        return str(got).lower() if got is not None else None
    return value.strip().lower() or None


# ---------------------------------------------------------------- live site

def fetch_live():
    """Return {post_id: {slug, date, link}} from the public WP REST API."""
    req = urllib.request.Request(API, headers={"User-Agent": "verify-content-status/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.load(resp)
    return {
        p["id"]: {
            "slug": p["slug"],
            "date": p["date"][:10],
            "link": p["link"],
        }
        for p in data
    }


# ---------------------------------------------------------------- calendar

def parse_calendar(path):
    """
    Return (posts, duplicate_conflicts).

    posts: {number: {"heading": str, "claims": {field: [(value, line)]}}}

    A field appearing more than once for the same post with DIFFERENT values is
    reported as an intra-file conflict. Post #4 carries exactly this: one block
    says Rank Math 100/100 with Phase 7 complete, an older research block below
    says 95/100 with Phase 7 outstanding.
    """
    posts, current = {}, None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            head = POST_HEADING.match(line.strip())
            if head:
                current = int(head.group(1))
                posts.setdefault(current, {
                    "heading": strip_md(head.group(2)),
                    "heading_line": lineno,
                    "claims": {},
                })
                continue
            if current is None:
                continue
            row = TABLE_ROW.match(line.rstrip())
            if not row:
                continue
            key = strip_md(row.group(1)).lower()
            field = FIELD_ALIASES.get(key)
            if not field:
                continue
            value = strip_md(row.group(2))
            posts[current]["claims"].setdefault(field, []).append((value, lineno))

    conflicts = []
    for num, post in posts.items():
        for field, entries in post["claims"].items():
            seen = {normalize(field, v) for v, _ in entries}
            seen.discard(None)  # an unparseable cell is not evidence of conflict
            if len(seen) > 1:
                where = ", ".join(f"L{ln}: {ascii_safe(v)!r}" for v, ln in entries)
                conflicts.append(f"Post #{num} declares conflicting {field} -> {where}")
    return posts, conflicts


def claim(post, field):
    """First recorded value for a field, or None."""
    entries = post["claims"].get(field)
    return entries[0][0] if entries else None


def all_normalized(post, fields, using=None):
    """
    Every distinct normalized value recorded across `fields`, with line numbers.

    WHY NOT just the first match: a post commonly records the same fact twice,
    e.g. Post #2 carries both `| URL | /cara-guna-chatgpt/ |` and
    `| Slug | /cara-guna-chatgpt/ |`. An earlier version checked `url or slug`
    and stopped at the first, so drift introduced in the *other* row passed the
    gate silently. Every recorded claim has to match the live site, not just one.

    `using` forces one extractor across all `fields`, for when the same fact is
    recorded under headings with different default shapes: the publish date lives
    both in `| Date | 2026-07-29 |` and inside `| Status | Published (2026-07-09) |`.
    Without the override the Status cell normalizes as free text and every
    published post reports a phantom date mismatch against itself.
    """
    out = {}
    for field in fields:
        for raw, lineno in post["claims"].get(field, []):
            value = using(raw) if using else normalize(field, raw)
            if value is not None:
                out.setdefault(str(value).lower(), []).append((field, lineno))
    return out


def is_published(post):
    heading = post["heading"].upper()
    status = (claim(post, "status") or "").upper()
    return "PUBLISHED" in heading or "PUBLISHED" in status


# ---------------------------------------------------------------- checks

def check_posts(posts, live, failures, say):
    say("\n== calendar vs live WordPress ==")
    live_ids = set(live)
    claimed_ids = set()

    for num in sorted(posts):
        post = posts[num]
        pid = first_int(claim(post, "post_id"))
        published = is_published(post)

        if not published:
            # Reverse drift: the calendar still says PLANNED but the slug is live.
            slug = slug_from(claim(post, "url")) or slug_from(claim(post, "slug"))
            hit = next((i for i, p in live.items() if p["slug"] == slug), None) if slug else None
            if hit:
                failures.append(
                    f"Post #{num} is marked not-published in {CALENDAR}, but "
                    f"/{slug}/ is LIVE (id {hit}). The calendar is behind reality.")
                say(f"  STALE    Post #{num} marked planned, but live as id {hit}")
            else:
                say(f"  ok       Post #{num} planned (not live, as expected)")
            continue

        if pid is None:
            failures.append(f"Post #{num} is marked PUBLISHED but records no Post ID")
            say(f"  MISSING  Post #{num} published with no Post ID")
            continue

        claimed_ids.add(pid)
        if pid not in live_ids:
            failures.append(
                f"Post #{num} claims Post ID {pid} as published, but that ID is "
                f"not live on {SITE} (deleted, drafted, or the ID is wrong)")
            say(f"  GONE     Post #{num} id {pid} not live")
            continue

        actual = live[pid]
        ok = True

        for want_slug, where in all_normalized(post, ("url", "slug")).items():
            if want_slug != actual["slug"]:
                spots = ", ".join(f"{f} L{ln}" for f, ln in where)
                failures.append(
                    f"Post #{num} (id {pid}) records slug '{want_slug}' ({spots}) "
                    f"but the live slug is '{actual['slug']}'")
                say(f"  DRIFT    Post #{num} slug {want_slug} != {actual['slug']}")
                ok = False

        for want_date, where in all_normalized(
                post, ("date", "status"), using=iso_date).items():
            if want_date != actual["date"]:
                spots = ", ".join(f"{f} L{ln}" for f, ln in where)
                failures.append(
                    f"Post #{num} (id {pid}) records publish date {want_date} "
                    f"({spots}) but the live date is {actual['date']}")
                say(f"  DRIFT    Post #{num} date {want_date} != {actual['date']}")
                ok = False

        if ok:
            say(f"  ok       Post #{num} id {pid} /{actual['slug']}/ {actual['date']}")

    # Untracked: live on the site, absent from the calendar.
    for pid in sorted(live_ids - claimed_ids):
        failures.append(
            f"Live post id {pid} (/{live[pid]['slug']}/) has no PUBLISHED entry in "
            f"{CALENDAR}. Published without recording it?")
        say(f"  UNTRACKED  id {pid} /{live[pid]['slug']}/")

    return len(live_ids)


def check_state(live_count, failures, say, fix):
    say("\n== STATE.json ==")
    path = os.path.join(REPO, STATE)
    if not os.path.exists(path):
        failures.append(f"{STATE} is missing")
        say(f"  MISSING  {STATE}")
        return
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    state = json.loads(raw)

    recorded = state.get("keyMetrics", {}).get("blogPosts")
    if recorded != live_count:
        if fix:
            state.setdefault("keyMetrics", {})["blogPosts"] = live_count
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(state, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            say(f"  FIXED    keyMetrics.blogPosts {recorded} -> {live_count}")
        else:
            failures.append(
                f"{STATE} keyMetrics.blogPosts is {recorded}, live count is "
                f"{live_count}  (fixable: --fix)")
            say(f"  DRIFT    blogPosts {recorded} != {live_count}")
    else:
        say(f"  ok       blogPosts {recorded}")


def check_next(posts, failures, say):
    """
    NEXT.md is prose, so this is a containment check, not a parse: if it names a
    post as the current target, that post must not already be published.
    """
    say("\n== NEXT.md ==")
    path = os.path.join(REPO, NEXT)
    if not os.path.exists(path):
        failures.append(f"{NEXT} is missing")
        say(f"  MISSING  {NEXT}")
        return
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    flagged = False
    for num in sorted(posts):
        if not is_published(posts[num]):
            continue
        for pattern in (f"Post #{num}", f"Post {num}"):
            m = re.search(
                rf"(next|current|todo|in progress|work on)[^\n]*{re.escape(pattern)}\b",
                text, re.IGNORECASE)
            if m:
                failures.append(
                    f"{NEXT} still points at Post #{num} as upcoming work, but the "
                    f"calendar marks it PUBLISHED: {m.group(0).strip()!r}")
                say(f"  STALE    NEXT.md targets published Post #{num}")
                flagged = True
                break
    if not flagged:
        say("  ok       no published post listed as upcoming")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    ap.add_argument("--fix", action="store_true",
                    help="rewrite the safely derivable fields (currently: "
                         "STATE.json keyMetrics.blogPosts)")
    ap.add_argument("--offline", action="store_true",
                    help="skip the live fetch; run only intra-file consistency checks")
    args = ap.parse_args()

    failures = []
    say = (lambda *a: None) if args.quiet else print

    cal_path = os.path.join(REPO, CALENDAR)
    if not os.path.exists(cal_path):
        print(f"FAIL - {CALENDAR} is missing; nothing to verify.")
        return 1

    posts, conflicts = parse_calendar(cal_path)

    say(f"\n== {CALENDAR} internal consistency ==")
    if conflicts:
        for c in conflicts:
            failures.append(c)
            say(f"  CONFLICT {c}")
    else:
        say(f"  ok       {len(posts)} post entries, no contradictory fields")

    if args.offline:
        say("\n(offline: skipped the live WordPress comparison)")
    else:
        try:
            live = fetch_live()
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"\nFAIL - could not read {SITE} ({exc.__class__.__name__}: {exc}).")
            print("Cannot verify status without the live site. Re-run when reachable,")
            print("or use --offline to run only the intra-file checks.")
            return 1

        live_count = check_posts(posts, live, failures, say)
        check_state(live_count, failures, say, args.fix)
        check_next(posts, failures, say)

    print()
    # ASCII only: the Windows console defaults to cp1252 and mangles anything else.
    if failures:
        print(f"FAIL - {len(failures)} drift problem(s):\n")
        for f in failures:
            print(f"  * {f}")
        print("\nThe docs no longer describe the live site. An agent reading them")
        print("will act on stale facts and will NOT warn you.")
        print("\nNOT checked here (no reliable API, verify by hand):")
        print("  * ClickRank AI Overview / Keyword Tracker entries")
        print("  * Screpy Rank Tracker entries and re-crawls")
        return 1

    if args.offline:
        # Must not claim agreement with a site we never contacted.
        print(f"PASS (offline) - {len(posts)} calendar entries are internally "
              f"consistent. The live site was NOT checked.")
        return 0

    print(f"PASS - {len(posts)} calendar entries agree with the live site.")
    print("Note: ClickRank and Screpy tracking are NOT covered by this gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
