# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 🔴 PRIORITY #1: Bricks-Only Policy (CRITICAL)

**RULE: EVERYTHING inside Bricks must be done via Bricks standard procedures — Bricks Builder GUI or Respira MCP. NO post-processing scripts. NO PowerShell CSS injection. NO background code. NO internal hacks. NO exceptions. If it can't be done through Bricks GUI or Respira MCP, it doesn't get done.**

**Exception:** Wrangler CLI is allowed for Cloudflare Pages deployment only — it's a deploy tool, not a Bricks internal operation.

This is a blogging business project, NOT a development project. The user does not want raw code hassles, background scripts, or post-processing pipelines. Everything must use Bricks' own standard operations and tools.

## ✅ Templates 185 & 52 — UNFROZEN (Respira MCP active)

**As of 2026-07-05, Respira MCP replaced the old Bricks MCP.** Respira takes a snapshot before every write and supports one-call rollback. The flattening bug was caused by the old Bricks MCP's `content:update_content` action — Respira does not use that API.

Templates 185 (Header) and 52 (Blog Archive) are now editable via Respira MCP with confidence. Always use `respira_extract_builder_content` before editing and keep the returned `snapshot_uuid` for rollback if needed.

## ✅ Devin's Permitted Scope

**You ARE permitted to:**
- Create and edit WordPress POSTS, PAGES, and Bricks templates via Respira MCP
- Manage menus via Respira MCP menu tools
- Run Simply Static export (WP Admin → Simply Static → Generate → Push)
- Run Wrangler deploy
- Edit AGENTS.md, ROADMAP.md, STATE.json, NEXT.md
- Install or configure plugins
- Manage media via Respira MCP

**You are NOT permitted to:**
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task
- Use the old Bricks MCP endpoint (`/wp-json/bricks-mcp/v1/mcp`) — it is decommissioned
- Use Raw HTML Code elements in Bricks templates

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

### 🧩 Respira MCP (PRIMARY TOOL — replaced old Bricks MCP 2026-07-05)

**Respira MCP is active on digitrust-lab.local.** Connected to Windsurf and Claude Desktop.

**Builder guide:** `BRICKS-BUILDER-GUIDE.md` — Bricks element concepts still apply (settings schema, `_cssCustom`, gotchas). Tool names in the guide refer to old Bricks MCP — use equivalent Respira tools instead.

### Decision Matrix

| Task | Use GUI | Use Respira MCP | Use Non-Bricks Code | Why |
|------|---------|----------------|---------------------|-----|
| Edit page/template content | ✅ WordPress/Bricks GUI | ✅ `respira_update_element` | ❌ | Primary tools |
| Add/remove pages | ✅ WordPress → Pages | ✅ `respira_create_custom_post` | ❌ | Either works |
| Change colors/typography | ✅ Bricks GUI | ✅ `respira_update_bricks_*` | ❌ | Visual editor or MCP |
| Manage WP menus | ✅ Appearance → Menus | ✅ `respira_*_menu*` tools | ❌ | GUI or MCP |
| Deploy to Cloudflare | ✅ Cloudflare dashboard | ❌ | ✅ Wrangler CLI | Deploy tool only |
| Edit templates 185/52 | ✅ With care | ✅ With snapshot | ❌ | Respira has rollback |

### ⚠️ Respira MCP Safety Protocol

- Every write auto-captures a snapshot — response includes `snapshot_uuid`
- Rollback: `respira_restore_snapshot` with the `snapshot_uuid`
- Before ANY template edit: run `respira_extract_builder_content` to see current state
- The old flattening bug (`content:update_content` regenerating IDs) does NOT affect Respira

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
| Header | 185 | header | ✅ Editable via Respira MCP (snapshot before edit) |
| Footer | 46 | footer | ✅ Native elements |
| Single Post | 10 | content | ✅ Native elements |
| Blog Archive | 52 | archive | ✅ Editable via Respira MCP (snapshot before edit) |

## Notes

- This is a WordPress + Simply Static + Cloudflare Pages blog, not a traditional codebase
- Static files live in `D:\Coding Zone\digitrust-lab-static`
- WordPress local URL: `https://digitrust-lab.local`
- Simply Static generate URL: `https://digitrust-lab.local/wp-admin/admin.php?page=simply-static-generate` (NOT `simply-static` — that's settings, not generate)
- Live URL: `https://www.digitrustlab.com` (fully migrated from `blog.digitrustlab.com`, which no longer has a DNS record — do not reference the old subdomain)
- Deploy: `npx wrangler pages deploy "D:\Coding Zone\digitrust-lab-static" --project-name=digitrust-lab-static --branch=main --commit-dirty=true` (or Cloudflare dashboard upload). **Always use the full path** — deploying from the wrong directory deploys source code instead of static HTML. `--commit-dirty=true` silences the git warning when running from inside a git repo.
- Respira MCP: connected to Windsurf and Claude Desktop (replaced old Bricks MCP on 2026-07-05)
- Respira API key stored in Claude Desktop via `.mcpb` install and in Windsurf `mcp_config.json`
- Old Bricks MCP bridge (`bricks-mcp-bridge.mjs`) is decommissioned — do not use
- Template type filter: Use `type: "content"` (not `"single"`) for single post templates
