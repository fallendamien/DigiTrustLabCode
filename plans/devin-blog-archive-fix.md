# Devin Task: Fix Blog Archive Template 52 — Template Conditions & Status Fix

## Context

DigiTrust Lab is a WordPress blog running:
- **Local WP:** `https://digitrust-lab.local` (PHP 8.2.29, Nginx, MySQL)
- **Builder:** Bricks Builder Ultimate 2.3.8
- **MCP:** Respira MCP (active, connected)
- **Deploy pipeline:** Simply Static → Wrangler → Cloudflare Pages

## The Bug

`/blog/` (the WordPress Posts page) shows the default Bricks `posts` widget instead of our custom template 52 design (heading, tagline, post card grid). The single post at `/apa-itu-ai/` works fine.

**Root cause (confirmed — 3 issues, all fixed 2026-07-09):**

1. **Template status was `private` (PRIMARY CAUSE):** Bricks only queries templates with `post_status: 'publish'` in `get_all_templates_by_type()` (database.php line 766). Template 52 was set to `private`, making it completely invisible to Bricks' template matching system. No condition could ever match because the template was never in the candidate list.

2. **`archiveType: any` does NOT match the WordPress posts page:** Bricks treats `is_home()` as `content_type: 'content'` (database.php line 492), NOT as an archive. The `archiveType` condition is only evaluated when `is_archive()` is true (database.php line 961). Since `is_home()` returns `false` for `is_archive()`, the `archiveType: any` condition can NEVER match on `/blog/`.

3. **Old `ids` condition referenced deleted page ID 260:** The previous template conditions included `ids: ['260']` for a Blog page that was deleted and recreated as page ID 277. The stale ID meant the `ids` condition never matched the current posts page.

**Fix (all 3 applied):**
1. Changed template status from `private` to `publish`
2. Removed `archiveType: any` condition (useless for posts page)
3. Set `ids: ['277']` as the sole condition — Bricks sets `$post_id = get_option('page_for_posts')` (277) on `is_home()`, so the `ids` condition matches with score 10 (highest priority)

> **Note on the `posts` element:** The original investigation incorrectly identified the Bricks `posts` element as the root cause. The `posts` element was already replaced with manual loop elements (container + image + heading + text-basic with dynamic data tags) in an earlier session. The real issue was purely template conditions + status. The manual loop pattern is correct and remains in place.

---

## Current Template 52 Structure (exact, verified via Respira)

```json
[
  {
    "type": "section", "id": "d1sect", "parent": 0,
    "settings": {
      "_background": {"color": {"raw": "#FAFAF8"}},
      "_padding": {"bottom": "0", "left": "0", "right": "0", "top": "0"}
    },
    "children": ["d2wrap"]
  },
  {
    "type": "container", "id": "d2wrap", "parent": "d1sect",
    "settings": {
      "_alignItems": "center", "_direction": "column",
      "_margin": {"left": "auto", "right": "auto"},
      "_padding": {"bottom": "40px", "left": "20px", "right": "20px", "top": "40px"},
      "_width": "100%", "_widthMax": "1200px"
    },
    "children": ["d3head", "d5grid", "d7pagn"]
  },
  {
    "type": "block", "id": "d3head", "parent": "d2wrap",
    "settings": {
      "_alignItems": "center",
      "_cssCustom": "#brxe-d3head{text-align:center;width:100%;}",
      "_direction": "column", "_margin": {"bottom": "32px"}, "_width": "100%"
    },
    "children": ["d4titl", "d4sub1"]
  },
  {
    "type": "heading", "id": "d4titl", "parent": "d3head",
    "settings": {
      "_margin": {"bottom": "6px", "top": "0"},
      "_typography": {"color": {"hex": "#1A1A1A"}, "font-size": "28px", "font-weight": "700"},
      "tag": "h1", "text": "Blog DigiTrust Lab"
    }
  },
  {
    "type": "text-basic", "id": "d4sub1", "parent": "d3head",
    "settings": {
      "_typography": {"color": {"hex": "#6B6B6B"}, "font-size": "13px"},
      "text": "Perkongsian AI Tools & Side Hustle Digital"
    }
  },
  {
    "type": "container", "id": "d5grid", "parent": "d2wrap",
    "settings": {
      "_cssCustom": "#brxe-d5grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;width:100%;} @media(max-width:991px){#brxe-d5grid{grid-template-columns:repeat(2,1fr);}} @media(max-width:478px){#brxe-d5grid{grid-template-columns:1fr;}}",
      "_width": "100%",
      "hasLoop": true,
      "query": {
        "is_main_query": true,
        "objectType": "post",
        "postType": ["post"],
        "postsPerPage": 9,
        "orderby": "date",
        "order": "DESC"
      }
    },
    "children": ["d6post"]  ← THIS IS THE PROBLEM ELEMENT
  },
  {
    "type": "posts",  ← BROKEN: archive-only widget, does nothing in this context
    "id": "d6post", "parent": "d5grid",
    "settings": {
      "_cssCustom": "#brxe-d6post .bricks-post-wrapper{...}"  ← styles lost
    }
  },
  {
    "type": "pagination", "id": "d7pagn", "parent": "d2wrap",
    "settings": {
      "_cssCustom": "#brxe-d7pagn .page-numbers{...}",
      "_margin": {"top": "32px"}
    }
  }
]
```

