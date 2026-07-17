# Devin Task: Redesign Homepage + Fix /blog/ + Fix Category Pages

## Context

DigiTrust Lab — Malaysian digital blog (AI Tools + Side Hustle). Static site: Local WP → Bricks Builder 2.3.8 → Simply Static → Wrangler → Cloudflare Pages.

**Live site:** https://www.digitrustlab.com  
**Local WP:** https://digitrust-lab.local  
**Respira MCP:** Active (use `respira_*` tools for all Bricks writes)  
**Design system:** `DESIGN.md` in project root (source of truth — read it before any UI work)

---

## Current State (4 problems to fix)

| URL | Current | Problem |
|---|---|---|
| `digitrustlab.com` (homepage) | "Blog DigiTrust Lab" heading + blank space | No Bricks homepage template — WP default fires, no post cards render |
| `digitrustlab.com/blog/` | Post card shows ✅ but title NOT linked | Dynamic link tag `{post_url}` didn't wire to the heading `link` setting in last session |
| `digitrustlab.com/category/ai-tools/` | Unstyled raw WP output (no Bricks template) | Template 52 `Archive` condition doesn't match `is_tax('category')` |
| `digitrustlab.com/category/digital-side-hustle/` | "Blog DigiTrust Lab" heading + empty grid | Template 52 fires (heading shows) but grid is empty — no posts in this category yet. Will self-resolve when posts are added. |

---

## Design System Reference (from `DESIGN.md` in root)

**Colors:**
- Orange accent: `#E8621A`
- Dark text: `#1A1A1A`
- Body text: `#3A3A3A`
- Warm white bg: `#FAFAF8`
- Subtle bg: `#F5F3EE`
- Border: `#EBEBEB`
- Warm gray meta: `#6B6B6B`
- CTA gradient: `#FFF3EE` → `#FFEADD`, border `#F5C4A0`

**Typography:** Plus Jakarta Sans throughout  
**Max content width:** 1200px (archive/grid), 720px (single post)  
**Card style:** white bg, 1px solid `#EBEBEB`, 10px border-radius, overflow hidden

---

## Task 0 — Fix Broken Dynamic Tags on Single Post Template (Template 10) ✅ COMPLETED

**Problem:** Three dynamic tags in Template 10 (Single Post, page_id: 10) were rendering as raw text instead of real values on every single post page (e.g. `/apa-itu-ai/`):

| What showed | Element ID | Root Cause |
|---|---|---|
| `{post_author:initial}` | `avtcrc` (orange avatar circle) | Bricks has no `:initial` modifier — invalid syntax. No dynamic tag exists for author first initial. |
| `{post_author}` | `mnamet` (author name text) | Wrong tag. Bricks uses `{author_name}` (not `{post_author:name}`) for author display name in text-basic elements. |
| `{rank_math_reading_time}` | `minfot` (date + reading time) | Rank Math does not register this tag with Bricks. No `post_reading_time` dynamic data tag exists either — reading time is only available via the native `post-reading-time` Bricks element. |

**Findings (verified via Bricks source code + Respira + frontend):**
- Author display name is `"Zed"`, first initial is `"Z"`
- The correct Bricks dynamic tag for author name is `{author_name}` (confirmed in `provider-wp.php` line 122, 1576-1581)
- `{post_author:name}` does NOT work — Bricks uses `{author_name}` as the tag, then internally resolves it via `get_author_tag_value()` with `field_type = 'name'`
- `{post_reading_time}` is NOT a dynamic data tag — it's a Bricks element (`post-reading-time`) that calculates reading time via JavaScript on the frontend (or server-side inside query loops)
- No Bricks filter or modifier exists to extract a single character from a dynamic tag (no `:initial`, `:first_char`, or `num_chars` filter)
- The `{echo:}` tag can call PHP functions, but that requires custom PHP — violates Bricks-only policy

### What Was Done (Actual Fix)

**Step 1 — Fix avatar circle (element `avtcrc`)**

Hardcoded `"Z"` — no dynamic tag exists for author first initial in Bricks. Single-author blog, so this is acceptable.

**Step 2 — Fix author name (element `mnamet`)**

Changed `{post_author}` → `{author_name}`. This is the correct Bricks dynamic tag (NOT `{post_author:name}` as the plan originally assumed).

**Step 3 — Restructure meta row for reading time**

