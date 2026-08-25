# NEXT — DigiTrust Lab

> **New device?** Device setup is not documented here — it is scripted in the
> TSOT, so it cannot go stale. Run:
> ```powershell
> & <tsot>\scripts\bootstrap-new-device.ps1 -IncludeClaude -ProjectPath <repo>
> & <tsot>\scripts\startup-integrity-check.ps1
> ```
> The only project-specific piece is `.mcp.json` in this repo (Respira, bound to
> digitrustlab.com), which arrives with `git pull`. Approve it once when Claude
> Code prompts, or its servers silently will not load.

## Current State

> **CURRENT STATUS — POST #7 CLOSEOUT COMPLETE (2026-08-25):** The earlier published article remains closed. Post #7 is live at `https://digitrustlab.com/cara-buat-nota-cantik-dengan-ai/` (ID 656). Claude Sonnet OAuth review, OpenAI naturalness, Rank Math, live link, Screpy Rank Tracker, ClickRank and exact GSC inspection gates passed. GSC showed `URL is on Google` and `Page is indexed` at 2026-08-25 15:52:44 (+08:00); no request was needed. Screpy Pages discovery remains a non-blocking pending item because the latest existing crawl predates publication.
>
> **Also completed 2026-08-25:** (1) WordPress site title + Rank Math Website Name changed to `DigiTrustLab` (Alternate Name `DigiTrust Lab`); `og:site_name` and JSON-LD `WebSite.name` verified live. Setting is at Rank Math → Titles & Meta → **Local SEO** — not under Global. (2) Homepage pagination activated (page 280): query loop moved from inert grid container `#brxe-778413` to card element `#brxe-4c6189` (`postsPerPage: 6`); pagination element `#brxe-cctbuz` added and rebound; `/page/2/` returns HTTP 200 with posts 7–10, no duplicates. `/page/2/` canonical left pointing at homepage — deliberate decision, not a bug.

## Next action

1. Select a new article topic.
2. Begin the standard Option C pipeline at WriterZen quota check, then Topic Discovery; do not start drafting before these gates.
3. Carry Post #7 Screpy Pages discovery as a non-blocking pending item: existing crawl `ojsmg8wv9al9ctqg` (started 2026-08-23T09:01:06Z, finished 09:01:38Z, last synced 09:02:44Z) does not contain the exact URL or slug. Do not start a crawl without explicit authorization. Keep the earlier closed article untouched.

### Post #7 — ✅ PUBLISHED (2026-08-24)

- WriterZen research and Content Creator report `244245` are complete; the WriterZen 0/3 image warning is documented and bypassed by the approved WordPress staging path.
- WordPress post `656` is published in category `Digital Skills`, with featured media `653` and in-content media `654` and `655`.
- Rank Math audit is `100/A` with focus keyword, SEO title, meta description, keyword density, image alt text, links and schema passing.
- Fresh authenticated-Chrome Claude Sonnet review and OpenAI review (`gpt-5.6-luna`, high) both pass all seven naturalness checks with high confidence and no blocking findings. Live revalidation passes 44 segments after duplicate-title cleanup with hash `3c09e64e64dcc8754c5aca24873046b896507e6df968555be374fc4a4d4c1b96`.
- Template-title structure gate passes live: Post `656` has no body H1, so the template title is rendered once. The deterministic gate is now mandatory for future drafts and live posts.
- Outbound link gate passes: 3 internal, 3 external, 1 dofollow, all destinations checked. Inbound review added one contextual link from Post #12 (ID 605); artifact: `content/link-reviews/cara-buat-nota-cantik-dengan-ai.json`.
- Screpy Rank Tracker row `cara buat nota cantik` is visible in both Desktop and Mobile tabs, Malaysia/Malay, Device: Both.
- ClickRank Keyword Tracker — verified 2026-08-25 15:19 (+08:00): exact keyword `cara buat nota cantik`, exact URL, Malaysia, Device All, visible row, 10/10 rows, initial position 0.
- ClickRank AI Overview Tracker — verified after reload 2026-08-25 15:19 (+08:00): exact keyword and URL, Malaysia/Malay, count 9; visible row status `Pending / N/A / N/A / 0% / 0 / No / Never`.
- ClickRank Website Optimization / Pages — exact URL added and verified after expanding `All`; exact slug appears in the full queue, with no recommendations applied.
- Google Search Console exact URL inspection passed 2026-08-25 15:52:44 (+08:00): `URL is on Google` and `Page indexing — Page is indexed`; no request was needed. Screpy Pages discovery remains pending because the latest existing crawl `ojsmg8wv9al9ctqg` predates publication and does not contain the exact URL or slug; no crawl was started.

