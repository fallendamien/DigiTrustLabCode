#!/usr/bin/env python3
"""Audit a Codex/Claude JSONL transcript for the EA router turn gate.

This is deliberately a fail-closed audit, not a tool-permission mechanism.
It checks the observable transcript contract: a substantive user turn must
receive a complete route receipt before its first tool/delegation call, and the
receipt must use the current router contract version.

``--project-root`` lets an invocation from a project directory resolve the
router SKILL.md and policy files from that project root instead of from the
two-levels-up default.  Omit it when invoking from within the canonical skill
location (the default keeps behaviour identical to before this flag existed).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "workspaces" / "executive-assistant" / "skills" / "inquiry-router" / "SKILL.md"
DEPARTMENTS = {"content", "seo", "operations", "research", "creative"}
ROUTE_RE = re.compile(
    r"(?im)^Route:\s*primary=(?P<primary>[a-z-]+);\s*secondary=(?P<secondary>.+?)\s*$"
)
FIELD_RE = {
    name: re.compile(rf"(?im)^{re.escape(name)}:\s*(?P<value>.+?)\s*$")
    for name in ("Route ID", "Router version", "Scope", "Allowed systems", "External writes")
}
VERSION_RE = re.compile(r"(?im)^Router contract version:\s*(?P<version>\S+)\s*$")
SUBSTANTIVE_TERMS = (
    "plan", "draft", "edit", "fix", "audit", "research", "generate", "implement",
    "publish", "analyze", "analyse", "compare", "deploy", "verify", "troubleshoot",
    "replace", "upload", "create", "write", "keyword", "writerzen", "wordpress",
    "image", "seo", "ranking", "indexing", "content", "router", "workflow",
)
BOOTSTRAP_MARKERS = (
    "<recommended_plugins>", "<app-context>", "<skills_instructions>",
    "<permissions instructions>", "# agents.md", "<instructions>",
)
ACTION_TYPES = {"function_call", "custom_tool_call", "computer_call", "mcp_tool_call", "tool_call"}


@dataclass(frozen=True)
class Event:
    index: int
    kind: str
    text: str = ""
    payload: dict[str, Any] | None = None


@dataclass(frozen=True)
class Receipt:
    index: int
    primary: str
    secondary: str
    route_id: str
    version: str
    scope: str
    allowed_systems: str
    external_writes: str
    handoff: str = ""


def content_text(content: Any) -> str:
    """Extract visible text from a response_item content array."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            value = item.get("text") or item.get("value")
            if isinstance(value, str):
                parts.append(value)
    return "\n".join(parts)


def router_version(router: Path = ROUTER) -> str:
    if not router.is_file():
        return ""
    match = VERSION_RE.search(router.read_text(encoding="utf-8"))
    return match.group("version").strip() if match else ""


def is_bootstrap_instruction(text: str) -> bool:
    head = text.lstrip().lower()[:600]
    return any(marker in head for marker in BOOTSTRAP_MARKERS)


def is_substantive_user(text: str) -> bool:
    if not text.strip() or is_bootstrap_instruction(text):
        return False
    lowered = text.lower()
    return any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in SUBSTANTIVE_TERMS)


def parse_receipt(index: int, text: str) -> tuple[Receipt | None, list[str]]:
    route = ROUTE_RE.search(text)
    if not route:
        return None, ["missing Route line"]
    primary = route.group("primary").lower()
    secondary = route.group("secondary").strip()
    failures: list[str] = []
    if primary not in DEPARTMENTS:
        failures.append(f"invalid primary department: {primary}")
    if secondary.lower() == "none":
        normalized_secondary = "none"
    else:
        normalized_secondary = secondary
        if not re.search(r"(?im)^Handoff(?: / approval)?:\s*\S", text):
            failures.append("non-none secondary lacks a concrete Handoff / approval line")

    values: dict[str, str] = {}
    for name, pattern in FIELD_RE.items():
        match = pattern.search(text)
        if not match:
            failures.append(f"missing {name} field")
        else:
            values[name] = match.group("value").strip()
    if values.get("External writes", "").lower() not in {"yes", "no"}:
        failures.append("External writes must be yes or no")

    receipt = Receipt(
        index=index,
        primary=primary,
        secondary=normalized_secondary,
        route_id=values.get("Route ID", ""),
        version=values.get("Router version", ""),
        scope=values.get("Scope", ""),
        allowed_systems=values.get("Allowed systems", ""),
        external_writes=values.get("External writes", ""),
    )
    for label, value in (("Route ID", receipt.route_id), ("Router version", receipt.version),
                         ("Scope", receipt.scope), ("Allowed systems", receipt.allowed_systems)):
        if not value or value.startswith("<"):
            failures.append(f"{label} is empty or still a placeholder")
    return receipt, failures


def iter_events(path: Path) -> tuple[list[Event], datetime | None]:
    events: list[Event] = []
    session_start: datetime | None = None
    for index, raw in enumerate(path.read_text(encoding="utf-8").splitlines()):
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            events.append(Event(index, "malformed"))
            continue
        if record.get("type") == "session_meta":
            timestamp = (record.get("payload") or {}).get("timestamp")
            if isinstance(timestamp, str):
                try:
                    session_start = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                except ValueError:
                    pass
            continue
        if record.get("type") != "response_item":
            continue
        payload = record.get("payload") or {}
        payload_type = payload.get("type")
        role = payload.get("role")
        if payload_type == "message" and role == "user":
            events.append(Event(index, "user", content_text(payload.get("content")), payload))
        elif payload_type == "message" and role == "assistant":
            events.append(Event(index, "assistant", content_text(payload.get("content")), payload))
        elif payload_type in ACTION_TYPES:
            events.append(Event(index, "action", payload=payload))
    return events, session_start


