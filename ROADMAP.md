# DigiTrust Lab — Roadmap

> **Status:** 🚧 In Progress
> **Current Phase:** Phase 1 — Foundation (Infrastructure DONE, Content Phase Started)
> **Last Updated:** 2026-07-11 (Session 13)
> **Monthly Revenue:** RM 69 (1 sale, pre-blog era)

---

## Progress Overview

```
Phase 1: Foundation         ██████████ 100% ✅ (Infrastructure)
Phase 1: Content             █░░░░░░░░░ 10% (1 post live, content phase started)
Phase 2: Compounding        ░░░░░░░░░░  0%
Phase 3: Traffic Growth     ░░░░░░░░░░  0%
Phase 4: Scale              ░░░░░░░░░░  0%
```

---

## Phase 1: Foundation 🏗️ (Month 1–3)

**Goal:** Blog live + 10 posts + Etsy shop open + 5 listings + MailerLite Day 1
**Income target:** RM 0–397/month
**Status:** Infrastructure complete — homepage built, all templates done, content is the only remaining bottleneck

### Blog Build
- [x] WordPress + Bricks Builder installed on Hostinger (WordPress 7.0, PHP 8.2, LiteSpeed)
- [x] Activate Bricks Builder Ultimate 2.3.8 (license active ✅)
- [x] Install Rank Math SEO 1.0.272 (active, usage tracking OFF)
- [x] WordPress core settings configured (tagline, timezone Kuala Lumpur, permalink = Post name)
- [x] Delete default WP content (Hello World post + Sample Page → Trash)
- [x] Create blog categories (AI Tools / Digital Side Hustle / Canva & Design / AI untuk Perniagaan Kecil)
- [x] Build Bricks Single Post Template (ID 10) — native Bricks elements, zero Code elements (rebuilt 2026-07-04)
- [x] Fix Template 10 sidebar — Post Popular query loop + Panduan Percuma email form (2026-07-05)
- [x] Migrate Bricks MCP → Respira MCP (2026-07-05) — old endpoint decommissioned, Respira active on Windsurf + Claude Desktop
- [x] Unfreeze templates 185 & 52 — Respira snapshots before every write, rollback via snapshot_uuid
- [x] Integrate Respira Prompt Book into AGENTS.md + BRICKS-BUILDER-GUIDE.md (primer, workflows, recipes, skills, playbooks)
- [x] Create 4 project workflows: /seo-audit, /a11y-scan, /monday-audit, /two-pass-build (2026-07-05)
- [x] Build Header template (ID 185) — logo, nav, search bar, CTA (rebuilt 2026-07-04)
- [x] Build Footer template (ID 46) — native Bricks elements (rebuilt 2026-07-04)
- [x] Build Blog Archive template (ID 52) — native Bricks elements, zero Code elements (rebuilt 2026-07-04)
- [x] GitHub Desktop repo created and published (`fallendamien/DigiTrustLabCode`, pushing to `master`)
- [x] Blog live at digitrustlab.com
- [x] TROUBLESHOOTING.md documents known issues (archived — see deprecated/ folder)
- [x] Create core pages: Tentang Kami, Polisi Privasi, Disclaimer, Hubungi Kami
- [x] Nav labels standardized to Malay (Tentang Kami, Hubungi Kami, Polisi Privasi)
- [x] Git repository initialized + Windsurf workspace bootstrapped (AGENTS.md, .windsurf/rules)
- [x] Fix mobile side menu contrast (white text on dark background)
- [x] Fix Tentang Kami URL slug (/tentang → /tentang-kami) + nav menu link
- [x] Fix Tentang Kami page element hierarchy (section > container > content with proper padding)
- [x] Fix footer mobile centering (copyright + links centered on mobile, horizontal with 24px gap)
- [x] Restore header template (new ID 185) after MCP destructive action — documented in AGENTS.md + TROUBLESHOOTING.md
- [x] **GUI-First Policy 100% clean** — all 4 templates rebuilt with native Bricks elements, zero Code elements (2026-07-04)
- [x] Bricks MCP full tool audit — 41 tool calls tested, 38 pass, 3 expected failures (2026-07-04)
- [x] Bridge enum truncation bug fixed — full action enums now visible to Claude Desktop (2026-07-04)
- [x] Document `template:update` silently ignores `elements` param — use `content:update_content` instead
- [x] Document `type: "content"` (not `"single"`) for template type filter
- [x] **Delete test post** — Hello World post already trashed (confirmed 2026-07-09)
- [x] **SEO pass + voice rewrite on all core pages** — Tentang Kami, Polisi Privasi, Disclaimer, Hubungi Kami rewritten with natural casual Malay voice (2026-07-07)
- [x] **DigiTrust Lab Writing Voice guide** — documented in AGENTS.md with red flags, green light patterns, humour guidelines (2026-07-07)
- [x] **Mobile header fixed** — Template 185 mobile layout: logo+hamburger row 1, full-width CTA button row 2 (2026-07-07)
- [x] **Draft pages cleaned** — Respira duplicate (ID 244) + default Privacy Policy (ID 3) deleted (2026-07-07)
- [x] **Build homepage (ID 280)** — Hero + Latest Posts query loop + Email CTA + Category pills (2026-07-10)
- [x] **Fix homepage query loop** — Bricks editor save required to activate hasLoop on pages (2026-07-10)
- [x] **Reading time pill unified** — solid black (#1a1a1a) + white text on both homepage and blog archive (2026-07-10)
- [x] **Hero copy refined** — "AI Tools & Side Hustle Digital untuk warga Malaysia" (2026-07-10)
- [ ] Set up Google Analytics 4
- [ ] Set up Google Search Console + submit sitemap
- [x] Verify ClickRank ownership (JS snippet) — snippet added to bricks_code_head, verified ✅ (2026-07-09)
- [ ] Add digitrustlab.com to Screpy
- [ ] Connect ClickRank to Google Search Console — pending GSC setup

### Tentang Kami — SEO Pass (Completed 2026-07-01)
- [x] Identified weak/translated-sounding Malay copy on `/tentang/`
- [x] Rewrote body copy — natural Malay voice, first-person founder ("Zed") framing, retained category keywords (AI tools, side hustle digital, perniagaan kecil)
- [x] Drafted new title tag: "Tentang DigiTrust Lab - AI Tools & Side Hustle Digital Malaysia"
- [x] Drafted new meta description (148 chars, includes 3 category keywords + experience/trust signal)
- [x] Apply rewrite in WordPress (Bricks) — pushed live 2026-07-03
- [ ] Set Rank Math schema type to `Person`/`AboutPage`, link "Zed" as author entity
- [ ] Set Rank Math focus keyword field
- [ ] Confirm OG/social share image is set
- [ ] Cross-check keyword choices against actual WriterZen data (current keywords are category-level estimates, not volume-validated)
- [x] Repeat same pass for Polisi Privasi, Disclaimer, Hubungi Kami (2026-07-07)

### Security Hardening (COMPLETED 2026-07-15)
- [x] Change admin username (created `zed_dtl`, transferred posts, deleted `admin`)
- [x] Change admin password (20+ char, stored in password manager)
- [x] Enable 2FA on WP Admin (WP 2FA plugin by Melapress — TOTP)
- [x] Enable 2FA on Hostinger hPanel (Account → Security)
- [x] Install Limit Login Attempts (block IPs after 3 failed attempts)
- [x] Hide WP login URL (WPS Hide Login — login URL changed to `/dtl-login`)
- [x] Disable XML-RPC (Hostinger security toggle)
- [x] Disable application passwords (Hostinger security toggle)
- [x] Force HTTPS (Hostinger security toggle)
- [x] Enable Cloudflare Bot Fight Mode (Security → Bots)
- [x] Enable Cloudflare AI Labyrinth (blocks rogue AI scrapers)
- [x] Enable Cloudflare Leaked Credentials Detection (blocks compromised passwords)
- [x] Activate Akismet Anti-spam (spam protection for comments + forms)
- [x] Update Respira plugin (updated to latest)
- [x] Keep all plugins updated (all current as of 2026-07-15)
- [ ] Add Cloudflare security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy — skipped, add later)

