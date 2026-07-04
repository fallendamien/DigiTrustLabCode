# Bricks MCP Absolute — Skill

## When to Use

**Trigger:** ANY task involving visual/styling changes to Bricks elements.
**Full rule:** See `AGENTS.md` § PRIORITY #1. **No exceptions for styling/layout/visual changes.**

## 🔴 FROZEN TEMPLATES — DO NOT TOUCH

**Template 185 (Header) and Template 52 (Blog Archive) are FROZEN.**

Do NOT read, write, open in Bricks GUI, or attempt to fix these templates via any method.
If a task requires changes to these templates, **STOP and tell Zamri**: "This requires touching a frozen template. Escalate to Claude."

## Protocol

### Step 1: Identify the Approach

```
Is this a visual/styling change?
  → YES → Use Bricks MCP. NO EXCEPTIONS.
  → NO → Is this a simple text edit?
    → YES → Guide user to WordPress/Bricks GUI
    → NO → Use Bricks MCP anyway

NEVER use post-process scripts, PowerShell, or any background code for Bricks tasks.
Wrangler CLI is allowed for deployment only.
```

### ✅ Permitted Scope
- Create and edit WordPress POSTS and PAGES (content only, not Bricks templates)
- Manage menus via Bricks MCP menu tools
- Run Simply Static export (WP Admin → Simply Static → Generate → Push)
- Run Wrangler deploy
- Install or configure plugins (not Bricks templates)
- Manage media via Bricks MCP

### ❌ NOT Permitted
- Write to template IDs 185 or 52 via any method
- Open template 185 or 52 in the Bricks visual editor
- Use `content:update_content` on post_id 185 or 52
- Use post-processing scripts, PowerShell, or mu-plugins for any styling task

### Step 2: Read the Builder Guide

Read `BRICKS-BUILDER-GUIDE.md` before editing elements. Key gotchas documented there:
- `_gap` doesn't work on containers → use `_cssCustom`
- `#brxe-{id}` not `%root%` for CSS selectors
- `_widthMax` not `_maxWidth`

### Step 3: Use the Right MCP Tool

| Task | MCP Tool | Key Properties |
|------|----------|----------------|
| Edit element padding | `content` (update_content) | `_padding: {top, right, bottom, left}` |
| Edit element colors | `content` (update_content) | `_typography: {color: {raw: "#hex"}}`, `_background: {color: {raw: "#hex"}}` |
| Custom CSS on element | `content` (update_content) | `_cssCustom: "#brxe-{id} { ... }"` |
| Responsive CSS | `content` (update_content) | `_cssCustom` with `@media` queries |
| Animation transitions | `content` (update_content) | `_cssCustom` with `transition` properties |
| Global classes | `design` (global_class) | Create/manage reusable classes |
| Page-level CSS | `code` (set_page_css) | Page-specific CSS injection |
| Template structure | `template` + `content` | Create/modify template elements |

**Full MCP tool reference:** `.devin/rules/bricks-standard-guide.md`

### Step 4: Verify After Changes

1. Re-export via Simply Static (WP Admin → Simply Static → Generate)
2. Deploy via Wrangler CLI or Cloudflare dashboard
3. Visually verify on live site
