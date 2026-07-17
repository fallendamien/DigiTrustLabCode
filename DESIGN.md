# Design System: DigiTrust Lab

> Source of truth for AI agents when generating or enhancing UI components for the DigiTrust Lab blog.
>
> **Last Updated:** 2026-07-10 (Session 10) — reflects native Bricks elements, homepage build, and lessons learned

---

## 1. Visual Theme & Atmosphere

**Warm, editorial, trustworthy.** The design evokes a premium digital magazine feel — clean warm-white backgrounds, burnt orange accents, and a structured two-column layout on posts. The homepage uses a modern full-width section layout with a hero, post card grid, email CTA, and category pills. Content-first approach with generous whitespace and readable typography. The aesthetic bridges "tech blog" and "Malaysian lifestyle publication" — approachable but authoritative.

**Key characteristics:**
- Light mode only (no dark mode planned)
- Warm neutral palette (not pure white/black)
- Orange accent used sparingly for CTAs, category pills, and highlights
- Card-based components with subtle borders and hover effects
- Plus Jakarta Sans throughout — modern, friendly, geometric
- Native Bricks elements (no code elements or `dtl-*` classes — those are legacy)

---

## 2. Color Palette

### Primary Colors

| Name | Hex | Role |
|------|-----|------|
| **Burnt Orange** | `#E8621A` | CTAs, category labels, accents, avatar bg, active nav |
| **Deep Charcoal** | `#1A1A1A` | Headlines, body text, footer background |
| **Warm White** | `#FAFAF8` | Page background, content area |

### Neutral Colors

| Name | Hex | Role |
|------|-----|------|
| **Warm Gray** | `#6B6B6B` | Meta text, captions, secondary info |
| **Body Gray** | `#3A3A3A` | Body paragraph text (slightly softer than headings) |
| **Cream** | `#F5F3EE` | TOC boxes, input fields, subtle backgrounds |
| **Light Border** | `#EBEBEB` | Card borders, dividers, input borders |
| **Thumb Placeholder** | `#F0EDE8` | Image thumbnail placeholders |

### Accent/Status Colors

| Name | Hex | Role |
|------|-----|------|
| **CTA Gradient Start** | `#FFF3EE` | CTA box gradient (light orange) |
| **CTA Gradient End** | `#FFEADD` | CTA box gradient (deeper orange) |
| **CTA Border** | `#F5C4A0` | CTA box border |
| **Category Pill BG** | `rgba(232,98,26,0.1)` | Category pill background (semi-transparent orange) |
| **Reading Time Pill BG** | `#1a1a1a` | Reading time pill background (solid black) |
| **Reading Time Pill Text** | `#FFFFFF` | Reading time pill text (white on black) |
| **Facebook Blue** | `#1877F2` | Facebook share button |
| **Black** | `#000000` | Twitter/X share button |
| **WhatsApp Green** | `#25D366` | WhatsApp share button |
| **Pinterest Red** | `#E60023` | Pinterest share button |
| **Footer Gray** | `#888888` | Footer text and links |

---

## 3. Typography

**Font Family:** `Plus Jakarta Sans`, system-ui, sans-serif

| Element | Weight | Size | Color | Usage |
|---------|--------|------|-------|-------|
| H1 (Post title) | 700 | 26px | `#1A1A1A` | Single post titles |
| H1 (Page title) | 700 | 26px | `#1A1A1A` | Static page titles |
| H2 (Section) | 700 | 18px | `#1A1A1A` | In-body section headers |
| H3 (Subsection) | 600 | 16px | `#1A1A1A` | Sub-headings |
| Body | 400 | 15px | `#3A3A3A` | Article body text, line-height 1.7 |
| Category Label | 600 | 11px | `#E8621A` | Uppercase, letter-spacing 0.06em |
| Meta Name | 600 | 12px | `#1A1A1A` | Author name |
| Meta Info | 400 | 12px | `#6B6B6B` | Date, reading time |
| TOC Title | 700 | 12px | `#1A1A1A` | "Isi Kandungan" label |
| TOC Item | 400 | 12px | `#6B6B6B` | Table of contents entries |
| CTA Label | 700 | 11px | `#E8621A` | Uppercase, "Rekomendasi" |
| CTA Title | 700 | 14px | `#1A1A1A` | CTA box heading |
| CTA Button | 600 | 12px | `#FFFFFF` | Button text on orange bg |
| Sidebar Card Title | 700 | 12px | `#1A1A1A` | With orange bottom border |
| Opt-in Input | 400 | 12px | `#6B6B6B` | Email placeholder |
| Opt-in Button | 700 | 12px | `#FFFFFF` | "Hantar Sekarang" |
| Opt-in Subtext | 400 | 10px | `#6B6B6B` | "Percuma. Berhenti langgan..." |
| Related Title | 600 | 11px | `#1A1A1A` | Popular post titles |
| Share Label | 400 | 12px | `#6B6B6B` | "Kongsi:" |
| Footer Text | 400 | 13px | `#888888` | Copyright, footer links |