### Email List (Day 1 — same week as blog launch)
- [ ] Create MailerLite free account
- [ ] Add simple opt-in to blog sidebar/footer
- [ ] Create lead magnet PDF: "50 Prompt AI Percuma untuk Perniagaan Malaysia"
- [ ] Replace simple opt-in with lead magnet opt-in (Week 2–3)

### Affiliates (Week 1)
- [ ] Register Klikjer (klikjer.com/affiliate)
- [ ] Register JV Warrior (jvwarrior.com/access/aff/signup)
- [ ] Apply AI Labs Malaysia (ailabs.com.my/affiliate-program) — Month 1

### Etsy Shop (Week 3–4)
- [ ] Competitor research on Etsy (15 min) — check saturation before listing
- [ ] Create Etsy shop — English name (PromptLabSEA / AIStudioMY / ZamriDesigns)
- [ ] List product #1: 30 AI Prompts for FB & IG Ads (Bahasa Melayu) — RM 15–25
- [ ] List product #2: 5 Canva Templates for IG Story (Small Business) — RM 12–20
- [ ] List product #3: Notion Dashboard for Freelancers (Malaysian Edition) — RM 18–30
- [ ] List product #4: 50 AI Prompts for Creating Digital eBooks — RM 15–25
- [ ] List product #5: Bundle — 30 AI Prompts + 5 Canva Templates — RM 29–39

