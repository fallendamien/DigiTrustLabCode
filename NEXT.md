# NEXT — DigiTrust Lab

## 🖥️ New device / cross-laptop setup — run the check, don't read a list

_Updated 2026-08-04. MCP for Claude Code is modular by scope._

```powershell
git -C <path>\agent-templates pull
git pull                     # from this repo — brings .mcp.json
& <path>\agent-templates\scripts\startup-integrity-check.ps1
```

The **🔌 Claude Code MCP** section names anything missing and how to fix it.
It reads the live config, so it cannot go stale the way a checklist does.
Expect **all checks passed, exit 0** — judge by that, not by a fixed count.

| Scope | File | Holds | Travels |
|-------|------|-------|---------|
| User | `~/.claude.json` | `fetch`, `pieces`, `chrome-devtools` | per-device |
| Project | `<repo>/.mcp.json` | `respira` @8.2.0 | **git** |
| Harness | `~/.claude/settings.json` | `MCP_TIMEOUT: 120000` | per-device |

What the script cannot see, because it is UI state and not a file:

> ⚠️ Claude Code prompts **once per project** to approve a committed
> `.mcp.json`. Until you accept, `respira` will not appear — and it looks
> exactly like a failed sync. Check this first.

Two other things worth knowing when the script reports a failure:

- `MCP_TIMEOUT` is not optional. `fetch` cold-starts at ~71s on a fresh npx
  cache; the 30s default kills it and it looks like a broken install.
- The Respira API key is **not** in git. It lives in the `RESPIRA_API_KEY`
  User env var, which `.mcp.json` expands. Set it before starting Claude Code
  — env vars are read at process start.

Verify Respira with an actual tool call, never `claude mcp list` or `curl`
(both report false failures — see `lessons.md`):

```
respira_diagnose_connection
```
Known-good 2026-08-04: `success: true` · 5/5 probes 200 + `application/json` ·
`html_instead_of_json: false` · 258 REST routes · 3 DB tables · plugin 8.1.10 ·
WP 7.0.2 · PHP 8.3.30 · MCP server 8.2.0.

**Open:** Google Calendar connector needs OAuth (UI only). Context7 appears
twice — account-managed, no config file on disk, nothing to delete.

## Current State

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

**⚠️ Remaining Phase 7 tasks (NOT done — pick up next session):**
- [ ] ClickRank → AI Overview Tracker: add `cara buat gambar ai` + URL (Malaysia, Malay)
- [ ] ClickRank → Keyword Tracker: same keyword + URL (focus keyword only)
- [ ] Screpy → Rank Tracker: same keyword + URL (Malaysia, desktop + mobile)
- [ ] Screpy → Pages → Analyze: re-crawl so the new URL is discovered
- [ ] Run `internal-link-builder` skill so Posts #1, #2, #3 link *down* to this post (it already links up to #1 and #3)

**Pipeline fixes shipped this session** (all committed): quota check, Topic Discovery, Golden Filter and Weak Spot gate added as mandatory phases; AGENTS.md pipeline summary corrected (it started at Keyword Explorer, which is why agents skipped research); Golden Score bands corrected; em dash rule conflict resolved; excerpt method documented after the WP UI silently failed.

## Post #3 — ✅ COMPLETE (2026-07-21)

All phases complete. Post published at /cara-buat-prompt-chatgpt/. Rank Math score: 100/100.

**Remaining Phase 7 tasks:**
- [ ] Run ClickRank optimization (bulk title + keyword tracker)
- [ ] Run internal link builder (add inbound links from Posts #1 and #2)

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
