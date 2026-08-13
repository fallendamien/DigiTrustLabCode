# Phase 2 — Architecture Spec: Claude+Codex Lean Structure

> **Date:** 2026-08-13
> **Status:** Ready for user review before Phase 3 implementation
> **Constraint:** `.windsurf/` dirs are TSOT symlinks (never delete files there).
> `.devin/` dirs are real git-tracked files (can move). `CLAUDE.md` is a TSOT symlink (edits affect this project only, but propagate via git sync).

---

## Part A: File & Directory Structure + Import Chain

### A1. Target Directory Layout

```
DigiTrustLabCode/
├── .claude/
│   ├── rules/                          # NEW — moved from .devin/rules/
│   │   ├── bricks-mcp-absolute.md
│   │   ├── bricks-standard-guide.md
│   │   ├── browser-preview.md
│   │   ├── content-planning.md
│   │   └── malay-skill-sync.md         # + added to imports
│   └── skills/                         # EXTENDED — moved from .devin/skills/ + 5 TSOT copies
│       ├── activity-report-composer/
│       ├── brand-voice-synthesizer/
│       ├── change-propagation/
│       ├── conversion-audit/
│       ├── design-system-synthesizer/
│       ├── e2e-seo-assistant/          # NEW — copied from TSOT
│       ├── email-sequence-writer/      # NEW — copied from TSOT
│       ├── geo-fundamentals/           # NEW — copied from TSOT
│       ├── internal-link-builder/
│       ├── landing-page-audit-alt/     # NEW — copied from TSOT (fix name: frontmatter)
│       ├── malay-voice-guide/
│       ├── marketing-skills-index/     # fix G:\ paths
│       ├── mobile-experience-report/
│       ├── prime-the-agent/
│       ├── programmatic-seo-builder/   # NEW — copied from TSOT
│       ├── readability-pass/
│       ├── respira-skills-index/
│       ├── seo-aeo-amplifier/
│       ├── stale-content-detector/
│       ├── technical-debt-audit/
│       ├── wordpress-ai-image-optimizer/
│       ├── wordpress-site-dna/
│       ├── write-post/
│       └── writerzen-keyword-research/
│       # DELETED: bricks-mcp-absolute/ — folded into rule + AGENTS.md
├── .devin/
│   ├── rules/.gitkeep                  # EMPTIED
│   └── skills/.gitkeep                 # EMPTIED
├── .windsurf/                          # SYMLINKS — untouched
│   ├── rules/ → TSOT workspace/rules/
│   └── skills/ → TSOT workspace/skills/
├── AGENTS.md                           # EDIT — path updates + Pieces removals
├── CLAUDE.local.md                     # EDIT — import block + Pieces cleanup
└── CLAUDE.md → TSOT                    # EDIT — on-demand table prune (⚠️ TSOT)
```

### A2. File Movement Table

