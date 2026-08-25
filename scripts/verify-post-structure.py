#!/usr/bin/env python3
"""Verify the reader-facing post structure used by the Bricks single-post template.

The single-post template renders the post title as the page H1.  Article body
HTML must therefore not contain another H1, otherwise readers see the title
twice and the page has duplicate H1 structure.

Usage:
    python scripts/verify-post-structure.py --file content/drafts/post.html
    python scripts/verify-post-structure.py --post-id 656
    python scripts/verify-post-structure.py --post-id 656 --json

Exit codes:
    0 = structure passes
    1 = body-structure violation
    2 = input or network/configuration error
"""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SITE = "https://digitrustlab.com"


class HeadingParser(HTMLParser):
    """Collect body H1 text without treating title metadata as body content."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._in_h1 = False
        self._parts: list[str] = []
        self.h1_texts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "h1":
            self._in_h1 = True
            self._parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "h1" and self._in_h1:
            text = " ".join("".join(self._parts).split())
            self.h1_texts.append(text)
            self._in_h1 = False
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._in_h1:
            self._parts.append(data)


def find_body_h1s(html: str) -> list[str]:
    parser = HeadingParser()
    parser.feed(html)
    parser.close()
    return parser.h1_texts


def check_html(html: str, *, title: str = "", source: str = "") -> dict[str, Any]:
    h1s = find_body_h1s(html)
    issues: list[dict[str, Any]] = []
    if h1s:
        for text in h1s:
            issue: dict[str, Any] = {
                "code": "body-h1-present",
                "message": "Post body contains an H1; the Bricks template already renders the post title as the page H1.",
                "text": text,
            }
            if title and text.casefold() == title.casefold():
                issue["code"] = "duplicate-template-title"
                issue["message"] = "Post body repeats the post title as an H1; remove the body H1 because the Bricks template supplies it."
            issues.append(issue)
    return {
        "passed": not issues,
        "source": source,
        "title": title,
        "body_h1_count": len(h1s),
        "body_h1_texts": h1s,
        "issues": issues,
    }


def fetch_post(post_id: int) -> dict[str, Any]:
    url = f"{SITE}/wp-json/wp/v2/posts/{post_id}?_fields=id,slug,status,title,content"
    request = Request(url, headers={"User-Agent": "DigiTrustLab-post-structure-gate/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"could not read WordPress post {post_id}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="HTML file containing the final post package/body")
    source.add_argument("--post-id", type=int, help="Published WordPress post ID")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    try:
        if args.file:
            html = args.file.read_text(encoding="utf-8")
            result = check_html(html, source=str(args.file))
        else:
            post = fetch_post(args.post_id)
            content = post.get("content", {}).get("rendered", "")
            title = post.get("title", {}).get("rendered", "")
            result = check_html(content, title=title, source=f"post {args.post_id} ({post.get('slug', '')})")
            result["post_id"] = args.post_id
            result["status"] = post.get("status")
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        if args.json:
            print(json.dumps({"passed": False, "configuration_error": str(exc)}, ensure_ascii=False))
        else:
            print(f"[ERROR] {exc}")
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["passed"]:
        print(f"[PASS] {result['source']}: no body H1; template title is not duplicated")
    else:
        print(f"[BLOCK] {result['source']}: body H1 detected")
        for issue in result["issues"]:
            print(f"- {issue['code']}: {issue['message']} ({issue['text']!r})")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