### WordPress 7.1 update — ✅ completed via Hostinger (2026-08-23)

- Hostinger reported `WordPress version updated successfully` and the dashboard shows WordPress `7.1`.
- Next operational check: flush LiteSpeed/Hostinger cache and smoke-test the homepage, `/blog/`, the published Canva article, its lightboxes, Bricks, Rank Math and the signup form.
- Hostinger suggested PHP 8.3 separately; leave that unchanged until a compatibility review is explicitly planned.

### Post #1 — ✅ ANI/AGI/ASI update and review fixes (2026-08-19)

- [x] WriterZen research completed: Topic Discovery `245998`, Keyword Explorer `1567455`
- [x] ANI/AGI/ASI explanatory section added to live Post #1 (ID 256); no standalone post number assigned
- [x] Claude Sonnet 5 review fixes applied: clearer transition, simplified AGI explanation, and grammar correction
- [x] Final AGI wording clarity refinement applied after targeted Claude re-review
- [x] Respira security validation passed; live read-back confirmed the final text and publish status
- [x] `verify-malay-voice.py 256` — 0 errors, 0 warnings
- [x] `verify-content-status.py` — calendar and live WordPress remain consistent
- [ ] No further Post #1 changes while the roadmap remains HIATUS unless Zamri explicitly resumes content execution

- 🖥️ **Primary editor: Zed** (since 2026-08-05) — Codex reached via ACP, Claude
  Code via terminal. Windsurf retained only for Devin; VS Code legacy. See
  `AGENTS.md` § "Editors — Zed is primary".
- ✅ Blog is LIVE at https://digitrustlab.com
- ✅ Homepage live at digitrustlab.com (2026-07-10)
- WordPress + Bricks Builder on Hostinger, served via Cloudflare proxy (no static export needed)
- ✅ **MIGRATION COMPLETE** — Local by Flywheel → Hostinger Business WordPress (2026-07-11)
- ✅ **EMAIL WORKING** — hello@digitrustlab.com active, all 4 DNS checks green (MX, SPF, DKIM, DMARC) (2026-07-11)
- ✅ **SSL COMPLETE** — Hostinger Lifetime SSL active + Cloudflare SSL/TLS Full (Strict) enabled (2026-07-12)
- ✅ Templates 185 & 52 UNFROZEN — Respira MCP active with snapshot/rollback (2026-07-05)
- ✅ Respira MCP replaced old Bricks MCP — connected to Windsurf + Claude Desktop
- ✅ Template 10 sidebar fixed — Post Popular query loop + Panduan Percuma email form
- Core pages: Homepage, Tentang Kami, Polisi Privasi, Disclaimer, Hubungi Kami
- 4 project workflows created: /seo-audit, /a11y-scan, /monday-audit, /two-pass-build
- ✅ **Infrastructure is DONE. Content is the only remaining bottleneck.**
- ✅ **Google Search Console + GA4 connected** — Rank Math Analytics green, GA4 tag live (2026-07-18)
- ✅ **Security hardening completed** — admin username changed, 2FA (WP + Hostinger), Limit Login Attempts, WPS Hide Login (/dtl-login), XML-RPC disabled, Cloudflare Bot Fight Mode + AI Labyrinth + Leaked Credentials Detection, Akismet, security headers via .htaccess (2026-07-15)
- ✅ **AI Search Optimization completed** — llms.txt live at /llms.txt, Web2Agent active for AI discovery (2026-07-15)
- ✅ **ClickRank keyword tracker active** — 5 keywords added (apa itu AI, cara guna ChatGPT, cara buat poster guna chatgpt, cara edit gambar guna chatgpt, cara buat resume guna chatgpt), targeting Malaysia, all devices (2026-07-18)
- ✅ **ClickRank bulk titles investigated** — confirmed it changes SEO `<title>` tags only, not H1 or page content (2026-07-18)
- ✅ **Screpy uptime fixed** — old project (dfd8e2388f) deleted, recreated via GSC import (new project wgspvb7lc3), uptime green (2026-07-18)
- ✅ **Post #2 published** — "Cara Guna ChatGPT untuk Membantu Kerja Harian Anda (Panduan Mudah 2026)" live at /cara-guna-chatgpt/ via WriterZen Option C pipeline (2026-07-18)
- ✅ **Post #3 published** — "Cara Buat Prompt ChatGPT: Panduan Mudah untuk Pemula Malaysia" live at /cara-buat-prompt-chatgpt/ via WriterZen Option C pipeline (2026-07-21)
- ✅ **Post #4 published** — "Cara Buat Gambar AI Percuma: Panduan Lengkap untuk Pemula 2026" live at /cara-buat-gambar-ai/, Rank Math 100/100, first post through the *corrected* pipeline (2026-07-29)

