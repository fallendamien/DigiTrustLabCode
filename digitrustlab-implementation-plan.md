# DigiTrust Lab — Implementation Plan
> **For:** Windsurf execution  
> **Stack:** Local WP → Bricks Builder 2.3.8 → Simply Static → GitHub → Cloudflare Pages  
> **WP Admin:** https://digitrust-lab.local/wp-admin/  
> **Local path:** ~\Local Sites\digitrust-lab\  
> **Live blog:** blog.digitrustlab.com  
> **Last updated:** 2026-06-29

---

## ✅ Already Done — Do Not Redo

- WordPress 7.0 installed locally (PHP 8.2.29, Nginx, MySQL 8.4.0)
- Bricks Builder 2.3.8 Ultimate — licensed and active
- Rank Math SEO 1.0.272 — active, usage tracking OFF
- Simply Static 3.7.7 — configured (output: `D:/Coding Zone/digitrust-lab-static`, relative path `/blog`)
- Blog categories created: AI Tools / Digital Side Hustle / Canva & Design / AI untuk Perniagaan Kecil
- Bricks Single Post Template — built (Post Title → Meta → Excerpt → TOC → Content → Social Sharing → Related Posts → Comments), condition: Post type = Post
- GitHub Desktop repo: `digitrust-lab-static`, 2630 files committed to main
- Bricks Header Template — built and live (Section + Container + Code element with full HTML)
- Header condition: Entire website ✅
- Code execution enabled for Administrator ✅
- Code signatures regenerated ✅
- blog.digitrustlab.com — live on Cloudflare Pages ✅

---

## 🔴 BLOCK A — Bricks Templates (Complete the UI)

### A1. Footer Template

Create new Bricks template: **Footer**, condition: All pages.

Use a single **Code element** (Execute code ON) with this HTML:

```html
<footer style="background:#1A1A1A;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;font-family:'Plus Jakarta Sans',system-ui,sans-serif;">
  <span style="font-size:11px;color:#888888;">© 2026 DigiTrust Lab · digitrustlab.com</span>
  <div style="display:flex;gap:16px;">
    <a href="/privasi" style="font-size:11px;color:#888888;text-decoration:none;">Privasi</a>
    <a href="/disclaimer" style="font-size:11px;color:#888888;text-decoration:none;">Disclaimer</a>
    <a href="/hubungi" style="font-size:11px;color:#888888;text-decoration:none;">Hubungi</a>
  </div>
</footer>
```

Steps:
1. Bricks → Templates → Add New → type: Footer
2. Add Code element inside the template canvas
3. Enable "Execute code" toggle
4. Paste HTML above
5. Template Settings → Conditions → Add → Entire website
6. Save → Regenerate code signatures

---

### A2. Global CSS Variables

Bricks → Settings → Custom Code → Global CSS field. Add:

```css
:root {
  --dtl-bg:        #FAFAF8;
  --dtl-text:      #1A1A1A;
  --dtl-accent:    #E8621A;
  --dtl-muted:     #6B6B6B;
  --dtl-surface:   #F5F3EE;
  --dtl-border:    #EBEBEB;
  --dtl-footer-bg: #1A1A1A;
  --dtl-font:      'Plus Jakarta Sans', system-ui, sans-serif;
}

body {
  background: var(--dtl-bg);
  font-family: var(--dtl-font);
  color: var(--dtl-text);
}
```

---

### A3. Plus Jakarta Sans Font

Bricks → Settings → Custom Fonts (or Google Fonts tab) → Add Plus Jakarta Sans, weights: 400, 500, 600, 700.

---

### A4. Update Author Profile

WP Admin → Users → admin profile:
- Display name: `Zamri Rosli`
- Biographical info: `Developer & digital entrepreneur yang bina bisnes sampingan dengan AI. Menulis tentang tools, strategi, dan pengalaman sebenar.`
- Save

---

### A5. Single Post Template — Refine Layout

The Single Post template already exists. Refine it with a proper 2-column layout:

**Layout:** Section → 2 columns inside (62% content / 38% sidebar)

