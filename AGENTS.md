# Project Rules

This file contains project-specific rules and operating standards for AI coding agents.

## 🔴 PRIORITY #1: Bricks-Native Policy (CRITICAL)

**RULE: Use Bricks MCP as the primary interface for all Bricks Builder operations. Prefer WordPress/Bricks GUI for simple content edits. Code is allowed IF AND ONLY IF it follows Bricks native standards (Bricks JSON schema, native element names, Bricks API/hooks). No random HTML, external frameworks, or non-Bricks code patterns.**

This is a blogging business project, NOT a development project. The user does not want raw code hassles when the same result can be achieved through the WordPress or Bricks Builder GUI. However, programmatic approaches that use Bricks' own data structures and APIs are acceptable when GUI automation isn't practical (e.g. browser automation of the Bricks editor is unreliable).

### 🧩 Bricks MCP Server (PRIMARY TOOL)

**Bricks MCP is installed and active on digitrust-lab.local.** Connected to Windsurf and Claude Desktop.

**Full tool reference:** `.devin/rules/bricks-standard-guide.md` (always_on)

**Rule: For ANY Bricks template task (read, write, modify, create), use Bricks MCP tools FIRST. Only fall back to direct DB/PHP if MCP is unavailable or the specific operation isn't supported by MCP.**

### 📖 Bricks Builder Guide (REFERENCE FILE)

**Full reference:** `.devin/rules/bricks-standard-guide.md`

