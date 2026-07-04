# NEXT — DigiTrust Lab

## Current State

- ✅ Blog is LIVE at https://blog.digitrustlab.com
- WordPress + Bricks Builder + Simply Static + Cloudflare Pages pipeline working
- All 4 templates native Bricks elements (zero Code elements): Header (185), Footer (46), Single Post (10), Blog Archive (52)
- Core pages: Homepage, Tentang Kami, Polisi Privasi, Disclaimer, Hubungi Kami
- Bricks MCP bridge enum truncation bug fixed (2026-07-04) — full action enums visible to Claude Desktop
- Bricks MCP full tool audit complete (2026-07-04) — 41 calls tested, all working correctly
- TROUBLESHOOTING.md documents 13+ known issues with solutions

## Completed (Sessions 1-6, 2026-06-28 to 2026-07-04)

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

## Next Steps (Priority Order)

1. **Write first blog post** — WriterZen keyword research → write → ClickRank optimization
2. **Set up Google Search Console + GA4** — verify ownership, submit sitemap
3. **Verify ClickRank ownership** — JS snippet on blog
4. **Add digitrustlab.com to Screpy** — monitoring
5. **Register Klikjer affiliate** — free, 50% commission, Malaysian eBooks
6. **Register JV Warrior affiliate** — Malaysian digital products
7. **Create Etsy shop** — choose clean shop name (NOT DigiTrust Lab)
8. **Create first Etsy listing** — "30 Prompt AI untuk Iklan FB & IG (Bahasa Melayu)"
9. **Set up MailerLite** — free account, newsletter form on blog
10. **Create lead magnet PDF** — "50 Prompt AI Percuma"

## Important Notes

- **Bricks-Only Policy**: ALL changes via Bricks Builder GUI or Bricks MCP. NO scripts, NO post-processing.
- **Export workflow**: GUI/MCP edits → Simply Static export → wrangler deploy (or Cloudflare dashboard)
- **Deploy**: `npx wrangler pages deploy "D:\Coding Zone\digitrust-lab-static" --project-name=digitrust-lab-static --branch=main --commit-dirty=true` (or Cloudflare dashboard). Always use the full path — deploying from the wrong directory deploys source code instead of static HTML.
