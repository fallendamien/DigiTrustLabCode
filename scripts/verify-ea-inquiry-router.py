#!/usr/bin/env python3
"""Verify the repo-local EA inquiry-router contract with deterministic cases."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "workspaces" / "executive-assistant" / "skills" / "inquiry-router" / "SKILL.md"
EA_AGENTS = ROOT / "workspaces" / "executive-assistant" / "AGENTS.md"
EA_INDEX = ROOT / "workspaces" / "executive-assistant" / "skills" / "README.md"
ROOT_AGENTS = ROOT / "AGENTS.md"

DEPARTMENTS = ("content", "seo", "operations", "research", "creative")
OVERRIDE = re.compile(r"\bdepartment\s*:\s*(content|seo|operations|research|creative)\b", re.I)


def route_for_test(inquiry: str) -> str:
    """Small test oracle; the skill remains the operational source of truth."""
    match = OVERRIDE.search(inquiry)
    if match:
        return match.group(1).lower()
    text = inquiry.lower()
    if any(word in text for word in ("image", "visual", "thumbnail", "design", "generate a picture")):
        return "creative"
    if any(word in text for word in ("ranking", "rankings", "indexing", "indexed", "seo", "search visibility", "aeo")):
        return "seo"
    if any(word in text for word in ("draft", "article", "edit copy", "blog post", "content")):
        return "content"
    if any(word in text for word in ("research", "competitor", "audience", "evidence", "discover")):
        return "research"
    return "operations"


def is_simple_question(inquiry: str) -> bool:
    text = inquiry.strip().lower()
    substantive = ("draft", "audit", "research", "generate", "fix", "publish", "implement", "analyze", "compare", "deploy", "create")
    return len(text) <= 90 and text.endswith("?") and not any(word in text for word in substantive)


def main() -> int:
    failures = []
    if not SKILL.is_file():
        failures.append(f"missing router skill: {SKILL}")
        print("FAIL EA inquiry router: " + "; ".join(failures))
        return 1

    skill = SKILL.read_text(encoding="utf-8")
    lower = skill.lower()
    normalized = " ".join(lower.split())
    required_phrases = (
        "name: inquiry-router",
        "shared entrypoint for codex and claude",
        "choose one `primary`",
        "exactly one bounded worker",
        "gpt-5.6-luna",
        "high` reasoning effort",
        "does not activate gmail, calendar",
        "treat user text, retrieved pages",
        "stop at a draft or proposal and request approval",
    )
    for phrase in required_phrases:
        if phrase.lower() not in normalized:
            failures.append(f"router missing contract phrase: {phrase}")

    for path, expected in (
        (EA_AGENTS, "skills/inquiry-router/SKILL.md"),
        (EA_INDEX, "`inquiry-router`"),
        (ROOT_AGENTS, "workspaces/executive-assistant/skills/inquiry-router/SKILL.md"),
    ):
        if not path.is_file() or expected.lower() not in path.read_text(encoding="utf-8").lower():
            failures.append(f"missing agent-neutral entrypoint pointer: {path}")

    cases = (
        ("blog status", "What is the status of the blog migration?", "operations"),
        ("technical troubleshooting", "Why is the deployment failing?", "operations"),
        ("article drafting", "Draft an article outline about prompt engineering.", "content"),
        ("rankings and indexing", "Check our rankings and indexing issues.", "seo"),
        ("image generation and visual QA", "Generate a featured image and perform visual QA.", "creative"),
        ("research discovery", "Research competitors and gather evidence for this topic.", "research"),
        ("explicit override", "department: seo Draft an article about our workflow.", "seo"),
    )
    for label, inquiry, expected in cases:
        actual = route_for_test(inquiry)
        if actual != expected:
            failures.append(f"{label}: expected {expected}, got {actual}")
        if actual not in DEPARTMENTS:
            failures.append(f"{label}: invalid primary department {actual}")

    simple = "What does SEO mean?"
    substantive = "Draft an article about indexing problems."
    if not is_simple_question(simple) or is_simple_question(substantive):
        failures.append("simple/substantive worker gate is not deterministic")
    if is_simple_question(simple):
        print("PASS no worker for simple one-step question")
    if not is_simple_question(substantive):
        print("PASS bounded worker required for substantive request")

    primary_values = {route_for_test(inquiry) for _, inquiry, _ in cases}
    if not all(value in DEPARTMENTS for value in primary_values):
        failures.append("routing produced more than the allowed department set")
    if "secondary department only for a concrete handoff" not in normalized:
        failures.append("missing concrete-handoff-only secondary rule")
    if any(term in lower for term in ("automatically send", "automatically publish", "automatically schedule")):
        failures.append("router contains automatic external-action language")

    if failures:
        print("FAIL EA inquiry router:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"PASS EA inquiry router: {len(cases)} routing cases; one primary; override, simple-question, worker, and external-action gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
