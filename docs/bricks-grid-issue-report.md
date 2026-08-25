# Bricks CSS Grid Issue — Report & Verdict

**Date:** 2026-07-19
**Site:** digitrustlab.com
**Page:** Homepage (ID 280)
**Element:** Grid container `#brxe-778413`
**Status:** ✅ RESOLVED

---

## TL;DR

On homepage element `#brxe-778413`, plain `1fr` grid tracks expanded to the element's content width (~1100px) instead of sharing space equally. Native Bricks `_display: grid` on this element triggered frontend JS that overrode `grid-template-columns` with pixel values. The deployed workaround uses `_cssCustom` with `minmax(0, 1fr)` + child width constraints.

---

## The Problem

Blog post cards on the homepage were stacking vertically (full width, 1100px each) instead of displaying in a 3-column grid. Massive empty space on the right side of the page.

**Affected element:** `#brxe-778413` — a Bricks container with Query Loop children (blog post cards).

---

## Debugging Timeline

### Phase 1: Initial `_cssCustom` approach (15:04 UTC)
- Applied `display:grid !important; grid-template-columns:repeat(3,1fr) !important` via `_cssCustom`
- **Result:** Cards showed as 1100px each — `1fr` expanded to fit Bricks' default container width
- **Verdict:** ❌ Failed — plain `1fr` doesn't work with 1100px containers

### Phase 2: Native Bricks grid settings (15:19–15:28 UTC)
- Switched to native Bricks settings: `_display: grid`, `_gridTemplateColumns: "repeat(3, 1fr)"`
- **Result:** Bricks added `brx-grid` class to the element, which triggered frontend JavaScript (`bricks.min.js`) that set pixel-based `grid-template-columns` values, completely overriding the CSS
- **Discovery:** Used `browser_evaluate` to inspect computed styles — found `grid-template-columns: 1100px 1100px 1100px` despite CSS rule saying `repeat(3, 1fr)`
- **Verdict:** ❌ Failed — Bricks JS actively overrides native grid settings

### Phase 3: Attempted responsive native settings (15:28 UTC)
- Tried `_gridTemplateColumns:tablet_portrait`, `_gridTemplateColumns:mobile_landscape`, etc.
- **Result:** Desktop view broke entirely — became mobile-like (single column)
- **User reaction:** "wtf its becoming worse!!!!!"
- **Verdict:** ❌ Failed — made things worse

### Phase 4: Snapshot restore (16:11 UTC)
- Restored to pre-session snapshot (ID 584, 14:57 UTC)
- **Result:** Reverted to original flex column layout (cards stacked vertically)
- **Verdict:** ⚠️ Safe state, but layout still broken (no grid)

### Phase 5: `_cssCustom` with `minmax(0, 1fr)` + child width override (17:29 UTC)
- Applied the correct fix:
  ```css
  #brxe-778413 {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 20px !important;
    width: 100% !important;
  }
  #brxe-778413 > * {
    min-width: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
  }
  ```
- **Result:** ✅ 3 equal columns at 373px each, proper responsive breakpoints
- **Verdict:** ✅ FIXED

---

## Root Cause Analysis

### What was NOT the problem
- ❌ Bricks CSS regeneration does NOT strip grid properties from `_cssCustom` — this was a false diagnosis
- ❌ The CSS rules were correctly generated in the stylesheet every time
- ❌ Cache was not the issue — `?nocache=1` confirmed the same behavior

### What WAS the problem
1. **Element width was 1160px, child cards had `width: 1100px`** — observed via `getComputedStyle` on `#brxe-778413` and `#brxe-4c6189` during this session
2. **Plain `1fr` tracks expanded to content size** — CSS spec says `1fr` is equivalent to `minmax(auto, 1fr)`, and `auto` means "fit content." With ~1100px content, each track became ~1100px
3. **Native `_display: grid` added `brx-grid` class on this element** — observed Bricks frontend JS setting pixel-based `grid-template-columns`, overriding CSS rules including `!important`
4. **Card elements had `width: 1100px`** — observed via `getComputedStyle` on `#brxe-4c6189` (class `brxe-container`) during this session

### The fix explained
- `minmax(0, 1fr)` — changes the minimum from `auto` to `0`, forcing tracks to shrink below content size and share space equally
- `> * { width: 100% !important }` — overrides the observed 1100px width on child elements for this container, so they respect the grid track size

---

## What Was Tried and Failed

| Approach | Result | Why |
|----------|--------|-----|
| `_cssCustom` with `1fr` | ❌ 1100px columns | `1fr` = `minmax(auto, 1fr)`, auto expands to content |
| Native `_display: grid` + `_gridTemplateColumns` | ❌ JS override | `brx-grid` class triggers Bricks JS |
| Native with responsive breakpoints | ❌ Broke desktop | JS override + breakpoint conflicts |
| `_cssCustom` with `1fr !important` | ❌ Still 1100px | `!important` doesn't help when track min is `auto` |