Since `{post_reading_time}` is NOT a dynamic data tag (only a Bricks element), we restructured `mtxtcl`:
- Changed `mtxtcl` from column to row direction with `flex-wrap: wrap`
- Set `mnamet` to `width: 100%` (so author name takes full line 1)
- Updated `minfot` text to `{post_date} ·` (date + separator only)
- Injected a native `post-reading-time` element (ID: `891b1e`) into `mtxtcl`
- Moved it from root level into `mtxtcl` via `respira_move_element`
- Styled it: `color: #6B6B6B`, `font-size: 12px`, `suffix: " min baca"`, `contentSelector: #brxe-bodycn`

**Step 4 — Cache clear + re-save**
- Regenerated Bricks CSS files
- Regenerated Bricks code signatures
- Re-saved Template 10 via `respira_update_custom_post`

### Verification (✅ All passed)

Verified on `https://digitrust-lab.local/apa-itu-ai/?nocache=2`:

| Element | Expected | Actual | Dynamic? |
|---|---|---|---|
| Avatar (`avtcrc`) | `Z` | `Z` ✅ | ❌ Hardcoded (no dynamic tag exists) |
| Author (`mnamet`) | `Zed` | `Zed` ✅ | ✅ `{author_name}` |
| Date (`minfot`) | `July 9, 2026 ·` | `July 9, 2026 ·` ✅ | ✅ `{post_date}` |
| Reading time (`891b1e`) | `X min baca` | `4 min baca` ✅ | ✅ Native `post-reading-time` element (JS-calculated) |

### Key Lessons

1. **`{author_name}` not `{post_author:name}`** — Bricks uses `author_*` prefix (not `post_author:*`). The tag is registered as `author_name` in `provider-wp.php` line 122.
2. **No reading time dynamic tag** — `post_reading_time` is an element type, not a dynamic data tag. Must use the native `post-reading-time` element.
3. **No character-level filters** — Bricks has `num_words` filter but no `num_chars` or `:initial` modifier. Can't extract first character of a dynamic tag value.
4. **`{echo:}` exists but requires PHP** — Could call custom functions, but violates Bricks-only policy for this project.

---

## Task 1 — Fix `/blog/` Post Title Link ✅ COMPLETED (Previous session)

**Problem:** The post card on `/blog/` showed the title as text but it wasn't clickable. The heading element's `link` setting was using `type: "dynamic"` which doesn't work for `{post_url}`.

**Root Cause:** Bricks `set_link_attributes()` in `base.php` requires `type: "external"` when the URL contains a dynamic data tag like `{post_url}`. The `type: "dynamic"` link type is for a different use case and doesn't resolve `{post_url}`.

**Fix Applied:** Updated heading element `mnjhh4` on Template 52 with:
```json
{
  "link": {
    "type": "external",
    "url": "{post_url}"
  }
}
```

**Key Lesson:** When linking to a post URL via dynamic data in Bricks, use `type: "external"` with `url: "{post_url}"`, NOT `type: "dynamic"` with `dynamicData: "{post_url}"`. The `external` link type detects the `{...}` pattern and routes it through `bricks_render_dynamic_data()` with `context: 'link'` (see `base.php` lines 2405-2426).

---

## Task 2 — Fix Category Pages (`/category/ai-tools/` etc.)

**Problem:** Template 52's `Archive` condition matches `is_home()` (the /blog/ posts page) but does NOT match `is_tax('category')` (taxonomy category archives). So `/category/ai-tools/` gets raw WP default output.

**Fix:** Add a second condition to Template 52 — `Archive → Categories & Tags` — so the template fires on both the posts page AND taxonomy archives.

**Steps:**

### 2a — Update Template 52 conditions in Bricks editor

Open `https://digitrust-lab.local/template/blog-archive/?bricks=run`

Go to: Gear icon → Template Settings → CONDITIONS

Current state: One condition = `Archive` (no sub-type)

**Add a second condition** (click `+ ADD CONDITION`):
- Type: `Archive`
- Archive type: `Categories & Tags`

Result: Template 52 now has TWO conditions:
1. `Archive` (no sub-type) — matches `/blog/` posts page via `is_home()`
2. `Archive → Categories & Tags` — matches `/category/ai-tools/` etc. via `is_tax()`

Save with Ctrl+S. Confirm "Template saved" toast.

### 2b — Update the heading to show dynamic archive title

Currently the heading in Template 52 is hardcoded: `"Blog DigiTrust Lab"`. On category pages it should show "AI Tools" or "Digital Side Hustle" instead.

