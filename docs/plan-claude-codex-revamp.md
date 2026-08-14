# Claude + Codex Revamp — Implementation Plan

✅ **All phases completed 2026-08-14**

> **Created:** 2026-08-13 (office laptop)
> **Continue on:** home PC
> **Decision source:** Claude Opus + Codex consensus session (see session transcript)
> **Status:** All phases complete ✅
> **Updated:** 2026-08-14 — all phases marked complete

---

## Goal

Migrate from 4-agent architecture (Claude Code + Codex + Devin + Windsurf) to a
lean **Claude Code + Codex only** setup, following Remy's department-based agent
model with stronger verification gates.

Also: fully retire **Pieces LTM** (going paid Aug 16, 2026) and replace with
file-based memory.

Target outcome: Remy-level department-based agent workflows, with a
Claude-Codex handoff layer and the existing content-quality verification system
preserved.

---

## Operating Model

```
You
  |
Claude (Opus) — orchestrator, researcher, content strategist
  |
Claude specialists (Sonnet 4.6 bounded-workers) — audit, SEO, Malay voice, link review
  |
Codex — implementation, validators, repository verification
  |
You approve external publication or irreversible actions
```

### Role Split

| Agent | Owns | Does NOT do |
|---|---|---|
| **Claude (Opus)** | Research, audit, architecture design, MCP verification, doctrine review, handoff briefs | File scaffolding, bulk moves, reference rewriting |
| **Claude subagents (Sonnet 4.6)** | Parallel file scanning, classification, content extraction | Implementation — findings go to Opus, not to disk |
| **Codex** | File creation, skill migration, reference cleanup, git operations, validator runs | Design decisions, triage judgment calls |
| **You** | Approve handoff briefs, review audit results, approve publishing/destructive actions | — |

### Handoff Protocol

At each phase boundary, Claude produces a **handoff brief** — a structured
markdown document that tells Codex exactly what to do. Codex executes the brief,
commits the work, and reports back. Claude then verifies before the next phase.

```
Claude: research + design → writes handoff brief
  ↓
User: reviews brief, approves
  ↓
Codex: implements exactly what the brief says
  ↓
Claude: verifies implementation matches brief
  ↓
Next phase
```

**One writer per artifact.** Claude and Codex never edit the same file in the
same phase. The handoff brief specifies who owns which files.

### Handoff Brief Required Sections

Every handoff brief MUST include all five:

1. **Exact scope and files** — full paths, whether create/modify/move/delete
2. **Invariants and forbidden changes** — what must NOT be touched
3. **Commands Codex must run** — verification commands with expected output
4. **Acceptance criteria** — measurable pass/fail gates
5. **Rollback instructions** — how to undo if a gate fails

---

## What We're Working With (measured 2026-08-13)

| Asset | Count | Location | Symlinked? |
|---|---|---|---|
| Devin skills | 20 | `.devin/skills/` | No — real project files |
| Devin rules | 5 | `.devin/rules/` | No — real project files |
| Windsurf skills | 125 | `.windsurf/skills/` | YES — symlink to TSOT |
| Windsurf rules | 34 | `.windsurf/rules/` | YES — symlink to TSOT |
| Claude project skills | 0 | `.claude/skills/` | N/A — empty |
| Claude global commands | 32 | `~/.claude/commands/` | YES — symlink to TSOT |
| Python scripts | 5 | `scripts/` | No |
| Python tests | 2 | `tests/` | No |
| Files with Pieces refs | 16 | Various | Mixed |

### The 6 Core Systems to Migrate

| System | Key assets | Why it matters |
|---|---|---|
| Content workflow | `write-post` skill, content-calendar, image-prompts | Drives every blog post |
| Malay voice + naturalness | `malay-voice-guide` skill, `verify-malay-naturalness.py`, rules JSON | Hardened in last 12 commits |
| Link quality | `verify-links.py`, `link-policy.json`, link-reviews | Same batch |
| WordPress status | `verify-content-status.py`, Respira MCP | Operational gate |
| Verification doctrine | `verification-protocol.md`, lessons files | Core safety |
| Bricks safety | Bricks-only policy, template IDs, snapshot protocol | Core safety |

### Files With Pieces References (16 files — all need updating)

