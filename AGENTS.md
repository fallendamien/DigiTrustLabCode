# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 🔴 PRIORITY #1: Bricks-Only Policy (CRITICAL)

**RULE: EVERYTHING inside Bricks must be done via Bricks standard procedures — Bricks Builder GUI or Bricks MCP. NO post-processing scripts. NO PowerShell CSS injection. NO background code. NO internal hacks. NO exceptions. If it can't be done through Bricks GUI or Bricks MCP, it doesn't get done.**

**Exception:** Wrangler CLI is allowed for Cloudflare Pages deployment only — it's a deploy tool, not a Bricks internal operation.

This is a blogging business project, NOT a development project. The user does not want raw code hassles, background scripts, or post-processing pipelines. Everything must use Bricks' own standard operations and tools.

## 🔴 FROZEN: Templates 185 (Header) and 52 (Blog Archive)

**EFFECTIVE IMMEDIATELY (2026-07-05): These templates are FROZEN. Do NOT touch them.**

Do not read them. Do not write them. Do not open them in the Bricks GUI. Do not attempt to fix them.
If a task requires changes to these templates, STOP and tell Zamri: "This requires touching a frozen template. Escalate to Claude."

**Background:** As of 2026-07-04, Devin has caused the flattening bug THREE times on these
two templates. Every write via MCP `content:update_content` regenerates all element IDs,
flattens all `parent` fields to `0`, and breaks `_cssCustom` selectors. The bug is in the
Bricks MCP API itself — not fixable from our side. Templates are frozen until a solution
is found (e.g., switching to Respira MCP which has snapshot/rollback).

## ✅ Devin's Permitted Scope

**You ARE permitted to:**
- Create and edit WordPress POSTS and PAGES (content only, not Bricks templates)
- Manage menus via Bricks MCP menu tools
- Run Simply Static export (WP Admin → Simply Static → Generate → Push)
- Run Wrangler deploy
- Edit AGENTS.md, ROADMAP.md, STATE.json, NEXT.md
- Install or configure plugins (not Bricks templates)

**You are NOT permitted to:**
- Touch template IDs 185 or 52 via any method (read, write, GUI, MCP)
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task

## ✅ Current Priority: Write and Publish Post #1

This is the only task that matters right now. Do NOT work on any template, design,
or infrastructure task unless Zamri explicitly instructs it.

## 🔴 UNRESOLVED: Category/Taxonomy Archives Don't Use Custom Template

Template ID 52 (Blog Archive) has condition `{"main": "archiveType", "archiveType": "any"}`
set via `template_condition:set`. This correctly applies to `/blog/` (post type
archive) but does NOT apply to `/category/ai-tools/` or `/category/digital-side-hustle/`
(taxonomy term archives).

**Confirmed via DOM inspection:** on category pages, `#brx-content` contains ONLY
`<div class="brxe-container"><div class="bricks-no-posts-wrapper">...</div></div>`
— none of our template's elements (section/header block/heading/grid) are present
at all. This means Bricks is not loading template 52 on taxonomy archives — it's
using some other fallback entirely.

