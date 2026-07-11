# NEXT — DigiTrust Lab

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

11. **Verify Post #1 is live** — "Apa Itu AI?" published Jul 9, check digitrustlab.com/apa-itu-ai/
12. **Set up Google Search Console + GA4** — verify ownership, submit sitemap
13. **Set up MailerLite** — free account, newsletter form on blog
14. **Add digitrustlab.com to Screpy** — monitoring
15. **Register Klikjer affiliate** — free, 50% commission, Malaysian eBooks
16. **Register JV Warrior affiliate** — Malaysian digital products
17. **Create Etsy shop** — choose clean shop name (NOT DigiTrust Lab)
18. **Create first Etsy listing** — "30 Prompt AI untuk Iklan FB & IG (Bahasa Melayu)"
19. **Create lead magnet PDF** — "50 Prompt AI Percuma"
20. **Write Post #2** — `cara guna ChatGPT` (est. 1,600–2,400 searches/mo MY, very low KD)
    - Title: "Cara Guna ChatGPT untuk Bantu Kerja Harian Korang (Panduan Mudah 2026)"
    - Slug: `/cara-guna-chatgpt/`
    - Category: AI Tools
    - Language: Malay
    - Outline: Apa itu ChatGPT → Cara start (free vs paid) → 5 cara praktikal (emel, ringkasan, idea konten, terjemah, jadual) → Prompt tips → CTA AI Mastery Module
    - Internal link: → Post #1 /apa-itu-ai/
    - Also add to WriterZen keyword list: "DigiTrust Lab Blog Posts"

## Scope Restrictions

- **UNFROZEN:** Templates 185 (Header) and 52 (Blog Archive) — editable via Respira MCP (snapshot before edit)
- **Permitted:** Posts, pages, menus, project docs, template edits via Respira MCP
- **NOT Permitted:** Old Bricks MCP endpoint (decommissioned), post-processing scripts, Raw HTML Code elements

## Important Notes

- **Bricks-Only Policy**: ALL changes via Bricks Builder GUI or Respira MCP. NO scripts, NO post-processing.
- **Templates**: 185 & 52 unfrozen — use Respira MCP with snapshot, rollback via `respira_restore_snapshot`
- **MailerLite TODO**: Template 10 sidebar has Bricks native form — replace with MailerLite embed when account created
- **Workflow**: Write in WordPress → Publish → Live instantly (LiteSpeed Cache + Cloudflare proxy)
- **Email**: hello@digitrustlab.com ✅ WORKING — all 4 DNS checks green, mailbox active at mail.hostinger.com
- **SSL**: Full (Strict) — Hostinger Lifetime SSL active + Cloudflare Full (Strict) enabled (2026-07-12)
- **Old approach**: Local WP + Simply Static + Cloudflare Pages fully decommissioned (2026-07-12). Archived docs in `deprecated/` folder
