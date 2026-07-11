# Devin Implementation Plan — UI Fixes & Single Post Template

> **Prepared by:** Claude (Session 11, 2026-07-10)  
> **Execute via:** Respira MCP + Bricks Builder GUI  
> **Do NOT:** Touch templates 185 (Header) or write raw HTML Code elements  
> **After all tasks:** Run Simply Static export → Wrangler deploy  

> **Task Status (updated 2026-07-11):**
> | Task | Status | Notes |
> |------|--------|-------|
> | Task 1 (Homepage Copy & Mobile) | ⬜ Pending | Not started |
> | Task 2 (Blog Archive Overflow) | ✅ Done | `min-width: 0` on `.brxe-qefl9u`, verified at 375px, deployed |
> | Task 3 (Category Pages) | ⬜ Pending | Needs Bricks GUI for condition change |
> | Task 4 (Single Post Redesign) | ⬜ Pending | Not started |
> | Task 5 (Export & Deploy) | ✅ Done | Blog page export fixed (additional_urls + mu-plugin), deployed via Wrangler |

---

## PRE-FLIGHT (do this first, every session)

```
1. Open Windsurf → confirm Respira MCP is connected (green dot)
2. Confirm local WP is running at https://digitrust-lab.local/
3. Read AGENTS.md before starting
4. Take a Respira snapshot of every template you will edit BEFORE touching it
   - respira_extract_builder_content(page_id=280) → note snapshot
   - respira_extract_builder_content(page_id=10)  → note snapshot
   - respira_extract_builder_content(page_id=52)  → note snapshot
```

---

## TASK 1 — Homepage Copy & Mobile Layout (Page ID 280)

### 1A — Hero Copy Changes

**Element `2994e0` (text-basic — orange eyebrow line)**  
Remove the text entirely — delete this element.