---

## 4. Component Patterns

### Buttons

| Type | Background | Text | Radius | Padding | Font |
|------|-----------|------|--------|---------|------|
| **Primary CTA** | `#E8621A` | `#FFFFFF` | 6px | 8px 16px | 12px / 600 |
| **Nav CTA** | `#E8621A` | `#FFFFFF` | 6px | 7px 14px | 12px / 600 |
| **Opt-in Submit** | `#E8621A` | `#FFFFFF` | 6px | 9px (full width) | 12px / 700 |
| **Share (circle)** | brand color | `#FFFFFF` | 50% | — | 11px / 700 |

### Cards

| Component | Background | Border | Radius | Padding |
|-----------|-----------|--------|--------|---------|
| **Sidebar Card** | `#FFFFFF` | 1px solid `#EBEBEB` | 10px | 16px |
| **TOC Box** | `#F5F3EE` | none | 8px | 14px 16px |
| **CTA Box** | gradient `#FFF3EE`→`#FFEADD` | 1px solid `#F5C4A0` | 10px | 16px |
| **Post Card (homepage)** | `#FFFFFF` | 1px solid `#EBEBEB` | 10px | 16px |

### Post Card (Homepage Latest Posts)

- Container: white bg, 1px border `#EBEBEB`, 10px radius, 16px padding
- Hover: subtle elevation via `transform: translateY(-2px)` + box-shadow
- Image: fixed height (200px), `object-fit: cover`, 4px radius at top
- Category pill: `rgba(232,98,26,0.1)` bg, `#E8621A` text, 12px radius, inline-block
- Title: 16px, 700 weight, `#1A1A1A`, link with hover color change
- Excerpt: 14px, `#6B6B6B`, 2-line clamp (`-webkit-line-clamp: 2`)
- Reading time pill: `#1a1a1a` bg, `#FFFFFF` text, 12px radius, inline-block

### Pills (Meta Badges)

| Type | Background | Text | Radius | Font |
|------|-----------|------|--------|------|
| **Category Pill** | `rgba(232,98,26,0.1)` | `#E8621A` | 12px | 11px / 600 |
| **Reading Time Pill** | `#1a1a1a` | `#FFFFFF` | 12px | 11px / 600 |

**Note:** Reading time pill style is unified across homepage and blog archive (Template 52) — solid black bg, white text. Applied via `_cssCustom` using `.brxe-{id}` class selector (NOT `#brxe-{id}` — see TROUBLESHOOTING.md).

### Sidebar Card Title

- Orange bottom border: `2px solid #E8621A`
- `display: inline-block` (border only under text, not full width)
- Padding-bottom: 6px, margin-bottom: 10px

### Inputs

| Component | Background | Border | Radius | Padding |
|-----------|-----------|--------|--------|---------|
| **Email Input** | `#F5F3EE` | 1px solid `#EBEBEB` | 6px | 8px 10px |

### Avatar

- Circle (50% radius)
- `28px × 28px`
- Background: `#E8621A`
- Text: white, 11px, 700 weight, centered
- Shows first letter of author name

### Share Buttons

- Circle (50% radius)
- `30px × 30px`
- Brand colors as background
- White text, 11px, 700 weight
- Spacing: 8px gap between buttons

