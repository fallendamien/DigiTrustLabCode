# Template 52 — Blog Archive Option C Layout

## Phase 1: Template rendering fix (2026-07-09)

**Fixed:** Template 52 was not rendering on `/blog/` due to 3 root causes:
1. **Template status was `private`** — Bricks only queries `publish` templates (database.php line 766)
2. **`archiveType: any` doesn't match `is_home()`** — Bricks treats posts page as `content_type: content`, not archive (database.php line 492, 961)
3. **Stale `ids: ['260']`** — Blog page was deleted and recreated as ID 277

**Fix applied:** Status → `publish`, condition → `ids: ['277']` only (score 10 match).

## Phase 2: Option C layout rebuild (2026-07-20)

**Goal:** Rebuild template 52 with "Option C" layout — featured hero post on top, 3-column grid below, pagination at bottom.

### Final layout (top to bottom)
```
d1sect (Section, bg #FAFAF8, no padding)
└── d2wrap (Container, max-width 1200px, padding 40 20 60)
    ├── d3head — Archive title + description (no query loop)
    ├── d4hero — Hero post (Query Loop: 1 post, offset 0)
    │   └── d4hcrd (Card: image left 48%, text right 52%)
    ├── d5glbl — "Artikel Lain" label (orange bottom border)
    ├── d5grid — 3-column grid (Query Loop: 9 posts, offset 1)
    │   └── qefl9u (Card: image top, text below)
    └── d7pagn — Pagination
```

### What was fixed
1. Element order was wrong — hero rendered at bottom instead of top
2. Hero query loop showed 2 posts instead of 1 (postsPerPage not respected)
3. Grid showed duplicate of hero post (offset not working)

### Tools that worked
- `respira_apply_builder_patch` with `{"children": [...]}` → successfully reordered elements (builder hash changed)
- `respira_inject_builder_content` with `mode: append` → successfully added new elements
- `respira_update_element` → works for non-query settings (padding, colors, typography)
- Bricks GUI → required to activate Query Loop settings (postsPerPage, offset)

### Tools that FAILED
- `respira_move_element` with position numbers → unreliable, positions don't map correctly
- `respira_move_element` with position -1 (append) → did not change DB order
- `respira_reorder_elements` → 500 error ("Element id not found among children")
- `respira_update_element` for query loop settings → NO-OP (settings already in DB but Bricks frontend ignores them)
- `respira_apply_builder_patch` for query settings → builder hash unchanged (no-op)

### Final fix required Bricks GUI
1. Opened template 52 in Bricks editor
2. Selected `d4hero` container → Query Loop was ON but Posts per page was unset (defaulting to 10)
3. Set Posts per page to `1`, Offset to `0`
4. Verified `d5grid` Query Loop: Posts per page `9`, Offset `1`
5. Saved template in Bricks GUI — this registered the query loops properly
6. Regenerated Bricks CSS + code signatures + purged LiteSpeed Cache

### Key lesson
Query loop settings written via Respira MCP to `_bricks_data` are stored in the DB but Bricks' frontend rendering engine does NOT activate them. The Bricks GUI editor must save the template to register query loops through Bricks' internal PHP hooks. This is a Bricks limitation, not a Respira bug.

## ⚠️ UNTESTED: pagination vs manual `offset` — test at post #11 (noted 2026-08-15)

**Status: not a known defect. A flagged risk that has never been exercised.**

The site has **7 published posts** and page one holds **10** (hero 1 + grid 9),
so a second page has never existed. `d7pagn` has therefore never rendered a real
result — in the Bricks builder (`?bricks=run`) it always shows "No pagination
results.", which is a builder placeholder and NOT a frontend fault.

Verified live query config on 2026-08-15 via `respira_bricks_query_loops`:

| Element | Query |
|---|---|
| `d4hero` | `postsPerPage: 1`, `offset: 0` |
| `qefl9u` (grid) | `posts_per_page: 9`, `offset: 1` |

**The risk.** WordPress normally derives the skip from the page number
(`posts_per_page × (page − 1)`). A manual `offset` overrides that calculation,
so page 2 may still skip only 1 post instead of 1 + 9 = 10. Separately,
`max_num_pages` is computed from `found_posts ÷ posts_per_page` **without**
subtracting the offset, so WordPress may advertise a page 2 that has no content.

At 11 posts:

| | Intended | Possible bug |
|---|---|---|
| Page 1 | hero (#1) + posts 2–10 | same |
| Page 2 | post 11 | posts 2–10 repeated, or empty |

Bricks' own query builder may already compensate. Unknown either way.

**Test when post #11 publishes:** load `/blog/?nocache=1`, click to page 2, and
confirm post 11 appears exactly once with no repeat from page 1.

**If it breaks**, the usual remedies are (a) drop the manual offset and exclude
the hero via `post__not_in`, or (b) adjust the offset per page in
`pre_get_posts`. Do not pre-emptively apply either — per the Bricks-Only Policy,
and because query-loop settings written via MCP do not register without a Bricks
GUI save (see Key lesson above).