## Post #4 — ✅ PUBLISHED (2026-07-29)

Live at https://digitrustlab.com/cara-buat-gambar-ai/ · Post ID 536 · Rank Math **100/100** · 849 words · 4 images · Prompt Engineering category (now activated, was empty).

**Keyword:** `cara buat gambar ai` — 720/mo, Golden Score 1.0, All-in-Title **0**.
**Note:** published under a documented Weak Spot override (measured 1, gate is 2) after four alternative angles were tested and found worse. Full rationale in `content/content-calendar.md`. Expect 6–12 months to page 1, not weeks.

**✅ Phase 7 COMPLETE (2026-08-01):**
- [x] ClickRank → AI Overview Tracker: `cara buat gambar ai` + URL (Malaysia/Malay) — returned **organic #51** on first check
- [x] ClickRank → Keyword Tracker: same keyword + URL (Malaysia, All devices)
- [x] Screpy → Rank Tracker: same keyword (Malaysia/Malay, **Mobile + Desktop** as two entries)
- [x] Screpy → re-crawl queued (`e4i4rqes8hcwfbo9`)
- [x] `internal-link-builder`: 5 links added. Post #4 went 0 → 3 inbound; **Post #6 was also orphaned** and went 0 → 2

**Pipeline fixes shipped this session** (all committed): quota check, Topic Discovery, Golden Filter and Weak Spot gate added as mandatory phases; AGENTS.md pipeline summary corrected (it started at Keyword Explorer, which is why agents skipped research); Golden Score bands corrected; em dash rule conflict resolved; excerpt method documented after the WP UI silently failed.

## Post #5 — ✅ PUBLISHED; PHASE 7 CLOSED WITH CLICKRANK DEFERRED (2026-08-22)

Live at https://digitrustlab.com/cara-buat-poster-guna-canva/ · Post ID 629 · 1,447 words.

**Verified:** WriterZen Topic Discovery/Keyword Explorer/Planner metrics; live publication; nine authentic Canva UI tutorial figures with native lightboxes; refreshed naturalness artifact (82/82, Claude Sonnet 5 + OpenAI `gpt-5.6-luna` high) after the scoped duplicate-title cleanup; Malay voice; link destinations; ClickRank Keyword Tracker and AI Overview rows; Screpy Rank Tracker in Desktop and Mobile tabs. Post #5 remains closed.

**Closure record:**

- Deferred and accepted — ClickRank Website Optimization / Pages returned `ERR_CONNECTION_CLOSED`; the official status page reports dead core and Google Data Synchronisation replicas. Recheck only after service recovery; no duplicate rows were submitted.
- [x] Screpy Pages — Analyze completed 2026-08-23 at 05:01 PM on crawler `41684`; Post #5 was discovered at the exact URL with HTTP `200` and page status `OK`.
- [x] Google Search Console — exact URL inspected 2026-08-23 at 21:00 (+08:00): **URL is on Google** and **Page is indexed**; no indexing request was needed.
- [x] WriterZen — fresh limits and all six Content Brief fields read 2026-08-23 at 21:04 (+08:00): Active lifetime plan; Article 66/70, Keyword Credit 38,506/40,000, AI words 2,637/8,000; report `244225` is readable and in `Writing` state.
- [x] WriterZen Seed keyword decision — Zamri accepted `Highest-volume keyword` as historical evidence; no WriterZen edit was made.
- [x] Template-title structure gate — live Post `629` has no body H1; the Bricks template supplies the single visible title. The duplicate-title correction was scoped to removing the redundant body H1; Post #5 was not reopened.
- [x] Update canonical docs, run validators, inspect the scoped diff, and commit/push — handoff commit `8d3c12b`.

## Post #11 — ✅ PUBLISHED (2026-08-08)

Live at https://digitrustlab.com/apa-itu-mcp-ai-dan-bagaimana-ia-berfungsi/ · Post ID 559 · Rank Math **100/A by Respira essential-check analysis**. The WordPress sidebar now displays **84/100**; only Content AI and cosmetic Title Readability warnings remain.

