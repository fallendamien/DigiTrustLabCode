# Codex Handoff Brief — Phase 3 (Scaffold)

> **Created by:** Claude (Opus) · **For:** Codex
> **Date:** 2026-08-13
> **Context:** Claude+Codex revamp, Phase 3. Architecture spec: `docs/architecture-spec.md`
> **One-writer rule:** Claude has already edited AGENTS.md doctrine tables (Batch A). Do NOT touch those sections. Your work is mechanical file moves and string replacements.

Execute these batches in order. Commit after each batch.

---

## Batch A — File Moves

### A1. Move `.devin/rules/` → `.claude/rules/`

```bash
mkdir -p .claude/rules
git mv .devin/rules/bricks-mcp-absolute.md .claude/rules/
git mv .devin/rules/bricks-standard-guide.md .claude/rules/
git mv .devin/rules/browser-preview.md .claude/rules/
git mv .devin/rules/content-planning.md .claude/rules/
git mv .devin/rules/malay-skill-sync.md .claude/rules/
```

### A2. Move `.devin/skills/` → `.claude/skills/` (19 dirs, skip bricks-mcp-absolute)

```bash
mkdir -p .claude/skills
# Move all skill dirs EXCEPT bricks-mcp-absolute
for dir in activity-report-composer brand-voice-synthesizer change-propagation conversion-audit design-system-synthesizer internal-link-builder malay-voice-guide marketing-skills-index mobile-experience-report prime-the-agent readability-pass respira-skills-index seo-aeo-amplifier stale-content-detector technical-debt-audit wordpress-ai-image-optimizer wordpress-site-dna write-post writerzen-keyword-research; do
  git mv ".devin/skills/$dir" ".claude/skills/$dir"
done
```

### A3. Archive bricks-mcp-absolute skill

```bash
mkdir -p deprecated/skills
git mv .devin/skills/bricks-mcp-absolute deprecated/skills/
```

### A4. Leave `.devin/` with .gitkeep

```bash
# After all moves, .devin/rules/ and .devin/skills/ should be empty
# Add .gitkeep to keep the dirs in git (backwards compat)
touch .devin/rules/.gitkeep .devin/skills/.gitkeep
git add .devin/rules/.gitkeep .devin/skills/.gitkeep
```

### A5. Copy 5 TSOT skills to `.claude/skills/`

The TSOT is at `C:\my_Projektz\agent-templates\workspace\skills\`. Copy these 5:

```bash
TSOT="C:/my_Projektz/agent-templates/workspace/skills"
for skill in e2e-seo-assistant email-sequence-writer geo-fundamentals landing-page-audit-alt programmatic-seo-builder; do
  cp -r "$TSOT/$skill" ".claude/skills/$skill"
done
git add .claude/skills/e2e-seo-assistant .claude/skills/email-sequence-writer .claude/skills/geo-fundamentals .claude/skills/landing-page-audit-alt .claude/skills/programmatic-seo-builder
```

### A6. Commit Batch A

```
feat(revamp): Phase 3 Batch A — move .devin/ to .claude/, copy 5 TSOT skills

- git mv .devin/rules/ → .claude/rules/ (5 files)
- git mv .devin/skills/ → .claude/skills/ (19 dirs)
- git mv bricks-mcp-absolute skill → deprecated/skills/
- cp 5 TSOT skills (e2e-seo-assistant, email-sequence-writer, geo-fundamentals,
  landing-page-audit-alt, programmatic-seo-builder)