---

## What To Do

### Step 1 — Take a snapshot before touching anything

```
respira_list_snapshots(post_id: 52)
```

Keep the latest `snapshot_uuid` for rollback if needed.

---

### Step 2 — Remove the broken `posts` element (d6post)

Use `respira_remove_element`:
```
identifier_type: "id"
identifier_value: "d6post"
post_id: 52
```

---

### Step 3 — Add post card child elements inside the d5grid loop container

The `d5grid` container already has `hasLoop: true` with a valid query. It just needs actual content children instead of the broken `posts` element.

Add these elements as children of `d5grid` (post_id: 52), in this order. Each element is a direct child of the loop container, so they repeat per post.

**New child structure — one post card = a container wrapping image + category + title + excerpt + date:**

#### 3a — Card container (replaces d6post as the loop item)
Use `respira_update_element` or `respira_apply_builder_patch` to inject the following flat element list into post_id 52. Use `respira_batch_update` if available, otherwise add elements one at a time using `respira_add_*` tools or direct content injection.

**Recommended approach:** Use `respira_inject_builder_content` with `mode: "append_to"` targeting `d5grid`, OR use `respira_batch_update` with the full new element list for d5grid's children.

The card structure (all children of d5grid, repeating per loop iteration):

```
d5grid (existing loop container — keep as-is, just replace children)
  └── [new] container "card wrap" — white card, border, border-radius, overflow hidden
        ├── [new] image — featured image, dynamic data, 160px height, cover
        ├── [new] container "card body" — padding 16px, column direction
        │     ├── [new] text-basic "category label" — {post_terms_category}, orange, uppercase, 10px, 600 weight
        │     ├── [new] heading "post title" — {post_title} linked to {post_url}, h2, 15px, 700 weight, dark
        │     ├── [new] text-basic "excerpt" — {post_excerpt:25}, 12px, grey, 2-line clamp
        │     └── [new] text-basic "date" — {post_date}, 11px, grey
```

**Exact element settings to recreate (preserve the visual design from the old `posts` element):**

**Card wrap container:**
```json
{
  "type": "container",
  "id": "GENERATE_NEW_6CHAR_ID",
  "parent": "d5grid",
  "settings": {
    "_direction": "column",
    "_background": {"color": {"hex": "#ffffff"}},
    "_border": {
      "style": "solid",
      "color": {"hex": "#EBEBEB"},
      "width": {"top": 1, "right": 1, "bottom": 1, "left": 1},
      "radius": {"top": "10px", "right": "10px", "bottom": "10px", "left": "10px"}
    },
    "_cssCustom": "#brxe-CARD_ID{overflow:hidden;}"
  }
}
```

**Featured image:**
```json
{
  "type": "image",
  "id": "GENERATE_NEW_6CHAR_ID",
  "parent": "CARD_ID",
  "settings": {
    "image": {"useDynamicData": "{featured_image}"},
    "_cssCustom": "#brxe-IMG_ID{width:100%;height:160px;object-fit:cover;display:block;}"
  }
}
```

**Card body container:**
```json
{
  "type": "container",
  "id": "GENERATE_NEW_6CHAR_ID",
  "parent": "CARD_ID",
  "settings": {
    "_direction": "column",
    "_padding": {"top": "16px", "right": "16px", "bottom": "16px", "left": "16px"},
    "_gap": "6px"
  }
}
```