### Blog Posts (1 post/week — Malay-first 70%) — 1 of 10 published
- [x] Post #1: "Apa Itu AI? (Dan Kenapa Ia Bukan Setakat Robot dalam Filem)" — published Jul 9 at digitrustlab.com/apa-itu-ai/
- [ ] Post #2: Cara Guna ChatGPT untuk Bantu Kerja Harian Korang (Panduan Mudah 2026) → AI Mastery affiliate *(natural follow-up to Post #1)*
- [ ] Post #3: 10 AI Tools Percuma untuk Perniagaan Malaysia 2026 → AI Mastery affiliate
- [ ] Post #4: Cara Jana Pendapatan dengan Canva Templates → Etsy listing link
- [ ] Post #5: Prompt AI untuk Buat Iklan Instagram yang Menarik → Etsy prompt pack
- [ ] Post #6: Review Modul AI Mastery: Worth It Ke? → AI Mastery direct sale
- [ ] Post #7: Cara Buat eBook Digital dengan AI (Step-by-Step) → Klikjer affiliate
- [ ] Post #8: 5 Template Notion untuk Freelancer Malaysia → Etsy Notion template
- [ ] Post #9: Cara Mula Jual Digital Products di Etsy Malaysia → Etsy + blog cross-link
- [ ] Post #10: AI vs Canva: Mana Lebih Baik untuk Design? → Both affiliate + Etsy

### Off-Page SEO (Week 1 — ongoing)
- [ ] Reddit/Lowyat answers — 2–3x/week, link naturally to blog posts
- [ ] Create Pinterest account — pin every blog post + every Etsy listing
- [ ] Set up Web 2.0 profiles (Medium, Dev.to, LinkedIn) — repurpose blog posts

---

## Phase 2: Compounding 🔥 (Month 4–6)

**Goal:** 25 blog posts + 15 Etsy listings + AdSense approved + Canva Pro affiliate
**Income target:** RM 200–1,273/month
**Status:** Not started

- [ ] Register Canva Pro affiliate (Month 2 — after first Etsy Canva listing live)
- [ ] Register iCore Hosting affiliate (Month 2 — after blog live)
- [ ] Apply Google AdSense (Month 4–5, after ~20 posts)
- [ ] Reach 15 Etsy listings
- [ ] Reach 25 blog posts
- [ ] Add Canva Pro affiliate link inside every Canva template product
- [ ] Create first English pillar post (3,000+ words, global audience)
- [ ] Upgrade MailerLite opt-in with lead magnet PDF
- [ ] Create Pinterest account (pins for every Etsy listing)
- [ ] Register Agent Builder affiliate