### Related/Popular Post Items

- Flex layout, 8px gap
- Thumbnail: `44px × 36px`, `#F0EDE8` bg, 4px radius
- Title: 11px, 600 weight
- Bottom border: 0.5px solid `#EBEBEB` (except last item)

---

## 5. Spacing & Layout

### Layout Structure — Single Post (Template 10)

```
┌─────────────────────────────────────────┐
│ Header (60px height, #FAFAF8 bg)       │
├──────────────────────┬──────────────────┤
│ Main Column          │ Sidebar          │
│ flex: 1              │ 240px fixed      │
│ max-width: 620px     │                  │
│ padding: 32px        │ padding: 24px 20px│
│ border-right: 1px    │                  │
├──────────────────────┴──────────────────┤
│ Footer (#1A1A1A bg, 16px 24px padding) │
└─────────────────────────────────────────┘
```

### Layout Structure — Homepage (Page ID 280)

```
┌─────────────────────────────────────────┐
│ Header (Template 185, #FAFAF8 bg)      │
├─────────────────────────────────────────┤
│ Hero Section (full-width)               │
│  - Eyebrow text (orange, 12px/600)      │
│  - H1 heading (28px/700, sentence case) │
│  - Subtext (16px, #6B6B6B)              │
├─────────────────────────────────────────┤
│ Latest Posts (query loop, 3-col grid)   │
│  - Section heading + "Lihat semua" link │
│  - Post cards (image, category, title,  │
│    excerpt, reading time pill)          │
├─────────────────────────────────────────┤
│ Email CTA Section                        │
│  - Gradient bg, email opt-in            │
├─────────────────────────────────────────┤
│ Category Pills Section                   │
│  - Category links as pill badges        │
├─────────────────────────────────────────┤
│ Footer (Template 46, #1A1A1A bg)        │
└─────────────────────────────────────────┘
```

### Layout Structure — Blog Archive (Template 52)

```
┌─────────────────────────────────────────┐
│ Header (Template 185)                   │
├─────────────────────────────────────────┤
│ Blog heading + tagline (centered)       │
│ Post grid (query loop, responsive cols)  │
│  - Post cards (same style as homepage)   │
│ Pagination                              │
├─────────────────────────────────────────┤
│ Footer (Template 46)                    │
└─────────────────────────────────────────┘
```

### Spacing Values

| Token | Value | Usage |
|-------|-------|-------|
| **xs** | 4px | Small gaps, avatar letter padding |
| **sm** | 8px | Category-to-title gap, share btn gap |
| **md** | 12px | Title-to-meta gap, CTA label-to-title |
| **lg** | 14px | Excerpt left padding, TOC item padding |
| **xl** | 16px | Card padding, CTA padding, share top border |
| **2xl** | 20px | Meta-to-content gap, CTA margin |
| **3xl** | 24px | Sidebar padding |
| **4xl** | 32px | Main column padding |

### Border Radius

| Value | Usage |
|-------|-------|
| 4px | Thumbnail corners |
| 6px | Buttons, inputs, logo mark |
| 8px | TOC box |
| 10px | Cards, CTA box |
| 50% | Avatar, share buttons |

### Content Width

- **Main column max-width:** 620px (optimal for Malay readability, ~65 chars/line)
- **Sidebar width:** 240px (fixed)
- **Total content area:** flex layout, sidebar does not shrink

---

## 6. Header & Footer

### Header

- Height: 60px
- Background: `#FAFAF8`
- Border-bottom: 1px solid `#EBEBEB`
- Layout: flex, space-between, align-center
- Padding: 0 24px
- Logo: orange square (28px, 6px radius) + "DigiTrust Lab" text (14px, 700)
- Nav links: 13px, `#6B6B6B`, 20px gap
- Active nav: `#E8621A`, 600 weight
- Nav CTA: orange button, right-aligned

### Footer

