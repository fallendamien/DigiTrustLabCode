# Phase 1 — Classification Audit Results

> **Date:** 2026-08-13
> **Scanners:** 6 Sonnet 4.6 bounded-workers (parallel)
> **Total items scanned:** 208 (20 Devin skills + 125 Windsurf skills + 39 rules + 8 scripts/tests + 16 Pieces-ref files)
> **Status:** Complete — ready for user + Codex review before Phase 2

---

## Executive Summary

| Triage | Count | Action |
|--------|-------|--------|
| **keep-as-is** | 120 | No changes needed — TSOT globals, agent-agnostic utilities |
| **archive** | 53 | Move import/remove from active load (paid ads, Windsurf-meta, Vue/React dev skills, irrelevant rules) |
| **migrate** | 13 | Move to `.claude/` namespace or add to CLAUDE.local.md imports |
| **fold** | 4 | Content duplicated in doctrine — merge into parent file |
| **remove-ref** | 2 | File stays, stale `.gemini` paths need updating |
| **Pieces cleanup** | 6 | 1 archive-whole-file, 4 remove-pieces-refs, 1 remove-agent-refs |
| **Doctrine rewrite** | 1 | AGENTS.md needs 2 targeted Pieces removals |

### Key Findings

1. **53 archive candidates** break into 3 clusters:
   - 29 paid-ads skills (Google/Meta/Reddit/LinkedIn) — zero relevance to WordPress blog
   - 13 Vue/React/Node dev skills — wrong tech stack for Bricks/WordPress
   - 11 Windsurf-meta + Antigravity skills — not portable to Claude+Codex

2. **4 files in the Pieces list don't exist** — already removed from TSOT at some point

3. **Zero Pieces references in any Devin skill** — all 20 are clean

4. **1 frontmatter name mismatch**: `landing-page-audit-alt` has `name: landing-page-audit` — fix before migrating

5. **3 import gaps in CLAUDE.local.md**: `commit-standards.md`, `malay-skill-sync.md` missing; `coding-standards.md` loaded but irrelevant (Vue-specific)

---

## Section 1: Items to MIGRATE (13)

### 1a: Devin rules → `.claude/rules/` (5 files)

These are correctly loaded by CLAUDE.local.md but live under the Devin-branded `.devin/rules/` namespace. Move the directory.

| Item | Current path | System | Notes |
|------|-------------|--------|-------|
| bricks-mcp-absolute.md | `.devin/rules/` | bricks-safety | Safety-critical |
| bricks-standard-guide.md | `.devin/rules/` | bricks-safety | Respira MCP tool reference |
| browser-preview.md | `.devin/rules/` | global-utility | Chrome session auth rule |
| content-planning.md | `.devin/rules/` | content-workflow | Calendar-as-SSOT rule |
| malay-skill-sync.md | `.devin/rules/` | malay-voice | **NOT currently in CLAUDE.local.md — add when moving** |

### 1b: Windsurf rules to promote (1)

| Item | Current path | System | Notes |
|------|-------------|--------|-------|
| commit-standards.md | `.windsurf/rules/` | global-utility | Always-on in Windsurf, missing from CLAUDE.local.md — add |

### 1c: Windsurf skills to migrate to `.claude/skills/` (6)