Use `respira_extract_builder_content(page_id: 52)` to get element IDs, then find the heading with `"text": "Blog DigiTrust Lab"` (element ID `d4titl`).

Update it to use a conditional dynamic tag:
```json
{
  "text": "{archive_title}"
}
```

Also update the subtitle element (`d4sub1`) which currently shows hardcoded tagline:
```json
{
  "text": "{archive_description}"
}
```

**Why:** `{archive_title}` returns "Blog DigiTrust Lab" on `/blog/` (the WP posts page title) and "AI Tools" / "Digital Side Hustle" on category pages. `{archive_description}` returns the category description set in WP Admin → Posts → Categories.

### 2c — Set category descriptions in WP Admin

Navigate to `https://digitrust-lab.local/wp-admin/edit-tags.php?taxonomy=category`

Set descriptions for each category:
- **AI Tools** → `"Panduan, tips, dan ulasan AI tools terbaik untuk bantu korang kerja lagi cepat dan produktif."`
- **Digital Side Hustle** → `"Cara jana pendapatan sampingan secara digital — dari produk digital, Etsy, hingga affiliate marketing."`
- **Canva & Design** → `"Tutorial Canva, template design, dan cara buat visual yang menarik walaupun bukan designer."`
- **AI untuk Perniagaan Kecil** → `"Cara perniagaan kecil Malaysia guna AI untuk jimat masa, tingkat jualan, dan tumbuh lagi pantas."`

Use `respira_update_term` for each:
```
taxonomy: "category"
id: [term_id]
description: "[description above]"
```

Or do it via WP Admin → Posts → Categories → Edit each category.

### 2d — Verify