| Source | Destination | Action | Notes |
|--------|-------------|--------|-------|
| `.devin/rules/*.md` (5 files) | `.claude/rules/` | `git mv` | All 5 rules |
| `.devin/skills/` (19 dirs) | `.claude/skills/` | `git mv` | All except bricks-mcp-absolute |
| `.devin/skills/bricks-mcp-absolute/` | `deprecated/skills/` | `git mv` | Folded |
| TSOT `e2e-seo-assistant/` | `.claude/skills/` | `cp -r` | From `C:\my_Projektz\agent-templates\workspace\skills\` |
| TSOT `email-sequence-writer/` | `.claude/skills/` | `cp -r` | Same |
| TSOT `geo-fundamentals/` | `.claude/skills/` | `cp -r` | Same |
| TSOT `landing-page-audit-alt/` | `.claude/skills/` | `cp -r` | Fix `name:` frontmatter after copy |
| TSOT `programmatic-seo-builder/` | `.claude/skills/` | `cp -r` | Same |

### A3. New Import Block (`CLAUDE.local.md`)

**Current (11 lines):**
```
@AGENTS.md
@.devin/rules/bricks-standard-guide.md
@.devin/rules/bricks-mcp-absolute.md
@.devin/rules/content-planning.md
@.devin/rules/browser-preview.md
@.windsurf/rules/verification-protocol.md
@.windsurf/rules/coding-standards.md
@.windsurf/rules/self-improvement-loader.md
@.windsurf/rules/pieces-ltm-integration.md
@.windsurf/rules/change-summary-rule.md
@.windsurf/rules/context7-default.md
```

**New (10 lines):**
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

| Change | Reason |
|--------|--------|
| `.devin/rules/*` → `.claude/rules/*` (4 lines) | Directory renamed |
| **ADD** `@.claude/rules/malay-skill-sync.md` | Was missing from imports |
| **ADD** `@.windsurf/rules/commit-standards.md` | Always-on for commits |
| **REMOVE** `@.windsurf/rules/coding-standards.md` | Vue-specific, irrelevant |
| **REMOVE** `@.windsurf/rules/pieces-ltm-integration.md` | Pieces retirement |

### A4. CLAUDE.md On-Demand Table (⚠️ TSOT edit)

Replace the current 22-row table with this 13-row version:

```markdown
| Trigger                          | Rule file                                    |
| -------------------------------- | -------------------------------------------- |
| Commit / PR                      | `.windsurf/rules/commit-standards.md`        |
| Roadmap / progress tracking      | `.windsurf/rules/roadmap-template.md`        |
| Visual communication             | `.windsurf/rules/visual-communication.md`    |
| Manual browser testing           | `.windsurf/rules/manual-browser-testing.md`  |
| Continuous improvement           | `.windsurf/rules/continuous-improvement.md`  |
| Knowledge item detection         | `.windsurf/rules/knowledge-radar.md`         |
| Wellness / break reminder        | `.windsurf/rules/wellness-monitor.md`        |
| System architecture              | `.windsurf/rules/system-architect.md`        |
| General advice / second opinion  | `.windsurf/rules/general-advisor.md`         |
| QA / bug review                  | `.windsurf/rules/qa-tester.md`               |
| Skill creation                   | `.windsurf/rules/skill-creator.md`           |
| Rule creation                    | `.windsurf/rules/rule-creator.md`            |
| Malay voice sync                 | `.claude/rules/malay-skill-sync.md`          |
```

### A5. AGENTS.md Path Updates

#### File Architecture table (~line 10)

```
OLD:
| `.devin/rules/` | Operational behaviour — safety checks, tool constraints | Devin only (auto-loaded every session) |
| `.devin/skills/` | On-demand task recipes — SEO audit, keyword research, image optimisation | Devin only (trigger-based, not auto-loaded) |

NEW:
| `.claude/rules/` | Operational rules — safety checks, tool constraints | Claude Code + Codex (always-on via CLAUDE.local.md) |
| `.claude/skills/` | On-demand task recipes — SEO audit, keyword research, image optimisation | Claude Code + Codex (trigger-based, not auto-loaded) |
```

#### Tier 1 doctrine table (4 rows, down from 5)

| File | What it governs |
|------|-----------------|
| `.windsurf/rules/verification-protocol.md` | The Iron Law |
| `.claude/rules/bricks-mcp-absolute.md` | Enforcement detail for PRIORITY #1 |
| `.windsurf/rules/context7-default.md` | Use Context7 for library/API docs |
| `.windsurf/rules/change-summary-rule.md` | Required output format after multi-file changes |

"Read all five" → "Read all four". Remove `pieces-ltm-integration.md` row.

#### Tier 2 doctrine table (4 rows, down from 5)

| Trigger | File |
|---------|------|
| Editing any Bricks element | `.claude/rules/bricks-standard-guide.md` |
| Content planning, keywords, calendar | `.claude/rules/content-planning.md` |
| Visual verification of frontend changes | `.claude/rules/browser-preview.md` |
| Session start, or stuck >10 min on a bug | `.windsurf/rules/self-improvement-loader.md` |

Remove `coding-standards.md` row.

#### Skills Auto-Trigger table — 9 path updates + 1 removal + 5 additions

All `.devin/skills/X` → `.claude/skills/X`. Remove `bricks-mcp-absolute` row.
Add new "Content Strategy Skills" section with: `e2e-seo-assistant`, `email-sequence-writer`, `geo-fundamentals`, `landing-page-audit-alt`, `programmatic-seo-builder`.

#### Body text inline refs (mechanical find-replace)

`.devin/skills/` → `.claude/skills/` and `.devin/rules/` → `.claude/rules/` at ~8 locations in prose.

### A6. Skill Cross-References to Update

After `git mv`, these files have dead `.devin/` path refs:

| File (post-move path) | Refs to update | Action |
|----------------------|----------------|--------|
| `.claude/skills/change-propagation/SKILL.md` | 2 lines (39-40) | `.devin/skills/` → `.claude/skills/`, `.devin/rules/` → `.claude/rules/` |
| `.claude/skills/respira-skills-index/SKILL.md` | 12 lines | sed `.devin/skills/` → `.claude/skills/` |
| `.claude/skills/readability-pass/SKILL.md` | 1 line (143) | `.devin/skills/malay-voice-guide` → `.claude/skills/malay-voice-guide` |
| `.claude/skills/write-post/SKILL.md` | 10 lines | sed `.devin/skills/` → `.claude/skills/` |
| `.claude/skills/marketing-skills-index/SKILL.md` | Full rewrite | Remove `G:\` paths, point 3 migrated skills to `.claude/skills/`, drop 4 non-migrated entries |

---

## Part B: Doctrine Consolidation + Pieces Removal

### B1. Pieces Removal — Exact Edits

#### B1.1 `CLAUDE.local.md` — 5 edits

**Edit 1a — Remove @import line:**
```
OLD:
@.windsurf/rules/self-improvement-loader.md
@.windsurf/rules/pieces-ltm-integration.md
@.windsurf/rules/change-summary-rule.md

NEW:
@.windsurf/rules/self-improvement-loader.md
@.windsurf/rules/change-summary-rule.md
```

**Edit 1b — Remove `pieces` row from Connectors table:**
```
OLD:
| `Context7` | Web (Anthropic-hosted remote) | None | ✅ Connected | Up-to-date library docs |
| `pieces` | Desktop (local, connects to PiecesOS `localhost:39300`) | Local only | ✅ Connected | Long-Term Memory |
| `Respira for WordPress` | Desktop | OAuth / API key (set in connector) | ✅ Connected | WordPress + Bricks editing |

NEW:
| `Context7` | Web (Anthropic-hosted remote) | None | ✅ Connected | Up-to-date library docs |
| `Respira for WordPress` | Desktop | OAuth / API key (set in connector) | ✅ Connected | WordPress + Bricks editing |
```

**Edit 1c — Update "fetch and pieces" advisory note:**
```
OLD:
> **`fetch` and `pieces` are NOT built-in/hosted — they are local Desktop
> extensions with no Web equivalent.** They only work in Claude Desktop and
> Claude Code (not on web/mobile/Cowork). Do NOT remove their entries from
> `claude_desktop_config.json` (see below) — doing so disables them entirely,
> since there's no remote fallback. This was a mistake I almost made on
> 2026-07-29 before checking — correct it if you see it suggested again.

NEW:
> **`fetch` is NOT built-in/hosted — it is a local Desktop extension with no
> Web equivalent.** It only works in Claude Desktop and Claude Code (not on
> web/mobile/Cowork). Do NOT remove its entry from `claude_desktop_config.json`
> (see below) — doing so disables it entirely, since there is no remote
> fallback.
```

**Edit 1d — Remove `pieces` from `claude_desktop_config.json` block:**
```
OLD:
{
  "mcpServers": {
    "pieces": { "command": "cmd.exe", "args": ["/d","/c","npx.cmd","-y","mcp-remote","http://localhost:39300/model_context_protocol/2024-11-05/sse"] },
    "fetch": { "command": "cmd.exe", "args": ["/d","/c","npx.cmd","-y","mcp-fetch-server"] }
  }
}

NEW:
{
  "mcpServers": {
    "fetch": { "command": "cmd.exe", "args": ["/d","/c","npx.cmd","-y","mcp-fetch-server"] }
  }
}
```

**Edit 1e — Update pre-session checklist (remove PiecesOS, update connector count):**
```
OLD:
2. PiecesOS running? (for Pieces LTM — check system tray)
3. Confirm all imports loaded — ask Claude to list what's in its context
4. Check MCP connectors in Settings → Connectors:
   - `fetch`, `Context7`, `pieces`, `Respira for WordPress`, `Screpy` — all 5 should be connected

NEW:
2. Confirm all imports loaded — ask Claude to list what's in its context
3. Check MCP connectors in Settings → Connectors:
   - `fetch`, `Context7`, `Respira for WordPress`, `Screpy` — all 4 should be connected
```

#### B1.2 `.windsurf/rules/context7-default.md` (⚠️ TSOT edit)

Remove the `## Priority` section entirely:
```
DELETE:
## Priority

This rule runs alongside Pieces LTM as a CRITICAL priority:
- **Pieces LTM** → past work history & context
- **Context7** → current library docs & code patterns
```

#### B1.3 `.windsurf/rules/self-improvement-loader.md` (⚠️ TSOT edit)

Remove step 4, renumber step 5:
```
OLD:
3. Scan for lessons relevant to today's task category
4. ✅ **NEW: Query Pieces LTM** — If Pieces MCP is available, ask `ask_pieces_ltm` for recent workstream context to fill gaps in memory
5. Keep those patterns in active context

NEW:
3. Scan for lessons relevant to today's task category
4. Keep those patterns in active context
```

#### B1.4 `content/writerzen-guide/13-keyword-planner-arrange-topics-clusters.md`

Two replacements:
- `Pieces LTM vision capture (screen activity recorded during viewing on 2026-07-14)` → `screen activity notes (viewing session on 2026-07-14)`
- `Pieces LTM vision capture — 2026-07-14 08:38–08:44 AM` → `screen activity notes — 2026-07-14 08:38–08:44 AM`

### B2. AGENTS.md Pieces Edits

**Tier 1 intro:** "Read all five" → "Read all four"

**Historical text (~line 727):**
```
OLD:
...found running without the verification protocol, the Pieces LTM rule, and both lessons files...

NEW:
...found running without the verification protocol and both lessons files...
```

### B3. Agent References — `docs/malay-voice-remediation-plan.md`

```
OLD:
> **Created:** 2026-07-30 · **Owner:** Devin · **Verification:** `scripts/verify-malay-voice.py`

NEW:
> **Created:** 2026-07-30 · **Owner:** Codex · **Verification:** `scripts/verify-malay-voice.py`
```

Verify with `grep -n "Owner.*Devin" docs/malay-voice-remediation-plan.md` — audit listed 2 occurrences but file may have only 1.

### B4. Fold Actions Summary

| Item | Location | Type | Action | Content to extract |
|------|----------|------|--------|-------------------|
| bricks-mcp-absolute skill | `.devin/skills/` | project-local | `git mv` to `deprecated/skills/` | None — fully covered by rule + AGENTS.md |
| behavioral-modes | `.windsurf/skills/` | TSOT symlink | No physical change | None — verbatim in CLAUDE.md § Behavioral Modes |
| brainstorming | `.windsurf/skills/` | TSOT symlink | No physical change | None — verbatim in CLAUDE.md § Socratic Gate |
| seo-fundamentals | `.windsurf/skills/` | TSOT symlink | No physical change | Diff vs seo-audit first; append unique thresholds to write-post if any |

---

## Part C: Ownership Matrix + Implementation Order

### C1. One-Writer-Per-Artifact Matrix

| Artifact | Action | Owner | Reason |
|----------|--------|-------|--------|
| `.devin/rules/` → `.claude/rules/` (5 files) | `git mv` | **Codex** | File moves |
| `.devin/skills/` → `.claude/skills/` (19 dirs) | `git mv` | **Codex** | File moves |
| `.devin/skills/bricks-mcp-absolute/` | `git mv` to `deprecated/` | **Codex** | Archive move |
| `.devin/` empty dirs + `.gitkeep` | Create | **Codex** | Housekeeping |
| 5 TSOT skills → `.claude/skills/` | `cp -r` | **Codex** | File creation |
| `landing-page-audit-alt/SKILL.md` frontmatter | Fix `name:` field | **Claude** | Content judgment |
| `CLAUDE.local.md` — import block | Rewrite per A3 | **Codex** | Mechanical path swap |
| `CLAUDE.local.md` — Pieces cleanup (5 edits) | Edit per B1.1 | **Codex** | Exact string replacements |
| `context7-default.md` — Pieces section | Delete per B1.2 | **Codex** | ⚠️ TSOT — state blast radius |
| `self-improvement-loader.md` — step 4 | Delete per B1.3 | **Codex** | ⚠️ TSOT — state blast radius |
| `writerzen-guide/13-*.md` — 2 Pieces refs | Replace per B1.4 | **Codex** | Exact string replacements |
| `docs/malay-voice-remediation-plan.md` | "Devin" → "Codex" per B3 | **Codex** | Mechanical |
| Skill cross-refs (5 files, ~37 lines) | sed `.devin/` → `.claude/` per A6 | **Codex** | Mechanical |
| `marketing-skills-index/SKILL.md` | Full rewrite | **Claude** | Content judgment — which entries to keep |
| `AGENTS.md` — File Architecture table | Rewrite per A5 | **Claude** | Doctrine content |
| `AGENTS.md` — Tier 1/2 tables | Rewrite per A5 + B2 | **Claude** | Doctrine content |
| `AGENTS.md` — Skills auto-trigger table | 9 updates + 1 removal + 5 additions | **Claude** | Doctrine routing — high stakes |
| `AGENTS.md` — inline `.devin/` prose refs | Find-replace ~8 locations | **Codex** | Mechanical after Claude's table edits |
| `AGENTS.md` — historical Pieces text | Edit per B2 | **Claude** | Doctrine prose |
| `CLAUDE.md` on-demand table | Replace per A4 | **Claude** | ⚠️ TSOT — confirm with user |

### C2. Implementation Batches

| Batch | Worker | Tasks | Dependency |
|-------|--------|-------|------------|
| **A** | Codex | All `git mv` + `git rm` + `.gitkeep` + `cp -r` | None |
| **A** | Claude | AGENTS.md doctrine tables (File Arch, Tier 1/2, Skills trigger, historical text) | None |
| **B** | Codex | `CLAUDE.local.md` full rewrite (imports + Pieces) + skill cross-ref sed + writerzen Pieces refs + malay-voice-remediation Devin→Codex | After Batch A |
| **B** | Claude | `marketing-skills-index` rewrite + `landing-page-audit-alt` frontmatter fix | After Batch A |
| **C** | Codex | AGENTS.md inline `.devin/` prose refs (mechanical find-replace) | After Claude's Batch A tables |
| **D** | Codex | TSOT edits: `context7-default.md` + `self-improvement-loader.md` (state blast radius first) | After Batch B |
| **E** | Claude | `CLAUDE.md` on-demand table (⚠️ TSOT — after user confirms) | After Batch D |

### C3. Post-Edit Verification

```bash
grep -ri "pieces\|search_memory\|ask_pieces_ltm\|PiecesOS\|Pieces LTM" \
  --include="*.md" --include="*.json" --include="*.py" \
  C:\my_Projektz\DigiTrustLabCode
```

**Expected survivors (exactly 5):**

| File | Why it survives |
|------|-----------------|
| `content/link-reviews/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi.json` | Outbound URL to pieces.app |
| `content/content-calendar.md` | Post #9 link metadata |
| `TROUBLESHOOTING.md` | Historical incident note |
| `docs/plan-claude-codex-revamp.md` | Architectural discussion |
| `docs/malay-voice-audit-2026-07-30.md` | "pieces" as count noun |

```bash
grep -ri "\.devin/" --include="*.md" C:\my_Projektz\DigiTrustLabCode
```

**Expected survivors:** Only historical/content references (TROUBLESHOOTING.md, plan docs, audit-results.md). Zero in CLAUDE.local.md, AGENTS.md, or any active skill/rule file.