**Quick summary:**
- **`BRICKS-BUILDER-GUIDE.md`** — Local reference for Bricks MCP element settings, style properties, animations, query loops, forms, components, popups, and gotchas
- **ALWAYS read it before editing Bricks elements via MCP** — prevents common trial-and-error mistakes (e.g. `_gap` doesn't work on containers, use `_cssCustom` instead; `#brxe-{id}` not `%root%`; `_widthMax` not `_maxWidth`)

### Decision Matrix

| Task | Use GUI | Use Bricks MCP | Use Bricks-Native Code | Use Non-Bricks Code | Why |
|------|---------|----------------|------------------------|---------------------|-----|
| Change nav labels | ✅ Bricks → Header template → edit text | ⚠️ Possible | ⚠️ Only if GUI impractical | ❌ | 2 min in GUI |
| Edit page content | ✅ WordPress → Pages → edit | ⚠️ Possible | ❌ | ❌ | Standard WP editing |
| Change footer links/labels | ✅ Bricks → Footer template → edit | ⚠️ Possible | ⚠️ Only if GUI impractical | ❌ | 2 min in GUI |
| Add/remove pages | ✅ WordPress → Pages | ❌ | ❌ | ❌ | Standard WP |
| Change colors/typography | ✅ Bricks → Settings → Custom CSS | ✅ `design` tool | ❌ | ❌ | Visual editor or MCP |
| Add/remove nav items | ✅ Bricks → Header template | ✅ `menu` tool | ⚠️ Only if GUI impractical | ❌ | Drag and drop or MCP |
| Rebuild template structure | ⚠️ Guide user in GUI | ✅ `template` + `content` tools | ✅ Bricks JSON fallback | ❌ | MCP is primary, JSON is fallback |
| Read template data | ❌ | ✅ `template` tool | ⚠️ Direct DB only if MCP down | ❌ | MCP is cleanest read path |
| Create/manage global classes | ❌ | ✅ `design` tool | ❌ | ❌ | MCP is primary for design tokens |
| Manage WP menus | ✅ Appearance → Menus | ✅ `menu` tool | ❌ | ❌ | GUI or MCP |
| Search bar injection | ❌ | ❌ | ❌ | ✅ PowerShell | Simply Static strips forms — no GUI fix |
| Double-slash link fix | ❌ | ❌ | ❌ | ✅ PowerShell | Simply Static bug — no GUI fix |
| Post-processing pipeline | ❌ | ❌ | ❌ | ✅ PowerShell | Automates export fixes across 100+ files |
| Deploy to Cloudflare | ❌ | ❌ | ❌ | ✅ Wrangler CLI | Faster than dashboard upload |

### Protocol

```
BEFORE writing any code for this project, ask:

1. Can this be done via Bricks MCP? → If YES, use MCP tools (template, content, design, menu, etc.)
2. Can this be done in the Bricks Builder GUI? → If YES (and MCP not suitable), guide the user to do it there
3. Can this be done in the WordPress admin GUI? → If YES, guide the user to do it there
4. Is this a Bricks template task where MCP is unavailable? → Use Bricks-native JSON/code (native element names only: section, container, block, nav-menu, button, search, image, etc.)
5. Is this a Simply Static export bug with no GUI fix? → Use PowerShell/code
6. Is this a bulk automation task across many files? → Use PowerShell/code

NEVER use raw HTML Code elements, inline styles, or non-Bricks frameworks for template structure.
NEVER use element name "code" in Bricks JSON.
NEVER write PHP mu-plugins or direct DB queries for Bricks tasks when MCP is available.
ALL Bricks JSON must use native element names and follow Bricks schema.
```

### ⚠️ Bricks MCP Destructive Actions (CRITICAL)

**These MCP actions silently destroy data. Always backup before using.**

| Action | What Happens | Prevention |
|--------|-------------|------------|
| `template update` with `type` change | **Wipes ALL elements** — returns `elements: []` | NEVER change type after elements exist |
| `content update_content` | **Replaces ALL elements** — not just the one you pass | Always provide the COMPLETE element array |
| `content delete` with `element_id` | **Trashes the entire post** — not just the element | NEVER use on templates with elements |

**Correct workflow for creating Bricks templates via MCP:**
```
1. `content create` — create template with title, post_type, status, AND elements all at once
2. `template set` — set template type and conditions (type + conditions together)
3. `content update_content` — update individual elements if needed (provide FULL array)
```

**NEVER use `template update` to change type after elements exist.**

### What Happened (Lesson Learned)

The previous sessions spent 45+ minutes writing PHP mu-plugins, dealing with serialized arrays, `wp_hash()` signatures, and DB queries — for tasks that would have taken **2 minutes in the Bricks GUI** (changing nav labels, editing page text, updating footer links).

**The code approach was needed initially** because the header was broken (missing signature, corrupted data). But once the header was working, all subsequent content edits (Tentang→Tentang Kami, Hubungi→Hubungi Kami, Zamri→Zed, 2024→2022, Privasi→Polisi Privasi) should have been done in the GUI.

### The Correct Workflow

```
1. Make content/layout changes via Bricks MCP (primary) or Bricks/WordPress GUI (simple edits)
2. Run Simply Static export (WP Admin → Simply Static → Generate)
3. Run post-process-static.ps1 (PowerShell — fixes export-only bugs)
4. Deploy via wrangler CLI
```

### When Code IS Appropriate

**Bricks MCP (PRIMARY — always use first):**
- Reading/writing templates, elements, global classes, theme styles
- Managing WordPress menus, media, components
- Page-level CSS/JS management
- Design tokens (palettes, variables, typography scales, fonts)

**Bricks-Native Code (fallback when MCP unavailable):**
- Writing Bricks template JSON with native element names (section, container, block, nav-menu, button, search, image)
- Bricks API hooks and filters (`add_filter('bricks/...')`, etc.)
- One-shot DB fixes when Bricks GUI AND MCP can't access broken data
- Template import/export via Bricks JSON format

**Non-Bricks Code (allowed for specific cases):**
- `post-process-static.ps1` — fixes Simply Static export bugs (form stripping, double-slash links)
- Wrangler CLI deploy — faster than dashboard
- Bulk find/replace across 100+ static HTML files

**NEVER Allowed:**
- Raw HTML Code elements in Bricks templates (element name "code")
- Inline HTML/CSS/JS pretending to be Bricks elements
- Non-Bricks frameworks (React, Vue, etc.) injected into templates
- Random PHP that doesn't use Bricks APIs or WordPress hooks
- PHP mu-plugins for Bricks tasks when MCP is available

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

## Notes

- This is a WordPress + Simply Static + Cloudflare Pages blog, not a traditional codebase
- Static files live in `D:\Coding Zone\digitrust-lab-static`
- WordPress local URL: `https://digitrust-lab.local`
- Live URL: `https://blog.digitrustlab.com`
- Deploy command: `npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main`
- Bricks MCP endpoint: `https://digitrust-lab.local/wp-json/bricks-mcp/v1/mcp`
- Bricks MCP connected to: Windsurf, Claude Desktop
