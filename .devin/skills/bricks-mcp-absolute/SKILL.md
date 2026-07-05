# Respira MCP Absolute — Skill

## When to Use

**Trigger:** ANY task involving visual/styling changes to Bricks elements.
**Full rule:** See `AGENTS.md` § PRIORITY #1. **No exceptions for styling/layout/visual changes.**

## ✅ Templates 185 & 52 — UNFROZEN (Respira MCP active)

Templates 185 (Header) and 52 (Blog Archive) are editable via Respira MCP with confidence.
- Always run `respira_extract_builder_content` before editing
- Keep `snapshot_uuid` from response for rollback via `respira_restore_snapshot`

## Protocol

### Step 1: Identify the Approach

```
Is this a visual/styling change?
  → YES → Use Respira MCP. NO EXCEPTIONS.
  → NO → Is this a simple text edit?
    → YES → Guide user to WordPress/Bricks GUI
    → NO → Use Respira MCP anyway

NEVER use post-process scripts, PowerShell, or any background code for Bricks tasks.
Wrangler CLI is allowed for deployment only.
```

### ✅ Permitted Scope
- Create and edit WordPress POSTS, PAGES, and Bricks templates via Respira MCP
- Manage menus via Respira MCP menu tools
- Run Simply Static export (WP Admin → Simply Static → Generate → Push)
- Run Wrangler deploy
- Install or configure plugins
- Manage media via Respira MCP

### ❌ NOT Permitted
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task
- Use the old Bricks MCP endpoint (`/wp-json/bricks-mcp/v1/mcp`) — decommissioned

### Step 2: Read the Builder Guide

Read `BRICKS-BUILDER-GUIDE.md` before editing elements. Key gotchas still apply:
- `_gap` doesn't work on containers → use `_cssCustom`
- `#brxe-{id}` not `%root%` for CSS selectors
- `_widthMax` not `_maxWidth`

> ⚠️ Tool names in the guide are old Bricks MCP — use equivalent `respira_*` tools.

### Step 3: Use the Right Respira Tool

| Task | Respira Tool |
|------|--------------|
| Read page/template elements | `respira_extract_builder_content` |
| Find a specific element | `respira_find_element` |
| Edit element settings/CSS | `respira_update_element` |
| Batch update multiple elements | `respira_batch_update` |
| Global classes | `respira_update_bricks_global_class` |
| Page-level CSS | `respira_update_page` (custom_css field) |
| Rollback a write | `respira_restore_snapshot` with `snapshot_uuid` |

**Full Respira tool reference:** `.devin/rules/bricks-standard-guide.md`

### Step 4: Verify After Changes

1. Re-export via Simply Static (WP Admin → Simply Static → Generate)
2. Deploy via Wrangler CLI or Cloudflare dashboard
3. Visually verify on live site