**What was tried (didn't work):**
- `archiveType: any` condition alone
- Adding a second condition `archivePostType: post`
- Adding `hasLoop: true` + `is_main_query: true` to the query object per the Bricks
  MCP builder guide's Archive Templates section

**Needs investigation:**
- Check `bricks:get_condition_schema` or `template_condition:types` for the correct
  condition to target taxonomy archives specifically (may need something like
  `archiveType: taxonomy` or a `terms` condition type, not `archivePostType`)
- Verify whether Bricks WP core theme even supports a single template covering
  BOTH post-type archives AND taxonomy archives, or if they need separate
  templates/conditions
- Check in Bricks GUI directly: Template 52 → Settings → Conditions, to see what
  the visual condition picker actually offers for taxonomy targeting

**Workaround in place:** `.bricks-archive-title-wrapper { display: none !important; }`
in WP Additional CSS hides the ugly "Category: X" heading. The "Nothing found"
state is cosmetic-only until Post #1 exists, but the missing centered header/grid
styling on category pages will persist even after posts are published, since the
custom template isn't being used there at all.

### 🧩 Bricks MCP Server (PRIMARY TOOL)

**Bricks MCP is installed and active on digitrust-lab.local.** Connected to Windsurf and Claude Desktop.

**Full tool reference:** `.devin/rules/bricks-standard-guide.md` (always_on)
**Builder guide:** `BRICKS-BUILDER-GUIDE.md` — read BEFORE editing Bricks elements via MCP

### Decision Matrix

| Task | Use GUI | Use Bricks MCP | Use Non-Bricks Code | Why |
|------|---------|----------------|---------------------|-----|
| Edit page content | ✅ WordPress → Pages → edit | ⚠️ Possible | ❌ | Standard WP editing |
| Add/remove pages | ✅ WordPress → Pages | ❌ | ❌ | Standard WP |
| Change colors/typography | ✅ Bricks → Settings → Custom CSS | ✅ `design` tool | ❌ | Visual editor or MCP |
| Manage WP menus | ✅ Appearance → Menus | ✅ `menu` tool | ❌ | GUI or MCP |
| Deploy to Cloudflare | ✅ Cloudflare dashboard upload | ❌ | ✅ Wrangler CLI | Deploy tool only, not Bricks internal |
| ⛔ Touch Template 185/52 | ❌ FROZEN | ❌ FROZEN | ❌ FROZEN | Escalate to Claude |

### ⚠️ Bricks MCP Destructive Actions

| Action | What Happens | Prevention |
|--------|-------------|------------|
| `template update` with `type` change | **Wipes ALL elements** | NEVER change type after elements exist |
| `template update` with `elements` param | **Silently ignores `elements`** | Use `content update_content` with `post_id` |
| `content update_content` | **Replaces ALL elements** + regenerates IDs (flattening bug) | ⛔ FROZEN for templates 185 & 52 |
| `content delete` with `element_id` | **Trashes the entire post** | NEVER use on templates with elements |

### Incident Log (Lessons Learned)

**Incident 1:** Spent 45+ min writing PHP mu-plugins for a 2-min GUI task.
**Incident 2 (2026-07-04):** Post-process CSS injection fought with Bricks native CSS, making mobile menu worse.
**Incident 3 (2026-07-04):** AI-created JSON backups had structural issues on re-import. User banned all AI-created backups.
**Incident 4 (2026-07-04/05):** Flattening bug destroyed templates 185 & 52 THREE times via MCP writes. Templates now FROZEN.

**Root cause:** Reaching for scripts/MCP writes instead of Bricks standard operations.

### Correct Workflow

```
1. Make all changes via Bricks Builder GUI (primary) or Bricks MCP (when GUI impractical)
2. Run Simply Static export (WP Admin → Simply Static → Generate)
3. Deploy via Wrangler CLI or Cloudflare dashboard
```

## Default Expectations

- Verify important code changes before claiming completion.
- Keep reusable workflows in shared TSOT when they are useful across projects.
- Keep project-specific decisions and constraints in this repo.
- Prefer updating shared skills and workflows at the source when they should apply everywhere.

## Communication Preferences

- Prefer visually engaging responses with clear structure when helpful.
- Use relevant emojis for headings, status, and scannability instead of plain wall-of-text responses.
- Keep technical explanations clear, but make the presentation feel lively and easy to scan.

## Troubleshooting Reference (CRITICAL)

**This is a blogging business project, NOT a development project.**

- **ALWAYS** read `TROUBLESHOOTING.md` at session start before working on this project
- **ALWAYS** check `TROUBLESHOOTING.md` before suggesting fixes or approaches — documented issues may already have solutions
- **ALWAYS** append new issues to `TROUBLESHOOTING.md` when encountering problems that took >5 minutes to resolve
- **DO NOT** use global `lessons.md` for this project — all project-specific issues stay in `TROUBLESHOOTING.md`
- **DO NOT** create separate troubleshooting files — one file, appended chronologically

### Quick Reference

| File | Purpose |
|------|---------|
| `BRICKS-BUILDER-GUIDE.md` | Bricks MCP reference — read BEFORE editing Bricks elements |
| `TROUBLESHOOTING.md` | All known issues, fixes, and prevention rules |
| `DESIGN.md` | Design system source of truth (colors, typography, components) |

### Key Template IDs

| Template | ID | Type | Status |
|----------|----|------|--------|
| Header | 185 | header | 🔴 FROZEN — do not touch |
| Footer | 46 | footer | ✅ Native elements |
| Single Post | 10 | content | ✅ Native elements |
| Blog Archive | 52 | archive | 🔴 FROZEN — do not touch |

## Notes

- This is a WordPress + Simply Static + Cloudflare Pages blog, not a traditional codebase
- Static files live in `D:\Coding Zone\digitrust-lab-static`
- WordPress local URL: `https://digitrust-lab.local`
- Simply Static generate URL: `https://digitrust-lab.local/wp-admin/admin.php?page=simply-static-generate` (NOT `simply-static` — that's settings, not generate)
- Live URL: `https://www.digitrustlab.com` (fully migrated from `blog.digitrustlab.com`, which no longer has a DNS record — do not reference the old subdomain)
- Deploy: `npx wrangler pages deploy "D:\Coding Zone\digitrust-lab-static" --project-name=digitrust-lab-static --branch=main --commit-dirty=true` (or Cloudflare dashboard upload). **Always use the full path** — deploying from the wrong directory deploys source code instead of static HTML. `--commit-dirty=true` silences the git warning when running from inside a git repo.
- Bricks MCP endpoint: `https://digitrust-lab.local/wp-json/bricks-mcp/v1/mcp`
- Bricks MCP connected to: Windsurf, Claude Desktop
- Bricks MCP bridge: `C:\Users\Zamri\bricks-mcp-bridge.mjs` (Claude Desktop only — Windsurf uses native MCP)
- Bridge fix (2026-07-04): Enum truncation bug fixed — full action enums now preserved for all tools
- Template type filter: Use `type: "content"` (not `"single"`) for single post templates
