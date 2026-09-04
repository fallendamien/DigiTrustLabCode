#!/usr/bin/env python3
"""Audit a Codex/Claude JSONL transcript for the EA router turn gate.

This is deliberately a fail-closed audit, not a tool-permission mechanism.
It checks the observable transcript contract for the active two-lane model:
fast-lane turns may execute directly, while guarded turns require a complete
current route receipt, required approval, and bounded-worker action. A project
root marker restores the legacy strict behavior for all substantive turns.

``--project-root`` lets an invocation from a project directory resolve the
router SKILL.md and policy files from that project root instead of from the
two-levels-up default. Omit it when invoking from within the canonical skill
location.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import tempfile
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
STRICT_MODE_RE = re.compile(r"(?m)^orchestration_mode: strict$")
GUARDED_RE = re.compile(
    r"(?ix)\b(?:push|publish|deploy|upload|send|delete|remove|reset|credential|"
    r"permission|live\s+(?:site|system)|external\s+write|history\s+rewrite|"
    r"destructive|irreversible|broad|independent(?:ly)?\s+review|production)\b"
)
APPROVAL_REQUIRED_RE = re.compile(
    r"(?ix)\b(?:push|publish|deploy|upload|send|delete|remove|reset|credential|"
    r"permission|live\s+(?:site|system)|external\s+write|history\s+rewrite|"
    r"purchase|payment|transfer)\b"
)
APPROVAL_FIELD_RE = re.compile(
    r"(?im)^(?:Handoff\s*/\s*approval|Approval):\s*(?P<value>.+?)\s*$"
)
# ROUTE_RE/FIELD_RE are deliberately line-anchored (^...$) so a receipt with a
# truncated or missing field is caught rather than silently glossed over. Some
# assistant messages render an otherwise-complete receipt as a SINGLE physical
# line, joining fields with a middle-dot separator instead of one field per
# line (e.g. "Route: primary=operations; secondary=none · Route ID: ... ·
# Router version: ..."). Without normalizing that into one field per line
# first, the line-anchored regexes cannot see "Route ID:", "Router version:",
# etc. mid-line, and a genuinely complete receipt gets reported as missing
# every field. Splitting only immediately before a recognized field label
# keeps this from ever touching an unrelated middle dot in ordinary prose.
RECEIPT_FIELD_LABELS = (
    "Route ID", "Router version", "Scope", "Allowed systems", "External writes",
    "Handoff / approval", "Handoff",
)
INLINE_RECEIPT_SEPARATOR_RE = re.compile(
    r"[ \t]*(?:·|–|—|-{2,})[ \t]*(?=(?:"
    + "|".join(re.escape(label) for label in RECEIPT_FIELD_LABELS)
    + r")\s*:)"
)


def normalize_receipt_text(text: str) -> str:
    """Split an inline single-line receipt into one field per line.

    Only splits immediately before a recognized field label, so this never
    rewrites ordinary prose that happens to contain a middle dot or em dash.
    """
    return INLINE_RECEIPT_SEPARATOR_RE.sub("\n", text)
SUBSTANTIVE_TERMS = (
    "plan", "draft", "edit", "fix", "audit", "research", "generate", "implement",
    "publish", "analyze", "analyse", "compare", "deploy", "verify", "troubleshoot",
    "replace", "upload", "create", "write", "keyword", "writerzen", "wordpress",
    "image", "seo", "ranking", "indexing", "content", "router", "workflow",
    "advice", "recommend", "recommendation", "opinion", "thought", "should",
    "strategy", "suitable", "fit", "belongs", "adopt", "install", "integrate",
    "integration", "repository", "repo", "github", "skill", "provider", "model",
    "plugin", "package", "external", "architecture", "policy",
)
# These patterns close the gap between a keyword-only audit and the policy's
# judgment gate.  In particular, an external URL or a recommendation about an
# artifact is substantive even when the user says "just advice" or "plan this
# first".  Keep this conservative: ordinary greetings and one-step how-to
# questions should remain direct-answer eligible.
EXTERNAL_ARTIFACT_RE = re.compile(
    r"(?ix)"
    r"(?:https?://|www\.|github\.com/|gitlab\.com/|bitbucket\.org/)"
)
JUDGMENT_RE = re.compile(
    r"(?ix)"
    r"(?:"
    r"\b(?:is|are|was|were)\s+(?:this|that|it|they)\s+(?:a\s+)?"
    r"(?:good|better|best|suitable|appropriate|worth|safe|reliable|useful)\b"
    r"|\bshould\s+(?:we|i|you)\b"
    r"|\b(?:would|could)\b[^\n.!?]{0,100}\b(?:integrat\w*|adopt\w*|install\w*|use|add)\b"
    r"|\b(?:what(?:'s| is)\s+your|give\s+me\s+your|need\s+your)\s+"
    r"(?:advice|opinion|thoughts?|recommendation)\b"
    r"|\b(?:recommend|advise|evaluate|assess|compare|review)\b[^\n.!?]{0,100}"
    r"\b(?:repo(?:sitory)?|tool|provider|model|skill|plugin|package|library|integration)\b"
    r")"
)
WORKER_ACTION_RE = re.compile(
    r"(?i)(?:spawn_agent|create_thread|handoff_thread|delegate(?:_task)?|subagent)"
)
BOOTSTRAP_MARKERS = (
    "<recommended_plugins>", "<app-context>", "<skills_instructions>",
    "<permissions instructions>", "# agents.md", "<instructions>",
)
ACTION_TYPES = {"function_call", "custom_tool_call", "computer_call", "mcp_tool_call", "tool_call"}

# --- Claude Code transcript support --------------------------------------
#
# Claude Code writes a different JSONL shape than Codex: top-level records
# tagged "user" / "assistant" with a nested "message" object, rather than
# Codex's "response_item" envelope. Tool calls arrive as "tool_use" blocks
# embedded inside an assistant message's content array, and tool *results*
# come back as a record tagged "user" whose content is entirely "tool_result"
# blocks -- those are not genuine human turns and must never be counted as
# one (the trap that produced false "no substantive user turns" failures).
CLAUDE_TEXT_BLOCK = "text"
CLAUDE_TOOL_USE_BLOCK = "tool_use"
CLAUDE_TOOL_RESULT_BLOCK = "tool_result"


@dataclass(frozen=True)
class Event:
    index: int
    kind: str
    text: str = ""
    payload: dict[str, Any] | None = None
    # Human-readable JSONL line number for display/labels. Codex events leave
    # this None and fall back to ``index`` (unchanged behaviour -- Codex uses
    # one event per line, so index already equals the line number). Claude
    # events set this explicitly because ``index`` there is scaled
    # (line_no * 1000 + sub-position) to preserve intra-message block order.
    line: int | None = None

    @property
    def display_line(self) -> int:
        return self.index if self.line is None else self.line


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


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def claude_user_text(content: Any) -> str | None:
    """Extract genuine human text from a Claude 'user' record's content.

    Returns ``None`` when the record carries no genuine human content -- most
    importantly, a record whose content is entirely ``tool_result`` blocks
    (a tool's return value, echoed back as a "user" record). Those are not
    real user turns and must not be counted as substantive turns.
    """
    if isinstance(content, str):
        return content
    if not isinstance(content, list) or not content:
        return None
    parts: list[str] = []
    saw_human_block = False
    for item in content:
        if isinstance(item, str):
            saw_human_block = True
            parts.append(item)
            continue
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == CLAUDE_TOOL_RESULT_BLOCK:
            continue
        saw_human_block = True
        if item_type == CLAUDE_TEXT_BLOCK and isinstance(item.get("text"), str):
            parts.append(item["text"])
        # Other block types (e.g. "image") carry no text but still prove this
        # is a genuine human turn, not a pure tool-result echo.
    if not saw_human_block:
        return None
    return "\n".join(parts)


def claude_events_from_assistant(line_no: int, content: Any) -> list[Event]:
    """Convert a Claude assistant message's content blocks into Events.

    Text blocks become "assistant" events; ``tool_use`` blocks become "action"
    events. Each is positioned immediately after the text that preceded it in
    the same message so the receipt-before-first-tool-call ordering check
    evaluates correctly against the actual block order. "thinking" blocks are
    internal reasoning, never a visible route receipt, and are ignored.
    """
    if not isinstance(content, list):
        return []
    events: list[Event] = []
    text_parts: list[str] = []
    sub = 0

    def flush_text() -> None:
        nonlocal sub
        if text_parts:
            events.append(Event(line_no * 1000 + sub, "assistant", "\n".join(text_parts), line=line_no))
            sub += 1
            text_parts.clear()

    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == CLAUDE_TEXT_BLOCK and isinstance(item.get("text"), str):
            text_parts.append(item["text"])
        elif item_type == CLAUDE_TOOL_USE_BLOCK:
            flush_text()
            events.append(Event(line_no * 1000 + sub, "action", payload=item, line=line_no))
            sub += 1
        # other block types (e.g. "thinking") carry no receipt/action signal
    flush_text()
    return events


def claude_events_from_line(line_no: int, record: dict[str, Any]) -> list[Event]:
    record_type = record.get("type")
    message = record.get("message") or {}
    if record_type == "user":
        text = claude_user_text(message.get("content"))
        if text is None:
            return []
        return [Event(line_no * 1000, "user", text, line=line_no)]
    if record_type == "assistant":
        return claude_events_from_assistant(line_no, message.get("content"))
    return []


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
    return (
        any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in SUBSTANTIVE_TERMS)
        or bool(EXTERNAL_ARTIFACT_RE.search(text))
        or bool(JUDGMENT_RE.search(text))
    )


def action_text(event: Event) -> str:
    """Serialize observable action metadata for worker-dispatch auditing."""
    if not event.payload:
        return ""
    return json.dumps(event.payload, ensure_ascii=False).lower()


def is_worker_action(event: Event) -> bool:
    if event.kind != "action":
        return False
    payload = event.payload or {}
    action_fields = " ".join(
        str(payload.get(key, ""))
        for key in ("name", "tool_name", "function", "function_name", "action", "command")
    )
    return bool(WORKER_ACTION_RE.search(action_fields))


def parse_receipt(index: int, text: str) -> tuple[Receipt | None, list[str]]:
    text = normalize_receipt_text(text)
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

    handoff_match = APPROVAL_FIELD_RE.search(text)
    handoff = handoff_match.group("value").strip() if handoff_match else ""
    receipt = Receipt(
        index=index,
        primary=primary,
        secondary=normalized_secondary,
        route_id=values.get("Route ID", ""),
        version=values.get("Router version", ""),
        scope=values.get("Scope", ""),
        allowed_systems=values.get("Allowed systems", ""),
        external_writes=values.get("External writes", ""),
        handoff=handoff,
    )
    for label, value in (("Route ID", receipt.route_id), ("Router version", receipt.version),
                         ("Scope", receipt.scope), ("Allowed systems", receipt.allowed_systems)):
        if not value or value.startswith("<"):
            failures.append(f"{label} is empty or still a placeholder")
    return receipt, failures


def is_guarded_user(text: str) -> bool:
    """Return whether the user request contains a guarded-lane trigger."""
    return bool(GUARDED_RE.search(text))


def requires_approval(text: str) -> bool:
    """Return whether the request crosses an explicit approval boundary."""
    return bool(APPROVAL_REQUIRED_RE.search(text))


def project_is_strict(project_root: Path = ROOT) -> bool:
    """Return whether the project opts into legacy strict orchestration."""
    agents = project_root / "AGENTS.md"
    if not agents.is_file():
        return False
    return bool(STRICT_MODE_RE.search(agents.read_text(encoding="utf-8")))


def run_project_mode_self_tests() -> list[str]:
    """Prove that the exact root marker selects strict mode and absence does not."""
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "AGENTS.md").write_text("# default project\n", encoding="utf-8")
        if project_is_strict(root):
            failures.append("default project incorrectly selected strict mode")
        (root / "AGENTS.md").write_text(
            "# strict project\n\norchestration_mode: strict\n", encoding="utf-8"
        )
        if not project_is_strict(root):
            failures.append("exact strict marker did not select strict mode")
    return failures


def iter_events(path: Path) -> tuple[list[Event], datetime | None]:
    events: list[Event] = []
    session_start: datetime | None = None
    earliest_claude_timestamp: datetime | None = None
    # start=1: JSONL line numbers are conventionally 1-based (what a human
    # sees in an editor / grep -n). enumerate() defaults to 0-based, which
    # silently shifted every reported "log line N" by one -- pointing the
    # label at the record BEFORE the real one. This affects both formats
    # equally since it is the shared line-counting loop; it does not change
    # which records are classified as user/assistant/action for either
    # format, only the human-facing line number attached to each Event.
    for index, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            events.append(Event(index, "malformed"))
            continue
        record_type = record.get("type")
        if record_type == "session_meta":
            timestamp = (record.get("payload") or {}).get("timestamp")
            if isinstance(timestamp, str):
                parsed = _parse_timestamp(timestamp)
                if parsed is not None:
                    session_start = parsed
            continue
        if record_type == "response_item":
            payload = record.get("payload") or {}
            payload_type = payload.get("type")
            role = payload.get("role")
            if payload_type == "message" and role == "user":
                events.append(Event(index, "user", content_text(payload.get("content")), payload))
            elif payload_type == "message" and role == "assistant":
                events.append(Event(index, "assistant", content_text(payload.get("content")), payload))
            elif payload_type in ACTION_TYPES:
                events.append(Event(index, "action", payload=payload))
            continue
        if record_type in ("user", "assistant"):
            # Claude Code transcript shape -- see claude_events_from_line().
            # Claude has no session_meta record, so track the earliest
            # top-level timestamp here as a fallback session start.
            top_level_timestamp = record.get("timestamp")
            if isinstance(top_level_timestamp, str):
                parsed = _parse_timestamp(top_level_timestamp)
                if parsed is not None and (
                    earliest_claude_timestamp is None or parsed < earliest_claude_timestamp
                ):
                    earliest_claude_timestamp = parsed
            events.extend(claude_events_from_line(index, record))
            continue
        # Housekeeping record types (ai-title, custom-title, last-prompt,
        # queue-operation, attachment, mode, system, etc.) carry no
        # router-relevant turn content and are intentionally ignored.
    if session_start is None:
        session_start = earliest_claude_timestamp
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


def audit_events(
    events: list[Event], expected_version: str, *, freshness: bool, strict: bool = False
) -> list[str]:
    failures: list[str] = []
    users = [event for event in events if event.kind == "user" and is_substantive_user(event.text)]
    if not users:
        return ["no substantive user turns were observable in the transcript"]

    for turn_no, user in enumerate(users, 1):
        next_user_index = next((candidate.index for candidate in users if candidate.index > user.index), None)
        window = [event for event in events if event.index > user.index and (next_user_index is None or event.index < next_user_index)]
        first_action = next((event for event in window if event.kind == "action"), None)
        label = f"turn {turn_no} (log line {user.display_line})"
        guarded = strict or is_guarded_user(user.text)
        if not guarded:
            continue
        first_assistant = next((event for event in window if event.kind == "assistant"), None)
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
        if not any(is_worker_action(event) for event in window):
            failures.append(
                f"{label}: substantive turn has no observable bounded-worker dispatch"
            )
        if requires_approval(user.text) and not receipt.handoff:
            failures.append(f"{label}: guarded action lacks required approval evidence")
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
        Event(1, "user", "Please independently review the router gate."),
        Event(2, "assistant", receipt),
        Event(3, "action", payload={"type": "custom_tool_call", "name": "spawn_agent", "model": "gpt-5.6-luna"}),
    ]


def synthetic_fast_lane_events() -> list[Event]:
    """A normal local turn may execute without a receipt or worker."""
    return [
        Event(1, "user", "Please inspect the local router file and summarize the current flow."),
        Event(2, "assistant", "I inspected the local router file."),
        Event(3, "action", payload={"type": "custom_tool_call", "name": "read_file"}),
    ]


def synthetic_external_evaluation_events(version: str) -> list[Event]:
    """Regression fixture for the original missed-delegation phrasing."""
    receipt = (
        "Route: primary=research; secondary=none\n"
        "Route ID: external-evaluation-1\n"
        f"Router version: {version}\n"
        "Scope: evaluate the referenced skill for department integration; stop at advice\n"
        "Allowed systems: repository policy files and the referenced public repository\n"
        "External writes: no\n"
    )
    return [
        Event(1, "user", "Please independently review whether https://github.com/example/tool.git is suitable to integrate."),
        Event(2, "assistant", receipt),
        Event(3, "action", payload={"type": "custom_tool_call", "name": "create_thread", "worker_model": "gpt-5.6-luna", "effort": "high"}),
    ]


def synthetic_no_worker_events(version: str) -> list[Event]:
    events = synthetic_external_evaluation_events(version)
    return events[:2] + [Event(3, "assistant", "Direct advice without a worker.")]


def synthetic_guarded_no_receipt_events() -> list[Event]:
    """A guarded action without a receipt must fail closed."""
    return [
        Event(1, "user", "Please push the repository to origin."),
        Event(2, "assistant", "I will push it now."),
    ]


def synthetic_approval_missing_events(version: str) -> list[Event]:
    """A guarded external action without approval evidence must fail closed."""
    receipt = (
        "Route: primary=operations; secondary=none\n"
        "Route ID: approval-missing-1\n"
        f"Router version: {version}\n"
        "Scope: push the repository to origin; stop after the push\n"
        "Allowed systems: local Git repository and configured origin only\n"
        "External writes: yes\n"
    )
    return [
        Event(1, "user", "Please push the repository to origin."),
        Event(2, "assistant", receipt),
        Event(3, "action", payload={"type": "custom_tool_call", "name": "spawn_agent"}),
    ]


def _write_jsonl(records: list[dict[str, Any]]) -> Path:
    handle = tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    )
    try:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    finally:
        handle.close()
    return Path(handle.name)


def _claude_user_record(content: Any, timestamp: str = "2026-08-18T00:00:00Z") -> dict[str, Any]:
    return {"type": "user", "message": {"role": "user", "content": content}, "timestamp": timestamp}


def _claude_assistant_record(content: Any, timestamp: str = "2026-08-18T00:00:01Z") -> dict[str, Any]:
    return {"type": "assistant", "message": {"role": "assistant", "content": content}, "timestamp": timestamp}


def _claude_receipt_text(
    version: str,
    route_id: str,
    *,
    external_writes: str = "no",
    approval: str = "",
) -> str:
    text = (
        "Route: primary=operations; secondary=none\n"
        f"Route ID: {route_id}\n"
        f"Router version: {version}\n"
        "Scope: verify the transcript gate only; stop after the audit\n"
        "Allowed systems: repository scripts and synthetic records only\n"
        f"External writes: {external_writes}\n"
    )
    if approval:
        text += f"Handoff / approval: {approval}\n"
    return text


def run_claude_format_unit_tests() -> list[str]:
    """Directly exercise the Claude extraction helpers (cases a-d)."""
    failures: list[str] = []

    # (a) plain-string user content -> counted
    text = claude_user_text("Please audit and fix the router parser.")
    if text != "Please audit and fix the router parser.":
        failures.append(f"(a) plain-string user text mismatch: {text!r}")

    # (b) text-block list -> counted
    text = claude_user_text([{"type": "text", "text": "Please plan and implement the fix."}])
    if text != "Please plan and implement the fix.":
        failures.append(f"(b) text-block-list user text mismatch: {text!r}")

    # (c) tool_result-only "user" record -> NOT counted (the critical trap)
    text = claude_user_text(
        [{"type": "tool_result", "tool_use_id": "abc", "content": [{"type": "text", "text": "ok"}]}]
    )
    if text is not None:
        failures.append(f"(c) tool_result-only user record incorrectly counted: {text!r}")

    # (d) assistant text + tool_use -> assistant event THEN action event, in order
    events = claude_events_from_assistant(
        7,
        [
            {"type": "thinking", "thinking": "internal reasoning, must be ignored"},
            {"type": "text", "text": "Route: primary=operations; secondary=none"},
            {"type": "tool_use", "id": "t1", "name": "spawn_agent", "input": {}},
        ],
    )
    kinds = [event.kind for event in events]
    if kinds != ["assistant", "action"] or not (events[0].index < events[1].index):
        failures.append(f"(d) assistant/action ordering wrong: {[(e.kind, e.index) for e in events]}")

    return failures


def run_claude_session_self_tests(expected_version: str) -> list[str]:
    """Full JSONL round trips through iter_events + audit_events (cases e-f)."""
    failures: list[str] = []
    receipt_text = _claude_receipt_text(
        expected_version,
        "claude-self-test-1",
        external_writes="yes",
        approval="user approved the bounded push test",
    )

    # (e) valid receipt before the first tool call -> PASS
    good_path = _write_jsonl(
        [
            _claude_user_record("Please push the router policy after the audit."),
            _claude_assistant_record(
                [
                    {"type": "text", "text": receipt_text},
                    {"type": "tool_use", "id": "t1", "name": "spawn_agent", "input": {}},
                ]
            ),
        ]
    )
    try:
        events, session_start = iter_events(good_path)
        result = audit_events(events, expected_version, freshness=False)
    finally:
        good_path.unlink(missing_ok=True)
    if result:
        failures.append(f"(e) claude session with valid receipt unexpectedly failed: {result!r}")
    if session_start is None:
        failures.append("(e) session_start not derived from earliest top-level Claude timestamp")

    # (f) NO receipt before the first tool call -> FAIL (proves real violations are still caught)
    bad_path = _write_jsonl(
        [
            _claude_user_record("Please push the router policy after the audit."),
            _claude_assistant_record(
                [
                    {"type": "tool_use", "id": "t1", "name": "spawn_agent", "input": {}},
                    {"type": "text", "text": "Working on it, no receipt emitted."},
                ]
            ),
        ]
    )
    try:
        events, _ = iter_events(bad_path)
        result = audit_events(events, expected_version, freshness=False)
    finally:
        bad_path.unlink(missing_ok=True)
    if not result:
        failures.append("(f) claude session WITHOUT a receipt incorrectly passed")

    # Trap regression: a tool_result-only "user" record in a full session
    # must not be counted as a phantom substantive user turn.
    trap_path = _write_jsonl(
        [
            _claude_user_record("Please push the router policy after the audit."),
            _claude_assistant_record(
                [
                    {"type": "text", "text": receipt_text},
                    {"type": "tool_use", "id": "t1", "name": "spawn_agent", "input": {}},
                ]
            ),
            _claude_user_record(
                [{"type": "tool_result", "tool_use_id": "t1", "content": [{"type": "text", "text": "done"}]}],
                timestamp="2026-08-18T00:00:02Z",
            ),
        ]
    )
    try:
        events, _ = iter_events(trap_path)
        user_event_count = sum(1 for event in events if event.kind == "user")
        result = audit_events(events, expected_version, freshness=False)
    finally:
        trap_path.unlink(missing_ok=True)
    if user_event_count != 1:
        failures.append(
            f"trap: tool_result-only record leaked into events as a user turn "
            f"({user_event_count} user events, expected 1)"
        )
    if result:
        failures.append(f"trap: claude session unexpectedly failed: {result!r}")

    return failures


def run_codex_iter_events_regression(expected_version: str) -> list[str]:
    """Prove the Codex (response_item) path through iter_events is unchanged (case g)."""
    failures: list[str] = []
    receipt_text = _claude_receipt_text(
        expected_version,
        "codex-self-test-1",
        external_writes="yes",
        approval="user approved the bounded push test",
    )
    path = _write_jsonl(
        [
            {"type": "session_meta", "payload": {"timestamp": "2026-08-18T00:00:00Z"}},
            {
                "type": "response_item",
                "payload": {"type": "message", "role": "user", "content": "Please push the router policy after the audit."},
            },
            {
                "type": "response_item",
                "payload": {"type": "message", "role": "assistant", "content": receipt_text},
            },
            {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "spawn_agent"}},
        ]
    )
    try:
        events, session_start = iter_events(path)
        result = audit_events(events, expected_version, freshness=False)
    finally:
        path.unlink(missing_ok=True)
    if result:
        failures.append(f"(g) codex iter_events regression failed: {result!r}")
    if session_start is None or session_start.year != 2026:
        failures.append(f"(g) codex session_meta timestamp regression: {session_start!r}")
    return failures


# --- Real-transcript ground truth (machine-specific) ---------------------
#
# Synthetic fixtures let both the line-number off-by-one and the inline
# middle-dot-separated-receipt defects through undetected, because nobody
# fabricated those exact shapes. This test runs the parser against an actual
# Claude Code session log on this machine and checks it against ground truth
# established by reading the raw file directly (grep/json.loads), not by
# trusting the parser's own output. It skips cleanly (prints a notice, empty
# failure list) when the file is absent, since the path is per-device.
REAL_CLAUDE_TRANSCRIPT_PATH = Path(
    r"C:\Users\zamrirosli.HEITECH\.claude\projects\C--my-Projektz-DigiTrustLabCode"
    r"\8359a67f-e0f8-4d13-886d-2708a9a55ee6.jsonl"
)
EXPECTED_REAL_TRANSCRIPT_USER_LINES = {4, 31, 45, 60, 84, 90, 105, 113, 119, 147}
EXPECTED_REAL_TRANSCRIPT_RECEIPT_LINES = {14, 69, 152}
EXPECTED_REAL_TRANSCRIPT_COMPLETE_RECEIPT_LINES = {69, 152}
FORBIDDEN_REAL_TRANSCRIPT_RECORD_TYPES = {
    "queue-operation", "system", "ai-title", "custom-title", "last-prompt", "attachment", "mode",
}


def run_real_transcript_self_test(
    expected_version: str, path: Path = REAL_CLAUDE_TRANSCRIPT_PATH
) -> list[str]:
    if not path.is_file():
        print(f"SKIP real-transcript self-test: file not found ({path})")
        return []

    failures: list[str] = []
    events, _ = iter_events(path)

    # (a) the originally-verified ground-truth user turns are still present
    # at their exact 1-based JSONL line numbers. This is a live session log
    # that keeps growing turn by turn as this very conversation continues, so
    # new lines appearing beyond this set is expected and not itself a
    # failure -- the earlier, already-written lines never change, and this
    # is what the subset check proves.
    user_lines = {event.display_line for event in events if event.kind == "user"}
    missing_ground_truth = EXPECTED_REAL_TRANSCRIPT_USER_LINES - user_lines
    if missing_ground_truth:
        failures.append(
            "(a) expected user-turn line number(s) not found: "
            f"{sorted(missing_ground_truth)} (got {sorted(user_lines)})"
        )

    # (a, independent cross-check) every reported user Event line number is,
    # by direct re-reading of the raw JSON (not by re-using the parser's own
    # extraction helpers), an actual type=="user" record whose content is not
    # purely tool_result blocks. This stays valid regardless of file growth
    # and independently guards against both the off-by-one defect and the
    # tool-result-echo trap.
    with path.open(encoding="utf-8") as handle:
        raw_lines = handle.readlines()
    for line_no in sorted(user_lines):
        if line_no > len(raw_lines):
            failures.append(f"(a) user Event line {line_no} is beyond end of file ({len(raw_lines)} lines)")
            continue
        try:
            record = json.loads(raw_lines[line_no - 1])
        except json.JSONDecodeError:
            failures.append(f"(a) user Event line {line_no} is not valid JSON")
            continue
        if record.get("type") != "user":
            failures.append(
                f"(a) user Event line {line_no} has record type {record.get('type')!r}, not 'user'"
            )
            continue
        content = (record.get("message") or {}).get("content")
        blocks = content if isinstance(content, list) else []
        all_tool_result = bool(blocks) and all(
            isinstance(block, dict) and block.get("type") == CLAUDE_TOOL_RESULT_BLOCK for block in blocks
        )
        if all_tool_result:
            failures.append(f"(a) user Event line {line_no} is a tool_result-only record (the trap)")

    # (b) the three known receipts are found; the two full ones parse complete.
    receipt_events_by_line: dict[int, Event] = {}
    for event in events:
        if event.kind == "assistant" and ROUTE_RE.search(normalize_receipt_text(event.text)):
            receipt_events_by_line[event.display_line] = event
    missing_receipts = EXPECTED_REAL_TRANSCRIPT_RECEIPT_LINES - set(receipt_events_by_line)
    if missing_receipts:
        failures.append(f"(b) expected receipt(s) not found at line(s): {sorted(missing_receipts)}")
    for line in EXPECTED_REAL_TRANSCRIPT_COMPLETE_RECEIPT_LINES:
        event = receipt_events_by_line.get(line)
        if event is None:
            continue  # already reported as missing above
        receipt, receipt_failures = parse_receipt(event.index, event.text)
        if receipt is None or receipt_failures:
            failures.append(
                f"(b) receipt at line {line} expected COMPLETE, got failures: {receipt_failures!r}"
            )

    # (c) housekeeping record types (queue-operation/system/ai-title/etc.)
    # must never produce an Event at their line number.
    event_lines = {event.display_line for event in events}
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            try:
                record = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if record.get("type") in FORBIDDEN_REAL_TRANSCRIPT_RECORD_TYPES and line_no in event_lines:
                failures.append(
                    f"(c) housekeeping record type {record.get('type')!r} at line {line_no} produced an Event"
                )

    return failures


def run_self_test() -> int:
    version = router_version() or "2026-09-04"
    fast = audit_events(synthetic_fast_lane_events(), version, freshness=False)
    good = audit_events(synthetic_events(version), version, freshness=False)
    bad = audit_events(synthetic_events(version, malformed=True), version, freshness=False)
    external = audit_events(synthetic_external_evaluation_events(version), version, freshness=False)
    no_worker = audit_events(synthetic_no_worker_events(version), version, freshness=False)
    guarded_no_receipt = audit_events(synthetic_guarded_no_receipt_events(), version, freshness=False)
    approval_missing = audit_events(synthetic_approval_missing_events(version), version, freshness=False)
    strict_no_receipt = audit_events(synthetic_fast_lane_events(), version, freshness=False, strict=True)
    strict_good = audit_events(synthetic_events(version), version, freshness=False, strict=True)
    project_mode = run_project_mode_self_tests()
    claude_unit_failures = run_claude_format_unit_tests()
    claude_session_failures = run_claude_session_self_tests(version)
    codex_regression_failures = run_codex_iter_events_regression(version)
    real_transcript_failures = run_real_transcript_self_test(version)
    ok = (
        not good
        and bad
        and not external
        and not fast
        and any("no observable bounded-worker dispatch" in failure for failure in no_worker)
        and guarded_no_receipt
        and any("required approval evidence" in failure for failure in approval_missing)
        and strict_no_receipt
        and not strict_good
        and not project_mode
        and not claude_unit_failures
        and not claude_session_failures
        and not codex_regression_failures
        and not real_transcript_failures
    )
    if not ok:
        print(
            "FAIL EA router runtime self-test: "
            f"fast={fast!r}, good={good!r}, malformed={bad!r}, external={external!r}, "
            f"no_worker={no_worker!r}, guarded_no_receipt={guarded_no_receipt!r}, "
            f"approval_missing={approval_missing!r}, strict_no_receipt={strict_no_receipt!r}, "
            f"strict_good={strict_good!r}, project_mode={project_mode!r}, "
            f"claude_unit={claude_unit_failures!r}, claude_session={claude_session_failures!r}, "
            f"codex_regression={codex_regression_failures!r}, "
            f"real_transcript={real_transcript_failures!r}"
        )
        return 1
    print(
        "PASS EA router runtime self-test: fast-lane direct execution, guarded receipt/worker/approval gates, "
        "strict-mode enforcement, external-evaluation regression, no-worker failure, malformed-receipt failure, "
        "Claude-format parsing (user/assistant/tool_result-trap/ordering), Codex iter_events regression, "
        "and real-transcript ground truth"
    )
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
    strict = project_is_strict(effective_root)
    failures = audit_events(
        events,
        expected_version,
        freshness=freshness_required(
            session_start,
            disabled=args.no_freshness,
            router=effective_router,
            root=effective_root,
        ),
        strict=strict,
    )
    if failures:
        print("FAIL EA router runtime:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    substantive = sum(event.kind == "user" and is_substantive_user(event.text) for event in events)
    mode = "strict" if strict else "two-lane"
    print(f"PASS EA router runtime: {substantive} substantive turn(s) satisfy {mode} lane requirements")
    return 0


if __name__ == "__main__":
    sys.exit(main())