Content column (max-width 720px) — existing elements in order:
1. Post Category (dynamic tag)
2. Post Title (H1)
3. Post Meta (author · date · reading time)
4. Post Excerpt (italic, orange left border)
5. Featured Image (full width, aspect ratio 1200×630)
6. TOC (Rank Math block)
7. Post Content
8. Inline CTA Box (Code element — see spec below)
9. Author Bio
10. Social Sharing
11. Related Posts
12. Comments

Sidebar column (240px, sticky top: 20px):
- Email opt-in card (placeholder — MailerLite embed added later)
- Popular Posts widget

**Inline CTA Box HTML** (Code element, Execute code ON):
```html
<div style="background:linear-gradient(135deg,#FFF3EE 0%,#FFEADD 100%);border:1px solid #F5C4A0;border-radius:10px;padding:16px;margin:24px 0;font-family:'Plus Jakarta Sans',system-ui,sans-serif;">
  <div style="font-size:11px;font-weight:700;color:#E8621A;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px;">Rekomendasi</div>
  <div style="font-size:14px;font-weight:700;color:#1A1A1A;margin-bottom:8px;">Modul AI Mastery — Belajar cara guna AI untuk perniagaan anda</div>
  <a href="https://digitrustlab.bcl.my/form/modul-ai-mastery" style="background:#E8621A;color:#fff;font-size:12px;font-weight:600;padding:8px 16px;border-radius:6px;text-decoration:none;display:inline-block;">Tengok Modul →</a>
</div>
```

**Condition:** Post type = Post (already set ✅)

---

### A6. Blog Index / Archive Template

Create new Bricks template: **Archive**, condition: Post archive.

Layout: Post grid — 2 columns on desktop, 1 column mobile.

