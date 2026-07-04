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

### ⚠️ Step 2.5: Pre-Write Verification (CRITICAL)

**Before ANY `content update_content` call on an existing template:**

1. **READ FIRST:** Call `template get` (or `content get` with `post_id`) to retrieve current elements
2. **VERIFY STRUCTURE:** Check every element has correct `parent` field (not `0` unless root section) and `children` arrays are intact
3. **PRESERVE NESTING:** When writing back, ALWAYS include explicit `children` arrays and correct `parent` refs on every element — never partially edit
4. **VERIFY AFTER WRITE:** Immediately call `template get` again to confirm nesting held and element IDs haven't changed
5. **NEVER open/save in Bricks GUI** without verifying structure first — GUI saves can trigger the flattening bug

**Known bug:** `content update_content` on template ID 52 (and possibly others) can flatten the structure — all elements get `parent: 0` and new auto-generated IDs, breaking `_cssCustom` selectors that reference old IDs.

**Symptom:** Title/subtitle render left-aligned instead of centered because `#brxe-{old_id}` CSS selector points at an element ID that no longer exists after the flattened save.

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

1. **Verify template structure** — `template get` to confirm nesting held (see Step 2.5)
2. Re-export via Simply Static (WP Admin → Simply Static → Generate)
3. Deploy via Wrangler CLI or Cloudflare dashboard
4. Visually verify on live site
