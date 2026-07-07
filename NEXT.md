# NEXT — DigiTrust Lab

## Current State

- ✅ Blog is LIVE at https://www.digitrustlab.com
- WordPress + Bricks Builder + Simply Static + Cloudflare Pages pipeline working
- ✅ Templates 185 & 52 UNFROZEN — Respira MCP active with snapshot/rollback (2026-07-05)
- ✅ Respira MCP replaced old Bricks MCP — connected to Windsurf + Claude Desktop
- ✅ Template 10 sidebar fixed — Post Popular query loop + Panduan Percuma email form
- Core pages: Homepage, Tentang Kami, Polisi Privasi, Disclaimer, Hubungi Kami
- TROUBLESHOOTING.md documents 14+ known issues with solutions
- 4 project workflows created: /seo-audit, /a11y-scan, /monday-audit, /two-pass-build

## Completed (Sessions 1-7, 2026-06-28 to 2026-07-05)

- ✅ Git repo initialized, Windsurf workspace bootstrapped
- ✅ Long-term revenue plan + affiliate research
- ✅ WordPress + Bricks installed on LocalWP
- ✅ Blog structure with all core pages
- ✅ Header/footer templates with nav, search bar, CTA
- ✅ Simply Static export → Cloudflare Pages deployment pipeline
- ✅ Nav labels standardized (Tentang Kami, Hubungi Kami, Polisi Privasi)
- ✅ Tentang page updated (Zed, 2022)
- ✅ Search bar resized (width 180px, height 32px)
- ✅ GUI-First Policy documented in AGENTS.md as Priority #1
- ✅ Footer template migrated from hardcoded code element to native Bricks elements
- ✅ Static export file analysis completed (2,694 files — 68% wp-includes bloat identified)
- ✅ Export optimized: 2,694 → 1,836 files (32% reduction)
- ✅ **All 4 templates rebuilt with native Bricks elements** — zero Code elements (2026-07-04)
- ✅ Bricks MCP full tool audit — 41 calls tested, 38 pass, 3 expected failures
- ✅ Bridge enum truncation bug fixed — Claude Desktop now sees all tool actions
- ✅ Documented `template:update` silently ignores `elements` + `type: "content"` not `"single"`
- ✅ Migrated Bricks MCP → Respira MCP (2026-07-05) — old endpoint decommissioned
- ✅ Templates 185 & 52 unfrozen — Respira snapshots before every write
- ✅ Respira Prompt Book integrated into AGENTS.md + BRICKS-BUILDER-GUIDE.md
- ✅ Template 10 sidebar fixed — query loop + email form matching design spec
- ✅ 4 project workflows created: /seo-audit, /a11y-scan, /monday-audit, /two-pass-build

## Next Steps (Priority Order)

1. **Write and publish Post #1** — THE ONLY PRIORITY RIGHT NOW
2. Set up Google Search Console + GA4 — verify ownership, submit sitemap
3. Verify ClickRank ownership — JS snippet on blog
4. Add digitrustlab.com to Screpy — monitoring
5. Register Klikjer affiliate — free, 50% commission, Malaysian eBooks
6. Register JV Warrior affiliate — Malaysian digital products
7. Create Etsy shop — choose clean shop name (NOT DigiTrust Lab)
8. Create first Etsy listing — "30 Prompt AI untuk Iklan FB & IG (Bahasa Melayu)"
9. Set up MailerLite — free account, newsletter form on blog
10. Create lead magnet PDF — "50 Prompt AI Percuma"

## Scope Restrictions

- **UNFROZEN:** Templates 185 (Header) and 52 (Blog Archive) — editable via Respira MCP (snapshot before edit)
- **Permitted:** Posts, pages, menus, Simply Static export, Wrangler deploy, project docs, template edits via Respira
- **NOT Permitted:** Old Bricks MCP endpoint (decommissioned), post-processing scripts, Raw HTML Code elements

## Important Notes

- **Bricks-Only Policy**: ALL changes via Bricks Builder GUI or Respira MCP. NO scripts, NO post-processing.
- **Templates**: 185 & 52 unfrozen — use Respira MCP with snapshot, rollback via `respira_restore_snapshot`
- **MailerLite TODO**: Template 10 sidebar has Bricks native form — replace with MailerLite embed when account created
- **Export workflow**: GUI/MCP edits → Simply Static export → wrangler deploy
- **Deploy command**: Run from `D:\Coding Zone\digitrust-lab-static`:
  ```powershell
  npx wrangler pages deploy . --project-name=digitrust-lab-static
  ```
  No wrangler.toml needed. Wrangler caches uploaded files — only changed files get re-uploaded.