**Phase 7 complete (2026-08-08):**
- [x] ClickRank → Keyword Tracker: `mcp ai` + URL, Malaysia, All devices
- [x] ClickRank → AI Overview Tracker: `mcp ai` + URL, Malaysia/Malay
- [x] Screpy → Rank Tracker: `mcp ai`, Malaysia/Malay, **Device: Both**; verified in Desktop and Mobile tabs
- [x] Screpy → crawler completed at 06:13 AM; new post discovered with HTTP 200 and page status `OK`
- [x] Google Search Console → URL is on Google; page indexing status is `Page is indexed`
- [x] Internal-link scan completed; no safe contextual inbound link was found in older posts, so no forced edit was made
- [ ] **Critical SEO follow-up:** Rank Math rewrite rules, origin sitemap generation, and sitemap-cache exclusions are repaired; clean `post-sitemap.xml`, `page-sitemap.xml`, `category-sitemap.xml`, and `author-sitemap.xml` URLs still serve LiteSpeed’s cached HTTP 404. Clear the persistent public cache through authenticated WordPress/Hostinger/Cloudflare controls, verify clean XML 200 responses, then re-submit the sitemap in Search Console. Evidence: `docs/post-11-revalidation-2026-08-09.md`

## Post #9 — 🚧 PUBLISHED; FINAL GATES HANDOFF (2026-08-10)

Live at https://digitrustlab.com/prompt-gemini-ai-untuk-edit-foto/ · Post ID 582 · Prompt Engineering · 1,732 words.

**Verified:** Rank Math 85/100 in the WordPress sidebar; Respira essential audit 100/A (13/13); Claude + OpenAI naturalness artifact and Malay voice gate pass; live rendered images Media 579–581 pass; outbound link gate pass (3 internal, 1 external dofollow); ClickRank Keyword Tracker, Website Optimization / Pages, and AI Overview Tracker are configured; Post #11's exact Pages URL is backfilled and visible without duplication.

**Luna must finish:**

- [x] Screpy Rank Tracker — added `prompt gemini ai untuk edit foto`, Malaysia/Malay, **Device: Both** in one action; fresh Desktop and Mobile snapshots both show the row.
- [ ] Screpy Pages — **Analyze** clicked at 03:14 (+08:00); crawl is still visibly **Analyzing...** on crawler `18151`, so the new Post #9 discovery/result is not yet recorded.
- [x] Google Search Console — inspection showed **URL is not on Google / URL is unknown to Google**; indexing request submitted successfully at 2026-08-10 02:42 (+08:00). Re-inspect later; a request is not proof of indexing.
- [x] Internal-link-builder scan — no safe contextual inbound link found; no link forced. Artifact: `content/link-reviews/prompt-gemini-ai-untuk-edit-foto.json`.
- [ ] Update the remaining docs and run all validators, then inspect the scoped diff and commit/push. Full step-by-step handoff: `content/post-9-luna-handoff.md`.

## Post #3 — ✅ COMPLETE (2026-07-21)

All phases complete. Post published at /cara-buat-prompt-chatgpt/. Rank Math score: 100/100.