Check these URLs on local:
- `https://digitrust-lab.local/category/ai-tools/` — should show "AI Tools" heading + Bricks card grid with "Apa Itu AI?" post
- `https://digitrust-lab.local/category/digital-side-hustle/` — should show "Digital Side Hustle" heading + empty grid (no posts yet — that's fine)

---

## Task 3 — Build the Homepage

**Problem:** Homepage (`digitrustlab.com`) has no Bricks template. It shows the WP default output which is just the posts page heading + nothing.

**Strategy:** At current stage (1 post, growing blog), the homepage should be a proper brand landing page — NOT just a post grid. It should:
1. Introduce DigiTrust Lab with a clear value proposition
2. Show the latest 3 posts as a preview
3. Drive email sign-ups

**How this works technically:** In WP Reading Settings, `homepage` is currently not set (both are blank after the earlier session). We need to:
- Create a new static "Home" page in WP
- Set it as the Homepage in WP Settings → Reading
- Keep Blog page (ID 260) as the Posts page
- Build the Home page content in Bricks

### 3a — Create the Home page

Use `respira_create_custom_post` or `respira_update_page` to create a page:
- Title: `Home`
- Slug: `/` (or just leave blank — WP uses it as static front)
- Status: `publish`

Or in WP Admin → Pages → Add New → Title: "Home" → Publish.

Get the new page ID.

### 3b — Set it as homepage in WP Settings → Reading

Use Respira:
```
respira_update_option(option: "page_on_front", value: [new_home_page_id])
```

(The `show_on_front` is already set to `page` from earlier session.)

### 3c — Build the Home page in Bricks

Open the Home page in Bricks editor: WP Admin → Pages → Home → Edit with Bricks

Build these sections using native Bricks elements:

---

#### SECTION 1 — Hero

```
Section (bg: #FAFAF8, padding top/bottom 60px)
  Container (max-width 720px, margin auto, direction column, align center, text-align center)
    text-basic — "AI Tools & Side Hustle Digital untuk Malaysia 🇲🇾"
                 font-size 11px, color #E8621A, font-weight 600, uppercase, letter-spacing 0.08em
                 margin-bottom 12px
    heading h1 — "Korang Pun Boleh Guna AI untuk Kerja dan Jana Pendapatan"
                 font-size 32px (mobile: 24px), font-weight 700, color #1A1A1A, line-height 1.3
                 margin-bottom 16px
    text-basic — "DigiTrust Lab berkongsi cara guna AI tools, buat side hustle digital, dan jana pendapatan tambahan — dalam bahasa yang korang faham."
                 font-size 15px, color #6B6B6B, line-height 1.6, max-width 520px
                 margin-bottom 32px
    Container (direction row, gap 12px, justify center, wrap)
      button — "Baca Artikel Terbaru"
               link: /blog/
               bg #E8621A, color white, 6px radius, 10px 20px padding, font-size 13px, weight 600
      button — "Tentang Kami"
               link: /tentang-kami/
               bg transparent, color #1A1A1A, border 1px solid #EBEBEB, 6px radius, 10px 20px padding
               font-size 13px, weight 600
```

---

#### SECTION 2 — Latest Posts (3-col grid)

```
Section (bg: #FAFAF8, padding top 40px bottom 60px)
  Container (max-width 1200px, margin auto, direction column, padding left/right 20px)

    Container (direction row, justify space-between, align center, margin-bottom 24px)
      heading h2 — "Artikel Terbaru"
                   font-size 20px, font-weight 700, color #1A1A1A
      text-basic — "→ Semua artikel"
                   link: /blog/
                   font-size 13px, color #E8621A, font-weight 600, text-decoration none

    Container (id: homegrid, hasLoop: true)
      query:
        objectType: post
        postType: ["post"]
        orderby: date
        order: DESC
        postsPerPage: 3
      _cssCustom: "#brxe-homegrid { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; width: 100%; }
                   @media(max-width:991px){ #brxe-homegrid { grid-template-columns: repeat(2,1fr); } }
                   @media(max-width:478px){ #brxe-homegrid { grid-template-columns: 1fr; } }"

      [LOOP CHILDREN — repeat per post:]

      Container "card" (direction column, bg #ffffff, border 1px solid #EBEBEB, border-radius 10px, overflow hidden)

        image (featured_image, width 100%, height 180px, object-fit cover)

        Container "card-body" (direction column, padding 16px, gap 8px)

          text-basic "{post_terms_category}"
            font-size 10px, font-weight 600, color #E8621A, uppercase, letter-spacing 0.05em

          heading h3 "{post_title}"
            link: dynamic → {post_url}
            font-size 15px, font-weight 700, color #1A1A1A, line-height 1.35
            _cssCustom: "a { color: #1A1A1A; text-decoration: none; } a:hover { color: #E8621A; }"

          text-basic "{post_excerpt:20}"
            font-size 12px, color #6B6B6B, line-height 1.5
            _cssCustom: "display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;"

          text-basic "{post_date}"
            font-size 11px, color #6B6B6B
```

---

#### SECTION 3 — Email Opt-in CTA strip

```
Section (bg: linear-gradient(135deg, #FFF3EE 0%, #FFEADD 100%), border-top 1px solid #F5C4A0, padding 40px 20px)
  Container (max-width 560px, margin auto, direction column, align center, text-align center)

    text-basic — "PERCUMA"
                 font-size 10px, font-weight 700, color #E8621A, uppercase, letter-spacing 0.1em
                 margin-bottom 8px

    heading h2 — "Dapatkan 50 Prompt AI Percuma untuk Perniagaan Malaysia"
                 font-size 20px, font-weight 700, color #1A1A1A
                 margin-bottom 8px

    text-basic — "Masukkan email korang dan kami hantar terus. Percuma. Berhenti langgan bila-bila masa."
                 font-size 13px, color #6B6B6B, line-height 1.5
                 margin-bottom 20px

    [Bricks form element — simple email opt-in]
    form:
      fields:
        - id: "eml001", type: email, placeholder: "Email korang...", required: true, width: 100
      actions: ["email"]
      emailSubject: "New DigiTrust Lab Opt-in"
      emailTo: "admin_email"
      submitButtonText: "Dapatkan Percuma →"
      successMessage: "✅ Dah hantar! Check inbox korang."
    form styling:
      input: bg #F5F3EE, border 1px solid #EBEBEB, radius 6px, padding 10px 12px, font-size 13px
      button: bg #E8621A, color white, radius 6px, font-size 13px, weight 700, padding 10px 16px, full width
      margin-top 8px on button
```

---

#### SECTION 4 — Category pills (navigation shortcuts)

```
Section (bg: #FAFAF8, padding 32px 20px, border-top 1px solid #EBEBEB)
  Container (max-width 800px, margin auto, direction column, align center)

    text-basic — "Terokai Mengikut Topik"
                 font-size 12px, color #6B6B6B, text-align center, margin-bottom 16px

    Container (direction row, justify center, gap 10px, wrap)
      button "🤖 AI Tools"        → link /category/ai-tools/
      button "💰 Side Hustle"     → link /category/digital-side-hustle/
      button "🎨 Canva & Design"  → link /category/canva-design/  (or use actual slug)
      button "🏪 AI untuk Bisnes" → link /category/ai-untuk-perniagaan-kecil/

    All category buttons:
      bg: #F5F3EE, color #1A1A1A, border 1px solid #EBEBEB
      radius 20px (pill), padding 8px 16px, font-size 12px, weight 600
      hover: bg #E8621A, color white, border-color #E8621A
```

---

### 3d — Set Bricks to use the Home page

After building, make sure WP knows to use it as the front page:
1. Confirm `show_on_front = page` (already set)
2. Confirm `page_on_front = [new home page ID]`
3. Confirm `page_for_posts = 260` (Blog page, already set)

Check `https://digitrust-lab.local/` — should show the new homepage, not the blog listing.

---

## Task 4 — Bricks Cache Clear + Deploy

> ⚠️ **Simply Static + Wrangler deploy is no longer used.** The site is served directly from Hostinger WordPress (LiteSpeed Cache + Cloudflare proxy). The export/deploy steps below are kept for historical reference only.

After ALL tasks above are complete:

### 4a — Clear Bricks cache
1. WP Admin → Bricks → Settings → click **"Regenerate CSS files"**
2. WP Admin → Bricks → Settings → click **"Regenerate code signatures"** (accept dialog)
3. Re-save both Template 52 and the Home page via Respira:
   ```
   respira_update_custom_post(type: "bricks_template", id: 52, status: "publish", edit_target: "live")
   respira_update_page(id: [home_page_id], status: "publish", edit_target: "live")
   ```

### 4b — Old export/deploy step (historical)
The previous workflow was: WP Admin → Simply Static → Generate → wait for completion.

### 4c — Old Wrangler deploy step (historical)
From `D:\Coding Zone\digitrust-lab-static`:
```powershell
npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main
```

**Current workflow:** After saving Bricks changes and purging LiteSpeed Cache, the live site updates automatically.

---

## Verification Checklist

Run through each URL after deploy:

| URL | Expected | Check |
|---|---|---|
| `digitrustlab.com/apa-itu-ai/` | Avatar = `Z`, author = `Zed`, date = `July 9, 2026 · X min read` | ☐ |
| `digitrustlab.com` | Hero + 3-post grid + opt-in + category pills | ☐ |
| `digitrustlab.com/blog/` | "Blog DigiTrust Lab" heading + post card with **clickable title** | ☐ |
| `digitrustlab.com/category/ai-tools/` | "AI Tools" heading + Bricks card + "Apa Itu AI?" post | ☐ |
| `digitrustlab.com/category/digital-side-hustle/` | "Digital Side Hustle" heading + empty grid (fine, no posts yet) | ☐ |

---

## Hard Rules (AGENTS.md)

- ✅ Respira MCP only — `respira_*` tools for all Bricks writes
- ✅ Snapshot Template 52 before editing: `respira_list_snapshots(post_id: 52)`, keep UUID
- ✅ Native Bricks elements only — no Code elements, no raw HTML widgets
- ✅ `#brxe-{elementId}` in `_cssCustom` (not `%root%`)
- ✅ Element IDs: exactly 6 lowercase alphanumeric characters
- ✅ Dynamic tags: bare `{tag}` in text, `{"useDynamicData": "{tag}"}` in image, `{"type": "dynamic", "dynamicData": "{tag}"}` in link
- ✅ After template edits: Regenerate CSS → Regenerate code signatures → re-save → Simply Static → Wrangler
- ❌ Do NOT touch Template 185 (Header) or Template 10 (Single Post) — not in scope
- ❌ Do NOT create a separate template for the category archive — extend Template 52 instead
- ❌ Do NOT use post-processing scripts, mu-plugins, or custom PHP

## Rollback

If Template 52 breaks:
```
respira_restore_snapshot(snapshot_uuid: "[uuid from before edits]")
```

If homepage breaks: delete the Home page and reset Reading Settings:
```
respira_update_option(option: "show_on_front", value: "posts")
```

---

## Priority Order

Execute in this exact order — each task is independent but ordered by risk:
1. **Task 0** (dynamic tag fixes on Template 10) — 10 min, 3 Respira calls, highest visible impact
2. **Task 1** (title link fix on Template 52) — 5 min, zero risk, immediate win
3. **Task 2** (category page fix) — 15 min, moderate, fixes unstyled pages
4. **Task 3** (homepage build) — 30 min, new page so no rollback risk
5. **Task 4** (cache clear + deploy) — do once at the very end, covers all changes
