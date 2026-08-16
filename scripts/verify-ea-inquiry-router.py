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
RUNTIME_AUDIT = ROOT / "scripts" / "verify-ea-router-runtime.py"
EA_SKILL_NAMES = ("inquiry-router", "referral-triage", "daily-brief", "meeting-prep")
EA_SKILL_ROOT = ROOT / "workspaces" / "executive-assistant" / "skills"
CLAUDE_SKILL_ROOT = ROOT / ".claude" / "skills"
WINDSURF_SKILL_ROOT = ROOT / ".windsurf" / "skills"
EA_ROUTER_POINTER = "workspaces/executive-assistant/skills/inquiry-router/SKILL.md"

DEPARTMENTS = ("content", "seo", "operations", "research", "creative")
OVERRIDE = re.compile(r"\bdepartment\s*:\s*(content|seo|operations|research|creative)\b", re.I)
EXTERNAL_ARTIFACT = re.compile(r"(?:https?://|www\.|github\.com/|gitlab\.com/|bitbucket\.org/)", re.I)
JUDGMENT_REQUEST = re.compile(
    r"(?:\b(?:is|are|was|were)\s+(?:this|that|it|they)\s+(?:a\s+)?"
    r"(?:good|better|best|suitable|appropriate|worth|safe|reliable|useful)\b"
    r"|\bshould\s+(?:we|i|you)\b"
    r"|\b(?:recommend|advise|evaluate|assess|compare|review)\b"
    r"|\b(?:what(?:'s| is)\s+your|give\s+me\s+your|need\s+your)\s+"
    r"(?:advice|opinion|thoughts?|recommendation)\b)",
    re.I,
)


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
    substantive = (
        "draft", "audit", "research", "generate", "fix", "publish", "implement",
        "analyze", "compare", "deploy", "create", "advice", "recommend",
        "opinion", "thought", "should", "strategy", "suitable", "fit", "belongs",
        "adopt", "install", "integrate", "integration", "repository", "repo",
        "github", "skill", "provider", "model", "plugin", "package", "external",
        "architecture", "policy",
    )
    return (
        len(text) <= 90
        and text.endswith("?")
        and not any(word in text for word in substantive)
        and not EXTERNAL_ARTIFACT.search(text)
        and not JUDGMENT_REQUEST.search(text)
    )


def frontmatter_value(text: str, key: str) -> str | None:
    """Read a simple single-line frontmatter field from a SKILL.md file."""
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(\S.*)\s*$", text)
    return match.group(1).strip() if match else None


def verify_skill_discovery(failures: list[str]) -> None:
    """Ensure Claude has thin bridges while EA skills retain one canonical source."""
    for name in EA_SKILL_NAMES:
        canonical = EA_SKILL_ROOT / name / "SKILL.md"
        claude_dir = CLAUDE_SKILL_ROOT / name
        claude_skill = claude_dir / "SKILL.md"
        windsurf_path = WINDSURF_SKILL_ROOT / name

        if not canonical.is_file():
            failures.append(f"missing canonical EA skill: {canonical}")
            canonical_name = None
            canonical_description = None
        else:
            canonical_text = canonical.read_text(encoding="utf-8")
            canonical_name = frontmatter_value(canonical_text, "name")
            canonical_description = frontmatter_value(canonical_text, "description")
            if canonical_name != name:
                failures.append(f"canonical EA skill name does not match directory: {canonical}")
            if canonical_description is None:
                failures.append(f"canonical EA skill missing description: {canonical}")
        if not claude_skill.is_file():
            failures.append(f"missing Claude EA skill path: {claude_skill}")
        elif claude_dir.is_symlink():
            failures.append(f"Claude EA skill bridge must be a real directory: {claude_dir}")
        else:
            bridge = claude_skill.read_text(encoding="utf-8")
            bridge_name = frontmatter_value(bridge, "name")
            bridge_description = frontmatter_value(bridge, "description")
            canonical_pointer = f"workspaces/executive-assistant/skills/{name}/SKILL.md"
            if bridge_name != name:
                failures.append(f"Claude EA bridge has mismatched name: {claude_skill}")
            if bridge_description is None:
                failures.append(f"Claude EA bridge missing description: {claude_skill}")
            elif canonical_description is not None and bridge_description != canonical_description:
                failures.append(f"Claude EA bridge description differs from canonical skill: {claude_skill}")
            if canonical_pointer.lower() not in bridge.lower():
                failures.append(f"Claude EA bridge missing canonical pointer: {claude_skill}")
            if len(bridge.splitlines()) > 20:
                failures.append(f"Claude EA bridge is too large; keep procedures canonical: {claude_skill}")
            if re.search(r"(?mi)^\s*#{1,3}\s+(route contract|procedure|steps?)\b", bridge):
                failures.append(f"Claude EA bridge duplicates a route/procedure section: {claude_skill}")

        if windsurf_path.exists() or windsurf_path.is_symlink():
            failures.append(f"EA skill must not be present in shared .windsurf/skills: {windsurf_path}")


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
        "router contract version: 2026-08-16",
        "emit a route receipt as the first assistant output",
        "precede every tool call",
        "after compaction, context reset",
        "carry the route receipt into every worker brief",
        "actual model id and effort",
        "verify-ea-router-runtime.py",
        "asks for advice, comparison",
        "external repository, url, tool, provider",
        "plan this first",
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

    discovery_failures = []
    verify_skill_discovery(discovery_failures)
    root_agents = ROOT_AGENTS.read_text(encoding="utf-8") if ROOT_AGENTS.is_file() else ""
    tier1_start = root_agents.lower().find("### tier 1")
    tier2_start = root_agents.lower().find("### tier 2")
    if tier1_start == -1:
        discovery_failures.append("root AGENTS.md is missing the Tier 1 heading")
    if tier2_start == -1:
        discovery_failures.append("root AGENTS.md is missing the Tier 2 heading")
    if tier1_start != -1 and tier2_start != -1 and tier2_start <= tier1_start:
        discovery_failures.append("root AGENTS.md Tier 2 heading appears before Tier 1")
    tier1 = root_agents[tier1_start:tier2_start] if tier1_start != -1 and tier2_start > tier1_start else ""
    if EA_ROUTER_POINTER.lower() not in tier1.lower():
        discovery_failures.append("EA router pointer is not in the root AGENTS.md Tier 1 table")
    failures.extend(discovery_failures)
    if not RUNTIME_AUDIT.is_file():
        failures.append(f"missing runtime router audit: {RUNTIME_AUDIT}")
    else:
        runtime_text = RUNTIME_AUDIT.read_text(encoding="utf-8").lower()
        for phrase in ("--session-log", "--self-test", "route id", "first tool", "freshness"):
            if phrase not in runtime_text:
                failures.append(f"runtime router audit missing contract check: {phrase}")
    if not discovery_failures:
        print("PASS EA skill discovery: 4 thin Claude bridges point to canonical skills; Codex Tier 1 router pointer present; no .windsurf collisions")

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
    external_evaluation = (
        "I want your advice: https://github.com/keemanxp/dbp-translator-claude.git "
        "is it a good one to integrate into Content? Plan this first?"
    )
    if not is_simple_question(simple) or is_simple_question(substantive) or is_simple_question(external_evaluation):
        failures.append("simple/substantive worker gate is not deterministic")
    if is_simple_question(simple):
        print("PASS no worker for simple one-step question")
    if not is_simple_question(substantive):
        print("PASS bounded worker required for substantive request")
    if not is_simple_question(external_evaluation):
        print("PASS external artifact/judgment request requires bounded worker")

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