- .devin/ dirs kept with .gitkeep for backwards compat
```

---

## Batch B — CLAUDE.local.md + Skill Cross-Refs + Pieces Cleanup

### B1. CLAUDE.local.md — Replace import block

Find the current `@import` block (11 lines starting after the explanatory text) and replace with:

```
@AGENTS.md
@.claude/rules/bricks-standard-guide.md
@.claude/rules/bricks-mcp-absolute.md
@.claude/rules/content-planning.md
@.claude/rules/browser-preview.md
@.claude/rules/malay-skill-sync.md
@.windsurf/rules/verification-protocol.md
@.windsurf/rules/commit-standards.md
@.windsurf/rules/self-improvement-loader.md
@.windsurf/rules/change-summary-rule.md
@.windsurf/rules/context7-default.md
```

Changes vs current: `.devin/rules/*` → `.claude/rules/*`, ADD `malay-skill-sync.md` + `commit-standards.md`, REMOVE `coding-standards.md` + `pieces-ltm-integration.md`.

### B2. CLAUDE.local.md — Pieces cleanup (5 exact edits)

All 5 edits are documented with exact old→new strings in `docs/architecture-spec.md` § B1.1. Apply all 5:

1. Remove the `@.windsurf/rules/pieces-ltm-integration.md` import line (already done by B1 above)
2. Remove the `pieces` row from the Installed Connectors table
3. Update the "fetch and pieces" advisory note to "fetch" only
4. Remove `pieces` entry from the `claude_desktop_config.json` code block
5. Update pre-session checklist: remove PiecesOS item, update connector count 5→4

### B3. Skill cross-ref sed (5 files)

After Batch A moves the files, these internal references are stale. Find-replace `.devin/skills/` → `.claude/skills/` and `.devin/rules/` → `.claude/rules/` in:

1. `.claude/skills/change-propagation/SKILL.md` — 2 lines
2. `.claude/skills/respira-skills-index/SKILL.md` — ~12 lines
3. `.claude/skills/readability-pass/SKILL.md` — 1 line
4. `.claude/skills/write-post/SKILL.md` — ~10 lines
5. `.claude/skills/writerzen-keyword-research/SKILL.md` — check for any `.devin/` refs

### B4. WriterZen Pieces refs

In `content/writerzen-guide/13-keyword-planner-arrange-topics-clusters.md`, replace:
- `Pieces LTM vision capture (screen activity recorded during viewing on 2026-07-14)` → `screen activity notes (viewing session on 2026-07-14)`
- `Pieces LTM vision capture — 2026-07-14 08:38–08:44 AM` → `screen activity notes — 2026-07-14 08:38–08:44 AM`

### B5. Malay voice remediation — Devin → Codex

In `docs/malay-voice-remediation-plan.md`, replace `Owner: Devin` → `Owner: Codex`. Verify with `grep -n "Owner.*Devin"` first — audit listed 2 occurrences but there may be only 1.

### B6. Commit Batch B

```
feat(revamp): Phase 3 Batch B — update imports, cross-refs, remove Pieces refs

- CLAUDE.local.md: new 10-line import block, Pieces connector removed
- 5 skill files: .devin/ → .claude/ path updates
- writerzen guide: Pieces LTM → screen activity notes
- malay-voice-remediation-plan: Owner Devin → Codex
```

---

## Batch C — AGENTS.md Inline Prose Refs

Claude has already updated the doctrine tables. Now do a mechanical find-replace of remaining `.devin/skills/` and `.devin/rules/` references in AGENTS.md prose (~8 locations). These are in body text, not in the tables Claude edited.

Known locations (grep for `.devin/` in AGENTS.md after Batch A):
- ~line 203: "AGENTS.md and `.devin/rules/`" → remove this sentence (Devin-specific)
- ~line 370: `.devin/skills/malay-voice-guide` → `.claude/skills/malay-voice-guide`
- ~line 504: `.devin/skills/malay-voice-guide` → `.claude/skills/malay-voice-guide`
- ~line 586: `.devin/skills/write-post` → `.claude/skills/write-post`
- ~line 671: `.devin/skills/write-post` → `.claude/skills/write-post`
- ~line 701: `.devin/skills/readability-pass` → `.claude/skills/readability-pass`
- ~line 702: `.devin/skills/write-post` → `.claude/skills/write-post`

After replacing, verify: `grep -n '\.devin/' AGENTS.md` should return ZERO results.

### Commit Batch C

```
feat(revamp): Phase 3 Batch C — AGENTS.md inline .devin/ → .claude/ prose refs
```

---

## Batch D — TSOT Edits (blast radius: all projects)

⚠️ These files are in the TSOT (`C:\my_Projektz\agent-templates\workspace\rules\`). Edits affect ALL projects on this machine.

### D1. `context7-default.md` — Remove Pieces section

Delete this entire section:

```markdown
## Priority

This rule runs alongside Pieces LTM as a CRITICAL priority:
- **Pieces LTM** → past work history & context
- **Context7** → current library docs & code patterns
```

### D2. `self-improvement-loader.md` — Remove Pieces step

Replace:
```
3. Scan for lessons relevant to today's task category
4. ✅ **NEW: Query Pieces LTM** — If Pieces MCP is available, ask `ask_pieces_ltm` for recent workstream context to fill gaps in memory
5. Keep those patterns in active context
```

With:
```
3. Scan for lessons relevant to today's task category
4. Keep those patterns in active context
```

### Commit Batch D (in the TSOT repo)

```
chore(revamp): remove Pieces LTM references from context7-default + self-improvement-loader
```

---

## Post-All-Batches Verification

Run these two greps and confirm results match expectations:

```bash
# Pieces refs — expect exactly 5 survivors (content refs only)
grep -ri "pieces\|search_memory\|ask_pieces_ltm\|PiecesOS\|Pieces LTM" --include="*.md" --include="*.json" --include="*.py" C:\my_Projektz\DigiTrustLabCode

# .devin/ refs — expect zero in active files (CLAUDE.local.md, AGENTS.md, skill/rule files)
grep -ri "\.devin/" --include="*.md" C:\my_Projektz\DigiTrustLabCode
```

Report the grep output as evidence.