---

## Phase 3: Traffic Growth 📊 (Month 7–12)

**Goal:** 50 posts + 25 Etsy + Ezoic active + 500+ email subs + DA 15–25
**Income target:** RM 800–4,015/month
**Status:** Not started

- [ ] Apply Ezoic (when 10K+ visits/month)
- [ ] Register Shopify MY affiliate
- [ ] Register Agent Builder affiliate (after WordPress blog running 3+ months)
- [ ] Reach 50 blog posts
- [ ] Reach 25–35 Etsy listings
- [ ] Reach 500 email subscribers
- [ ] Start KDP (Kindle Direct Publishing) — AI-generated low-content books
- [ ] Email newsletter sponsorship (when 500+ subscribers)
- [ ] Monthly pillar posts (3,000+ words)
- [ ] Refresh/update old posts
- [ ] Sponsored posts (DA 20+)

---

## Phase 4: Scale 🚀 (Month 13–24)

**Goal:** 100+ posts + 50 Etsy + Mediavine + Own course + RM 5K+/month
**Income target:** RM 3,000–18,400/month
**Status:** Not started

- [ ] Apply Mediavine (when 50K sessions/month)
- [ ] Launch own course: "Panduan Lengkap Jana Pendapatan dengan AI untuk Perniagaan Malaysia"
- [ ] Reach 100+ blog posts
- [ ] Reach 50 Etsy listings
- [ ] Reach 1,000+ email subscribers
- [ ] Gumroad premium bundles
- [ ] Revisit web services option (BCL landing pages for MY resellers)
- [ ] Salary replacement achieved

---

## Future Enhancements 💡

*Features to consider after MVP launch:*

- Web services layer (parked for future phase)
- Paid ads return (only after organic validation)
- YouTube channel (repurpose blog content)
- Online community (Discord/Telegram)
- B2B consulting (AI implementation for Malaysian SMEs)

### Tech Debt 🔧

- [x] Convert Single Post template (ID 10) from Code element to native Bricks elements
- [x] Convert Blog Archive template (ID 52) from Code element to native Bricks elements
- [ ] Replace Bricks native form on Template 10 sidebar with MailerLite embed (when MailerLite account created)
- [ ] Clean leftover metadata on Template 10 (after_children/after_element from failed MCP inject — harmless but untidy)
- [x] **Mobile horizontal overflow on `/blog/` — fixed** — CSS Grid `min-width: auto` on card containers caused track inflation. Fix: `min-width: 0` on grid children. Verified live at 375px. (2026-07-11)

---

## Key Milestones