## What Worked

| Approach | Result | Why |
|----------|--------|-----|
| `_cssCustom` with `minmax(0, 1fr)` + `> * { width: 100% !important }` | ✅ 373px × 3 | Forces tracks to shrink + overrides child width |

---

## Deployed Workaround (as applied to #brxe-778413)

```css
#brxe-CONTAINER_ID {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: 20px !important;
  width: 100% !important;
}
#brxe-CONTAINER_ID > * {
  min-width: 0 !important;
  max-width: 100% !important;
  width: 100% !important;
}
@media (max-width: 991px) {
  #brxe-CONTAINER_ID {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }
}
@media (max-width: 767px) {
  #brxe-CONTAINER_ID {
    grid-template-columns: 1fr !important;
  }
}
```

**Apply via Respira MCP:**
```
respira_update_element(
  post_id: <PAGE_ID>,
  identifier_type: "id",
  identifier_value: "<CONTAINER_ID>",
  edit_target: "live",
  confirm_live_edit: true,
  updates: {
    "_cssCustom": "<CSS above with correct ID>"
  }
)
```

**After applying:**
1. Regenerate Bricks CSS (WP Admin → Bricks → Settings → Regenerate CSS files)
2. Purge LiteSpeed Cache (WP Admin → LiteSpeed → Toolbox → Purge All - LSCache)
3. Verify frontend with `?nocache=1`

---

## Observations for AI Agent Reference (Windsurf, Codex, Claude, etc.)

1. On this element, native `_display: grid` was overridden by Bricks JS — reproduce and verify before assuming the same on other elements
2. `minmax(0, 1fr)` resolved the `1fr` expansion issue on this element — verify before applying elsewhere
3. `> * { width: 100% !important }` was needed because child cards had `width: 1100px` on this element
4. `_cssCustom` survived CSS regeneration in this session
5. After any Respira DB write: Regenerate Bricks CSS → Purge LiteSpeed → Verify with `?nocache=1`

---

## Verification Evidence

```
Grid: #brxe-778413
display: grid
grid-template-columns: 373.328px 373.328px 373.344px
gap: 20px
cardCount: 3
cardWidths: [373, 373, 373]
titles: ["Test Post 3 — Dummy", "Cara Guna ChatGPT untuk Memban", "Apa Itu AI? (Dan Kenapa Ia Buk"]
```

**Verified:** 2026-07-19 01:30 UTC+8 via `browser_evaluate` on `https://digitrustlab.com/?nocache=1`

---

## Scope and Confidence

This workaround is verified only for homepage element `#brxe-778413`. Reproduce and verify before applying it to any other grid.

This report documents an incident on a specific element. It does not override AGENTS.md's existing Bricks layout policy.

---

## Phase 2: Homepage pagination — root cause and fix (2026-08-25)

**Status:** ✅ RESOLVED

### Problem

Homepage (page 280) was displaying all published posts in one grid instead of paginating. The query loop was on the grid container `#brxe-778413`. That element has **no `hasLoop` property**, so Bricks treated it as inert and fell back to the WordPress default of 10 posts. With 10 posts and no active loop, the pagination element had nothing to page over.

### Root cause

Bricks only activates pagination for a query loop element that carries a `hasLoop: true` flag. `#brxe-778413` (the grid container) never had this flag set — the loop settings were sitting in `_bricks_data` but Bricks' rendering engine ignored them. This is the same class of issue documented in `template-52-layout.md` § "Key lesson" (query loop settings written via MCP are stored in DB but not activated until Bricks GUI saves the template through its PHP hooks).

### Fix applied

1. Query loop moved to the card element `#brxe-4c6189` with `postsPerPage: 6`. That element already carried `hasLoop`, so Bricks activated the loop immediately.
2. Pagination element `#brxe-cctbuz` added as a sibling below the grid container. On first add it defaults to **Main query** and renders "No pagination results." It must be rebound to the `4c6189` loop before it works — this is the trap to remember.

### Verification (logged-out, 2026-08-25)

- Homepage: 6 cards rendered, no excess posts.
- `/page/2/`: HTTP 200, posts 7–10 visible, no duplicates, one grid (no PRIORITY #3 query-loop-on-section regression).
- `/blog/`: unchanged — hero + 9-grid layout intact.
- No PHP errors.

### Canonical decision — `/page/2/` points at homepage, not self-referencing

Rank Math sets the paginated homepage canonical to the homepage root. This was reviewed and **deliberately left as-is**:

- Individual posts are indexed at their own URLs and via `post-sitemap.xml`.
- `/blog/` (template 52) is the canonical post archive and carries proper archive canonicals.
- The paginated homepage view (`/page/2/`) is thin duplicate content that does not need indexing.
- Changing the canonical would require altering a site-wide Rank Math setting to fix a non-problem.

Do not "fix" this in a future session — the decision is intentional.
