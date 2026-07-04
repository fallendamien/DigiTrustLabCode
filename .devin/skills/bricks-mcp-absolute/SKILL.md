# Bricks MCP Absolute — Skill

## When to Use

**Trigger:** ANY task involving visual/styling changes to Bricks elements.
**Full rule:** See `AGENTS.md` § PRIORITY #1. **No exceptions for styling/layout/visual changes.**

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