- ✅ Meta Ads run — 1 confirmed sale (Mohamad Rafek, RM 69, Jun 10 2026)
- ✅ SEO tool stack complete (WriterZen + ClickRank + Screpy — all lifetime)
- ✅ Bricks Builder Ultimate owned (unlimited sites, lifetime)
- ✅ Domain digitrustlab.com live on Cloudflare
- ✅ Long-term plan finalised + gaps fixed (Jun 28 2026)
- ✅ WordPress + Bricks Builder running on Hostinger
- ✅ Bricks Builder 2.3.8 installed + licensed (ACTIVE)
- ✅ Rank Math SEO installed + configured (usage tracking OFF)
- ✅ WordPress settings configured (timezone KL, permalink = post name)
- ✅ Default WP content deleted (Hello World + Sample Page)
- ✅ Blog categories created (AI Tools, Digital Side Hustle, Canva & Design, AI untuk Perniagaan Kecil)
- ✅ Bricks Single Post Template built + condition set (Post type = Post)
- ✅ Header + Footer templates built
- ✅ GitHub repo published (`fallendamien/DigiTrustLabCode`)
- ✅ **Blog LIVE at digitrustlab.com (confirmed 2026-07-01)**
- ✅ Core pages live (Tentang Kami, Polisi Privasi, Disclaimer, Hubungi Kami)
- ✅ Tentang Kami SEO/copy pass completed + pushed live (2026-07-03)
- ✅ Mobile menu contrast fix + footer mobile centering + Tentang Kami padding fix (2026-07-03)
- ✅ Header template restored (ID 140) after MCP destructive action (2026-07-03)
- ✅ Respira MCP migrated + templates unfrozen (2026-07-05)
- ✅ Template 10 sidebar matches design spec (2026-07-05)
- ✅ ClickRank ownership verified + snippet live on all pages (2026-07-09)
- ✅ content/SEO-CHEATSHEET.md created + keyword research done for Post #1 (cara guna AI, KD=0, 140/mo) (2026-07-09)
- ✅ FABLE5-WORDS-OF-WISDOM.md created (2026-07-09)
- ✅ Em dash writing rule added to AGENTS.md (2026-07-09)
- ✅ Homepage built with 4 sections (Hero, Latest Posts, Email CTA, Category Pills) (2026-07-10)
- ✅ Query loop fix documented — Bricks pages need editor save to activate hasLoop (2026-07-10)
- ✅ Reading time pill design unified across homepage + blog archive (2026-07-10)
- ✅ **Homepage live at digitrustlab.com** (2026-07-10)
- ✅ **Mobile overflow fixed on `/blog/`** — `min-width: 0` on grid children, verified at 375px viewport (2026-07-11)
- ✅ **Migration COMPLETE** — Local by Flywheel → Hostinger Business WordPress (2026-07-11)
- ✅ **Email working** — hello@digitrustlab.com active, all 4 DNS checks green (MX, SPF, DKIM, DMARC) (2026-07-11)
- ✅ **SSL COMPLETE** — Hostinger Lifetime SSL active + Cloudflare SSL/TLS Full (Strict) enabled (2026-07-12)
- ✅ **Menu links fixed** — all point to digitrustlab.com (2026-07-12)
- ✅ **Respira MCP reconfigured** — Windsurf + Claude Desktop connected to Hostinger site (2026-07-12)
- ✅ **Old approach deprecated** — Local WP + Simply Static + Cloudflare Pages docs moved to deprecated/ folder (2026-07-12)
- ✅ **Post #1 published** — "Apa Itu AI?" live at digitrustlab.com/apa-itu-ai/ (Jul 9) (1 of 10 done)
- 🎯 First Etsy sale — target: Month 2
- 🎯 First affiliate commission — target: Month 3
- 🎯 RM 200/month — target: Month 6
- 🎯 RM 1,000/month — target: Month 9–12
- 🎯 Salary replacement — target: Month 18–24

---

## Current KPIs

| Metric | Current | Target (Month 12) |
|---|---|---|
| Blog posts live | 1 | 50+ |
| Monthly blog visits | 0 | 10,000+ |
| Etsy listings | 0 | 25+ |
| Email subscribers | 0 | 500+ |
| Keywords top 10 | 0 | 15+ |
| Monthly revenue | RM 69 (pre-blog) | RM 2,000+ |

---

## Hostinger Stack (Current — Migrated 2026-07-11)

| Component | Version | Status |
|---|---|---|
| WordPress | 7.0 | ✅ Running at digitrustlab.com |
| PHP | 8.2 | ✅ Hostinger |
| Web Server | LiteSpeed | ✅ |
| Database | MySQL | ✅ Hostinger |
| Bricks Builder | 2.3.8 Ultimate | ✅ Licensed |
| Rank Math SEO | 1.0.272 | ✅ Active |
| LiteSpeed Cache | — | ✅ Active |
| Cloudflare Proxy | — | ✅ Active (Full Strict SSL) |
| Email | hello@digitrustlab.com | ✅ Working |

