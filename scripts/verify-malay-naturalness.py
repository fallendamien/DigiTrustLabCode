#!/usr/bin/env python3
"""
verify-malay-naturalness.py — hard evidence gate for natural Malay content.

This checker is deliberately separate from verify-malay-voice.py. The existing
checker handles deterministic spelling, slang, punctuation, brand, and markup
rules. This checker validates the evidence produced by two independent reviews
of the final document with the naturalness checklist: one Claude/Anthropic
review and one OpenAI review.

The review artifact is not a general score. It must prove that both reviewers
covered the same content hash, every segment passed every binary check with
high confidence, and no unresolved decision remains.

USAGE
    python scripts/verify-malay-naturalness.py --file draft.html --review review.json
    python scripts/verify-malay-naturalness.py --post-id 559 --review review.json
    python scripts/verify-malay-naturalness.py ... --json

EXIT CODES
    0 = deterministic checks and review evidence pass
    1 = publication blocked by content or review evidence
    2 = source, rules, or review-artifact parsing/configuration error
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


SITE = "https://digitrustlab.com"
RULES_PATH = Path(__file__).resolve().parents[1] / "content" / "malay-naturalness-rules.json"
REQUIRED_CHECKS = (
    "natural_usage",
    "literal_translation",
    "bureaucratic_stiffness",
    "technical_term_choice",
    "read_aloud_clarity",
    "terminology_consistency",
)
CLAUDE_FAMILIES = {"anthropic", "claude"}
REQUIRED_REVIEW_FAMILIES = {"openai", *CLAUDE_FAMILIES}
BLOCK_TAGS = {"blockquote", "caption", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6", "li", "p", "title"}
SKIP_TAGS = {"script", "style", "noscript", "svg"}
META_NAMES = {
    "description",
    "og:description",
    "og:title",
    "twitter:description",
    "twitter:title",
    "rank_math_description",
    "rank_math_title",
}


def normalize_text(value: str) -> str:
    """Normalize reader-facing text for matching and stable hashing."""
    return re.sub(r"\s+", " ", html_lib.unescape(value or "")).strip()


def hash_text(value: str) -> str:
    return hashlib.sha256(normalize_text(value).encode("utf-8")).hexdigest()


class SegmentParser(HTMLParser):
    """Extract reader-facing content without external HTML dependencies."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.segments: list[dict[str, str]] = []
        self.stack: list[dict[str, Any]] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = {key.lower(): value or "" for key, value in attrs}

        if self.skip_depth:
            if tag in SKIP_TAGS or tag == "div":
                self.skip_depth += 1
            return
        if tag in SKIP_TAGS:
            self.skip_depth = 1
            return
        if tag == "div" and "ez-toc" in f"{attributes.get('id', '')} {attributes.get('class', '')}".lower():
            self.skip_depth = 1
            return

        if tag == "img" and normalize_text(attributes.get("alt", "")):
            self.segments.append({"kind": "alt", "text": normalize_text(attributes["alt"])})
            return

        if tag == "meta":
            name = (attributes.get("name") or attributes.get("property") or "").lower()
            content = normalize_text(attributes.get("content", ""))
            if name in META_NAMES and content:
                self.segments.append({"kind": "metadata", "text": content})
            return

        if tag in BLOCK_TAGS:
            if self.stack:
                self.stack[-1]["has_child_block"] = True
            segment_kind = tag
            if attributes.get("data-naturalness-kind", "").lower() == "excerpt":
                segment_kind = "excerpt"
            self.stack.append(
                {"tag": tag, "kind": segment_kind, "text": [], "has_child_block": False}
            )

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.skip_depth:
            if tag in SKIP_TAGS or tag == "div":
                self.skip_depth -= 1
            return
        if tag not in BLOCK_TAGS or not self.stack:
            return

        context = self.stack.pop()
        if context["tag"] != tag:
            return
        text = normalize_text("".join(context["text"]))
        if text and not context["has_child_block"]:
            self.segments.append({"kind": context["kind"], "text": text})

    def handle_data(self, data: str) -> None:
        if self.skip_depth or not self.stack:
            return
        for context in self.stack:
            context["text"].append(data)


def extract_html_segments(source_html: str) -> list[dict[str, str]]:
    parser = SegmentParser()
    parser.feed(source_html)
    parser.close()
    return parser.segments