def freshness_required(
    session_start: datetime | None,
    *,
    disabled: bool,
    router: Path = ROUTER,
    root: Path = ROOT,
) -> bool:
    if disabled or session_start is None:
        return False
    try:
        router_mtime = datetime.fromtimestamp(router.stat().st_mtime, tz=timezone.utc)
        root_mtime = datetime.fromtimestamp((root / "AGENTS.md").stat().st_mtime, tz=timezone.utc)
    except OSError:
        return True
    start = session_start.astimezone(timezone.utc)
    return router_mtime > start or root_mtime > start


def audit_events(events: list[Event], expected_version: str, *, freshness: bool) -> list[str]:
    failures: list[str] = []
    users = [event for event in events if event.kind == "user" and is_substantive_user(event.text)]
    if not users:
        return ["no substantive user turns were observable in the transcript"]

    for turn_no, user in enumerate(users, 1):
        next_user_index = next((candidate.index for candidate in users if candidate.index > user.index), None)
        window = [event for event in events if event.index > user.index and (next_user_index is None or event.index < next_user_index)]
        first_assistant = next((event for event in window if event.kind == "assistant"), None)
        first_action = next((event for event in window if event.kind == "action"), None)
        label = f"turn {turn_no} (log line {user.index})"
        if first_assistant is None:
            failures.append(f"{label}: no observable assistant route receipt")
            continue
        receipt, receipt_failures = parse_receipt(first_assistant.index, first_assistant.text)
        if receipt is None or receipt_failures:
            for failure in receipt_failures:
                failures.append(f"{label}: {failure}")
            continue
        if first_action is not None and first_action.index < first_assistant.index:
            failures.append(f"{label}: tool/delegation occurred before the route receipt")
        if expected_version and receipt.version != expected_version:
            failures.append(f"{label}: stale Router version {receipt.version!r}; expected {expected_version!r}")
        if freshness and receipt.version != expected_version:
            failures.append(f"{label}: router/policy files changed after session start; fresh receipt required")
    return failures


def synthetic_events(version: str, *, malformed: bool = False) -> list[Event]:
    receipt = (
        "Route: primary=operations; secondary=none\n"
        "Route ID: self-test-turn-1\n"
        f"Router version: {version}\n"
        "Scope: verify the transcript gate only; stop after the audit\n"
        "Allowed systems: repository scripts and synthetic records only\n"
        "External writes: no\n"
    )
    if malformed:
        receipt = "Route: primary=operations; secondary=none\n"
    return [
        Event(1, "user", "Please audit the router gate."),
        Event(2, "assistant", receipt),
        Event(3, "action", payload={"type": "custom_tool_call", "name": "read_only_check"}),
    ]


def run_self_test() -> int:
    version = router_version() or "2026-08-16"
    good = audit_events(synthetic_events(version), version, freshness=False)
    bad = audit_events(synthetic_events(version, malformed=True), version, freshness=False)
    if good or not bad:
        print(f"FAIL EA router runtime self-test: good={good!r}, malformed={bad!r}")
        return 1
    print("PASS EA router runtime self-test: receipt ordering, fields, and malformed-receipt failure")
    return 0


def resolve_router(project_root: Path | None) -> tuple[Path, Path]:
    """Return (effective_router, effective_root) for the given project root.

    When *project_root* is None the canonical TSOT paths are used (default
    behaviour — resolves relative to this script's own location).  When
    supplied, the router is resolved from that project directory first at
    ``workspaces/executive-assistant/skills/inquiry-router/SKILL.md``, then
    falling back to ``.windsurf/skills/inquiry-router/SKILL.md`` for projects
    that still expose the skill through the shared symlink tree.
    """
    if project_root is None:
        return ROUTER, ROOT
    pr = project_root.resolve()
    candidate = pr / "workspaces" / "executive-assistant" / "skills" / "inquiry-router" / "SKILL.md"
    if not candidate.is_file():
        candidate = pr / ".windsurf" / "skills" / "inquiry-router" / "SKILL.md"
    return candidate, pr


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-log", type=Path, help="Codex/Claude JSONL session log to audit")
    parser.add_argument("--self-test", action="store_true", help="run deterministic in-memory checks")
    parser.add_argument("--no-freshness", action="store_true", help="skip file-mtime freshness check")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "project root whose router SKILL.md and policy files define the expected version; "
            "defaults to the repo root two levels up from this script"
        ),
    )
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if not args.session_log:
        parser.error("--session-log is required unless --self-test is used")
    if not args.session_log.is_file():
        print(f"FAIL EA router runtime: missing session log {args.session_log}")
        return 1
    effective_router, effective_root = resolve_router(args.project_root)
    if not effective_router.is_file():
        print(f"FAIL EA router runtime: router SKILL.md not found (tried {effective_router})")
        return 1
    events, session_start = iter_events(args.session_log)
    expected_version = router_version(effective_router)
    if not expected_version:
        print("FAIL EA router runtime: router contract version is missing")
        return 1
    failures = audit_events(
        events,
        expected_version,
        freshness=freshness_required(
            session_start,
            disabled=args.no_freshness,
            router=effective_router,
            root=effective_root,
        ),
    )
    if failures:
        print("FAIL EA router runtime:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    substantive = sum(event.kind == "user" and is_substantive_user(event.text) for event in events)
    print(f"PASS EA router runtime: {substantive} substantive turn(s) have current receipts before actions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
