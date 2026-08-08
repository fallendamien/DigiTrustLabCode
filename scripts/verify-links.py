#!/usr/bin/env python3
"""Verify DigiTrust Lab editorial link quality before and after publication.

The checker is intentionally separate from Rank Math. It validates structural
link policy that Rank Math does not prove: descriptive anchors, HTTPS,
internal/external link counts, editorial rel attributes, self-links, and a
recorded inbound-link decision for live posts.

USAGE
    python scripts/verify-links.py --file final.html
    python scripts/verify-links.py --post-id 559 --inbound-review content/link-reviews/slug.json
    python scripts/verify-links.py --post-id 559 --inbound-review ... --check-destinations --json

EXIT CODES
    0 = link policy and required evidence pass
    1 = content or link-policy failure
    2 = source, configuration, parsing, or network verification failure
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://digitrustlab.com"
POLICY_PATH = ROOT / "content" / "link-policy.json"
EDITORIAL_SCHEMES = {"http", "https"}
SKIP_SCHEMES = {"mailto", "tel", "sms"}


def normalize_text(value: str) -> str:
    return " ".join(html_lib.unescape(value or "").split()).strip()


def normalize_path(path: str) -> str:
    path = path or "/"
    if not path.startswith("/"):
        path = "/" + path
    if path != "/":
        path = path.rstrip("/") + "/"
    return path


def canonical_url(value: str, base: str = SITE + "/") -> str:
    parsed = urllib.parse.urlsplit(urllib.parse.urljoin(base, value))
    host = (parsed.hostname or "").lower()
    return urllib.parse.urlunsplit(
        (
            parsed.scheme.lower(),
            host + (f":{parsed.port}" if parsed.port else ""),
            normalize_path(parsed.path),
            parsed.query,
            "",
        )
    )


class LinkParser(HTMLParser):
    """Extract anchor attributes and visible text without third-party HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self.current: dict[str, Any] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a" or self.current is not None:
            return
        attributes = {key.lower(): value or "" for key, value in attrs}
        self.current = {
            "href": attributes.get("href", ""),
            "rel": attributes.get("rel", ""),
            "target": attributes.get("target", ""),
            "text": [],
        }

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self.current is None:
            return
        current = self.current
        self.current = None
        self.links.append(
            {
                "href": normalize_text(str(current["href"])),
                "rel": normalize_text(str(current["rel"])),
                "target": normalize_text(str(current["target"])),
                "text": normalize_text("".join(current["text"])),
            }
        )

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.current["text"].append(data)


def extract_links(source_html: str) -> list[dict[str, str]]:
    parser = LinkParser()
    parser.feed(source_html)
    parser.close()
    return parser.links


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load link policy: {exc}") from exc
    if not isinstance(policy, dict) or policy.get("schema_version") != 1:
        raise ValueError("link policy must be an object with schema_version 1")
    for key in (
        "site_host",
        "editorial_min_internal_links",
        "editorial_max_internal_links",
        "editorial_min_external_links",
        "generic_anchor_texts",
        "blocked_editorial_rel_tokens",
        "allowed_nofollow_domains",
    ):
        if key not in policy:
            raise ValueError(f"link policy is missing '{key}'")
    return policy


def load_html(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"cannot read HTML source: {exc}") from exc


def fetch_json(url: str, user_agent: str = "digitrustlab-link-check") -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot fetch {url}: {exc}") from exc


def fetch_post(post_id: int) -> dict[str, Any]:
    data = fetch_json(f"{SITE}/wp-json/wp/v2/posts/{post_id}?_fields=id,slug,link,content")
    if not isinstance(data, dict) or not data.get("id") or not isinstance(data.get("content"), dict):
        raise RuntimeError(f"WordPress response for post {post_id} is incomplete")
    return data