```
.windsurf/rules/context7-default.md
.windsurf/rules/pieces-ltm-integration.md
.windsurf/rules/self-improvement-loader.md
.windsurf/rules/self-improvement-loop.md
.windsurf/rules/session-summary-protocol.md
.windsurf/skills/content-repurposer/SKILL.md
.windsurf/skills/content-strategy/SKILL.md
content/link-reviews/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi.json
content/writerzen-guide/13-keyword-planner-arrange-topics-clusters.md
content/content-calendar.md
docs/knowledge-library/delegation-patterns.md
docs/malay-voice-audit-2026-07-30.md
docs/malay-voice-remediation-plan.md
AGENTS.md
CLAUDE.local.md
TROUBLESHOOTING.md
```

---

## Phase 0 — Freeze Baseline

**Owner:** Claude (trivial, no handoff needed)
**Time estimate:** ~2 minutes

### Tasks

- [x] `git tag pre-revamp-baseline` on current HEAD
- [x] Verify tag: `git show pre-revamp-baseline --quiet`
- [x] Note: the untracked `CLAUDE.md.bak_20260804_202141` is NOT captured by
      a git tag — retain it manually until Phase 5

### Rollback

If the revamp fails at any phase, reset to this tag:
```bash
git checkout pre-revamp-baseline
```

---

## Phase 1 — Read-Only Classification Audit

**Owner:** Claude (Opus orchestrates, Sonnet 4.6 subagents scan)
**Time estimate:** ~15-20 minutes
**Output:** `docs/audit-results.md` — the triage table that becomes Codex's
implementation spec in later phases

### Claude's Subagent Allocation (6 parallel scanners)

| Agent | Scope | Item count |
|---|---|---|
| **Scanner 1** | `.devin/skills/` — all 20 skills | 20 |
| **Scanner 2** | `.windsurf/skills/` A-D | ~35 |
| **Scanner 3** | `.windsurf/skills/` E-P | ~45 |
| **Scanner 4** | `.windsurf/skills/` Q-Z | ~45 |
| **Scanner 5** | All rules + scripts + tests | 46 |
| **Scanner 6** | Pieces refs + doctrine files | 16+ |

### Classification Schema

Each item gets one row:

```markdown
| Item | Source path | System | Triage | Dependencies | Pieces ref? | Notes |
```

**System** (pick one):
- `content-workflow`
- `malay-voice`
- `link-quality`
- `wordpress-status`
- `verification`
- `bricks-safety`
- `global-utility`
- `none`

**Triage** (pick one):
- `migrate` — move to `.claude/skills/` or `docs/ai/`
- `fold` — content belongs inside shared doctrine, not standalone
- `archive` — move to `deprecated/`
- `keep-as-is` — already in the right place
- `remove-ref` — file stays but agent-specific references need updating

### After Phase 1

Claude merges scanner outputs into `docs/audit-results.md` with summary counts.
**User reviews with Codex before Phase 2 begins.**

---

## Phase 2 — Design Lean Architecture

**Owner:** Claude (Opus + 2 Sonnet subagents for drafting)
**Time estimate:** ~10-15 minutes
**Depends on:** Phase 1 audit reviewed and approved

### Claude's Subagent Allocation

| Agent | Task |
|---|---|
| **Designer 1** | Draft `docs/ai/` shared doctrine files — extract from `AGENTS.md` (732 lines) and rules into: `project-context.md`, `safety-boundaries.md`, `verification.md`, `malay-voice.md`, `bricks-policy.md`, `workflow-contract.md` |
| **Designer 2** | Draft thin `CLAUDE.md` (~100 lines) and `AGENTS.md` (~100 lines) adapters. Draft `memory/` protocol. Draft Claude-Codex handoff contract. |

### Output (design docs only — Claude does NOT create the final files)

- `docs/architecture-spec.md` containing:
  - Proposed `docs/ai/` file list with contents
  - New `CLAUDE.md` template
  - New `AGENTS.md` template
  - Memory protocol spec
  - Handoff contract

### After Phase 2

Claude presents the architecture spec. **User reviews with Codex.**
Once approved, Claude writes the **Phase 3 handoff brief** for Codex.

---

## Phase 3 — Scaffold New Structure

**Owner:** Codex implements from Claude's handoff brief
**Time estimate:** ~20-30 minutes
**Depends on:** Phase 2 design approved