- Background: `#1A1A1A`
- Padding: 16px 24px
- Layout: flex, space-between, align-center
- Copyright: 13px, `#888888`
- Footer links: 13px, `#888888`, 16px gap
- Sticky to bottom via: `body { display: flex; flex-direction: column; min-height: 100vh; overflow-x: clip; }` + `#brx-content { flex: 1 1 auto; }`
- **IMPORTANT:** Use `overflow-x: clip` NOT `overflow-x: hidden` — `hidden` collapses `min-height: 100vh` in Chromium (see TROUBLESHOOTING.md)

---

## 7. CSS Approach — Native Bricks Elements

The site now uses **native Bricks elements** styled via Bricks' settings and `_cssCustom`. The old `dtl-*` classes from the code-element era are **legacy** and no longer the primary styling mechanism.

### Styling Methods (in priority order)

1. **Bricks element settings** — `_typography`, `_backgroundColor`, `_padding`, `_margin`, etc. (set via Respira MCP or Bricks GUI)
2. **`_cssCustom` on individual elements** — for properties not exposed as Bricks settings (e.g., `object-fit`, `line-clamp`, hover effects)
3. **`bricks_global_settings.customCss`** — for site-wide rules (body, `#brx-content`, `#brx-header`, `#brx-footer`, overflow fixes)

### Selector Convention

| Context | Selector | Why |
|---------|----------|-----|
| **Standalone elements** | `#brxe-{id}` | Element ID is stable |
| **Inside query loops** | `.brxe-{id}` | IDs regenerate per iteration — class matches all iterations |
| **Global layout** | `#brx-content`, `#brx-header`, `#brx-footer` | Bricks area IDs, stable across all pages |

**CRITICAL:** Elements inside query loops get new IDs on each iteration. Always use `.brxe-{id}` (class) not `#brxe-{id}` (ID) for `_cssCustom` on loop elements. See TROUBLESHOOTING.md.

### Legacy `dtl-*` Classes (Reference Only)

These classes existed in the old code-element templates. They are NOT used in current native Bricks elements but may appear in historical references:

`dtl-post-wrap`, `dtl-main`, `dtl-sidebar`, `dtl-category`, `dtl-h1`, `dtl-meta`, `dtl-avatar`, `dtl-meta-name`, `dtl-meta-info`, `dtl-excerpt`, `dtl-toc`, `dtl-toc-title`, `dtl-body`, `dtl-cta`, `dtl-cta-label`, `dtl-cta-title`, `dtl-cta-btn`, `dtl-share`, `dtl-share-label`, `dtl-share-btn`, `dtl-sidebar-card`, `dtl-sidebar-title`, `dtl-optin-input`, `dtl-optin-btn`, `dtl-optin-sub`, `dtl-related`, `dtl-related-thumb`, `dtl-related-title`

---

## 8. Motion & Animation

- **No complex animations** — this is a static blog, performance is priority
- Transitions (if any): `transition: all 0.2s ease` for hover states
- No parallax, no scroll-triggered animations
- Share buttons: subtle opacity change on hover (`0.8`)

---

## 9. Responsive Behavior

| Breakpoint | Behavior |
|------------|----------|
| **Desktop** (>768px) | Two-column with sidebar (posts), full-width sections (homepage) |
| **Mobile** (≤768px) | Single column, sidebar collapses below content, post grid → 1 column |

**Mobile rules:**
- Sidebar stacks below main content
- Nav links collapse (hamburger / off-canvas menu)
- Main column padding reduces to 16px
- Font sizes stay the same (already mobile-friendly)
- CTA box remains full-width
- Homepage post grid collapses to 1 column
- `body { overflow-x: clip }` prevents horizontal scroll from off-canvas menu (see TROUBLESHOOTING.md)
- Gutenberg content pages: `width: 100%; box-sizing: border-box` required with `max-width` to prevent mobile overflow

---

## 10. Page Templates

### Homepage (Page ID: 280)

Full-width section layout (no sidebar) with 4 sections:
1. **Hero** — eyebrow text (orange), H1 heading (sentence case), subtext
2. **Latest Posts** — query loop with 3-column post card grid, section heading + "Lihat semua" link
3. **Email CTA** — gradient background, email opt-in
4. **Category Pills** — category links as pill badges