def fetch_published_content(endpoint: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        url = (
            f"{SITE}/wp-json/wp/v2/{endpoint}?per_page=100&page={page}"
            "&_fields=id,slug,link,content"
        )
        try:
            batch = fetch_json(url, user_agent="digitrustlab-inbound-link-check")
        except RuntimeError as exc:
            # A site without a public pages endpoint should not prevent the
            # post scan from checking posts, but posts remain mandatory.
            if endpoint == "pages" and " 404 " in f" {exc} ":
                return items
            raise
        if not isinstance(batch, list):
            raise RuntimeError(f"WordPress {endpoint} response is not a list")
        items.extend(item for item in batch if isinstance(item, dict))
        if len(batch) < 100:
            return items
        page += 1


def classify_link(link: dict[str, str], site_host: str) -> dict[str, Any]:
    href = link["href"]
    parsed = urllib.parse.urlsplit(urllib.parse.urljoin(SITE + "/", href))
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    is_fragment = href.startswith("#") or (not href and not parsed.path)
    is_skip_scheme = scheme in SKIP_SCHEMES
    is_editorial = not is_fragment and not is_skip_scheme and bool(href)
    is_internal = is_editorial and host in {site_host.lower(), f"www.{site_host.lower()}"}
    return {
        **link,
        "scheme": scheme,
        "host": host,
        "is_fragment": is_fragment,
        "is_editorial": is_editorial,
        "is_internal": is_internal,
        "is_external": is_editorial and not is_internal,
        "normalized_url": canonical_url(href),
        "rel_tokens": {token.casefold() for token in link["rel"].split()},
    }


def link_fingerprint(links: list[dict[str, Any]]) -> str:
    rows = []
    for link in links:
        if not link["is_editorial"]:
            continue
        rows.append(
            "\0".join(
                (
                    "internal" if link["is_internal"] else "external",
                    link["normalized_url"],
                    link["text"],
                    " ".join(sorted(link["rel_tokens"])),
                )
            )
        )
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def validate_links(
    source_html: str,
    policy: dict[str, Any],
    *,
    source_url: str = "",
) -> dict[str, Any]:
    raw_links = extract_links(source_html)
    site_host = str(policy["site_host"])
    source_canonical = canonical_url(source_url) if source_url else ""
    links = [classify_link(link, site_host) for link in raw_links]
    # Easy Table of Contents renders same-page links as absolute URLs with a
    # fragment. Treat those like href="#section", not as contextual self-links.
    for link in links:
        parsed = urllib.parse.urlsplit(urllib.parse.urljoin(SITE + "/", link["href"]))
        if parsed.fragment and source_canonical and link["normalized_url"] == source_canonical:
            link["is_fragment"] = True
            link["is_editorial"] = False
            link["is_internal"] = False
            link["is_external"] = False
    editorial = [link for link in links if link["is_editorial"]]
    internal = [link for link in editorial if link["is_internal"]]
    external = [link for link in editorial if link["is_external"]]
    issues: list[dict[str, str]] = []
    generic_anchors = {normalize_text(str(item)).casefold() for item in policy["generic_anchor_texts"]}
    blocked_rel = {normalize_text(str(item)).casefold() for item in policy["blocked_editorial_rel_tokens"]}
    allowed_nofollow = {str(item).lower() for item in policy["allowed_nofollow_domains"]}
    for index, link in enumerate(editorial, start=1):
        label = f"link-{index}"
        if not link["href"]:
            issues.append({"code": "empty-href", "detail": f"{label}: href is empty"})
        if not link["text"]:
            issues.append({"code": "empty-anchor", "detail": f"{label}: visible anchor text is empty"})
        elif link["text"].casefold() in generic_anchors:
            issues.append(
                {"code": "generic-anchor", "detail": f"{label}: replace generic anchor '{link['text']}' with descriptive text"}
            )
        if policy.get("require_https") and link["scheme"] != "https":
            issues.append({"code": "https-required", "detail": f"{label}: editorial URL must use HTTPS ({link['href']})"})
        if link["is_internal"] and source_canonical and link["normalized_url"] == source_canonical:
            issues.append({"code": "self-link", "detail": f"{label}: page links to itself ({link['href']})"})
        if link["is_external"]:
            blocked = link["rel_tokens"] & blocked_rel
            if blocked and link["host"] not in allowed_nofollow:
                issues.append(
                    {"code": "editorial-rel", "detail": f"{label}: external editorial link has blocked rel token(s): {', '.join(sorted(blocked))}"}
                )

    minimum_internal = int(policy["editorial_min_internal_links"])
    maximum_internal = int(policy["editorial_max_internal_links"])
    minimum_external = int(policy["editorial_min_external_links"])
    if len(internal) < minimum_internal:
        issues.append({"code": "internal-links-missing", "detail": f"need at least {minimum_internal} contextual internal link(s); found {len(internal)}"})
    if len(internal) > maximum_internal:
        issues.append({"code": "internal-links-too-many", "detail": f"maximum is {maximum_internal} contextual internal link(s); found {len(internal)}"})
    if len(external) < minimum_external:
        issues.append({"code": "external-links-missing", "detail": f"need at least {minimum_external} editorial external link(s); found {len(external)}"})
    if policy.get("require_external_dofollow") and external:
        dofollow = [link for link in external if "nofollow" not in link["rel_tokens"]]
        if not dofollow:
            issues.append({"code": "external-dofollow-missing", "detail": "at least one editorial external link must be dofollow"})

    return {
        "passed": not issues,
        "issues": issues,
        "links": [
            {
                key: value
                for key, value in link.items()
                if key not in {"rel_tokens"}
            }
            | {"rel_tokens": sorted(link["rel_tokens"])}
            for link in links
        ],
        "counts": {
            "all_anchors": len(raw_links),
            "editorial": len(editorial),
            "internal": len(internal),
            "external": len(external),
            "external_dofollow": sum(1 for link in external if "nofollow" not in link["rel_tokens"]),
            "fragments_excluded": sum(1 for link in links if link["is_fragment"]),
        },
        "link_hash": link_fingerprint(links),
    }


def inbound_sources(target: dict[str, Any], *, post_id: int) -> list[dict[str, Any]]:
    target_url = canonical_url(str(target.get("link", "")))
    found: list[dict[str, Any]] = []
    for endpoint in ("posts", "pages"):
        for item in fetch_published_content(endpoint):
            if int(item.get("id", -1)) == post_id:
                continue
            html = str(item.get("content", {}).get("rendered", ""))
            for link in extract_links(html):
                href = link.get("href", "")
                if href and canonical_url(href, str(item.get("link", SITE + "/"))) == target_url:
                    found.append(
                        {
                            "source_id": int(item["id"]),
                            "source_slug": str(item.get("slug", "")),
                            "source_url": str(item.get("link", "")),
                            "anchor": link.get("text", ""),
                        }
                    )
    return found


def load_inbound_review(path: Path) -> dict[str, Any]:
    try:
        review = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load inbound-link review: {exc}") from exc
    if not isinstance(review, dict) or review.get("schema_version") != 1:
        raise ValueError("inbound-link review must be an object with schema_version 1")
    return review


def validate_inbound_review(
    review: dict[str, Any],
    *,
    post: dict[str, Any],
    link_result: dict[str, Any],
    sources: list[dict[str, Any]],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if review.get("post_id") != post.get("id"):
        issues.append({"code": "inbound-post-id", "detail": "inbound review post_id does not match the live post"})
    if review.get("slug") != post.get("slug"):
        issues.append({"code": "inbound-slug", "detail": "inbound review slug does not match the live post"})
    if review.get("link_hash") != link_result["link_hash"]:
        issues.append({"code": "inbound-link-hash", "detail": "inbound review is stale; the live links changed"})
    inbound = review.get("inbound")
    if not isinstance(inbound, dict):
        return issues + [{"code": "inbound-evidence-missing", "detail": "inbound review must include an inbound object"}]
    decision = inbound.get("decision")
    if decision not in {"links_found", "no_safe_context"}:
        issues.append({"code": "inbound-decision", "detail": "decision must be links_found or no_safe_context"})
    actual_ids = sorted({item["source_id"] for item in sources})
    recorded_ids = sorted({int(value) for value in inbound.get("source_ids", [])}) if isinstance(inbound.get("source_ids", []), list) else []
    if actual_ids != recorded_ids:
        issues.append({"code": "inbound-source-mismatch", "detail": f"recorded inbound source IDs {recorded_ids} do not match live scan {actual_ids}"})
    if decision == "links_found" and not sources:
        issues.append({"code": "inbound-decision-invalid", "detail": "links_found requires at least one live inbound source"})
    if decision == "no_safe_context":
        reason = normalize_text(str(inbound.get("reason", "")))
        if sources:
            issues.append({"code": "inbound-decision-invalid", "detail": "no_safe_context is invalid when live inbound links exist"})
        if len(reason) < 20:
            issues.append({"code": "inbound-reason-missing", "detail": "no_safe_context requires a specific reason of at least 20 characters"})
    return issues


def check_destinations(links: list[dict[str, Any]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for index, link in enumerate(links, start=1):
        if not link["is_editorial"]:
            continue
        url = link["normalized_url"]
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "digitrustlab-link-check"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                status = response.status
        except urllib.error.HTTPError as exc:
            if exc.code == 405:
                request = urllib.request.Request(url, headers={"User-Agent": "digitrustlab-link-check"})
                try:
                    with urllib.request.urlopen(request, timeout=20) as response:
                        status = response.status
                except urllib.error.HTTPError as retry_exc:
                    status = retry_exc.code
                except (urllib.error.URLError, TimeoutError) as retry_exc:
                    issues.append({"code": "destination-unverified", "detail": f"link-{index}: {url} ({retry_exc})"})
                    continue
            else:
                status = exc.code
        except (urllib.error.URLError, TimeoutError) as exc:
            issues.append({"code": "destination-unverified", "detail": f"link-{index}: {url} ({exc})"})
            continue
        if status in {404, 410}:
            issues.append({"code": "broken-destination", "detail": f"link-{index}: {url} returned HTTP {status}"})
        elif status >= 400:
            issues.append({"code": "destination-unverified", "detail": f"link-{index}: {url} returned HTTP {status}"})
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="final HTML file to inspect")
    source.add_argument("--post-id", type=int, help="published WordPress post ID to fetch")
    parser.add_argument("--inbound-review", type=Path, help="auditable inbound-link decision JSON (required with --post-id)")
    parser.add_argument("--check-destinations", action="store_true", help="verify each editorial URL over HTTPS")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        policy = load_policy()
        post: dict[str, Any] | None = None
        if args.file:
            source_html = load_html(args.file)
            source_url = ""
        else:
            post = fetch_post(args.post_id)
            source_html = str(post.get("content", {}).get("rendered", ""))
            source_url = str(post.get("link", ""))
        result = validate_links(source_html, policy, source_url=source_url)
        if args.check_destinations:
            result["issues"].extend(check_destinations(result["links"]))
        sources: list[dict[str, Any]] = []
        if post is not None:
            if not args.inbound_review:
                result["issues"].append({"code": "inbound-review-missing", "detail": "--post-id requires --inbound-review evidence"})
            else:
                sources = inbound_sources(post, post_id=int(post["id"]))
                review = load_inbound_review(args.inbound_review)
                result["issues"].extend(validate_inbound_review(review, post=post, link_result=result, sources=sources))
            result["inbound"] = {
                "count": len(sources),
                "sources": sources,
            }
        result["passed"] = not result["issues"]
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            status = "PASS" if result["passed"] else "BLOCK"
            print(f"[{status}] {result['counts']} link counts; link_hash={result['link_hash']}")
            for issue in result["issues"]:
                print(f"- {issue['code']}: {issue['detail']}")
            if "inbound" in result:
                print(f"Inbound links found: {result['inbound']['count']}")
        return 0 if result["passed"] else 1
    except (ValueError, RuntimeError, OSError) as exc:
        if args.as_json:
            print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"[ERROR] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
