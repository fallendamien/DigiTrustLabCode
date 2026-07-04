# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 🔴 PRIORITY #1: Bricks-Only Policy (CRITICAL)

**RULE: EVERYTHING inside Bricks must be done via Bricks standard procedures — Bricks Builder GUI or Bricks MCP. NO post-processing scripts. NO PowerShell CSS injection. NO background code. NO internal hacks. NO exceptions. If it can't be done through Bricks GUI or Bricks MCP, it doesn't get done.**

**Exception:** Wrangler CLI is allowed for Cloudflare Pages deployment only — it's a deploy tool, not a Bricks internal operation.

This is a blogging business project, NOT a development project. The user does not want raw code hassles, background scripts, or post-processing pipelines. Everything must use Bricks' own standard operations and tools.

### 🧩 Bricks MCP Server (PRIMARY TOOL)

**Bricks MCP is installed and active on digitrust-lab.local.** Connected to Windsurf and Claude Desktop.

**Full tool reference:** `.devin/rules/bricks-standard-guide.md` (always_on)

**Rule: For ANY Bricks template task (read, write, modify, create), use Bricks MCP tools. NO EXCEPTIONS for styling/layout/visual changes. Only fall back to direct DB/PHP if MCP is literally unavailable (server down).**

### 📖 Bricks Builder Guide (REFERENCE FILE)

**Full reference:** `.devin/rules/bricks-standard-guide.md`

**Quick summary:**
- **`BRICKS-BUILDER-GUIDE.md`** — Local reference for Bricks MCP element settings, style properties, animations, query loops, forms, components, popups, and gotchas
- **ALWAYS read it before editing Bricks elements via MCP** — prevents common trial-and-error mistakes (e.g. `_gap` doesn't work on containers, use `_cssCustom` instead; `#brxe-{id}` not `%root%`; `_widthMax` not `_maxWidth`)

### Decision Matrix

| Task | Use GUI | Use Bricks MCP | Use Non-Bricks Code | Why |
|------|---------|----------------|---------------------|-----|
| Change nav labels | ✅ Bricks → Header template → edit text | ⚠️ Possible | ❌ | 2 min in GUI |
| Edit page content | ✅ WordPress → Pages → edit | ⚠️ Possible | ❌ | Standard WP editing |
| Change footer links/labels | ✅ Bricks → Footer template → edit | ⚠️ Possible | ❌ | 2 min in GUI |
| Add/remove pages | ✅ WordPress → Pages | ❌ | ❌ | Standard WP |
| Change colors/typography | ✅ Bricks → Settings → Custom CSS | ✅ `design` tool | ❌ | Visual editor or MCP |
| Add/remove nav items | ✅ Bricks → Header template | ✅ `menu` tool | ❌ | Drag and drop or MCP |
| Rebuild template structure | ⚠️ Guide user in GUI | ✅ `content` tool (`update_content`) | ❌ | `template:update` only does metadata |
| Read template data | ❌ | ✅ `template` tool (`get`) | ❌ | MCP is cleanest read path |
| Write/replace elements | ❌ | ✅ `content` tool (`update_content`) | ❌ | `template:update` silently ignores `elements` |
| Create/manage global classes | ❌ | ✅ `design` tool | ❌ | MCP is primary for design tokens |
| Manage WP menus | ✅ Appearance → Menus | ✅ `menu` tool | ❌ | GUI or MCP |
| Search bar | ✅ Bricks → add Search element | ✅ `content` tool | ❌ | Native Bricks element |
| Deploy to Cloudflare | ✅ Cloudflare dashboard upload | ❌ | ✅ Wrangler CLI | Deploy tool only, not Bricks internal |

### Protocol

```
BEFORE doing anything for this project, ask:

1. Can this be done in the Bricks Builder GUI? → If YES, guide the user to do it there
2. Can this be done via Bricks MCP? → If YES, use MCP tools (template, content, design, menu, etc.)
3. Can this be done in the WordPress admin GUI? → If YES, guide the user to do it there
4. None of the above? → STOP. Do not use scripts, PowerShell, post-processing, or any non-Bricks method.

NEVER use raw HTML Code elements, inline styles, or non-Bricks frameworks for template structure.
NEVER use element name "code" in Bricks JSON.
NEVER write PHP mu-plugins or direct DB queries for Bricks tasks.
NEVER use post-process scripts, PowerShell, or background code for Bricks styling/template tasks.
Wrangler CLI is allowed for deployment only (not for Bricks internal operations).
ALL Bricks JSON must use native element names and follow Bricks schema.
```

### ⚠️ Bricks MCP Destructive Actions (CRITICAL)

**These MCP actions silently destroy data. Always backup before using.**

| Action | What Happens | Prevention |
|--------|-------------|------------|
| `template update` with `type` change | **Wipes ALL elements** — returns `elements: []` | NEVER change type after elements exist |
| `template update` with `elements` param | **Silently ignores `elements`** — returns success but elements unchanged | Use `content update_content` with `post_id` to write elements |
| `content update_content` | **Replaces ALL elements** — not just the one you pass | Always provide the COMPLETE element array |
| `content delete` with `element_id` | **Trashes the entire post** — not just the element | NEVER use on templates with elements |

**Correct workflow for creating Bricks templates via MCP:**
```
1. `content create` — create template with title, post_type, status, AND elements all at once
2. `template set` — set template type and conditions (type + conditions together)
3. `content update_content` — update individual elements if needed (provide FULL array)
```

**NEVER use `template update` to change type after elements exist.**
**NEVER use `template update` to write elements — it only updates metadata (title, status, slug, type, tags, bundles). Use `content update_content` with `post_id` instead.**

### What Happened (Lesson Learned — MULTIPLE TIMES)

**Incident 1:** Previous sessions spent 45+ minutes writing PHP mu-plugins, dealing with serialized arrays, `wp_hash()` signatures, and DB queries — for tasks that would have taken **2 minutes in the Bricks GUI**.

**Incident 2 (2026-07-04):** Instead of using Bricks MCP to fix footer layout, mobile menu animation, and Tentang Kami padding, CSS was injected via `post-process-static.ps1`. The injected CSS fought with Bricks' native CSS, making the mobile menu animation WORSE (sudden disappear, jittery opening). The padding fix also didn't work because post-process CSS was being overridden by Bricks' own exported styles.

**Incident 3 (2026-07-04):** JSON backup files created by AI had structural issues when re-imported via Bricks GUI — elements were missing after import. User decided to handle all backups manually and banned all AI-created backup mechanisms.

**Root cause:** Reaching for PowerShell/scripts instead of Bricks standard operations.

**Lesson: EVERYTHING via Bricks standard procedures. NO scripts. NO post-processing. NO exceptions.**

### The Correct Workflow

```
1. Make all changes via Bricks Builder GUI (primary) or Bricks MCP (when GUI impractical)
2. Run Simply Static export (WP Admin → Simply Static → Generate)
3. Deploy via Wrangler CLI or Cloudflare dashboard
```

### When Code IS Appropriate

**NEVER for Bricks tasks.** All Bricks work must be done through Bricks GUI or Bricks MCP. No scripts, no post-processing, no background code for Bricks internal operations. Wrangler CLI for deployment is the only exception.

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
| Header | 185 | header | ✅ Native elements |
| Footer | 46 | footer | ✅ Native elements |
| Single Post | 10 | content | ✅ Native elements |
| Blog Archive | 52 | archive | ✅ Native elements |

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