**Category label:**
```json
{
  "type": "text-basic",
  "id": "GENERATE_NEW_6CHAR_ID",
  "parent": "BODY_ID",
  "settings": {
    "text": "{post_terms_category}",
    "_typography": {
      "font-size": "10px",
      "font-weight": "600",
      "color": {"hex": "#E8621A"},
      "text-transform": "uppercase",
      "letter-spacing": "0.05em"
    },
    "_margin": {"bottom": "4px"}
  }
}
```

**Post title (linked):**
```json
{
  "type": "heading",
  "id": "GENERATE_NEW_6CHAR_ID",
  "parent": "BODY_ID",
  "settings": {
    "tag": "h2",
    "text": "{post_title}",
    "link": {"type": "dynamic", "dynamicData": "{post_url}"},
    "_typography": {
      "font-size": "15px",
      "font-weight": "700",
      "color": {"hex": "#1A1A1A"},
      "line-height": "1.35"
    },
    "_margin": {"bottom": "6px", "top": "0"},
    "_cssCustom": "#brxe-TITLE_ID a{color:#1A1A1A;text-decoration:none;}"
  }
}
```

**Excerpt:**
```json
{
  "type": "text-basic",
  "id": "GENERATE_NEW_6CHAR_ID",
  "parent": "BODY_ID",
  "settings": {
    "text": "{post_excerpt:25}",
    "_typography": {
      "font-size": "12px",
      "color": {"hex": "#6B6B6B"},
      "line-height": "1.5"
    },
    "_cssCustom": "#brxe-EXCERPT_ID{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}"
  }
}
```

**Date:**
```json
{
  "type": "text-basic",
  "id": "GENERATE_NEW_6CHAR_ID",
  "parent": "BODY_ID",
  "settings": {
    "text": "{post_date}",
    "_typography": {
      "font-size": "11px",
      "color": {"hex": "#6B6B6B"}
    },
    "_margin": {"top": "4px"}
  }
}
```

> **Element ID rules:** Every Bricks element ID must be exactly 6 lowercase alphanumeric characters (e.g. `c1a2rd`, `imgwrp`, `bdytxt`). Generate unique IDs — never duplicate an existing ID on the page.

---

### Step 4 — Fix the template conditions (CRITICAL — 3 issues found)

#### Issue 1: Template status must be `publish` (not `private`)

Bricks queries templates with `post_status: 'publish'` only (database.php line 766). If the template is `private`, it is invisible to the template matching system — no condition will ever match.

```
respira_update_custom_post(type: "bricks_template", id: 52, status: "publish")
```

#### Issue 2: `archiveType: any` does NOT work for the posts page

WordPress `is_home()` (the posts page at `/blog/`) returns `false` for `is_archive()`. Bricks treats `is_home()` as `content_type: 'content'` (database.php line 492). The `archiveType` condition is only evaluated inside `if ( is_archive() && $condition['main'] === 'archiveType' )` (database.php line 961). Therefore, `archiveType: any` can NEVER match the posts page.

#### Issue 3: Use `ids` condition targeting the Blog page ID (277)

On `is_home()`, Bricks sets `$post_id = get_option('page_for_posts')` (database.php line 438-439). For our site, this is page ID 277. The `ids` condition checks `in_array($post_id, $condition['ids'])` (database.php line 911) and assigns score 10 (highest priority).

**The correct final condition is `ids: ['277']` only** (no `archiveType`, no old page IDs):

Save via Bricks AJAX (the reliable method — `templateSettings` meta key is protected and direct Respira meta updates may not persist correctly):

```javascript
// Run in browser console on a WP admin page
const formData = new FormData();
formData.append('action', 'bricks_save_post');
formData.append('postId', '52');
formData.append('nonce', '36dae4decb'); // Get current nonce from window.bricksData?.nonce
formData.append('templateSettings', JSON.stringify({
  templateConditions: [
    { id: 'cond001', main: 'ids', ids: ['277'] }
  ]
}));

fetch('/wp-admin/admin-ajax.php', { method: 'POST', body: formData })
  .then(r => r.json()).then(console.log);
```

> **Why `ids` works:** On `is_home()`, Bricks sets `$post_id = page_for_posts` (277). The `ids` condition matches this with score 10 (line 911-913), which is the highest possible score. This overrides any other template that might match.
>
> **Why `archiveType` fails:** `is_archive()` returns `false` on the posts page. The `archiveType` condition check at line 961 is gated behind `if ( is_archive() )`, so it's never reached.
>
> **Why template status matters:** `get_all_templates_by_type()` queries with `post_status: 'publish'` (line 766). A `private` template is never in the candidate list, so no condition is ever evaluated for it.