**WP Admin:** https://digitrustlab.com/wp-admin/
**Hosting:** Hostinger Business WordPress (IP: 145.79.28.85)
**Live site:** https://digitrustlab.com/ (via Cloudflare proxy)
**Email:** https://mail.hostinger.com (hello@digitrustlab.com)
**GitHub repo:** https://github.com/fallendamien/DigiTrustLabCode
**Deploy:** No static export needed — site is dynamic WordPress on Hostinger

---

## IMMEDIATE NEXT SESSION — Start Here

1. **Write Post #1** — "Apa Itu AI? (Dan Kenapa Ia Bukan Setakat Robot dalam Filem)" → already published (Jul 9), verify it's live at digitrustlab.com/apa-itu-ai/
2. **Set up MailerLite** — Day 1 priority, still outstanding. Simple opt-in first, lead magnet PDF Week 2–3
3. **Set up Google Search Console + GA4** — do right after verifying Post #1 is live so indexing starts immediately
4. **Register Klikjer affiliate** — Week 1 task, still pending
5. **Add digitrustlab.com to Screpy** — rank tracking setup

> **Infrastructure is DONE.** All templates, pages, export pipeline, mobile fixes, and deploy workflow are complete. Content is the only remaining bottleneck.

---

## Revenue Stack

```
Layer 5 (Month 18+): Mediavine Premium Ads
Layer 4 (Month 12+): Ezoic Display Ads
Layer 3 (Month 1+):  Affiliate — Klikjer + JV Warrior + Canva Pro + AI Labs
Layer 2 (Month 1+):  Etsy Digital Products
Layer 1 (Month 1+):  Blog SEO Content — THE ENGINE
```

---

## Language Strategy

- **Blog:** Malay-first 70% (low competition SEA) + English 30% (pillar posts, higher RPM, backlink bait)
- **Etsy:** English titles + English descriptions. Malay content inside the product itself.
- **Rule:** Never translate same post into both languages (duplicate content)
- **Voice standard (updated 2026-07-06):** All core pages audited and rewritten with natural casual Malay voice. Full voice guide documented in `AGENTS.md` under "DigiTrust Lab Writing Voice". Key rule: write Malay directly in Malay, never translate from English. Use `korang`/`kami`, avoid `anda`/`pengguna`. All future content must follow this standard — posts, pages, email copy, everything.

---

## Off-Page SEO — Closed Loop (No Outreach Needed)

```
Etsy listing (DA 88) → links to blog post
Blog post → links to Etsy listing
Pinterest pin → links to both
```

Reddit/Lowyat answers 2–3x/week + Web 2.0 profiles (Medium, Dev.to) — one-time setup.

---

## What NOT To Do

- ❌ Run paid ads again — proven failure at current stage
- ❌ More than 1 post/week initially — quality > quantity
- ❌ Spread across too many platforms — Blog + Etsy + 2 affiliates only
- ❌ Quit day job before Month 18
- ❌ Skip email list — start Day 1, not Month 2
- ❌ Keep building infrastructure once blog is live — content is now the bottleneck

---

## Notes

**Tech stack:** Hostinger Business WordPress → Bricks Builder Ultimate → LiteSpeed Cache → Cloudflare proxy (RM0/month hosting via Cloudflare)
**SEO tools:** WriterZen (keyword research) → ClickRank (optimize) → Screpy (track)
**Payment:** BCL.my (AI Mastery reseller, keep as-is) → Etsy Payments (own products)
**Domain:** digitrustlab.com (Cloudflare Registrar, Zone ID: 94c8c2bff83a3ed15b7405d507eca68e)
**Hosting:** Hostinger Business WordPress, IP 145.79.28.85
**Email:** hello@digitrustlab.com (Hostinger email, all DNS checks green)
**SSL:** Cloudflare SSL/TLS = Flexible (Hostinger Lifetime SSL installing — switch to Full Strict when done)
**Bricks license key:** stored in Bitwarden (removed from repo for security)
**GitHub repo:** fallendamien/DigiTrustLabCode (branch: master)
