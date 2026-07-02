# Design System: DigiTrust Lab

> Source of truth for AI agents when generating or enhancing UI components for the DigiTrust Lab blog.

---

## 1. Visual Theme & Atmosphere

**Warm, editorial, trustworthy.** The design evokes a premium digital magazine feel — clean warm-white backgrounds, burnt orange accents, and a structured two-column layout. Content-first approach with generous whitespace and readable typography. The aesthetic bridges "tech blog" and "Malaysian lifestyle publication" — approachable but authoritative.

**Key characteristics:**
- Light mode only (no dark mode planned)
- Warm neutral palette (not pure white/black)
- Orange accent used sparingly for CTAs and highlights
- Card-based components with subtle borders
- Plus Jakarta Sans throughout — modern, friendly, geometric

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

### Layout Structure

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
- Sticky to bottom via flexbox: `body { display: flex; flex-direction: column; min-height: 100vh; } footer { margin-top: auto; }`

---

## 7. CSS Class Naming Convention

All custom classes use the `dtl-` prefix (DigiTrust Lab):

| Class | Element |
|-------|---------|
| `.dtl-post-wrap` | Outer flex container (main + sidebar) |
| `.dtl-main` | Main content column |
| `.dtl-sidebar` | Sidebar column |
| `.dtl-category` | Category label above title |
| `.dtl-h1` | Post/page title |
| `.dtl-meta` | Author meta row (flex) |
| `.dtl-avatar` | Circular author avatar |
| `.dtl-meta-name` | Author name |
| `.dtl-meta-info` | Date + reading time |
| `.dtl-excerpt` | Italic excerpt with orange left border |
| `.dtl-toc` | Table of contents box |
| `.dtl-toc-title` | TOC heading |
| `.dtl-body` | Article body content |
| `.dtl-cta` | CTA box (gradient bg) |
| `.dtl-cta-label` | CTA "Rekomendasi" label |
| `.dtl-cta-title` | CTA heading text |
| `.dtl-cta-btn` | CTA orange button |
| `.dtl-share` | Share row (flex) |
| `.dtl-share-label` | "Kongsi:" label |
| `.dtl-share-btn` | Individual share circle |
| `.dtl-sidebar-card` | White card in sidebar |
| `.dtl-sidebar-title` | Card title with orange underline |
| `.dtl-optin-input` | Email input field |
| `.dtl-optin-btn` | Submit button |
| `.dtl-optin-sub` | Subtext below opt-in |
| `.dtl-related` | Popular post item (flex) |
| `.dtl-related-thumb` | Thumbnail placeholder |
| `.dtl-related-title` | Post title in sidebar |

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
| **Desktop** (>768px) | Two-column with sidebar |
| **Mobile** (≤768px) | Single column, sidebar collapses below content |

**Mobile rules:**
- Sidebar stacks below main content
- Nav links collapse (hamburger or horizontal scroll)
- Main column padding reduces to 16px
- Font sizes stay the same (already mobile-friendly)
- CTA box remains full-width

---

## 10. Page Templates

### Single Post Template (ID: 10)

Full two-column layout with:
- Category label, H1, author meta, excerpt, TOC, body, CTA box, share buttons
- Sidebar: opt-in card + popular posts card

### Blog Archive Template (ID: 52)

Post grid/list with:
- Post cards (thumbnail, category, title, excerpt, meta)
- Same sidebar as single post
- Pagination at bottom

### Static Page Template (for Privasi, Disclaimer, Hubungi, Tentang)

**Current state:** Plain, unstyled — using default WordPress template.

**Target state:** Should use a simplified version of the single post layout:
- Header (same as blog)
- Centered content column (max-width 620px, no sidebar)
- Page title with orange category-style label above
- Styled content with `dtl-body` typography
- CTA box at bottom (where relevant)
- Footer (same as blog)

---

## 11. Design Rules (from spec)

1. **Max content width 720px** — optimal for Malay readability (65-70 chars/line)
2. **Featured image 1200×630px** — for social sharing and Google snippets
3. **Sticky sidebar on desktop** — opt-in stays visible while scrolling
4. **Orange CTA box in every post** — 1 contextual affiliate box per post, mid-content
5. **Reading time in post meta** — reduces bounce rate, auto-calculated by Rank Math
6. **WhatsApp in share buttons** — Malaysian audience shares via WhatsApp primarily
7. **Author bio with name + photo** — Google E-E-A-T signal
8. **No sidebar on mobile** — single column, 99% mobile audience