---

### Step 5 — Clear Bricks cache (CRITICAL — do not skip)

After any template change, Bricks caches the rendered HTML separately from the DB. The static export will pick up stale content if you skip this.

Do these in order via Respira or WP Admin:

1. **Regenerate CSS files:** `respira_bricks_health_check` triggers this, or do it manually via WP Admin → Bricks → Settings → "Regenerate CSS files"
2. **Regenerate code signatures:** WP Admin → Bricks → Settings → "Regenerate code signatures" (accept the confirmation dialog)
3. **Re-save the template:** `respira_update_custom_post(type: "bricks_template", id: 52, status: "publish", edit_target: "live")` — forces Bricks to re-render

---

### Step 6 — Verify on local

Navigate to `https://digitrust-lab.local/blog/` and confirm:
- ✅ "Blog DigiTrust Lab" heading visible
- ✅ "Perkongsian AI Tools & Side Hustle Digital" tagline visible
- ✅ Post card for "Apa Itu AI?" visible with: featured image (or placeholder), category label "AI TOOLS" in orange, post title linked, excerpt text, date
- ✅ No broken layout or error messages
- ✅ Single post `/apa-itu-ai/` still works (unaffected)

---

### Step 7 — Simply Static export + deploy

Only after local verification passes:

1. WP Admin → Simply Static → Generate → wait for completion
2. From `D:\Coding Zone\digitrust-lab-static`:
   ```powershell
   npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main
   ```
3. Verify `https://www.digitrustlab.com/blog/` shows the post card

---

## Hard Rules (from AGENTS.md — do not violate)

- ✅ Use Respira MCP for all Bricks writes (`respira_*` tools only)
- ✅ Take a snapshot before editing Template 52
- ✅ Use only native Bricks elements — no Code elements, no raw HTML widgets
- ✅ Use `#brxe-{elementId}` in `_cssCustom` (not `%root%` — that only works in the GUI)
- ✅ All element IDs: exactly 6 lowercase alphanumeric characters
- ✅ Dynamic tags in text fields: bare `{tag}`, in image fields: `{"useDynamicData": "{tag}"}`, in links: `{"type": "dynamic", "dynamicData": "{tag}"}`
- ❌ Do NOT use the old Bricks MCP endpoint (`/wp-json/bricks-mcp/v1/mcp`) — decommissioned
- ❌ Do NOT use post-processing scripts, mu-plugins, or custom PHP for styling
- ❌ Do NOT touch Template 185 (Header) — not part of this task

## Rollback

If anything goes wrong at any step:
```
respira_restore_snapshot(snapshot_uuid: "<uuid from Step 1>")
```
This restores Template 52 to its pre-edit state.

---

## Summary of Changes

| What | Before | After |
|------|--------|-------|
| Template status | `private` (invisible to Bricks) | `publish` (visible to template matching) |
| Template condition | `archiveType: any` + `ids: ['260']` (deleted page) | `ids: ['277']` (current Blog page) |
| Loop child element | `posts` (archive-only widget, replaced earlier) | Manual container + image + heading + text-basic elements with dynamic data |
| `is_main_query` | `true` | `true` (unchanged — keep this) |
| `/blog/` rendering | Default Bricks `posts` widget | Custom heading + tagline + post card grid |

## Key Bricks Source Code References

| File | Line(s) | What it does |
|------|---------|--------------|
| `includes/database.php` | 438-439 | Sets `$post_id = page_for_posts` on `is_home()` |
| `includes/database.php` | 492 | Maps `is_home` to `content_type: 'content'` |
| `includes/database.php` | 766 | Queries templates with `post_status: 'publish'` only |
| `includes/database.php` | 897-928 | `ids` condition matching — checks `in_array($post_id, $condition['ids'])`, score 10 |
| `includes/database.php` | 961 | `archiveType` condition — gated behind `if ( is_archive() )`, never reached on `is_home()` |
| `includes/templates.php` | 405-408 | `flush_templates_cache` on `save_post` hook |
| `includes/ajax.php` | 2306-2313 | Bricks AJAX save for `templateSettings` (includes `templateConditions`) |
| `includes/ajax.php` | 1468-1472 | `$bricks_data_changed` only true if `content`/`header`/`footer`/`pageSettings` in POST |
| `functions.php` | 94 | `BRICKS_DB_TEMPLATE_SETTINGS` = `_bricks_template_settings` |
