# Handoff — EA router runtime audit cannot verify Claude sessions

**Date:** 2026-08-18
**From:** Claude Opus session on the office laptop
**To:** Codex
**File in play:** `scripts/verify-ea-router-runtime.py` — **modified, uncommitted, do not assume it works**

---

## TL;DR

`verify-ea-router-runtime.py` was written to audit Codex transcripts. It has **never been able to read a Claude Code transcript** — on any Claude session it reports `no substantive user turns were observable` and exits 1, which is indistinguishable from a real violation.

Two attempts to fix the parser today got closer but each shipped confidently wrong output while passing its own tests. The working tree currently holds attempt #2. **Verify before trusting any of it.**

A revert was proposed and **not executed** — the user stopped it deliberately so this handoff could carry the in-progress work.

---

## Why this matters

The EA router turn gate (`workspaces/executive-assistant/skills/inquiry-router/SKILL.md`, contract version 2026-08-16) requires a route receipt before any tool call. That rule is **prompt-level only** — nothing enforces it at runtime. This script is the sole mechanism that can tell you whether it was actually followed.

While it is broken, the honest status is: **EA routing compliance on Claude is unverified.**

Note the delegation gate is a separate thing and *is* genuinely enforced — the `PreToolUse` hook was wired today and denies at the tool layer. Do not conflate the two.

---

## Format difference (the root problem)

| | Codex | Claude Code |
|---|---|---|
| User turn | `{"type":"response_item","payload":{"type":"message","role":"user",...}}` | `{"type":"user","message":{"role":"user","content": str OR block list}}` |
| Assistant | same shape, `role":"assistant"` | `{"type":"assistant","message":{"content":[{"type":"text"...},{"type":"tool_use"...}]}}` |
| Tool call | its own `payload.type` in `ACTION_TYPES` | a `tool_use` **block inside** an assistant message |
| Session start | `session_meta` record | no such record — use earliest top-level `timestamp` |

**Traps that already bit us:**

1. **Tool results arrive as `"type":"user"` records** whose content is all `tool_result` blocks. Counting them as user turns produces phantom turns. Attempt #2 handles this correctly.
2. Housekeeping record types must be ignored entirely: `ai-title`, `custom-title`, `last-prompt`, `queue-operation`, `attachment`, `mode`, `system`.
3. Line numbering was 0-based in the original `enumerate(...)`, so every reported "log line N" was off by one — **on the Codex path too**. Attempt #2 changed it to `start=1`. This is a real pre-existing bug worth keeping.
4. Receipts may be emitted as a **single physical line** with fields separated by ` · ` (U+00B7), not one field per line. `ROUTE_RE`/`FIELD_RE` are `^...$`-anchored so they cannot see those. Attempt #2 added `normalize_receipt_text()` which splits before recognised field labels. **This part is verified working** (see evidence below).

---

## Current state of attempt #2 — verified findings

Reference transcript used throughout (machine-specific, this session):

```
C:\Users\zamrirosli.HEITECH\.claude\projects\C--my-Projektz-DigiTrustLabCode\8359a67f-e0f8-4d13-886d-2708a9a55ee6.jsonl
```

### What is confirmed working

Receipt parsing. Tested directly against the three real receipts in that log:

```
line 14  ROUTE_RE match: True   all 5 fields found
line 69  ROUTE_RE match: True   all 5 fields found
line 152 ROUTE_RE match: True   all 5 fields found
```

Ground-truth human user turns are at lines: **4, 31, 45, 60, 84, 90, 105, 113, 119, 147**.
Receipts are at lines: **14, 69, 152**.

### What is still broken — two open defects

**Defect A — turn-to-receipt matching.**
The audit reports `turn 2 (log line 60): missing Route line`, while the receipt at line 69 sits inside that same turn window (next user turn is line 84) and parses completely. The reader works; the attribution of a receipt to its turn does not. Suspect the window/ordering logic interacting with the scaled index scheme attempt #2 introduced (`line_no*1000+sub`, with a `display_line` property for printing).

**Defect B — `is_worker_action()` does not recognise Claude delegation.**
It reports `substantive turn has no observable bounded-worker dispatch` for the turns at lines 4 and 147. Both dispatched a subagent — `Agent` `tool_use` blocks exist at lines **21** and **153**. The function looks for Codex-shaped dispatch metadata (`custom_tool_call` / `create_thread` / `worker_model`) and needs a Claude branch keyed on `tool_use` with `name == "Agent"` (capture `subagent_type` and `model` from `input` if you want the model attestation checked).

### Findings that are TRUE — do not "fix" these away

Of the 6 findings attempt #2 emits, 4 are false (above). These 2 are real and were confirmed by reading the raw transcript:

- Turns at lines **84** and **105** genuinely have **no receipt**.
- Turn at line **147**: a `Bash` tool call at line 149 **preceded** the receipt at line 152. That is a genuine ordering violation of the router contract.

**Any parser fix must still report these.** A version that goes green is wrong.

---

## What went wrong in the process (worth not repeating)

Both attempts passed `--self-test` — including a real-transcript test added in attempt #2 — while producing wrong audit output. The tests asserted the parts that already worked and never asserted turn-to-receipt matching or dispatch recognition.

The general lesson, already in `lessons.md` in its skill-shaped form: **a green suite says nothing about contact with reality.** Any further work here should assert against the real transcript, with hard expected values, for every claim the audit can make — not just for parsing.

---

## Suggested next steps for Codex

1. Read the current diff (`git diff scripts/verify-ea-router-runtime.py`). Decide: build on attempt #2, or revert to `HEAD` and restart from the format notes above. Attempt #2's `normalize_receipt_text()` and the tool_result-trap handling are worth keeping either way.
2. Fix defect B first — it is small and self-contained.
3. Fix defect A — likely the scaled-index/window interaction.
4. Extend the real-transcript test to assert, as hard values: the 10 user-turn lines, the 3 receipt lines, that turns 84 and 105 report missing receipts, that turn 147 reports the ordering violation, and that turns 4 and 147 are recognised as having a worker dispatch.
5. Keep the Codex path behaviourally identical apart from the line-number off-by-one fix, which is a genuine correction.
6. Do not commit until the audit output has been checked line-by-line against the raw transcript by hand at least once.

## Constraints

- Single file: `scripts/verify-ea-router-runtime.py`. Nothing else was touched.
- UTF-8, no BOM. Preserve.
- No commit, no push, until verified.
- Backup of the pre-change file: `%TEMP%\claude\C--my-Projektz-DigiTrustLabCode\8359a67f-e0f8-4d13-886d-2708a9a55ee6\scratchpad\verify-ea-router-runtime.py.bak` (scratchpad is session-scoped and may be cleaned — `git checkout -- scripts/verify-ea-router-runtime.py` is the reliable revert).

## Unrelated context from the same session (already done, no action needed)

- `PreToolUse` orchestration hook wired; matcher widened to cover all Respira namespaces plus live-write verbs including `reset`. `~/.claude/settings.json`.
- Duplicate `psp-emi` project key removed from `~/.claude.json` (PowerShell could not parse it).
- Startup integrity check: **52/52 passing** when run from the repo root with `pwsh` (not `powershell` — the scripts are UTF-8 no-BOM and 5.1 mis-decodes them).
- Both repos clean and level with `origin/master`.