def build_document(
    source_html: str,
    *,
    title: str = "",
    excerpt: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    segments: list[dict[str, str]] = []
    if normalize_text(title):
        segments.append({"kind": "title", "text": normalize_text(title)})
    segments.extend(extract_html_segments(source_html))
    if normalize_text(excerpt):
        segments.append({"kind": "excerpt", "text": normalize_text(excerpt)})
    for key, value in (metadata or {}).items():
        if key in META_NAMES and isinstance(value, str) and normalize_text(value):
            segments.append({"kind": "metadata", "text": normalize_text(value)})

    normalized_segments = []
    for index, segment in enumerate(segments, start=1):
        text = normalize_text(segment["text"])
        normalized_segments.append(
            {
                "id": f"seg-{index:03d}",
                "kind": segment["kind"],
                "text": text,
                "hash": hash_text(f"{segment['kind']}\0{text}"),
            }
        )

    canonical = "\n".join(f"{segment['kind']}\0{segment['text']}" for segment in normalized_segments)
    return {
        "segments": normalized_segments,
        "content_hash": hash_text(canonical),
    }


def fetch_post(post_id: int) -> tuple[dict[str, Any], dict[str, Any]]:
    url = f"{SITE}/wp-json/wp/v2/posts/{post_id}?_fields=id,slug,status,title,content,excerpt,meta"
    request = urllib.request.Request(url, headers={"User-Agent": "digitrustlab-naturalness-check"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)

    title = data.get("title", {}).get("rendered", "")
    excerpt = data.get("excerpt", {}).get("rendered", "")
    document = build_document(
        data.get("content", {}).get("rendered", ""),
        title=title,
        excerpt=excerpt,
        metadata=data.get("meta") if isinstance(data.get("meta"), dict) else None,
    )
    return data, document


def load_rules(path: Path) -> dict[str, Any]:
    rules = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rules, dict) or rules.get("schema_version") != 1:
        raise ValueError("rules file must be an object with schema_version 1")
    for key in ("rejected_phrases", "approved_technical_terms", "context_dependent_terms", "approved_exceptions"):
        if not isinstance(rules.get(key), list):
            raise ValueError(f"rules file field '{key}' must be a list")
    return rules


def phrase_entries(rules: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return [entry for entry in rules[key] if isinstance(entry, dict) and normalize_text(str(entry.get("phrase", "")))]


def deterministic_findings(document: dict[str, Any], rules: dict[str, Any]) -> list[dict[str, Any]]:
    exceptions = {
        normalize_text(str(entry.get("phrase", ""))).casefold()
        for entry in rules.get("approved_exceptions", [])
        if isinstance(entry, dict) and entry.get("phrase")
    }
    findings: list[dict[str, Any]] = []
    for entry in phrase_entries(rules, "rejected_phrases"):
        phrase = normalize_text(str(entry["phrase"]))
        if phrase.casefold() in exceptions:
            continue
        for segment in document["segments"]:
            if phrase.casefold() in segment["text"].casefold():
                findings.append(
                    {
                        "code": "rejected-phrase",
                        "segment_id": segment["id"],
                        "kind": segment["kind"],
                        "phrase": phrase,
                        "preferred": entry.get("preferred", ""),
                        "detail": entry.get("rationale", "Confirmed naturalness regression."),
                    }
                )
    return findings


def review_issue(code: str, detail: str, **extra: Any) -> dict[str, Any]:
    return {"code": code, "detail": detail, **extra}


def validate_evaluation(evaluation: Any, reviewer_id: str, location: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not isinstance(evaluation, dict):
        return [review_issue("reviewer-entry-missing", f"{location}: missing evaluation for {reviewer_id}")]

    checks = evaluation.get("checks")
    if not isinstance(checks, dict):
        issues.append(review_issue("checks-missing", f"{location}: checks must be an object"))
    else:
        missing = [name for name in REQUIRED_CHECKS if name not in checks]
        failed = [name for name in REQUIRED_CHECKS if checks.get(name) is not True]
        if missing:
            issues.append(review_issue("checks-incomplete", f"{location}: missing {', '.join(missing)}"))
        if failed:
            issues.append(review_issue("check-failed", f"{location}: failed {', '.join(failed)}"))

    if evaluation.get("confidence") != "high":
        issues.append(review_issue("confidence-not-high", f"{location}: confidence must be high"))

    findings = evaluation.get("findings", [])
    if findings:
        issues.append(review_issue("reviewer-finding", f"{location}: unresolved reviewer findings remain"))
    return issues


def validate_review(
    document: dict[str, Any],
    review: dict[str, Any] | None,
    *,
    expected_post_id: int | None = None,
    expected_slug: str | None = None,
    source_status: str | None = None,
    require_published: bool = False,
) -> list[dict[str, Any]]:
    if review is None:
        return [review_issue("review-missing", "No naturalness review artifact was supplied.")]
    if not isinstance(review, dict):
        return [review_issue("review-invalid", "Review artifact must be a JSON object.")]

    issues: list[dict[str, Any]] = []
    if review.get("schema_version") != 2:
        issues.append(review_issue("schema-version", "Review artifact must use schema_version 2."))
    if review.get("status") != "pass":
        issues.append(review_issue("review-status", "Review artifact status must be pass."))
    if review.get("content_hash") != document["content_hash"]:
        issues.append(review_issue("content-hash", "Review content_hash does not match the supplied content."))
    if expected_post_id is not None and review.get("post_id") != expected_post_id:
        issues.append(review_issue("post-id", "Review artifact post_id does not match the live post."))
    if expected_slug is not None and review.get("slug") != expected_slug:
        issues.append(review_issue("post-slug", "Review artifact slug does not match the live post."))
    if require_published and source_status != "publish":
        issues.append(review_issue("post-status", "Live verification requires a published post."))

    reviewers = review.get("reviewers")
    if not isinstance(reviewers, list) or len(reviewers) != 2:
        issues.append(review_issue("reviewer-count", "Exactly two reviewer records are required: Claude and OpenAI."))
        reviewers = reviewers if isinstance(reviewers, list) else []

    reviewer_ids = []
    families = []
    for reviewer in reviewers:
        if not isinstance(reviewer, dict):
            issues.append(review_issue("reviewer-invalid", "Each reviewer record must be an object."))
            continue
        reviewer_id = str(reviewer.get("id", ""))
        family = normalize_text(str(reviewer.get("model_family", ""))).casefold()
        model = normalize_text(str(reviewer.get("model", "")))
        if not reviewer_id or not family or not model:
            issues.append(review_issue("reviewer-identity", "Each reviewer needs id, model_family, and model."))
        reviewer_ids.append(reviewer_id)
        families.append(family)
        if family not in REQUIRED_REVIEW_FAMILIES:
            issues.append(review_issue("reviewer-family", f"Reviewer {reviewer_id or '<unknown>'} must be Claude/Anthropic or OpenAI."))
    if len(set(reviewer_ids)) != len(reviewer_ids):
        issues.append(review_issue("reviewer-duplicate", "Reviewer IDs must be unique."))
    if not any(family in CLAUDE_FAMILIES for family in families):
        issues.append(review_issue("reviewer-coverage", "A Claude/Anthropic reviewer is required."))
    if "openai" not in families:
        issues.append(review_issue("reviewer-coverage", "An OpenAI reviewer is required."))
    document_review = review.get("document_review")
    if not isinstance(document_review, dict):
        issues.append(review_issue("document-review-missing", "Document-level review evidence is required."))
        document_review = {}
    for reviewer_id in reviewer_ids:
        issues.extend(validate_evaluation(document_review.get(reviewer_id), reviewer_id, "document_review"))

    artifact_segments = review.get("segments")
    if not isinstance(artifact_segments, list):
        issues.append(review_issue("segments-missing", "Segment-level review evidence is required."))
        artifact_segments = []
    by_id = {str(item.get("id")): item for item in artifact_segments if isinstance(item, dict) and item.get("id")}
    if len(by_id) != len(artifact_segments):
        issues.append(review_issue("segment-duplicate", "Segment IDs must be unique and non-empty."))

    expected_ids = {segment["id"] for segment in document["segments"]}
    actual_ids = set(by_id)
    for missing_id in sorted(expected_ids - actual_ids):
        issues.append(review_issue("segment-missing", f"Review has no evidence for {missing_id}."))
    for extra_id in sorted(actual_ids - expected_ids):
        issues.append(review_issue("segment-extra", f"Review contains unknown segment {extra_id}."))

    expected_by_id = {segment["id"]: segment for segment in document["segments"]}
    for segment_id, expected in expected_by_id.items():
        artifact = by_id.get(segment_id)
        if not artifact:
            continue
        if artifact.get("hash") != expected["hash"]:
            issues.append(review_issue("segment-hash", f"Review hash does not match {segment_id}."))
        evaluations = artifact.get("reviewers")
        if not isinstance(evaluations, dict):
            issues.append(review_issue("segment-reviewers-missing", f"{segment_id}: reviewer evidence is missing."))
            continue
        for reviewer_id in reviewer_ids:
            issues.extend(validate_evaluation(evaluations.get(reviewer_id), reviewer_id, segment_id))

    disagreements = review.get("disagreements", [])
    if disagreements:
        issues.append(review_issue("disagreement-unresolved", "Reviewers still disagree."))
    resolutions = review.get("human_resolutions", [])
    if any(isinstance(item, dict) and item.get("resolved") is not True for item in resolutions):
        issues.append(review_issue("human-resolution-unresolved", "A human resolution is still unresolved."))
    return issues


def evaluate(
    document: dict[str, Any],
    review: dict[str, Any] | None,
    rules: dict[str, Any],
    *,
    expected_post_id: int | None = None,
    expected_slug: str | None = None,
    source_status: str | None = None,
    require_published: bool = False,
) -> dict[str, Any]:
    deterministic = deterministic_findings(document, rules)
    review_issues = validate_review(
        document,
        review,
        expected_post_id=expected_post_id,
        expected_slug=expected_slug,
        source_status=source_status,
        require_published=require_published,
    )
    issues = [
        *[
            review_issue(
                finding["code"],
                f"{finding['kind']} {finding['segment_id']}: {finding['phrase']} -> {finding['preferred']}",
                finding=finding,
            )
            for finding in deterministic
        ],
        *review_issues,
    ]
    return {
        "passed": not issues,
        "content_hash": document["content_hash"],
        "segment_count": len(document["segments"]),
        "segment_manifest": [
            {"id": segment["id"], "kind": segment["kind"], "hash": segment["hash"]}
            for segment in document["segments"]
        ],
        "deterministic_findings": deterministic,
        "review_issues": review_issues,
        "issues": issues,
    }


def load_review(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def print_report(result: dict[str, Any], source_label: str) -> None:
    mark = "PASS" if result["passed"] else "BLOCKED"
    print(f"[{mark}] Malay naturalness gate — {source_label}")
    print(f"Content hash: {result['content_hash']}")
    print(f"Segments: {result['segment_count']}")
    if not result["issues"]:
        print("Two independent high-confidence reviews, Claude and OpenAI, and deterministic rules passed.")
        return
    for issue in result["issues"]:
        print(f"- {issue['code']}: {issue['detail']}")
    print("Publication must remain blocked until every issue is resolved and reviewed again.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="Final HTML file to validate")
    source.add_argument("--post-id", type=int, help="Published WordPress post ID to validate")
    parser.add_argument("--review", type=Path, required=True, help="Naturalness review JSON artifact")
    parser.add_argument("--rules", type=Path, default=RULES_PATH, help="Naturalness rules JSON")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args(argv)

    try:
        rules = load_rules(args.rules)
        if args.file:
            raw = args.file.read_text(encoding="utf-8")
            document = build_document(raw)
            source_label = str(args.file)
        else:
            data, document = fetch_post(args.post_id)
            source_label = f"post {data.get('id', args.post_id)} ({data.get('slug', '')})"
        review = load_review(args.review)
    except FileNotFoundError as exc:
        print(f"Configuration/source file not found: {exc}", file=sys.stderr)
        return 2
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError, TimeoutError) as exc:
        print(f"Could not load naturalness gate input: {exc}", file=sys.stderr)
        return 2

    evaluation_options: dict[str, Any] = {}
    if args.post_id:
        evaluation_options = {
            "expected_post_id": data.get("id"),
            "expected_slug": data.get("slug"),
            "source_status": data.get("status"),
            "require_published": True,
        }
    result = evaluate(document, review, rules, **evaluation_options)
    if args.json:
        print(json.dumps({"source": source_label, **result}, ensure_ascii=False, indent=2))
    else:
        print_report(result, source_label)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