**Hero copy (current):**
- Eyebrow: `AI Tools & Side Hustle Digital untuk warga Malaysia`
- H1: `Anda boleh guna AI untuk membuat kerja dan menjana pendapatan` (sentence case)

**Note:** Query loops on pages require a Bricks editor save to activate on frontend (see TROUBLESHOOTING.md).

### Single Post Template (ID: 10)

Full two-column layout with:
- Category label, H1, author meta (avatar + name + date/reading time), excerpt, TOC, body, CTA box, share buttons
- Sidebar: opt-in card + popular posts card
- Reading time: native Bricks `post-reading-time` element with `suffix: " min baca"`
- Date: `{post_date}` dynamic tag
- Author name: `{author_name}` dynamic tag (NOT `{post_author}`)
- Post URL links: `link: {type: "external", url: "{post_url}"}` (NOT `type: "dynamic"`)

### Blog Archive Template (ID: 52)

Post grid with:
- Heading "Blog DigiTrust Lab" + tagline (centered)
- Post cards (thumbnail, category pill, title, excerpt, reading time pill)
- Reading time pill: solid black `#1a1a1a` bg, white text (unified with homepage)
- Pagination at bottom
- No sidebar (full-width layout)
- Template condition: `ids: ['277']` (targets Blog page ID, NOT `archiveType` — see TROUBLESHOOTING.md)

### Header Template (ID: 185)

Native Bricks elements (no code elements):
- Logo, navigation, nav CTA button
- Mobile off-canvas menu
- Background: `#FAFAF8`, border-bottom: 1px solid `#EBEBEB`

### Footer Template (ID: 46)

Native Bricks elements:
- Copyright text, footer links
- Background: `#1A1A1A`, text: `#888888`
- 13px font size

### Static Pages (Privasi, Disclaimer, Hubungi, Tentang)

Gutenberg content pages styled via global CSS:
- `#brx-content.wordpress { width: 100%; max-width: 800px; margin: 0 auto; padding: 60px 24px 80px; box-sizing: border-box; }`
- No sidebar, centered content column
- No category labels (those are for blog posts only)

---

## 11. Design Rules (from spec, updated)

1. **Max content width 620px (posts) / 800px (pages)** — optimal for Malay readability (65-70 chars/line)
2. **Featured image 1200×630px** — for social sharing and Google snippets
3. **Sticky sidebar on desktop (posts only)** — opt-in stays visible while scrolling
4. **Orange CTA box in every post** — 1 contextual affiliate box per post, mid-content
5. **Reading time in post meta** — reduces bounce rate. Calculated via custom PHP function `post_date_reading_time()` using `{echo:}` tag (NOT Rank Math — see TROUBLESHOOTING.md)
6. **WhatsApp in share buttons** — Malaysian audience shares via WhatsApp primarily
7. **Author bio with name + photo** — Google E-E-A-T signal
8. **No sidebar on mobile** — single column, 99% mobile audience
9. **Reading time pill unified** — solid black `#1a1a1a` bg, white text, consistent across homepage and blog archive
10. **`overflow-x: clip` not `hidden`** — `hidden` collapses `min-height: 100vh` in Chromium
11. **`.brxe-{id}` for query loop elements** — IDs regenerate per iteration, use class selectors not ID selectors
12. **Homepage has no sidebar** — full-width sections, post card grid instead

---

## 12. Key Element IDs (Quick Reference)

| Page/Template | ID | Key Elements |
|---------------|-----|--------------|
| Homepage | 280 | Hero (eyebrow `2994e0`, H1 `dbb365`), Latest Posts query loop, Email CTA, Category Pills |
| Blog Archive | 52 (template) | Heading, tagline, post card query loop, reading time pill (`n62cj0`), pagination |
| Single Post | 10 (template) | Category, H1, author meta, excerpt, TOC, body, CTA, share, sidebar |
| Header | 185 (template) | Logo, nav, CTA button, mobile menu |
| Footer | 46 (template) | Copyright, footer links |
| Blog Page | 277 | WordPress posts page (set in Settings → Reading) |

**Note:** Element IDs within templates may change after Bricks editor saves. Always run `respira_extract_builder_content` to get current IDs before editing.