**Phase 7 complete.** ClickRank + Screpy tracking active; 3 inbound internal links (Posts #1, #2, #4).

## Completed (Sessions 1-12, 2026-06-28 to 2026-07-11)

- ✅ Git repo initialized, Windsurf workspace bootstrapped
- ✅ Long-term revenue plan + affiliate research
- ✅ WordPress + Bricks installed
- ✅ Blog structure with all core pages
- ✅ Header/footer templates with nav, search bar, CTA
- ✅ Nav labels standardized (Tentang Kami, Hubungi Kami, Polisi Privasi)
- ✅ Tentang page updated (Zed, 2022)
- ✅ Search bar resized (width 180px, height 32px)
- ✅ GUI-First Policy documented in AGENTS.md as Priority #1
- ✅ Footer template migrated from hardcoded code element to native Bricks elements
- ✅ **All 4 templates rebuilt with native Bricks elements** — zero Code elements (2026-07-04)
- ✅ Migrated Bricks MCP → Respira MCP (2026-07-05) — old endpoint decommissioned
- ✅ Templates 185 & 52 unfrozen — Respira snapshots before every write
- ✅ Respira Prompt Book integrated into AGENTS.md + BRICKS-BUILDER-GUIDE.md
- ✅ Template 10 sidebar fixed — query loop + email form matching design spec
- ✅ 4 project workflows created: /seo-audit, /a11y-scan, /monday-audit, /two-pass-build

### Sessions 8-12 (2026-07-07 to 2026-07-11)
- ✅ SEO + voice rewrite on all core pages (Tentang, Privasi, Disclaimer, Hubungi)
- ✅ DigiTrust Lab Writing Voice guide documented in AGENTS.md
- ✅ Mobile header fixed (Template 185 — logo+hamburger row 1, CTA row 2)
- ✅ Draft pages cleaned (Respira duplicate + default Privacy Policy deleted)
- ✅ Homepage built (ID 280) — Hero + Latest Posts + Email CTA + Category Pills
- ✅ Query loop fix documented — Bricks pages need editor save to activate hasLoop
- ✅ Reading time pill unified (solid black #1a1a1a + white text)
- ✅ Homepage deployed live
- ✅ ClickRank ownership verified + snippet live on all pages
- ✅ content/SEO-CHEATSHEET.md + FABLE5-WORDS-OF-WISDOM.md created
- ✅ Em dash writing rule added to AGENTS.md
- ✅ Mobile horizontal overflow fixed on `/blog/` — verified at 375px

## Next Steps (Priority Order)

> **Infrastructure COMPLETE. SSL Full (Strict) active. Docs cleaned up. Content phase begins.**

### 🔐 Security Hardening (COMPLETED 2026-07-15)

- [x] **Change admin username** — created `zed_dtl`, transferred posts, deleted `admin`
- [x] **Change admin password** — 20+ char random, stored in password manager
- [x] **Enable 2FA on WP Admin** — WP 2FA plugin (Melapress) installed + TOTP configured
- [x] **Enable 2FA on Hostinger hPanel** — Account → Security → Two-factor authentication
- [x] **Install Limit Login Attempts** — plugin installed + configured (3 retries, 20min lockout)
- [x] **Hide WP login URL** — WPS Hide Login installed, login URL changed to `/dtl-login`
- [x] **Disable XML-RPC** — enabled via Hostinger security toggle
- [x] **Disable application passwords** — enabled via Hostinger security toggle
- [x] **Force HTTPS** — enabled via Hostinger security toggle
- [x] **Enable Cloudflare Bot Fight Mode** — Security → Bots → ON
- [x] **Enable Cloudflare AI Labyrinth** — blocks rogue AI scrapers
- [x] **Enable Cloudflare Leaked Credentials Detection** — blocks compromised passwords at login
- [x] **Activate Akismet Anti-spam** — spam protection for comments + forms
- [x] **Update Respira plugin** — updated to latest via WP Admin → Plugins
- [x] **Keep all plugins updated** — all plugins current as of 2026-07-15
- [x] **Add security headers** — X-Frame-Options, X-Content-Type-Options, Referrer-Policy (added via .htaccess on Hostinger)

### AI Search Optimization (COMPLETED 2026-07-15)

- [x] **Enable LLMs.txt file** — generated at `https://digitrustlab.com/llms.txt`, validated successfully
- [x] **Enable Web2Agent** — AI discovery service active, content updates tracked for AI indexes (initial spinner lag resolved after Cloudflare propagation)

> These features complement ClickRank (traditional SEO) by helping ChatGPT, Perplexity, Claude, and Gemini discover and cite DigiTrust Lab content.

### Migration Steps (COMPLETED)

1. ✅ Sign up Hostinger Business WordPress plan
2. ✅ Export WordPress from Local by Flywheel via All-in-One WP Migration
3. ✅ Install WordPress on Hostinger
4. ✅ Import `.wpress` file to Hostinger
5. ✅ LiteSpeed Cache active on Hostinger
6. ✅ Update Cloudflare DNS → A record to 145.79.28.85 (Hostinger)
7. ✅ Cloudflare SSL/TLS: Full (Strict), Always Use HTTPS, Automatic HTTPS Rewrites
8. ✅ Cloudflare caching: Standard aggressive, 4hr browser TTL
9. ✅ Respira MCP reconnected to Hostinger site
10. ✅ Simply Static + third-party Bricks MCP deleted
11. ✅ Built-in Bricks MCP disabled
12. ✅ WordPress URLs updated to HTTPS
13. ✅ Permalinks saved
14. ✅ Email setup: hello@digitrustlab.com — mailbox created, all DNS records added (MX, SPF, DKIM, DMARC)
15. ✅ DNS records corrected — MX → mx1/mx2.hostinger.com, SPF → _spf.mail.hostinger.com
16. ✅ All 4 Hostinger email DNS checks green (MX, SPF, DKIM, DMARC)
17. ✅ Hostinger Lifetime SSL active (2026-07-12)
18. ✅ Cloudflare SSL/TLS upgraded to Full (Strict) (2026-07-12)
19. ✅ Menu links fixed — all point to digitrustlab.com (2026-07-12)
20. ✅ Respira MCP configs updated for Windsurf + Claude Desktop (2026-07-12)
21. ✅ Old approach docs deprecated and moved to deprecated/ folder (2026-07-12)

### Post-Migration (Content Phase)

11. ✅ **Post #1 live** — "Apa Itu AI?" published at digitrustlab.com/apa-itu-ai/ (2026-07-09)
12. ✅ **Set up Google Search Console + GA4** — Search Console verified, GA4 property 'DigiTrust Lab' connected, tag installed (2026-07-18)
13. ✅ **Set up MailerLite** — account created (ID 2502865), embed form cUeVaM live on homepage + single post sidebar
14. ✅ **ClickRank keyword tracker** — 5 keywords added, targeting Malaysia, all devices (2026-07-18)
15. ✅ **Security hardening** — admin username changed, 2FA, Limit Login Attempts, WPS Hide Login, Cloudflare Bot/AI/Leaked Credentials, Akismet, security headers (2026-07-15)
16. ✅ **AI Search Optimization** — llms.txt + Web2Agent active (2026-07-15)
17. ✅ **Add digitrustlab.com to Screpy** — project recreated via GSC import, uptime green (2026-07-18)
18. ✅ **Post #2 published** — "Cara Guna ChatGPT untuk Membantu Kerja Harian Anda (Panduan Mudah 2026)" live at /cara-guna-chatgpt/ (2026-07-18)
19. ✅ **Post #3 published** — "Cara Buat Prompt ChatGPT: Panduan Mudah untuk Pemula Malaysia" live at /cara-buat-prompt-chatgpt/ (2026-07-21, Rank Math 100/100)
20. **Run ClickRank optimization for Post #3** — bulk title optimization + add "cara buat prompt chatgpt" to keyword tracker
21. **Run internal link builder** — add inbound links from Posts #1 and #2 to Post #3
22. ✅ **301 redirect set up** — `digitrustlab.com/form/modul-ai-mastery` → `store.digitrustlab.com/form/modul-ai-mastery` via Rank Math Redirections (2026-07-18)
23. **Register Klikjer affiliate** — free, 50% commission, Malaysian eBooks
24. **Register JV Warrior affiliate** — Malaysian digital products
25. **Create Etsy shop** — choose clean shop name (NOT DigiTrust Lab)
26. **Create first Etsy listing** — "30 Prompt AI untuk Iklan FB & IG (Bahasa Melayu)"
27. **Create lead magnet PDF** — "50 Prompt AI Percuma"
28. **Write Post #4** — 10 Prompt AI untuk Buat Illustration Flat (dengan Contoh)
    - Category: Prompt Engineering
    - Use WriterZen Option C pipeline (Keyword Explorer → Keyword Planner → Content Brief → Content Creator → publish)

## Scope Restrictions

- **UNFROZEN:** Templates 185 (Header) and 52 (Blog Archive) — editable via Respira MCP (snapshot before edit)
- **Permitted:** Posts, pages, menus, project docs, template edits via Respira MCP
- **NOT Permitted:** Old Bricks MCP endpoint (decommissioned), post-processing scripts, Raw HTML Code elements

## Important Notes

- **Bricks-Only Policy**: ALL changes via Bricks Builder GUI or Respira MCP. NO scripts, NO post-processing.
- **Templates**: 185 & 52 unfrozen — use Respira MCP with snapshot, rollback via `respira_restore_snapshot`
- **MailerLite**: ✅ Account 2502865 active — embed form cUeVaM live on homepage + single post sidebar. Next: create lead magnet PDF to replace simple opt-in
- **Workflow**: Write in WordPress → Publish → Live instantly (LiteSpeed Cache + Cloudflare proxy)
- **Email**: hello@digitrustlab.com ✅ WORKING — all 4 DNS checks green, mailbox active at mail.hostinger.com
- **SSL**: Full (Strict) — Hostinger Lifetime SSL active + Cloudflare Full (Strict) enabled (2026-07-12)
- **Old approach**: Local WP + Simply Static + Cloudflare Pages fully decommissioned (2026-07-12). Archived docs in `deprecated/` folder