| Item | Current path | System | Notes |
|------|-------------|--------|-------|
| e2e-seo-assistant | `.windsurf/skills/` | content-workflow | Full SEO checklist, no agent hooks |
| email-sequence-writer | `.windsurf/skills/` | content-workflow | AIDA/PAS/BAB for MailerLite |
| geo-fundamentals | `.windsurf/skills/` | content-workflow | GEO/AI search citation — core to AI blog |
| landing-page-audit-alt | `.windsurf/skills/` | content-workflow | CRO analysis. **Fix `name:` frontmatter first** |
| programmatic-seo-builder | `.windsurf/skills/` | content-workflow | Scalable SEO page templates |
| marketing-skills-index | `.devin/skills/` | global-utility | **Fix hardcoded `G:\` paths first** |

### 1d: Devin skill to fix (1)

| Item | Issue | Fix |
|------|-------|-----|
| marketing-skills-index | Hardcoded `G:\Zamzam Biznez\...` paths | Make device-agnostic via TSOT symlink |

---

## Section 2: Items to FOLD into Doctrine (4)

| Item | Source | Fold into | Reason |
|------|--------|-----------|--------|
| bricks-mcp-absolute (skill) | `.devin/skills/` | Already covered by `.devin/rules/bricks-mcp-absolute.md` + AGENTS.md PRIORITY #1 | Triple redundancy — skill adds drift risk |
| behavioral-modes | `.windsurf/skills/` | Already in global CLAUDE.md § Behavioral Modes | Duplicate |
| brainstorming | `.windsurf/skills/` | Already in global CLAUDE.md § Socratic Gate | Duplicate |
| seo-fundamentals | `.windsurf/skills/` | Merge into seo-audit skill (130 lines, high overlap) | Short, overlapping |

---

## Section 3: Items to ARCHIVE (53)

### 3a: Paid-ads skills (29) — batch archive

All Google/Meta/Reddit/LinkedIn paid advertising skills. Zero relevance to WordPress blog.

```
ab-test-analyzer, ab-test-setup-and-analysis, account-structure-review,
ad-copy-variant-generator, ad-extension-audit, ad-spend-allocator,
anomaly-detection, attribution-model-comparison, audience-overlap-analysis,
bid-strategy-recommendations, budget-scenario-planner,
campaign-naming-convention-builder, channel-mix-optimizer,
client-report-narratives, competitor-creative-analysis,
conversion-path-analysis, cpa-diagnostics, creative-fatigue-detection,
day-hour-performance-breakdown, device-performance-split,
frequency-cap-recommendations, geo-performance-analysis, google-ads-audit,
icp-research-assistant, keyword-cannibalization-check, landing-page-audit,
linkedin-ads-audit, meta-ads-audit, pacing-monitor,
performance-benchmarking, quality-score-breakdown, reddit-ads-audit,
retargeting-window-analysis, roas-forecasting, search-term-mining,
wasted-spend-finder, weekly-account-summary
```

**Note:** These are TSOT globals. "Archive" means removing from DigiTrust Lab's active consideration, NOT deleting from the TSOT (other projects may use them).

### 3b: Dev-stack skills (13) — wrong tech for WP blog

```
firebase-patterns, i18n-localization, mcp-builder, mobile-design,
mobile-layout-debugging, nodejs-best-practices, pinia-patterns,
primevue-patterns, production-code-audit, python-patterns,
frontend-design, performance-profiling, red-team-tactics
```

### 3c: Windsurf-meta + Antigravity skills (11) — not portable

```
environment-master, failure-postmortem, generate-gitignore,
impasse-detector, paste-sanitizer, pre-action-guard,
rule-creator, skill-creator, template-management,
workflow-verification, observation-engineer
```

### 3d: Windsurf rules to drop from DigiTrust Lab (13)

Remove from active load / on-demand table. TSOT files stay for other projects.

```
code-redundancy-detection.md, coding-standards.md, dark-mode-standards.md,
deployment.md, dev-server-preferences.md, editor-setup.md,
global-rules-stats-sync.md, interaction-rules.md, model-orchestrator.md,
multi-role-simulator.md, no-browser-alerts.md, ui-consistency.md,
ui-ux-specialist.md, ux-excellence.md
```

---

## Section 4: Items to UPDATE (remove-ref) (2)

| File | Issue | Fix |
|------|-------|-----|
| `.windsurf/rules/continuous-improvement.md` | Stale `$env:USERPROFILE\.gemini\.agent-templates\` path | Update to current TSOT path. **TSOT edit — affects all projects** |
| `.windsurf/rules/knowledge-radar.md` | Stale `C:\Users\Zamri\.gemini\antigravity\knowledge\` path | Update to current TSOT location. **TSOT edit — affects all projects** |

---

## Section 5: Pieces/LTM Cleanup (6 files + 1 rewrite)

### 5a: Archive whole file (1)

| File | Reason |
|------|--------|
| `.windsurf/rules/pieces-ltm-integration.md` | Entire file IS the Pieces integration — nothing survives removal |

### 5b: Remove Pieces references (4 files)

| File | What to remove | What stays |
|------|---------------|------------|
| `.windsurf/rules/context7-default.md` | Strip `## Priority` section mentioning Pieces LTM | Core Context7 rules |
| `.windsurf/rules/self-improvement-loader.md` | Remove step 4 (Query Pieces LTM) | Steps 1-3, 5 (lessons loading) |
| `content/writerzen-guide/13-keyword-planner-arrange-topics-clusters.md` | Replace 2× "Pieces LTM vision capture" with "screen activity notes" | Core lesson content |
| `CLAUDE.local.md` | Remove: @import line, pieces connector row, pieces config block, PiecesOS checklist item, pieces from connector list | Everything else |

