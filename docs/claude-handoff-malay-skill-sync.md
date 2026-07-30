# Handoff for Claude — Fix & relocate `malay-skill-sync.md`

> ✅ **RESOLVED** — 2026-07-30 · Commit `a0e6b68` · Rule created, both trees synced, drift detection added, red-green verified. Do NOT re-execute.

**Raised:** 2026-07-30 by Windsurf (Devin)
**Status:** ~~Ready for Claude to pick up~~ ✅ Done

## Problem

`malay-skill-sync.md` is a DigiTrust Lab-specific rule that currently lives **only** in the global TSOT rules folder (via `.windsurf/rules/` symlink → `E:\My Drive\windsurf\.agent-templates\workspace\rules\`). It is **not** in `.devin/rules/` where Devin actually loads project rules from.

Additionally, the file has **outdated content** that doesn't match the current state of the Malay voice guide.

## What's Outdated

The file currently says:

1. **"semi-formal" references** — The SKILL.md frontmatter and AGENTS.md both now say **"natural formal–semi-formal BM"**, not just "semi-formal". The rule file's description and checklist still say "semi-formal" only.

2. **Section count is wrong** — The rule says "currently 13 semi-formal sections". The actual SKILL.md has **14 numbered sections** (1–13 plus Section 11b). AGENTS.md already says "14 sections" at line 444.

3. **"What NOT to Change" section** references "semi-formal references only" — should say "natural formal–semi-formal".

4. **Missing `bricks-backup` skill reference** — The `.windsurf` version of `bricks-mcp-absolute.md` (also in global TSOT) references a `bricks-backup` skill that doesn't exist in `.devin/skills/`. This is a separate issue but worth noting.

## Current State (Verified)

| Location | Exists? | Content |
|----------|---------|---------|
| `.devin/rules/malay-skill-sync.md` | ❌ No | Not present — Devin can't load this rule |
| `.windsurf/rules/malay-skill-sync.md` (→ global TSOT) | ✅ Yes | Outdated — says "13 semi-formal sections" |
| `.devin/skills/malay-voice-guide/SKILL.md` | ✅ Yes | Has 14 sections, says "natural formal–semi-formal" |
| `AGENTS.md` line 444 | ✅ Yes | Says "14 sections (natural formal–semi-formal BM standard)" |

## Tasks for Claude

### Task 1: Update the file content

Fix `malay-skill-sync.md` to match current state:

- Change all "semi-formal" → "natural formal–semi-formal" in:
  - Frontmatter description
  - Checklist step 1 ("currently 14 natural formal–semi-formal sections")
  - "What NOT to Change" section
- Update section count from 13 → 14
- Verify the trigger conditions still make sense

### Task 2: Copy to `.devin/rules/`

Place the updated file at:
```
g:\Zamzam Biznez\DigiTrustLabCode\.devin\rules\malay-skill-sync.md
```

### Task 3: Remove from global TSOT (optional — discuss with user first)

The file at `E:\My Drive\windsurf\.agent-templates\workspace\rules\malay-skill-sync.md` should eventually be removed since it's project-specific, not global. But this affects all machines/projects, so confirm with the user first.

### Task 4: Verify

- Confirm `.devin/rules/malay-skill-sync.md` exists with updated content
- Confirm AGENTS.md section count (14) matches the rule's checklist count (14)
- Run `git status` to see the new file

## Context Files

- Current rule (outdated): `.windsurf/rules/malay-skill-sync.md` (symlink to global TSOT)
- Malay voice guide: `.devin/skills/malay-voice-guide/SKILL.md` (14 sections, "natural formal–semi-formal")
- AGENTS.md summary: line 444 — "Quick summary of the 14 sections (natural formal–semi-formal BM standard)"
- Other DigiTrust Lab-specific files also stuck in global TSOT: `bricks-mcp-absolute.md`, `continuous-improvement.md`, `deployment.md`, `general-advisor.md`, `self-improvement-loader.md`, `self-improvement-loop.md`, `visual-communication.md` (total 8 files — separate cleanup needed)