### Handoff Brief (Claude writes this, Codex executes it)

The brief will contain:

1. **File creation list** — exact paths and contents for every `docs/ai/` file
2. **Skill migration list** — which skills move from `.devin/skills/` or
   `.windsurf/skills/` to `.claude/skills/`, with exact source and destination
3. **Reference update list** — every file that needs Pieces/Devin/Windsurf
   references removed or rewritten, with exact old-string → new-string pairs
4. **New CLAUDE.md** — full text, ready to overwrite
5. **New AGENTS.md** — full text, ready to overwrite
6. **New CLAUDE.local.md imports** — updated `@import` block

### Codex's Implementation Tasks

| Task | Files touched |
|---|---|
| Create `docs/ai/` directory and all doctrine files | ~6 new files |
| Create new `CLAUDE.md` and `AGENTS.md` | 2 files overwritten |
| Update `CLAUDE.local.md` imports | 1 file |
| Migrate skills to `.claude/skills/` | ~15-20 skill directories |
| Remove Pieces references from 16 files | 16 files |
| Set up `memory/` directory with protocol | 1-2 new files |
| Commit all changes | 1 commit |

### After Phase 3

Codex reports completion. Claude verifies:
- [x] `git diff --stat` matches expected changes
- [x] No skill content was lost
- [x] `grep -ri "pieces\|search_memory\|ask_pieces_ltm"` returns zero matches
- [x] `CLAUDE.md` and `AGENTS.md` both under 100 lines
- [x] `docs/ai/` files exist with correct content
- [x] Scripts and tests unchanged

---

## Phase 4 — Prove the Workflow

**Owner:** Split — see ownership table below
**Time estimate:** ~30 minutes
**Depends on:** Phase 3 verified by Claude

### Verification Ownership

| Agent | Owns | Rationale |
|---|---|---|
| **Claude** | MCP connectivity, live WordPress/Bricks behavior, browser/editor evidence | Requires MCP tools and live site access |
| **Codex** | File structure, validators, tests, git diff, reference/path scans | Requires repo access and command execution |
| **Both** | Final acceptance review — each signs off independently | Neither alone can cover the full surface |

### Claude's Verification

1. Open fresh Claude Code session in the repo
2. Verify doctrine loads correctly (no import errors)
3. Invoke one content skill from `.claude/skills/`
4. Call `respira_diagnose_connection` — must succeed
5. Verify no Pieces MCP errors
6. Spot-check one Bricks template read via `respira_extract_builder_content`

### Codex's Verification

1. Confirm `AGENTS.md` is readable and leads to `docs/ai/` doctrine
2. Run `python scripts/verify-content-status.py` — must exit 0
3. Run `python scripts/verify-malay-naturalness.py` on an existing post
4. Run `python -m pytest tests/` — all tests must pass
5. Verify no broken file references in migrated skills
6. `grep -ri "pieces\|search_memory\|ask_pieces_ltm"` — must return zero

### Success Criteria (ALL must pass)

- [x] Claude Code session loads doctrine without errors
- [x] At least one skill invocable from `.claude/skills/`
- [x] Respira MCP responds
- [x] All Python validators pass
- [x] No Pieces errors or missing-tool warnings
- [x] Codex can read and follow the new doctrine chain

### Failure Protocol

If any gate fails: fix it, re-run Phase 4. Do NOT proceed to Phase 5 until
all gates pass.

---

## Phase 5 — Archive Old Layers

**Owner:** Codex implements from Claude's handoff brief
**Time estimate:** ~10 minutes
**Depends on:** Phase 4 all gates passed

### Key Rule: Archive First, Delete Nothing

Move files to `deprecated/` first. Do NOT delete any file until Claude
completes the final reference scan AND Codex verifies the repository state.
Only then may truly dead files be removed (with user approval).

### Handoff Brief Contents

1. **Move list** — `.devin/` → `deprecated/devin/`, `.windsurf/` →
   `deprecated/windsurf/`
2. **CLAUDE.local.md cleanup** — remove any remaining `@import` lines pointing
   to `.windsurf/` or `.devin/`
3. **Global config cleanup** — update `~/.claude/CLAUDE.md` to remove
   Windsurf/Devin references