**Element `dbb365` (h1 heading)**  
Change text from:
```
Korang pun boleh guna AI untuk buat kerja dan jana pendapatan
```
To:
```
Guna AI untuk Jana Pendapatan Tambahan
```
Keep all existing typography settings (font-size 32, weight 700, color #1A1A1A, line-height 1.3).

**Element `c6c956` (subheadline text-basic)**  
Change text from:
```
DigiTrust Lab berkongsi cara guna AI tools, buat side hustle digital, dan jana pendapatan tambahan — dalam bahasa yang korang faham.
```
To:
```
Panduan praktikal AI tools dan peluang pendapatan digital — dalam bahasa Malaysia yang mudah difahami.
```

### 1B — Hero Section Mobile Padding Fix

**Element `821824` (section — hero wrapper)**  
Add mobile breakpoint override:
```
_padding (mobile, max-width 478px):
  top: 40
  bottom: 40
  left: 0
  right: 0
```

**Element `6a08c8` (container — hero inner)**  
Add mobile breakpoint override for padding:
```
_padding (mobile, max-width 478px):
  left: 16
  right: 16
```
Change `_widthMax` from `720` to `600` (tighter on desktop too, better reading width).

### 1C — Article Grid Section Mobile Fix

**Element `c47f41` (container — "Artikel Terbaru" wrapper)**  
Add mobile breakpoint padding override:
```
_padding (mobile, max-width 478px):
  top: 24
  left: 16
  right: 16
```

**Element `778413` (container — 3-col grid loop)**  
The existing CSS already has `@media(max-width:478px){grid-template-columns:1fr;}` — this is correct.  
Verify this is working. If the grid is still 3-col on mobile, update `_cssCustom` to:
```css
#brxe-hm02gr {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  width: 100%;
}
@media (max-width: 767px) {
  #brxe-hm02gr { grid-template-columns: 1fr; }
}
```
(Changed breakpoint from 478px to 767px so tablets also go single column.)

### 1D — Email CTA Section Mobile Fix

**Element `74e786` (section — email CTA)**  
Add mobile padding override:
```
_padding (mobile, max-width 478px):
  top: 32
  bottom: 32
  left: 16
  right: 16
```

**Element `afb8cc` (form)**  
Update `_cssCustom` to remove `max-width:420px` on mobile:
```css
#brxe-hm03fm { width: 100%; max-width: 420px; margin: 0 auto; }
@media (max-width: 478px) { #brxe-hm03fm { max-width: 100%; } }
```

### 1E — Category Pills Section Mobile Fix

**Element `2a9ce6` (section — category pills)**  
Add mobile padding override:
```
_padding (mobile, max-width 478px):
  top: 24
  bottom: 24
  left: 16
  right: 16
```

**Element `b8bfe4` (container — pills row)**  
Existing `_cssCustom` already has `flex-wrap:wrap;gap:10px;justify-content:center;` — this is correct.  
No change needed here.

### 1F — Save & Verify Homepage

After all edits:
1. Open https://digitrust-lab.local/ in browser
2. Use Chrome DevTools → toggle device toolbar → iPhone SE (375px)
3. Verify: no horizontal scroll, all sections stack vertically, text is readable, buttons are full-width or near-full-width
4. Verify h1 reads: "Guna AI untuk Jana Pendapatan Tambahan"
5. Verify eyebrow "AI Tools & Side Hustle Digital untuk warga Malaysia" is GONE

---

## TASK 2 — Blog Archive Horizontal Scroll Fix (Template ID 52)

### Root Cause
The horizontal scroll on `/blog/` is caused by an element inside Template 52 that exceeds viewport width — most likely the grid container `d5grid` or the image element `ayo2hr` lacking `max-width:100%`.

### 2A — Fix Image Overflow

**Element `ayo2hr` (image inside post card)**  
Update `_cssCustom` from:
```css
#brxe-cdimgx { width:100%; height:160px; object-fit:cover; display:block; }
```
To:
```css
#brxe-ayo2hr { width:100%; max-width:100%; height:160px; object-fit:cover; display:block; overflow:hidden; }
```
Note: The existing `_cssCustom` targets `#brxe-cdimgx` which is the WRONG ID. Fix it to target `#brxe-ayo2hr` (the actual element ID).

### 2B — Fix Section/Container Overflow

**Element `d1sect` (top-level section)**  
Add to `_cssCustom`:
```css
#brxe-d1sect { overflow-x: clip; }
```
Use `clip` not `hidden` (avoids collapsing min-height in Chromium).

**Element `d2wrap` (main wrapper container)**  
Add to `_cssCustom`:
```css
#brxe-d2wrap { overflow-x: clip; }
```

### 2C — Fix Grid Breakpoints

**Element `d5grid` (3-col grid container)**  
Update `_cssCustom` to:
```css
#brxe-d5grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 100%;
}
@media (max-width: 991px) {
  #brxe-d5grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 767px) {
  #brxe-d5grid { grid-template-columns: 1fr; }
}
```

### 2D — Verify Blog Archive

1. Navigate to https://digitrust-lab.local/blog/
2. Chrome DevTools → iPhone SE (375px)
3. Confirm: NO horizontal scrollbar, post cards stack single column, images don't overflow

---

## TASK 3 — Fix Category Pages Showing Homepage Content

### Root Cause (documented in AGENTS.md)
Template 52 has condition `ids: ['277']` only — matches the Blog page specifically.  
Category pages (`/category/digital-side-hustle/`) are true WordPress archives (`is_archive()=true`).  
They currently fall through to the default WordPress theme template, which renders the homepage or a default loop.

### 3A — Add Archive Condition to Template 52

Open Template 52 in **Bricks Builder GUI** (not Respira — conditions must be set via GUI):

1. Go to https://digitrust-lab.local/wp-admin/edit.php?post_type=bricks_template
2. Find template ID 52 ("blog-archive") → click "Edit with Bricks"
3. Click Settings (top right gear icon) → Conditions
4. Current condition: `Content type: Page` + `Pages: Blog (ID 277)` — KEEP THIS
5. Click "+ Add Condition" → add a SECOND condition:
   - Type: `Archive`
   - Archive type: `Term archive` (or "Taxonomy archive")
   - Leave taxonomy blank (matches ALL taxonomies — category, tag, etc.)
6. Save template with Ctrl+S

**Expected result:** Template 52 now renders on both `/blog/` AND `/category/*/` pages.

### 3B — Fix Archive Title Dynamic Tag

**Element `d4titl` (h1 in archive header, text = `{archive_title}`)**  
The `{archive_title}` dynamic tag should automatically output:
- "Blog DigiTrust Lab" on `/blog/`  
- "AI Tools" on `/category/ai-tools/`  
- "Digital Side Hustle" on `/category/digital-side-hustle/`

Verify this is working after the condition fix. If `{archive_title}` outputs "Category: AI Tools" with the "Category:" prefix, add a custom CSS to hide the prefix OR use `{term_name}` instead.

**If prefix appears**, update element `d4titl` text to `{term_name}` for category pages. To handle both blog and category, use:
```
{archive_title}
```
And add this CSS to element `d4titl` settings → `_cssCustom`:
```css
#brxe-d4titl { text-transform: capitalize; }
```

### 3C — Verify Category Pages

1. Navigate to https://digitrust-lab.local/category/digital-side-hustle/
2. Should show Template 52 layout with "Digital Side Hustle" heading (NOT homepage content)
3. Navigate to https://digitrust-lab.local/category/ai-tools/
4. Should show Template 52 layout with "AI Tools" heading
5. Navigate to https://digitrust-lab.local/blog/ — must still work correctly

---

## TASK 4 — Single Post Template Redesign (Template ID 10)

### Design Goals
- Clean, consistent, publication-quality layout used for EVERY new post
- Correct semantic order: Category pill → H1 → Meta (author + date + read time) → Excerpt → Featured image → TOC → Body → CTA → Share → Author bio
- Mobile-first: sidebar collapses below content on mobile, not hidden
- Fix the broken dynamic tags: `{author_name}`, `{post_date}`, `{post_reading_time}`
- Remove the messy `after_element` / `after_children` metadata artifacts

### Current Element Structure (for reference)
```
section#sectn1
  └── container#contnr (row → column on mobile)
        ├── block#mainbl (main content column)
        │     ├── text-basic#catlbl     → {post_terms_category}
        │     ├── heading#h1titl        → {post_title} [h1]
        │     ├── block#metarw          → author row
        │     │     ├── text-basic#avtcrc → avatar circle "Z"
        │     │     └── block#mtxtcl
        │     │           ├── text-basic#mnamet → {author_name}
        │     │           ├── text-basic#minfot → {post_date} ·
        │     │           └── post-reading-time#891b1e
        │     ├── text-basic#excrpt     → {post_excerpt} [italic blockquote]
        │     ├── image#featim          → {featured_image}
        │     ├── block#tocbox          → Table of Contents
        │     ├── post-content#bodycn   → post body
        │     ├── block#ctabox          → AI Mastery CTA
        │     ├── post-sharing#shrrow   → social share
        │     └── post-author#biobox    → author bio box
        └── block#sidebl (sticky sidebar)
              ├── block#optcrd          → email opt-in card
              └── block#popcrd          → popular posts card
```

### 4AA — Fix Sidebar Opt-in Card Copy (Element IDs in block `optcrd`)

**Element `optttl` (card title text-basic)**
Change text from:
```
Panduan Percuma
```
To:
```
Dapatkan Panduan Percuma
```

**Element `optdsc` (description text-basic)**
Change text from:
```
Dapatkan 50 Prompt AI percuma untuk perniagaan Malaysia
```
To:
```
50 Prompt AI yang korang boleh guna terus untuk buat kerja dan jimat masa.
```

**Element `optsub` (small print text-basic)**
Change text from:
```
Percuma. Berhenti langgan bila-bila masa.
```
To:
```
Percuma sepenuhnya. Unsubscribe bila-bila masa.
```

**Element `nofkdz` (form — submit button text)**
Change `submitButtonText` from `"Send"` (default, never updated) to:
```
Hantar →
```
Do this via `respira_update_element` on element `nofkdz`, updating `settings.submitButtonText`.

---

### 4A — Fix Dynamic Tags

**Element `mnamet` (author name)**  
Current text: `{author_name}` — this should work if the post has an author set.  
Verify it renders correctly. If blank, change to `{post_author}` (older Bricks dynamic tag).

**Element `minfot` (date + separator)**  
Current text: `{post_date} ·`  
This is correct. Verify it outputs a real date (e.g. "9 Julai 2026 ·").  
If it outputs the raw tag as text, change to `{echo:get_the_date('j F Y')} ·`

**Element `891b1e` (post-reading-time)**  
Current: `contentSelector: #brxe-bodycn`, `suffix: " min baca"`  
This should work. Verify it shows a number (e.g. "4 min baca").

### 4B — Fix Meta Row Layout

**Element `mtxtcl` (block containing name + date + read time)**  
Current `_cssCustom`: `#brxe-mtxtcl{flex-wrap:wrap;gap:0 4px;}`  
Update to make name on one line and date+readtime on second line:
```css
#brxe-mtxtcl {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
```

**Element `mnamet` (author name)**  
Remove `_width: "100%"` — not needed with column direction.  
Update `_cssCustom` to add:
```css
#brxe-mnamet { font-size: 12px; font-weight: 600; color: #1A1A1A; }
```

Create a new **row sub-container** inside `mtxtcl` to hold `minfot` + `891b1e` side by side:
- New container (direction: row, gap: 4px, align-items: center)
  - Move `minfot` inside it
  - Move `891b1e` inside it

**Element `minfot`**  
Update text to: `{post_date}` (remove the trailing ` ·` — use a separator via CSS or a dot element instead)  
Update `_cssCustom`:
```css
#brxe-minfot::after { content: " · "; color: #6B6B6B; }
```

### 4C — Fix Featured Image Styling

**Element `featim` (featured image)**  
Update settings:
```
_cssCustom: #brxe-featim { width:100%; border-radius:8px; overflow:hidden; margin-bottom:24px; }
            #brxe-featim img { width:100%; height:auto; display:block; aspect-ratio:16/9; object-fit:cover; }
_margin: { bottom: "24px" }
_width: "100%"
```
Remove the hardcoded radius from `_border` settings — keep it only in `_cssCustom` to avoid conflicts.

### 4D — Fix Post Content Typography

**Element `bodycn` (post-content)**  
Update `_cssCustom` to a complete, consistent typography system:
```css
#brxe-bodycn { font-size: 15px; line-height: 1.75; color: #3A3A3A; }
#brxe-bodycn h2 { font-size: 20px; font-weight: 700; color: #1A1A1A; margin: 32px 0 12px; padding-bottom: 8px; border-bottom: 2px solid #EBEBEB; }
#brxe-bodycn h3 { font-size: 17px; font-weight: 700; color: #1A1A1A; margin: 24px 0 10px; }
#brxe-bodycn h4 { font-size: 15px; font-weight: 700; color: #1A1A1A; margin: 20px 0 8px; }
#brxe-bodycn p { margin-bottom: 16px; }
#brxe-bodycn a { color: #E8621A; text-decoration: underline; }
#brxe-bodycn a:hover { color: #C4501A; }
#brxe-bodycn ul, #brxe-bodycn ol { margin: 0 0 16px 20px; }
#brxe-bodycn li { margin-bottom: 6px; line-height: 1.6; }
#brxe-bodycn blockquote { border-left: 3px solid #E8621A; padding: 12px 16px; margin: 20px 0; background: #FFF8F5; font-style: italic; color: #3A3A3A; border-radius: 0 6px 6px 0; }
#brxe-bodycn img { max-width: 100%; height: auto; border-radius: 6px; margin: 16px 0; }
#brxe-bodycn code { background: #F5F3EE; padding: 2px 6px; border-radius: 4px; font-size: 13px; font-family: monospace; }
#brxe-bodycn pre { background: #1A1A1A; color: #F5F3EE; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 20px 0; }
#brxe-bodycn hr { border: none; border-top: 1px solid #EBEBEB; margin: 28px 0; }
```
Update base `_typography`:
```
font-size: "15px"
line-height: "1.75"
color: #3A3A3A
```

### 4E — Fix Main Column Spacing

**Element `mainbl` (main content block)**  
Update `_cssCustom`:
```css
#brxe-mainbl { border-right: 1px solid #EBEBEB; }
@media (max-width: 991px) {
  #brxe-mainbl {
    border-right: none;
    border-bottom: 1px solid #EBEBEB;
    max-width: 100%;
    padding: 20px 16px;
  }
}
```
Update `_padding`:
```
top: "40px"
right: "40px"
bottom: "40px"
left: "0"
```
(Remove left padding on main column since the outer container handles it)

### 4F — Fix Sidebar Mobile Collapse

**Element `sidebl` (sidebar block)**  
Update `_cssCustom`:
```css
#brxe-sidebl { flex-shrink: 0; position: sticky; top: 80px; align-self: flex-start; }
@media (max-width: 991px) {
  #brxe-sidebl {
    width: 100%;
    position: static;
    padding: 20px 16px;
  }
}
```
Update `_width` from `"240px"` to `"260px"` (slightly wider for readability).

### 4G — Fix Excerpt Styling

**Element `excrpt` (post excerpt — italic blockquote style)**  
This is already styled as a pull quote. Verify the CSS is:
```css
#brxe-excrpt {
  border-left: 3px solid #E8621A;
  padding: 12px 16px;
  margin-bottom: 24px;
  font-style: italic;
  background: #FFF8F5;
  border-radius: 0 6px 6px 0;
}
```
Update if different from above.

### 4H — Fix TOC Box

**Element `tocbox` (table of contents block)**  
Update `_cssCustom` (add if not present):
```css
#brxe-tocbox { border-left: 3px solid #E8621A; }
```
Verify `toctxt` label says "Isi Kandungan" — correct, no change needed.  
Verify `tocsct` (post-toc element) is present — correct.

### 4I — Fix Category Label

**Element `catlbl` (category pill at top)**  
Update `_cssCustom`:
```css
#brxe-catlbl {
  display: inline-block;
  letter-spacing: .06em;
  margin-bottom: 10px;
  background: rgba(232,98,26,0.1);
  padding: 3px 10px;
  border-radius: 4px;
}
```

### 4J — Fix Avatar Circle

**Element `avtcrc` (orange circle with "Z")**  
The text is hardcoded as "Z". This is fine for now (faceless brand — Zed).  
Verify width/height are `28px` and border-radius is `50%`.  
No change needed.

### 4K — Add Reading Progress Bar (NEW — optional but recommended)

After element `sectn1` closes, the Header template (185) handles the top bar.  
To add a reading progress bar, add this to the **`_cssCustom`** of `mainbl`:
```css
/* Reading progress indicator via CSS only */
```
Skip this for now — implement in a future session.

### 4L — Fix Outer Container Spacing

**Element `contnr` (outermost row container)**  
Update `_padding`:
```
top: "40px"
right: "20px"
bottom: "60px"
left: "20px"
```
Update `_cssCustom`:
```css
#brxe-contnr { gap: 0; }
@media (max-width: 991px) { #brxe-contnr { flex-direction: column; } }
```
No change needed here — existing is correct.

### 4M — Verify Single Post Template

1. Navigate to https://digitrust-lab.local/apa-itu-ai/
2. Check on desktop (1200px): two-column layout (content left, sidebar right)
3. Check on mobile (375px): single column, sidebar below content
4. Verify element order top-to-bottom:
   - ✅ Category pill (orange, uppercase)
   - ✅ H1 title (large, bold)
   - ✅ Author circle + name + date + read time (meta row)
   - ✅ Excerpt (italic, orange left border)
   - ✅ Featured image (full width, 16:9)
   - ✅ Table of Contents box
   - ✅ Post body content
   - ✅ AI Mastery CTA box
   - ✅ Social share row
   - ✅ Author bio box
5. Verify no horizontal scroll on mobile
6. Verify H2 headings inside post body have bottom border separator
7. Verify links inside body are orange (#E8621A)

---

## TASK 5 — Deploy

After ALL tasks above are verified on local:

### 5A — Simply Static Export
1. Go to https://digitrust-lab.local/wp-admin/admin.php?page=simply-static-generate
2. Click "Push" — wait for "Done! Finished in ~00:09:xx"
3. Verify activity log shows "Fetched X of X pages/files" with no errors

### 5B — Verify index.html
Open `D:\Coding Zone\digitrust-lab-static\index.html` in a text editor:
- Confirm today's file modified timestamp
- Confirm contains "Jana Pendapatan Tambahan" (new H1 copy)
- Confirm does NOT contain "untuk warga Malaysia" (old eyebrow — deleted)

### 5C — Wrangler Deploy
```bash
cd "D:\Coding Zone\digitrust-lab-static"
npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main
```
Wait for "✨ Success! Uploaded X files"

### 5D — Live Verification
Check all 4 URLs:
- [ ] https://www.digitrustlab.com/ — new H1, no eyebrow, mobile layout correct
- [ ] https://www.digitrustlab.com/blog/ — no horizontal scroll, cards display correctly
- [ ] https://www.digitrustlab.com/category/digital-side-hustle/ — shows blog archive layout (NOT homepage)
- [ ] https://www.digitrustlab.com/apa-itu-ai/ — clean post layout, all elements in correct order

---

## EXECUTION ORDER

```
Task 3A → Bricks GUI (category condition — must be GUI, not Respira)
Task 1A → Respira (homepage copy)
Task 1B–1E → Respira (homepage mobile fixes)
Task 2A–2C → Respira (blog archive overflow)
Task 4A–4L → Respira (single post template)
Task 3B–3C → Verify category pages
Task 5 → Export + Deploy
```

Do Task 3A FIRST because it requires the Bricks GUI, and you want to confirm conditions work before doing the other Respira edits in the same session.

---

## WHAT NOT TO DO

- ❌ Do NOT use Code elements or raw HTML blocks
- ❌ Do NOT edit template 185 (Header) — it's working fine
- ❌ Do NOT add `overflow-x: hidden` to body or html — use `clip` only
- ❌ Do NOT deploy with Wrangler until you've verified all 4 URLs on local first
- ❌ Do NOT change the blog post content of "Apa Itu AI?" — only the template around it
- ❌ Do NOT remove the sidebar from single post template — collapse it on mobile instead