### 5c: Remove agent references (1 file)

| File | What to change |
|------|---------------|
| `docs/malay-voice-remediation-plan.md` | "Owner: Devin" → "Owner: Codex" (2 occurrences) |

### 5d: Targeted AGENTS.md rewrite (2 edits only)

1. Remove `pieces-ltm-integration.md` row from Tier 1 doctrine table
2. Remove "the Pieces LTM rule" clause from historical explanation

### 5e: No-action files (intentional Pieces references in content)

These mention Pieces as content data, not as tool invocations. Leave as-is.

```
content/link-reviews/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi.json  (outbound URL to pieces.app)
content/content-calendar.md  (Post #9 link metadata)
TROUBLESHOOTING.md  (historical incident note)
docs/plan-claude-codex-revamp.md  (architectural discussion — this plan)
docs/malay-voice-audit-2026-07-30.md  ("pieces" as count noun only)
```

### 5f: Files that don't exist (4 — already removed from TSOT)

```
.windsurf/rules/self-improvement-loop.md
.windsurf/rules/session-summary-protocol.md
.windsurf/skills/content-repurposer/SKILL.md
.windsurf/skills/content-strategy/SKILL.md
```

---

## Section 6: CLAUDE.local.md Import Changes

| Action | File |
|--------|------|
| **Remove** | `@.windsurf/rules/pieces-ltm-integration.md` |
| **Remove** | `@.windsurf/rules/coding-standards.md` (Vue-specific, irrelevant) |
| **Add** | `@.windsurf/rules/commit-standards.md` (always-on, applies to commits) |
| **Add** | `@.devin/rules/malay-skill-sync.md` → will become `@.claude/rules/malay-skill-sync.md` |
| **Rename prefix** | All `@.devin/rules/` → `@.claude/rules/` after directory move |

---

## Section 7: Items to KEEP-AS-IS (120)

Not listed individually — these are TSOT globals (coding patterns, testing, architecture, Vue/TS utilities) and project-local scripts/tests that are already agent-agnostic and correctly placed. Full per-item tables in scanner scratchpad files.

Notable keep-as-is items relevant to DigiTrust Lab:

| Item | Type | System | Why it matters |
|------|------|--------|---------------|
| write-post | Devin skill | content-workflow | End-to-end post pipeline (Phases -2 to 7) |
| malay-voice-guide | Devin skill | malay-voice | Hard publish gate |
| internal-link-builder | Devin skill | link-quality | Strategic link building with snapshots |
| verification-protocol.md | Windsurf rule | verification | The Iron Law |
| seo-audit | Windsurf skill | content-workflow | Comprehensive SEO framework |
| schema-markup | Windsurf skill | content-workflow | JSON-LD structured data |
| i-have-adhd | Windsurf skill | global-utility | Auto-loaded, single source of truth in TSOT |
| All 6 Python scripts | scripts/ | various | Agent-agnostic gates |
| Both test files | tests/ | various | Agent-agnostic regression tests |

---

## Post-Cleanup Verification Command

After all edits, run:

```bash
grep -ri "pieces\|search_memory\|ask_pieces_ltm\|PiecesOS\|Pieces LTM" --include="*.md" --include="*.json" --include="*.py" C:\my_Projektz\DigiTrustLabCode
```

**Expected survivors** (all no-action content references):
- `content/link-reviews/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi.json` — outbound URL
- `content/content-calendar.md` — Post #9 link metadata
- `TROUBLESHOOTING.md` — historical incident note
- `docs/plan-claude-codex-revamp.md` — this migration's architectural discussion
- `docs/malay-voice-audit-2026-07-30.md` — "pieces" as count noun

---

## Next Step

User reviews this audit with Codex. Once approved, Claude proceeds to **Phase 2** (Design Lean Architecture).