4. **Commands audit** — list which `~/.claude/commands/` still reference
   deprecated paths (note only — don't break working commands)
5. **Final tag** — `git tag post-revamp-v1`

### After Phase 5

Claude does final verification:
- [x] No broken `@import` references
- [x] `.devin/` and `.windsurf/` in `deprecated/` only
- [x] Tag `post-revamp-v1` exists
- [x] Clean `git status`

---

## Phase 6 — Executive Assistant Pilot (Future)

**Not part of this migration.** Separate initiative after the lean base is
proven.

Create a new workspace folder:
```
workspaces/executive-assistant/
├── claude.md           # "You are my EA..."
├── memory.md           # Self-updating preferences
└── skills/             # Daily brief, meeting prep, referrals
```

Connect: Gmail, Google Calendar, Granola, Notion, Stripe.
Success criteria: ~30 min saved per day, draft-quality output, no unauthorized
external actions.

---

## Subagent Summary (Claude side only)

| Phase | Claude subagents | Model | Purpose |
|---|---|---|---|
| 0 | 0 | Opus direct | Tag baseline |
| 1 | 6 | Sonnet 4.6 | Classification scan (parallel) |
| 2 | 2 | Sonnet 4.6 | Architecture drafting |
| 3 | 0 | — | Claude writes handoff brief only |
| 4 | 0-1 | Sonnet 4.6 | MCP verification (optional) |
| 5 | 0 | — | Claude writes handoff brief only |
| **Total** | **8-9** | | |

Codex handles all implementation in Phases 3 and 5.
Opus never touches implementation files — only writes briefs and verifies results.

---

## Risk Register

| Risk | Mitigation |
|---|---|
| Lose skill content during migration | Phase 1 audit creates full inventory; `pre-revamp-baseline` tag enables rollback |
| Respira MCP breaks | Phase 4 gate: `respira_diagnose_connection` must pass before archiving |
| `CLAUDE.md` too thin, loses context | Phase 2 designs reviewed before implementation; doctrine lives in `docs/ai/` |
| Codex can't read new structure | Phase 4 gate: explicit Codex verification step |
| Home PC has different paths | `CLAUDE.local.md` is per-device and gitignored — recreate on home PC |
| Pieces references survive undetected | Phase 3 brief includes grep verification; Phase 4 confirms zero matches |
| Global commands break | Phase 5 audits each command before archiving |
| Claude and Codex edit same file | Handoff protocol prevents this — one writer per artifact per phase |

---

## How to Continue on Home PC

1. `git pull` in the DigiTrustLabCode repo
2. Read this file: `docs/plan-claude-codex-revamp.md`
3. **For Claude:** "Read `docs/plan-claude-codex-revamp.md` and execute Phase 0,
   then Phase 1. You are the orchestrator — use Sonnet 4.6 bounded-workers for
   scanning. Do not implement anything — produce audit results only."
4. After Phase 1, send `docs/audit-results.md` to Codex for review
5. After Phase 2, send `docs/architecture-spec.md` to Codex for review
6. After each review, Claude writes the handoff brief, Codex implements

### If Pieces is already dead (after Aug 16)

Ignore Pieces MCP errors on startup — Phase 3 removes all references.
Or preemptively remove the Pieces connector from Settings → Connectors.

### Home PC Differences

- Different drive letter for Google Drive (irrelevant after migration)
- Different `CLAUDE.local.md` (recreate from template if missing)
- Devin may still be running — do NOT use it for DigiTrust work during migration

---

## Decision Log

| Date | Decision | Participants |
|---|---|---|
| 2026-08-13 | Drop Devin + Windsurf, go Claude + Codex only | Claude, Codex, Zamri |
| 2026-08-13 | Retire Pieces (going paid Aug 16) | Claude, Codex, Zamri |
| 2026-08-13 | Shared doctrine in `docs/ai/`, thin adapters | Claude, Codex |
| 2026-08-13 | 6 core systems migrate, rest archive | Claude, Codex |
| 2026-08-13 | File-based memory replaces Pieces LTM | Claude, Codex |
| 2026-08-13 | Claude+Codex handoff model: Claude researches/designs, Codex implements | Zamri |
| 2026-08-13 | Opus orchestrates only, Sonnet 4.6 scans, Codex builds | Zamri |
| 2026-08-13 | Executive Assistant pilot AFTER base migration | Claude, Codex |