Each post card:
- Featured image (aspect ratio 16:9, border-radius 8px)
- Category tag (11px, uppercase, #E8621A)
- Title (16px, weight 700, #1A1A1A)
- Excerpt (13px, #6B6B6B, 2 lines max)
- Date + reading time (12px, #6B6B6B)
- "Baca selanjutnya →" link (#E8621A)

Use Bricks **Posts** element with loop query: post_type = post, posts_per_page = 10, orderby = date.

---

## 🟡 BLOCK B — Core Pages

Create these pages in WP Admin → Pages → Add New, then build in Bricks.

### B1. About Page (`/tentang`)

Content (write in Bricks Rich Text element):
- H1: "Tentang DigiTrust Lab"
- Intro: Who Zamri is, why this blog exists
- What the blog covers (AI tools, digital side hustle, Malaysian context)
- Author photo + bio section
- CTA: "Baca post pertama saya →"

Bricks template condition: Page = Tentang

### B2. Privacy Policy (`/privasi`)

Standard Malaysian-context privacy policy. Key points:
- What data is collected (email via MailerLite, analytics via GA4)
- How it's used
- Third-party services (Google Analytics, MailerLite, Etsy links)
- Contact: [email address]

### B3. Disclaimer (`/disclaimer`)

- Affiliate disclosure (Klikjer, AI Mastery reseller)
- Earnings disclaimer (results not guaranteed)
- Content accuracy disclaimer

### B4. Contact Page (`/hubungi`)

Simple page with:
- Email address
- Note: response within 48 hours
- Optional: simple contact form (WP built-in or Rank Math form)

---

## 🟡 BLOCK C — Deploy Pipeline

### C1. Export via Simply Static

WP Admin → Simply Static → Generate Static Files
- Output directory: `D:/Coding Zone/digitrust-lab-static`
- Relative path: `/blog`
- Click "Generate" — wait ~8 min for 2600+ files

### C2. Push to GitHub

GitHub Desktop:
1. Open repo `digitrust-lab-static`
2. Review changed files
3. Commit message: "Update: footer, templates, core pages"
4. Push to origin (main branch)

### C3. Verify on Cloudflare Pages

1. Cloudflare Pages will auto-deploy on push (1–2 min)
2. Visit blog.digitrustlab.com — verify header + footer visible
3. Visit a blog post URL — verify Single Post template rendering
4. Check mobile view (Chrome DevTools → iPhone 12)

---

## 🟡 BLOCK D — Analytics & SEO Setup

### D1. Google Analytics 4

1. analytics.google.com → Create property → DigiTrust Lab
2. Get Measurement ID (G-XXXXXXXXXX)
3. WP Admin → Rank Math → General Settings → Analytics → paste GA4 ID
4. OR: Bricks → Settings → Custom Code → Header scripts → paste GA4 script tag

### D2. Google Search Console

1. search.google.com/search-console → Add property → URL prefix: `https://blog.digitrustlab.com`
2. Verify via HTML tag → paste in Rank Math → General Settings → Webmaster Tools → Google
3. After verification: Submit sitemap → `https://blog.digitrustlab.com/blog/sitemap_index.xml`

### D3. ClickRank Ownership Verification

1. Go to clickrank.ai → dashboard → add site → `https://blog.digitrustlab.com`
2. Copy JS ownership snippet
3. Paste into Bricks → Settings → Custom Code → Header scripts
4. Export static → push → verify live
5. Back in ClickRank → verify ownership
6. Connect ClickRank to Google Search Console (OAuth)

---

## 🟢 BLOCK E — Email List (Day 1)

### E1. MailerLite Setup

1. Create free account at mailerlite.com (free up to 1,000 subscribers)
2. Create a Group: "DigiTrust Lab Subscribers"
3. Create a Form: embedded, single field (email only)
   - Headline: "Dapatkan 50 Prompt AI Percuma"
   - Button: "Hantar Sekarang"
   - Success message: "Terima kasih! Check email anda."
4. Copy embed code

### E2. Embed in Blog Sidebar

In Bricks Single Post Template → Sidebar column → Email opt-in card:
- Replace placeholder content with MailerLite embed (Code element, Execute code ON)

### E3. Lead Magnet PDF (Week 2–3)

Create PDF: "50 Prompt AI Percuma untuk Perniagaan Malaysia"
- Use Canva template
- 10 pages max, simple design
- Cover + 10 categories × 5 prompts
- Export PDF → upload to WP Media Library
- Update MailerLite form automation: send PDF download link on subscribe

---

## 🟢 BLOCK F — Affiliates

### F1. Register Klikjer

1. Go to klikjer.com → Daftar sebagai affiliate (free)
2. Browse catalog for AI/digital business eBooks
3. Get affiliate links
4. Create `/rekomendasi` page on blog with affiliate links

### F2. AI Mastery in Blog

The inline CTA box (see A5) already links to the BCL form. No ads — warm organic traffic only.

---

## 🔵 BLOCK G — First Blog Post

### Post #1: RM501 Facebook Ads Story

**Title (Malay):** "Saya Habis RM501 untuk Iklan Facebook — Ini Yang Saya Belajar"  
**Category:** Digital Side Hustle  
**Target keyword:** "iklan facebook untuk bisnes kecil malaysia" (WriterZen research)  
**Estimated length:** 1,500–2,000 words  
**Language:** Malay (70% rule)

**Outline:**
1. Hook — the RM501 loss, no drama just facts
2. What I was selling and why I chose Facebook Ads
3. 3 mistakes I made (funnel, audience, offer)
4. What I learned: organic-first sequencing
5. What I'm doing now instead (blog + Etsy)
6. Inline CTA: AI Mastery module
7. Conclusion + internal links

**Workflow:**
1. WriterZen → research keyword → get outline
2. Write in WP editor (Gutenberg or Bricks)
3. ClickRank → paste draft → optimise for Google + AI search
4. Rank Math score > 80 before publishing
5. Add featured image (1200×630, Canva)
6. Set excerpt (1–2 sentence hook)
7. Publish
8. Export Simply Static → push to GitHub → verify live

---

## 📋 Execution Order

| # | Block | Task | Priority | Est. Time |
|---|-------|------|----------|-----------|
| 1 | A2 | Global CSS variables | 🔴 High | 10 min |
| 2 | A3 | Plus Jakarta Sans font | 🔴 High | 10 min |
| 3 | A1 | Footer template | 🔴 High | 20 min |
| 4 | A4 | Update author profile | 🔴 High | 5 min |
| 5 | A5 | Refine Single Post template | 🔴 High | 45 min |
| 6 | A6 | Blog Index / Archive template | 🟡 Med | 30 min |
| 7 | C1–C3 | Export → GitHub → verify | 🔴 High | 15 min |
| 8 | B1–B4 | Core pages (About, Privacy, Disclaimer, Contact) | 🟡 Med | 60 min |
| 9 | D1 | Google Analytics 4 | 🟡 Med | 15 min |
| 10 | D2 | Google Search Console + sitemap | 🟡 Med | 15 min |
| 11 | E1–E2 | MailerLite setup + embed | 🔴 High | 30 min |
| 12 | D3 | ClickRank verification | 🟡 Med | 15 min |
| 13 | F1 | Register Klikjer | 🟡 Med | 15 min |
| 14 | G | Write + publish Post #1 | 🔴 High | 3–4 hrs |

**Total estimated time: ~8–9 hours** (fits 1 weekend)

---

## 🎨 Design Reference

All colours, spacing, and component specs are in:  
`digitrustlab-blog-design-spec.md` (project knowledge)  
`digitrustlab_blog_design_spec.html` (visual mockup — open in browser)

### Quick colour reference

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#FAFAF8` | Page bg, content areas |
| Text | `#1A1A1A` | Headings, body |
| Accent | `#E8621A` | CTAs, links, active nav |
| Muted | `#6B6B6B` | Meta, captions, nav |
| Surface | `#F5F3EE` | TOC box, sidebar cards |
| Border | `#EBEBEB` | Dividers, card borders |
| Footer bg | `#1A1A1A` | Footer |

### Typography

| Element | Size | Weight | Colour |
|---------|------|--------|--------|
| H1 | 36px desktop / 28px mobile | 700 | `#1A1A1A` |
| H2 | 22px | 700 | `#1A1A1A` |
| H3 | 17px | 600 | `#1A1A1A` |
| Body | 16px | 400 | `#3A3A3A` |
| Meta | 12px | 400 | `#6B6B6B` |
| Nav | 13px | 400/600 active | `#6B6B6B` / `#E8621A` |
| CTA button | 12px | 600 | `#FFFFFF` on `#E8621A` |

---

## 🔑 Key Credentials & Config

| Item | Value |
|------|-------|
| WP Admin | https://digitrust-lab.local/wp-admin/ |
| Local site path | ~\Local Sites\digitrust-lab\ |
| Static output | D:/Coding Zone/digitrust-lab-static |
| GitHub repo | digitrust-lab-static (main branch) |
| Cloudflare zone ID | 94c8c2bff83a3ed15b7405d507eca68e |
| Live URL | blog.digitrustlab.com |
| BCL slug | digitrustlab |
| BCL form ID | 10636 (Modul AI Mastery) |
| Pixel ID | 1402085223143293 (paused — do not activate) |

---

## ⚠️ Hard Rules for Windsurf

1. **Never touch Meta Ads** — permanently paused. Do not create campaigns, edit ad sets, or touch the ad account.
2. **BCL embed must be used as-is** — do not modify the BCL checkout form HTML. Custom landing pages only for own original products.
3. **No new paid subscriptions** — tool stack is final: WriterZen + ClickRank + Screpy + Claude. No new tools.
4. **Language rule** — blog posts: 70% Malay, 30% English. Never translate same post into both languages (duplicate content).
5. **Blog path is `/blog`** — Simply Static is configured for relative path `/blog`. Do not change this.
6. **Regenerate code signatures after every Code element change** — Bricks Settings → Custom Code → Regenerate code signatures. Otherwise code won't execute on frontend.
7. **Export Simply Static after every template/page change** — changes only go live after: Simply Static export → GitHub push → Cloudflare Pages deploy.
